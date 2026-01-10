import os
from fileinput import filename

from ext import db, app

from models import Product, Comment, User

with app.app_context():
    db.drop_all()
    db.create_all()
    print("ბაზა წარმატებით შეიქმნა!")
    admin = User( username="admin", password="adminpass", role="Admin")

    db.session.add(admin)
    db.session.commit()
