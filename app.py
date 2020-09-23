#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy import text

from flask_migrate import Migrate
from datetime import datetime
from helper import query_to_dict
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO_Done: connect to a local postgresql database
migrate = Migrate(app, db)

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

    def __init__(self, name, city, state, address, genres, phone, image_link, facebook_link, website, seeking_talent, seeking_description):
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

    # TODO_done: implement any missing fields, as a database migration using Flask-Migrate

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

    def __init__(self, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description):
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

    # TODO_done: implement any missing fields, as a database migration using Flask-Migrate

# TODO_done Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = "shows"
  id = db.Column(db.Integer, primary_key=True)
  show_date = db.Column(db.DateTime, nullable=False)
  venue_id =  db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
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

#----------------------------------------------------------------------------#
# margin
#---------


#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO_done: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  # First we get the unique cities (and states) in our venues table
  sql = 'SELECT DISTINCT city, state FROM venues;'
  result = db.engine.execute(sql)
  cities = [row[0] for row in result]
  sql = 'SELECT DISTINCT state FROM venues;'
  result = db.engine.execute(sql)
  states = [row[0] for row in result]

  # Now we loop the cities to get the available venues
  venues_arr = []
  for city in cities:
    sql = f"SELECT * FROM venues WHERE city = '{city}';"
    venues = db.engine.execute(sql)
    venues_in_same_state = []
    for venue in venues:
      venues_in_same_state.append(venue)
    venues_arr.append(venues_in_same_state)

  # Formong the upcoming shows and venues arr
  new_venues_arr = []
  for arr in venues_arr:
    new_venues_arr.append([])
  for i in range(len(venues_arr)):
    for ven in venues_arr[i]:
      sql = f"SELECT * FROM shows WHERE venue_id = {ven.id} AND show_date > now();"
      shows = db.engine.execute(sql)
      venue_upcoming_shows = [row[0] for row in shows]
      new_venues_arr[i].append({
        "id": ven.id,
        "name": ven.name,
        "num_upcoming_shows": len(venue_upcoming_shows),
      })

  # Forming the response
  data_temp = []
  for i in range(len(cities)):
    data_temp.append({
      "city": cities[i],
      "state": states[i],
      "venues" : new_venues_arr[i]
    })
  return render_template('pages/venues.html', areas=data_temp);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO_done: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  form_value = request.form.get('search_term')
  sql = text(f"SELECT * FROM venues WHERE name ILIKE '%{form_value}%';")
  found_venues = db.engine.execute(sql)
  data = []
  count = 0
  for venue in found_venues:
    sql = text(f"SELECT * FROM shows WHERE venue_id = {venue.id} AND show_date > now();")
    shows = db.engine.execute(sql)
    venue_upcoming_shows = [row[0] for row in shows]
    data.append({
    "id": venue.id,
    "name": venue.name,
    "num_upcoming_shows": len(venue_upcoming_shows)
  })
    count += 1;

  response_temp = {
    "count": count,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response_temp, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO_done: replace with real venue data from the venues table, using venue_id

  # Checking of the venue exists
  sql = text(f"SELECT * FROM venues WHERE id = {venue_id};")
  venue_arr = query_to_dict(db.engine.execute(sql))
  if len(venue_arr) == 0:
    flash("Venue doesn't exist!")
    return render_template('errors/404.html', category='error')

  # Getting the venue
  venue =  venue_arr[0]

  # Getting the venue past show arr
  sql = text(f"SELECT * from shows WHERE venue_id = {venue['id']} AND show_date < now();")
  venue_past_show = query_to_dict(db.engine.execute(sql))

  # Getting the venues upcoming shows
  sql = text(f"SELECT * from shows WHERE venue_id = {venue['id']} AND show_date > now();")
  venue_upcoming_show = query_to_dict(db.engine.execute(sql))

  # Forming the past shows arr
  venue_past_show_with_artist_details = []
  for show in venue_past_show:
    sql = text(f"SELECT * from artists WHERE id = {show['artist_id']};")
    show_artist = query_to_dict(db.engine.execute(sql))[0]
    venue_past_show_with_artist_details.append({
      "artist_id": show_artist['id'],
      "artist_name": show_artist['name'],
      "artist_image_link": show_artist['image_link'],
      "start_time": show['show_date'].strftime("%m/%d/%Y, %H:%M:%S")
    })

  # Forming the upcoming shows arr
  venue_upcoming_show_with_artist_details = []
  for show in venue_upcoming_show:
    sql = text(f"SELECT * from artists WHERE id = {show['artist_id']};")
    show_artist = query_to_dict(db.engine.execute(sql))[0]
    venue_upcoming_show_with_artist_details.append({
      "artist_id": show_artist['id'],
      "artist_name": show_artist['name'],
      "artist_image_link": show_artist['image_link'],
      "start_time": show['show_date'].strftime("%m/%d/%Y, %H:%M:%S")
    })

  # Forming the response data
  data = {
    "id": venue['id'],
    "name": venue['name'],
    "genres": venue['genres'] if venue['genres'] else [],
    "address": venue['address'],
    "city": venue['city'],
    "state": venue['state'],
    "phone": venue['phone'],
    "website": venue['website'],
    "facebook_link": venue['facebook_link'],
    "seeking_talent": venue['seeking_talent'],
    "seeking_description": venue['seeking_description'],
    "image_link": venue['image_link'],
    "past_shows": venue_past_show_with_artist_details,
    "upcoming_shows": venue_upcoming_show_with_artist_details,
    "past_shows_count": len(venue_past_show_with_artist_details),
    "upcoming_shows_count": len(venue_upcoming_show_with_artist_details),
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO_done: insert form data as a new Venue record in the db, instead
  # TODO_done: modify data to be the data object returned from db insertion

  # Trying to post the data to the database
  seeking_talent = True if request.form['seeking_talent'] == "True" else False
  posted_successfully = True
  try:
    sql = text(f'''INSERT INTO venues (name, city, state, address, genres, phone, image_link, facebook_link, website, seeking_talent, seeking_description) VALUES ('{request.form['name']}', '{request.form['city']}', '{request.form['state']}',  '{request.form['address']}', ARRAY {request.form.getlist('genres')}, '{request.form['phone']}',  '{request.form['image_link']}', '{request.form['facebook_link']}', '{request.form['website']}',  {seeking_talent}, '{request.form['seeking_description']}'); ''')
    db.engine.execute(sql)
    db.session.commit()
  except():
    posted_successfully = False
    db.session.rollback()
  finally:
    db.session.close()
  if posted_successfully:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  else:
    flash('Venue ' + request.form['name'] + ' was not successfully listed!')
    return render_template('errors/404.html', category='error')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO_done: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  # Note that upon successful deletion, the user will be directed to home page by the browser (from the frontend)
  deleted_successfully = True
  try:
    # Deleting any shows in that venue
    sql = text(f'DELETE FROM shows WHERE venue_id = {venue_id};')
    db.engine.execute(sql)
    # Deleting the venue and saving
    sql = text(f'DELETE FROM venues WHERE id = {venue_id};')
    db.engine.execute(sql)
    db.session.commit()
  except():
    deleted_successfully = False
    db.session.rollback()
  finally:
    db.session.close()
  if deleted_successfully:
    return jsonify({}), 204
  else:
    abort(400)



#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO_done: replace with real data returned from querying the database
  sql = text("SELECT * FROM artists;")
  all_artists = query_to_dict(db.engine.execute(sql))
  data = []
  for artist in all_artists:
    data.append({
      "id": artist['id'],
      "name": artist['name']
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO_done: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  # Searching for the artist
  artist_name = request.form.get('search_term')
  sql = text(f"SELECT * FROM artists WHERE name ILIKE '%{artist_name}%';")
  found_artists = query_to_dict(db.engine.execute(sql))

  # Forming the data
  data = []
  for artist in found_artists:
    sql = text(f"SELECT * FROM shows WHERE artist_id = {artist['id']} AND show_date > now();")
    upcoming_shows = query_to_dict(db.engine.execute(sql))
    data.append({
      "id":  artist['id'],
      "name": artist['name'],
      "num_upcoming_shows": len(upcoming_shows)
    })

  # Forming the response
  response={
    "count": len(found_artists),
    "data": data
  }

  # Sending the response
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO_done: replace with real venue data from the venues table, using venue_id

  # Checking if the artist exists
  sql = text(f"SELECT * FROM artists WHERE id = {artist_id};")
  artist_arr = query_to_dict(db.engine.execute(sql))
  if len(artist_arr) == 0:
    flash("Artist not found!")
    return render_template('errors/404.html', category='error')

  # Getting the artist
  artist = artist_arr[0]

  # Getting the artist past show arr
  sql = text(f"SELECT * from shows WHERE artist_id = {artist['id']} AND show_date < now();")
  artist_past_show = query_to_dict(db.engine.execute(sql))

  # Getting the artist upcoming shows
  sql = text(f"SELECT * from shows WHERE artist_id = {artist['id']} AND show_date > now();")
  artist_upcoming_show = query_to_dict(db.engine.execute(sql))

  # Forming the past shows arr
  #artist_past_show = [show for show in artist.shows if show.show_date < datetime.now()]
  artist_past_show_with_venue_details = []
  for show in artist_past_show:
    sql = text(f"SELECT * from venues WHERE id = {show['venue_id']};")
    show_venue = query_to_dict(db.engine.execute(sql))[0]
    #show_venue = Venue.query.filter(Venue.id == show.venue_id).first()
    artist_past_show_with_venue_details.append({
      "venue_id": show_venue['id'],
      "venue_name": show_venue['name'],
      "venue_image_link": show_venue['image_link'],
      "start_time": show['show_date'].strftime("%m/%d/%Y, %H:%M:%S")
    })

  # Forming the upcoming shows arr
  #artist_upcoming_show = [show for show in artist.shows if show.show_date > datetime.now()]
  artist_upcoming_show_with_venue_details = []
  for show in artist_upcoming_show:
    sql = text(f"SELECT * from venues WHERE id = {show['venue_id']};")
    show_venue = query_to_dict(db.engine.execute(sql))[0]
    #show_venue = Venue.query.filter(Venue.id == show.venue_id).first()
    artist_upcoming_show_with_venue_details.append({
      "venue_id": show_venue['id'],
      "venue_name": show_venue['name'],
      "venue_image_link": show_venue['image_link'],
      "start_time": show['show_date'].strftime("%m/%d/%Y, %H:%M:%S")
    })

  # Forming the response data
  data={
    "id": artist['id'],
    "name": artist['name'],
    "genres": artist['genres'] if artist['genres'] else [],
    "city": artist['city'],
    "state": artist['state'],
    "phone": artist['phone'],
    "website": artist['website'],
    "facebook_link": artist['facebook_link'],
    "seeking_venue": artist['seeking_venue'],
    "seeking_description": artist['seeking_description'],
    "image_link": artist['image_link'],
    "past_shows": artist_past_show_with_venue_details,
    "upcoming_shows": artist_upcoming_show_with_venue_details,
    "past_shows_count": len(artist_past_show_with_venue_details),
    "upcoming_shows_count": len(artist_upcoming_show_with_venue_details),
  }

  # Sending the response data
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO_done: populate form with fields from artist with ID <artist_id>

  # Getting the artist
  sql = text(f"SELECT * from artists WHERE id = {artist_id};")
  artist_to_modify = query_to_dict(db.engine.execute(sql))[0]
  #artist_to_modify = Artist.query.filter(Artist.id == artist_id).first()

  # Forming the response
  artist={
    "id": artist_to_modify['id'],
    "name": artist_to_modify['name'],
    "genres": artist_to_modify['genres'] if artist_to_modify['genres'] else [],
    "city": artist_to_modify['city'],
    "state": artist_to_modify['state'],
    "phone": artist_to_modify['phone'],
    "website": artist_to_modify['website'],
    "facebook_link": artist_to_modify['facebook_link'],
    "seeking_venue": artist_to_modify['seeking_venue'],
    "seeking_description": artist_to_modify['seeking_description'],
    "image_link": artist_to_modify['image_link']
  }

  # Populating the form with the artist data
  form = ArtistForm(**artist)

  # Returning the response
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO_done: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  # Trying to post the data to the database
  seeking_venue = True if request.form['seeking_venue'] == "True" else False
  updated_successfully = True
  try:
    sql = text(f'''UPDATE artists SET name = '{request.form['name']}', city = '{request.form['city']}', state = '{request.form['state']}', phone = '{request.form['phone']}', genres = ARRAY {request.form.getlist('genres')}, image_link = '{request.form['image_link']}', facebook_link = '{request.form['facebook_link']}', website = '{request.form['website']}', seeking_venue = {seeking_venue}, seeking_description = '{request.form['seeking_description']}' WHERE id = {artist_id}; ''')
    db.engine.execute(sql)
    db.session.commit()
  except():
    updated_successfully = False
    db.session.rollback()
  finally:
    db.session.close()
  if updated_successfully:
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
    return render_template('pages/home.html')
  else:
    flash('Artist ' + request.form['name'] + ' was not successfully updated!')
    return render_template('errors/404.html', category='error')


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO_done: populate form with values from venue with ID <venue_id>

  # Getting the venue to modify
  sql = text(f"SELECT * FROM venues WHERE id = {venue_id}")
  venue_to_modify = query_to_dict(db.engine.execute(sql))[0]

  # Forming the venue data
  venue={
    "id": venue_to_modify['id'],
    "name": venue_to_modify['name'],
    "genres": venue_to_modify['genres'] if venue_to_modify['genres'] else [],
    "address": venue_to_modify['address'],
    "city": venue_to_modify['city'],
    "state": venue_to_modify['state'],
    "phone": venue_to_modify['phone'],
    "website": venue_to_modify['website'],
    "facebook_link": venue_to_modify['facebook_link'],
    "seeking_talent": venue_to_modify['seeking_talent'],
    "seeking_description": venue_to_modify['seeking_description'],
    "image_link": venue_to_modify['image_link']
  }

  # Populating the form with the venue data
  form = VenueForm(**venue)

  # Returning the response
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO_done: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  # Trying to post the data to the database
  seeking_talent = True if request.form['seeking_talent'] == "True" else False
  updated_successfully = True
  try:
    sql = text(f'''UPDATE venues SET name = '{request.form['name']}', city = '{request.form['city']}', state = '{request.form['state']}', address = '{request.form['address']}', phone = '{request.form['phone']}', genres = ARRAY {request.form.getlist('genres')}, image_link = '{request.form['image_link']}', facebook_link = '{request.form['facebook_link']}', website = '{request.form['website']}', seeking_talent = {seeking_talent}, seeking_description = '{request.form['seeking_description']}' WHERE id = {venue_id}; ''')
    db.engine.execute(sql)
    db.session.commit()
  except():
    updated_successfully = False
    db.session.rollback()
  finally:
    db.session.close()
  if updated_successfully:
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
    return render_template('pages/home.html')
  else:
    flash('Venue ' + request.form['name'] + ' was not successfully updated!')
    return render_template('errors/404.html', category='error')


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO_done: insert form data as a new Venue record in the db, instead
  # TODO_done: modify data to be the data object returned from db insertion

  # Trying to post the data to the database
  seeking_venue = True if request.form['seeking_venue'] == "True" else False
  posted_successfully = True
  try:
    sql = text(f'''INSERT INTO artists (name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description) VALUES ('{request.form['name']}', '{request.form['city']}', '{request.form['state']}', '{request.form['phone']}', ARRAY {request.form.getlist('genres')},  '{request.form['image_link']}', '{request.form['facebook_link']}', '{request.form['website']}',  {seeking_venue}, '{request.form['seeking_description']}'); ''')
    db.engine.execute(sql)
    db.session.commit()
  except():
    posted_successfully = False
    db.session.rollback()
  finally:
    db.session.close()
  if posted_successfully:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  else:
    flash('Artist ' + request.form['name'] + ' was not successfully listed!')
    return render_template('pages/home.html', category='error')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO_done: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  # Getting all the available shows
  sql = text("SELECT * FROM shows;")
  all_shows = query_to_dict(db.engine.execute(sql))

  # Forming the response data
  data = []
  for show in all_shows:
    sql = text(f"SELECT * from venues WHERE id = {show['venue_id']}")
    show_venue = query_to_dict(db.engine.execute(sql))[0]
    sql = text(f"SELECT * from artists WHERE id = {show['artist_id']}")
    show_artist = query_to_dict(db.engine.execute(sql))[0]
    data.append({
      "venue_id": show_venue['id'],
      "venue_name": show_venue['name'],
      "artist_id": show_artist['id'],
      "artist_name": show_artist['name'],
      "artist_image_link": show_artist['image_link'],
      "start_time": show['show_date'].strftime("%m/%d/%Y, %H:%M:%S")
    })

  # Sending the response data
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO_done: insert form data as a new Show record in the db, instead

  # Getting and parsing the form
  error_parsing_input = False
  artist_id = 0
  venue_id = 0
  show_time = None
  try:
    artist_id = int(request.form['artist_id'])
    venue_id = int(request.form['venue_id'])
    show_time = datetime.strptime(request.form['start_time'], '%Y-%m-%d %H:%M:%S')
  except(ValueError):
    error_parsing_input = True
  if error_parsing_input:
    flash('Please enter valid input!', category='error')
    return render_template('errors/500.html')

  # Checking if the artist and venue exist
  valid_data = True
  sql = text(f"SELECT * FROM venues WHERE id = {venue_id}")
  venue_arr = query_to_dict(db.engine.execute(sql))
  sql = text(f"SELECT * FROM artists WHERE id = {artist_id}")
  artist_arr = query_to_dict(db.engine.execute(sql))
  if len(venue_arr) == 0 or  len(artist_arr) == 0:
    valid_data = False
  if not valid_data:
    flash('Please enter an existing venue and artist!', category='error')
    return render_template('errors/404.html')

  # Posting the show
  posted_successfully = True
  try:
    sql = text(f"INSERT INTO shows (show_date, venue_id, artist_id) VALUES ('{show_time}', {venue_id}, {artist_id});")
    db.engine.execute(sql)
    db.session.commit()
  except():
    posted_successfully = False
    db.session.rollback()
  finally:
    db.session.close()
  if posted_successfully:
    flash('Show was successfully listed!')
    return render_template('pages/home.html')
  else:
    flash('Show was not successfully listed!')
    return render_template('errors/500.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
