from flask import render_template, redirect, flash, session, url_for
from werkzeug.security import check_password_hash

from forms import RegisterForm, ProductForm, LoginForm
from models import Product, Comment, User
from ext import app, db, login_manager
from flask_login import login_user, logout_user, login_required
import os

profiles = []



@app.route("/")
def home():
    role = "user"
    cart_items = len(get_cart_items())
    return render_template("HOME.html", products=Product.query.all(), role=role, cart_items=cart_items)




@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash("თქვენ წარმატებით დარეგისტრირდით,  გაიარეთ ავტორიზაცია", "success")
        return redirect("/login")

    return render_template("login.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(form.username.data == User.username).first()
        if user and user.check_password(form.password.data):
            login_user(user)

            flash("თქვენ წარმატებით გაიარეთ ავტორიზაცია", "success")
            return redirect("/")
        else:
            flash("მოხდა შეცდომა", "danger")


    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()

    return redirect("/")


@app.route("/create_product", methods=["GET", "POST"])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data)

        image = form.image.data
        img_location = os.path.join(app.root_path, "static", "images", image.filename)
        image.save(img_location)

        new_product.image = image.filename

        db.session.add(new_product)
        db.session.commit()

        flash("პროდუქტი წარმატებით დაემატა", "success")
        return redirect("/")

    return render_template("create_product.html", form=form)


@app.route("/edit_product/<int:product_id>", methods=["POST", "GET"])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data

        db.session.commit()

        flash("პროდუქტი წარმატებით განახლდა!", "success")
        return redirect("/")

    return render_template("create_product.html", form=form)


@app.route("/delete/<int:product_id>")
@login_required
def delete(product_id):
    product = Product.query.get(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("პროდუქტი წარმატებით წაიშალა", "danger")
    return redirect("/")


@app.route("/detailed/<int:product_id>")
def detailed(product_id):
    product = Product.query.get(product_id)
    comments = Comment.query.filter(Comment.product_id == product_id)
    return render_template("detailed.html", product=product, comments=comments)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/profiles/<int:profile_id>")
def profile(profile_id):
    return render_template("profile.html", user=profiles[profile_id])


def get_cart_items():
    return session.get('cart', [])

@app.route("/cart")
def cart():
    cart_product_ids = get_cart_items()
    length = len(cart_product_ids)
    if cart_product_ids:
        products = Product.query.filter(Product.id.in_(cart_product_ids)).all()
        total_sum = sum(product.price for product in products)
    else:
        products = []
    return render_template('cart.html', products=products, cart_items=length, total_sum=total_sum)

@app.route('/add_to_cart/<int:item_id>', methods=['GET', 'POST'])
def add_to_cart(item_id):
    cart = session.get('cart', [])
    cart.append(item_id)

    session['cart'] = cart
    return redirect("/")

@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    if item_id in cart:
        cart.remove(item_id)
        session['cart'] = cart

    return redirect("/cart")
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))