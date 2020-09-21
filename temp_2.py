'''
v1 = Venue('The Musical Hop', 'San Francisco', 'CA', '11A, National tr, prox St', '02-44675123',
           "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
           "https://www.facebook.com/ahmed.khaled.739",
           "https://hassanin-portofolio.herokuapp.com/",
           False,
           "This is a description text one!")
v2 = Venue('Park Square Live Music & Coffee', 'San Francisco', 'CA', 'Address_2', '02-22578621',
           "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
           "https://www.facebook.com/ahmed.khaled.739",
           "https://hassanin-portofolio.herokuapp.com/",
           True,
           "This is a description text two!")
v3 = Venue('The Dueling Pianos Bar', 'New York', 'NY', 'Address_Ny', '02-35675123',
           "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
           "https://www.facebook.com/ahmed.khaled.739",
           "https://hassanin-portofolio.herokuapp.com/",
           False,
           "This is a description text three!")
db.session.add_all([v1, v2, v3])
db.session.commit()
'''

'''
artist_1 = Artist("John Doe", "San Francisco", "CA", "01097963741", ["Jaz", "Disco"],
                  "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
                  "https://www.facebook.com/ahmed.khaled.739",
                  "https://hassanin-portofolio.herokuapp.com/",
                  True,
                  "My artist description One")
artist_2 = Artist("John Doe", "New York", "NA", "01097963741", ["Pop", "Rock"],
                  "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
                  "https://www.facebook.com/ahmed.khaled.739",
                  "https://hassanin-portofolio.herokuapp.com/",
                  False,
                  "")
artist_3 = Artist("John Doe", "San Francisco", "CA", "01097963741", [],
                  "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
                  "https://www.facebook.com/ahmed.khaled.739",
                  "https://hassanin-portofolio.herokuapp.com/",
                  False,
                  "My artist description three")
db.session.add_all([artist_1, artist_2, artist_3])
db.session.commit()
'''

'''
show_one = Show(datetime(2020, 5, 17), 10, 1)
show_two = Show(datetime(2020, 10, 17), 10, 1)
show_three = Show(datetime(2020, 6, 18), 11, 2)
show_four = Show(datetime(2020, 11, 18), 11, 2)
show_five = Show(datetime(2020, 7, 19), 12, 3)
show_six = Show(datetime(2020, 12, 19), 12, 3)
db.session.add_all([show_one, show_two, show_three, show_four, show_five, show_six])
db.session.commit()
'''


'''
# First we get the unique cities in our venues table
cities = []
for venue_entry in db.session.query(Venue.city).distinct():
  city = venue_entry[0]
  cities.append(city)
# Now we loop the cities to get the available venues
venues_arr = []
for city in cities:
  venue_data = Venue.query.filter(Venue.city == city).all()
  venues_arr.append(venue_data)
# Forming the response
data_temp = []
for i in range(len(cities)):
  data_temp.append({
    "city": cities[i],
    "state": venues_arr[i][0].state,
    "venues": venues_arr[i]
  })

print(data_temp)
'''

for show in ven.shows:
    if show.show_date > datetime.now():
        upcoming_shows += 1
ven["num_upcoming_shows"] = upcoming_shows

for key in request.form:
    if key == 'genres':
        print(request.form[f"{key}"])



 # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
#-------------------------------------------------------------------------------------------------------------------
# Artists
#--------
data = [{
    "id": 4,
    "name": "Guns N Petals",
}, {
    "id": 5,
    "name": "Matt Quevedo",
}, {
    "id": 6,
    "name": "The Wild Sax Band",
}]
#-------------------------------------------------------------------------------------------------------------------
# Shows
#-------
data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]


# on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')