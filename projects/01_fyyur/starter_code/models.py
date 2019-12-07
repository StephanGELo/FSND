from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship
from flask import Flask
from app import app
from datetime import datetime
from sqlalchemy.dialects import postgresql

db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.String(), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)

  @property
  def venue_name(self):
    return Venue.query.get(self.venue_id).name
  
  @property
  def artist_name(self):
    return Artist.query.get(self.artist_id).name
  
  @property
  def artist_image_link(self):
    return Artist.query.get(self.artist_id).image_link
  
  def serialize(self):
    return { "id": self.id,
             "start_time": self.start_time,
             "venue_id": self.venue_id,
             "venue_name": self.venue_name,
             "artist_id": self.artist_id,
             "artist_name": self.artist_name,
             "artist_image_link": self.artist_image_link
    }

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    genres = db.Column(postgresql.ARRAY(db.String(120)))
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(), nullable=True)
    shows = db.relationship('Show', backref='venue', lazy=True)
    
    # def __repr__(self):
    #   return '<Venue %r>'% self
    
    @property
    def past_shows(self):
      now = datetime.now()
      past_shows = [show for show in self.shows if datetime.strptime(
        show.start_time, '%Y-%m-%dT%H:%M:%S.%fZ') < now]
      return past_shows
    
    @property
    def past_shows_count(self):
      return len(self.past_shows)
    
    @property
    def upcoming_shows(self):
      now = datetime.now()
      upcoming_shows = [show for show in self.shows if datetime.strptime(
        show.start_time, '%Y-%m-%dT%H:%M:%S.%fZ') > now]
      return upcoming_shows
    
    @property
    def upcoming_shows_count(self):
      return len(self.upcoming_shows)
    
    def serialize(self):
      return {'id': self.id,
              'name': self.name,
              'genres': self.genres,
              'address': self.address,
              'city': self.city,
              'state': self.state,
              'phone': self.phone,
              'image_link': self.image_link,
              'website': self.website,
              'facebook_link': self.facebook_link,
              'seeking_talent': self.seeking_talent,
              'seeking_description': self.seeking_description,
              'past_shows': self.past_shows,
              'past_shows_count': self.past_shows_count,
              'upcoming_shows': self.upcoming_shows,
              'upcoming_shows_count':self.upcoming_shows_count    
      }

  
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    genres = db.Column(postgresql.ARRAY(db.String(120)))
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(), nullable=True)
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(), nullable=True)
    shows = db.relationship('Show', backref='artist', lazy=True)
    
    def __repr__(self):
      return '<Artist %r>'% self

    @property
    def past_shows(self):
      now = datetime.now()
      past_shows = [show for show in self.shows if datetime.strptime(show.start_time, '%Y-%m-%dT%H:%M:%S.%fZ') < now]
      return past_shows

    @property
    def past_shows_count(self):
      return len(self.past_shows)
    
    @property
    def upcoming_shows(self):
      now = datetime.now()
      upcoming_shows = [show for show in self.shows if datetime.strptime(show.start_time, '%Y-%m-%dT%H:%M:%S.%fZ') > now]
      return upcoming_shows
    
    @property
    def upcoming_shows_count(self):
      return len(self.upcoming_shows)

    def serialize(self):
      return { "id":self.id,
               "name": self.name,
               "genres": self.genres.split(','),
               "city": self.city,
               "state": self.state,
               "phone": self.phone,
               "image_link": self.image_link,
               "website": self.website,
               "facebook_link": self.facebook_link,
               "seeking_venue": self.seeking_venue,
               "seeking_description": self.description,
               "past_shows": self.past_shows,
               "past_shows_count": self.past_shows_count,
               "upcoming_shows": self.upcoming_shows,
               "upcoming_shows_count":self.upcoming_shows_count
      }

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
   

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.



# Data insertion into the database
'''
#------Venue------#
 INSERT INTO 
 "Venue"(id,name,genres,address,city,state,phone,website,facebook_link,seeking_talent,seeking_description,image_link) 
 VALUES(1,'The Musical Hop',ARRAY['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk'],'1015 Folsom Street','San Francisco','CA','123-123-1-234','https://www.themusicalhop.com','https://www.facebook.com/TheMusicalHop',True,'We are on the lookout for a local artist to play every two weeks. Please call us.','https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60');
 
 INSERT INTO 
 "Venue"(id,name,genres,address,city,state,phone,website,facebook_link,seeking_talent,image_link)
 VALUES(2,'The Dueling Pianos Bar',ARRAY['Classical', 'R&B', 'Hip-Hop'],'335 Delancey Street','New York','NY','914-003-1132','https://www.theduelingpianos.com','https://www.facebook.com/theduelingpianos',False,'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80');
 
 INSERT INTO 
 "Venue"
 (id,name,genres,address,city,
 state,phone,website,facebook_link,
 seeking_talent,image_link)
 VALUES(3,'Park Square Live Music & Coffee',
 ARRAY['Rock n Roll', 'Jazz', 'Classical', 'Folk'],
 '34 Whiskey Moore Ave','San Francisco','CA',
 '415-000-1234',
 'https://www.parksquarelivemusicandcoffee.com',
 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
 False,
 'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80');

#----ARTIST-------#

INSERT INTO
"Artist"(id,name,genres,city,state,phone,
website,facebook_link,seeking_venue,seeking_description,image_link)
 VALUES(4,'Guns N Petals',ARRAY['Rock n Roll'],
 'San Francisco','CA','326-123-5000',
 'https://www.gunsnpetalsband.com',
 'https://www.facebook.com/GunsNPetals',True,
 'Looking for shows to perform at in the San Francisco Bay Area!',
 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80');
 
INSERT INTO
"Artist"(id,name,genres,city,state,phone,
facebook_link,seeking_venue,image_link)
 VALUES(5,'Matt Quevedo',ARRAY['Jazz'],
 'New York','NY','300-400-5000',
 'https://www.facebook.com/mattquevedo923251523',
 False,
 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80');

INSERT INTO
"Artist"(id,name,genres,city,state,phone,
seeking_venue,image_link)
 VALUES(6,'The Wild Sax Band',ARRAY['Jazz','Classical'],
 'San Francisco','CA','432-325-5432',False,
 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80');
 
 INSERT INTO
 "Show"(start_time,venue_id,artist_id) 
 VALUES('2019-05-21T21:30:00.000Z',1,4);
 
 INSERT INTO
 "Show"(start_time,venue_id,artist_id) 
 VALUES('2019-06-15T23:00:00.000Z',3,5);

INSERT INTO
 "Show"(start_time,venue_id,artist_id) 
 VALUES('2035-04-01T20:00:00.000Z',3,6);

INSERT INTO
 "Show"(start_time,venue_id,artist_id) 
 VALUES('2035-04-08T20:00:00.000Z',3,6);

 INSERT INTO
 "Show"(start_time,venue_id,artist_id) 
 VALUES('2035-04-15T20:00:00.000Z',3,6);
 '''
 