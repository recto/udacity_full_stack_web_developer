from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item
from datetime import date

engine = create_engine("sqlite:///item_category.db")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

categories = [{"name": "Soccer", "user_id":"1"},
              {"name": "Basketball", "user_id":"1"},
              {"name": "Baseball", "user_id":"1"}]

items = [{"name":"Soccer Cleats", "description":"The cleats for hard ground",
          "category_id":"1", "user_id":"1", "date": date.today()},
         {"name":"Soccer Ball", "description":"Size 5 soccer ball.",
          "category_id":"1", "user_id":"1", "date": date.today()},
         {"name":"Basketball Ball", "description":"Basketball ball.",
          "category_id":"2", "user_id":"1", "date": date.today()},
         {"name":"Basketball Shoes", "description":"Basketball shoes.",
          "category_id":"2", "user_id":"1", "date": date.today()},
         {"name":"Baseball bat", "description":"Baseball bat.",
          "category_id":"3", "user_id":"1", "date": date.today()},
         {"name":"Baseball Helmet", "description":"Baseball helmet. Size M.",
          "category_id":"3", "user_id":"1", "date": date.today()}]


user = User(name="Itsuo Okamoto", email="itsuo.okamoto@gmail.com",
            picture="https://lh6.googleusercontent.com/-hHksYOdrpPY/AAAAAAAAAAI/AAAAAAAA5Jg/I-LbJS6P3do/photo.jpg")
session.add(user)
session.commit()

for cat in categories:
    category = Category(user_id=1, name=cat["name"])
    session.add(category)
session.commit()

for i in items:
    item = Item(user_id=i["user_id"], name=i["name"],
            description=i["description"], category_id=i["category_id"],
            date = i["date"])
    session.add(item)
session.commit()

print "added items!"
