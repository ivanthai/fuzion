from app import db


class Vrbo(db.Model):
    __tablename__ = 'vrbo'

    listing_id = db.Column(db.Integer, primary_key=True)
    vrbo_id = db.Column(db.Integer)

    def __init__(self, listing_id, vrbo_id):
        self.listing_id = listing_id
        self.vrbo_id = vrbo_id

    def __repr__(self):
        return '<id {}>'.format(self.listing_id)
