#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import render_template, request, Response, flash, redirect, url_for, abort, jsonify
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy import text
from datetime import datetime

from config import app, db
from helper import query_to_dict
from models import *


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
  data = []
  for i in range(len(cities)):
    data.append({
      "city": cities[i],
      "state": states[i],
      "venues" : new_venues_arr[i]
    })
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
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

  response = {
    "count": count,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # Checking of the venue exists
  sql = text(f"SELECT * FROM venues WHERE id = {venue_id};")
  venue_arr = query_to_dict(db.engine.execute(sql))
  if len(venue_arr) == 0:
    flash("Venue doesn't exist!", category='error')
    return render_template('errors/404.html')

  # Getting the venue
  venue =  venue_arr[0]

  # Getting the venue past show arr
  sql = text(f"SELECT shows.show_date, shows.artist_id FROM shows INNER JOIN venues ON shows.venue_id = venues.id WHERE venues.id = {venue_id} AND shows.show_date < now();")
  venue_past_show = query_to_dict(db.engine.execute(sql))

  # Getting the venues upcoming shows
  sql = text(f"SELECT shows.show_date, shows.artist_id FROM shows INNER JOIN venues ON shows.venue_id = venues.id WHERE venues.id = {venue_id} AND shows.show_date > now();")
  venue_upcoming_show = query_to_dict(db.engine.execute(sql))

  # Forming the past shows arr
  venue_past_show_with_artist_details = []
  for show in venue_past_show:
    sql = text(f"SELECT shows.show_date, artists.id, artists.name, artists.image_link FROM shows INNER JOIN artists ON shows.artist_id = artists.id WHERE artists.id = {show['artist_id']} AND shows.show_date > now();")
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
    sql = text(f"SELECT shows.show_date, artists.id, artists.name, artists.image_link FROM shows INNER JOIN artists ON shows.artist_id = artists.id WHERE artists.id = {show['artist_id']} AND shows.show_date > now();")
    show_artist = query_to_dict(db.engine.execute(sql))[0]
    print(show_artist)
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
    flash('Venue ' + request.form['name'] + ' was not successfully listed!', category='error')
    return render_template('errors/404.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
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
  # Searching for the artist
  artist_name = request.form.get('search_term')
  sql = text(f"SELECT * FROM artists WHERE name ILIKE '%{artist_name}%';")
  found_artists = query_to_dict(db.engine.execute(sql))

  # Forming the data
  data = []
  for artist in found_artists:
    sql = text(f"SELECT shows.show_date, shows.artist_id FROM shows INNER JOIN artisits ON shows.artist_id = artists.id WHERE artists.id = {artist['id']} AND shows.show_date > now();")
    #sql = text(f"SELECT * FROM shows WHERE artist_id = {artist['id']} AND show_date > now();")
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
  # Checking if the artist exists
  sql = text(f"SELECT * FROM artists WHERE id = {artist_id};")
  artist_arr = query_to_dict(db.engine.execute(sql))
  if len(artist_arr) == 0:
    flash("Artist not found!", category='error')
    return render_template('errors/404.html')

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
    sql = text(f"SELECT shows.show_date, venues.id, venues.name, venues.image_link FROM shows INNER JOIN venues ON shows.venue_id = venues.id WHERE venues.id = {show['venue_id']} AND shows.show_date < now();")
    show_venue = query_to_dict(db.engine.execute(sql))[0]
    artist_past_show_with_venue_details.append({
      "venue_id": show_venue['id'],
      "venue_name": show_venue['name'],
      "venue_image_link": show_venue['image_link'],
      "start_time": show['show_date'].strftime("%m/%d/%Y, %H:%M:%S")
    })

  # Forming the upcoming shows arr
  artist_upcoming_show_with_venue_details = []
  for show in artist_upcoming_show:
    sql = text(f"SELECT shows.show_date, venues.id, venues.name, venues.image_link FROM shows INNER JOIN venues ON shows.venue_id = venues.id WHERE venues.id = {show['venue_id']} AND shows.show_date > now();")
    show_venue = query_to_dict(db.engine.execute(sql))[0]
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
  # Getting the artist
  sql = text(f"SELECT * from artists WHERE id = {artist_id};")
  artist_to_modify = query_to_dict(db.engine.execute(sql))[0]

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
    flash('Artist ' + request.form['name'] + ' was not successfully updated!', category='error')
    return render_template('errors/404.html')


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
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
    flash('Venue ' + request.form['name'] + ' was not successfully updated!', category='error')
    return render_template('errors/404.html')


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
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
    flash('Artist ' + request.form['name'] + ' was not successfully listed!', category='error')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
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

