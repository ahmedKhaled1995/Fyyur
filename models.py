from config import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String()), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(), nullable=True)
    shows = db.relationship("Show", backref="venue", lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, city, state, address, genres, phone, image_link, facebook_link,
                 website, seeking_talent, seeking_description):
        self.name = name
        self.city = city
        self.state = state
        self.address = address
        self.genres = genres
        self.phone = phone
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.website = website
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description

    def __str__(self):
        return {"id": self.id, "name": self.name}

    def serialize(self):
        return {
              "id": self.id,
              "name": self.name,
              "city": self.city,
              "state": self.state,
              "address": self.address,
              "genres": self.genres,
              "phone": self.phone,
              "image_link": self.image_link,
              "facebook_link": self.facebook_link,
              "website": self.website,
              "seeking_talent": self.seeking_talent,
              "seeking_description": self.seeking_description
              }


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=True)
    state = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String()), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=True, default=False)
    seeking_description = db.Column(db.String(), nullable=True)
    shows = db.relationship("Show", backref="artist", lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, city, state, phone, genres, image_link,
                 facebook_link, website, seeking_venue, seeking_description):
        self.name = name
        self.city = city
        self.state = state
        self.phone = phone
        self.genres = genres
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.website = website
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description

    def __str__(self):
        return {"id": self.id, "name": self.name}

    def serialize(self):
        return {
              "id": self.id,
              "name": self.name,
              "city": self.city,
              "state": self.state,
              "phone": self.phone,
              "genres": self.genres,
              "image_link": self.image_link,
              "facebook_link": self.facebook_link,
              "website": self.website,
              "seeking_venue": self.seeking_venue,
              "seeking_description": self.seeking_description
        }


class Show(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True)
    show_date = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)

    def __init__(self, date, venue_id, artist_id):
        self.show_date = date
        self.venue_id = venue_id
        self.artist_id = artist_id

    def __str__(self):
        return {"id": self.id, "venue_id": self.venue_id, "artist_id": self.artist_id}

    def serialize(self):
        return {
          "id": self.id,
          "show_date": self.show_date,
          "venue_id": self.venue_id,
          "artist_id": self.artist_id,
        }
