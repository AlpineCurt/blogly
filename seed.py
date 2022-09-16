"""Seed file to make sample data for blogly database"""

from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name="Jeff", last_name="Goldblum", image_url=f"https://d26oc3sg82pgk3.cloudfront.net/files/media/edit/image/21525/square_thumb%402x.jpg")
u2 = User(first_name="Stevie", last_name="Budd", image_url="https://img.sharetv.com/shows/characters/thumbnails/schitts_creek_ca.stevie_budd.jpg")
u3 = User(first_name="Husky", last_name="The Dog", image_url="https://cdn141.picsart.com/286202642070201.jpg?type=webp&to=crop&r=256")
u4 = User(first_name="Doc", last_name="Brown", image_url="https://www.realmodscene.com/uploads/monthly_2017_02/5895f58b1b011_doctesta.thumb.jpg.4916f7e8b25380eaef00e8fbf148b7d5.jpg")

p1 = Post(title="Great Scott!", content="I found a way to improve the flux capacitor!", user=4)
p2 = Post(title="Husky Noises", content="AaarroooAAAHHRRROOOooooRRAAAA!", user=3)
p3 = Post(title="Ew, David!", content="I'm not the one that says Ew, David", user=2)
p4 = Post(title="In the Jeep", content="Getting chased by a T-Rex and this guy won't drive any faster.  fml", user=1)
p5 = Post(title="Marty!", content="It's your kids, marty!  Something's gotta be done about your kids!", user=4)
p6 = Post(title="Need to go outside", content="I really gotta pee", user=3)

db.session.add_all([u1, u2, u3, u4])
db.session.commit()

db.session.add_all([p1, p2, p3, p4, p5, p6])
db.session.commit()