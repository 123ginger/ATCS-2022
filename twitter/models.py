"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT, DATETIME
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    following = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.follower_id",
                             secondaryjoin="User.username==Follower.following_id")
    
    followers = relationship("User", 
                             secondary="followers",
                             primaryjoin="User.username==Follower.following_id",
                             secondaryjoin="User.username==Follower.follower_id",
                             overlaps="following")

    def __init__(self, username, password):
            # id auto-increments
            self.username = username
            self.password = password
    
    def __repr__(self):
        return "@ " + self.username


class Follower(Base):
    __tablename__ = "followers"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    follower_id = Column('follower_id', TEXT, ForeignKey('users.username'))
    following_id = Column('following_id', TEXT, ForeignKey('users.username'))

    def __init__(self, follower_id, following_id):
            # id auto-increments
            self.follower_id = follower_id
            self.following_id = following_id



class Tweet(Base):
    __tablename__ = "tweets"

    #columns
    id = Column("id", INTEGER, primary_key=True)
    content = Column('content', TEXT)
    timestamp = Column('timestamp', TEXT)
    username = Column('username', TEXT)
    tags = relationship("Tag", secondary="tweettags", back_populates="tweets")

    def __init__(self, content, timestamp, username):
            # id auto-increments
            self.content = content
            self.timestamp = timestamp
            self.username = username
    
    def __repr__(self):
        tag_string = ""
        for tag in self.tags:
             tag_string += str(tag)
        return "\n@" + self.username + "\n" + self.content + "\n" + tag_string + "\n" + self.timestamp

        

class Tag(Base):
    __tablename__ = "tags"

    #columns
    id = Column("id", INTEGER, primary_key=True)
    content = Column('content', TEXT)
    tweets = relationship("Tweet", secondary="tweettags", back_populates="tags")


    def __init__(self, content):
            # id auto-increments
            self.content = content
    
    def __repr__(self):
        return self.content
    

class TweetTag(Base):
    __tablename__ = "tweettags"

    #columns
    id = Column('id', INTEGER, primary_key=True)
    tag_id = Column('tag_id', TEXT, ForeignKey('tags.id'))
    tweet_id = Column('tweet_id', TEXT, ForeignKey('tweets.id'))

    def __init__(self, tag_id, tweet_id):
        # id auto-increments
        self.tag_id = tag_id
        self.tweet_id = tweet_id
    

    

