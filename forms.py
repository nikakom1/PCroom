from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, RadioField,FloatField, DateField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, length, equal_to

class RegisterForm(FlaskForm):
    profile_img = FileField("აირჩიე პროფილის ფოტო",
                            validators=[DataRequired(), FileAllowed(["png", "jpg", "jpeg"])])
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter Password", validators=[DataRequired(), length(min=8, max=64,
                                                                                  message="პაროლის სიგრძე უნდა იყოს 8დან 64 სიმბოლომდე")])
    repeat_password = PasswordField("გაიმეორე პაროლი", validators=[DataRequired(), equal_to("password",
                                                                                            message="პაროლები უნდა ემთხვეოდეს ერთმანეთს")])
    gender = RadioField("აირჩიე სქესი", choices=["კაცი", "ქალი"])
    birthday = DateField("აირჩიე დაბადების თარიღი")
    submit = SubmitField("რეგისტრაცია")

class LoginForm(FlaskForm):
    username = StringField("Enter Username")
    password = PasswordField("Enter Password")
    login = SubmitField("LOG IN")



class ProductForm(FlaskForm):
    image = FileField("აირჩიე პროდუქტის ფოტო",
                            validators=[FileAllowed(["png", "jpg", "jpeg"])])
    name = StringField("შექმენი პროდუქტის სახელი")
    price = FloatField("შეიყვანე პროდუქტის ფასი")

    submit = SubmitField("შექმნა")
