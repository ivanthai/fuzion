from app import db


class Airbnb(db.Model):
    __tablename__ = 'airbnb'

    listing_id = db.Column(db.Integer, primary_key=True)
    airbnb_id = db.Column(db.Integer)

    def __init__(self, listing_id, airbnb_id):
        self.listing_id = listing_id
        self.airbnb_id = airbnb_id

    def __repr__(self):
        return '<id {}>'.format(self.listing_id)
