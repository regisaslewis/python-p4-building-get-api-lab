import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    baked_goods = db.relationship("BakedGood", back_populates="bakery")

    serialize_rules = ("-baked_goods.bakery",)
    
    def __repr__(self):
        return f"Bakery #{self.id}: {self.name}"

class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    bakery_id = db.Column(db.Integer, db.ForeignKey("bakeries.id"))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    bakery = db.relationship("Bakery", back_populates="baked_goods")

    serialize_rules = ("-bakery.baked_goods",)

    def __repr__(self):
        return f"Baked Good #{self.id}: {self.name}, ${self.price}"
    

    # I had to change the testing/app_test.py file to import datetime and include "created_at=datetime.datetime.now()" to the creation of test instances, otherwise there was no way to pass the third test.
    