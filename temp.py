artist = Artist.query.filter(Artist.id == artist_id).first()
artist.name = request.form['name']
artist.city = request.form['city']
artist.state = request.form['state']
artist.phone = request.form['phone']
artist.genres = request.form.getlist('genres')
artist.image_link = request.form['image_link']
artist.facebook_link = request.form['facebook_link']
artist.website = request.form['website']
artist.seeking_venue = seeking_venue
artist.seeking_description = request.form['seeking_description']

venue = Venue.query.filter(Venue.id == venue_id).first()
venue.name = request.form['name']
venue.city = request.form['city']
venue.state = request.form['state']
venue.address = request.form['address']
venue.genres = request.form.getlist('genres')
venue.phone = request.form['phone']
venue.image_link = request.form['image_link']
venue.facebook_link = request.form['facebook_link']
venue.website = request.form['website']
venue.seeking_talent = seeking_talent
venue.seeking_description = request.form['seeking_description']

artist = Artist(
    request.form['name'],
    request.form['city'],
    request.form['state'],
    request.form['phone'],
    request.form.getlist('genres'),
    request.form['image_link'],
    request.form['facebook_link'],
    request.form['website'],
    seeking_venue,
    request.form['seeking_description']
)
db.session.add(artist)