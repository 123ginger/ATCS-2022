from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:

    def __init__(self, current_user = None, logged_in = None):
        self.current_user = current_user
        self.logged_in = logged_in
        
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        while True:
            handle = input("What will your twitter handle be? ")
            password = input("Enter a password: ")
            password_check = input("Re-enter your password: ")
            #how to check to see if handle is already taken?
            check = db_session.query(User).where(User.username == handle).first()
            if check == None and password == password_check:
                break
            else:
                print("\nYour password doesnt match or the username is already taken. Try again. ")
                print("Please enter a new username: ")
        user = User(handle, password)
        self.logged_in = True
        self.current_user = user
        db_session.add(user)
        db_session.commit()



    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        while True:
            username = input("Username: ")
            password = input("Password: ")
            user = db_session.query(User).where((User.username == username) and (User.password == password)).first()
            if user is None:
                print("Username or password is invalid")
            else:
                print("Welcome " + username + "!")
                self.current_user = user
                self.logged_in = True
                break
        


    def logout(self):
        self.current_user = None 
        self.logged_in = False

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        print("Welcome to ATCS twitter")
        print("Please select a menu option")
        option = int(input("1. Login \n2. Register User \n3. Exit\n" ))
        if option == 1:
            self.login()
        elif option == 2:
            self.register_user()
        elif option == 3:
            self.end()



    
    def follow(self):
        while True:
            friend = input("Who would you like to follow? ")
            person = db_session.query(User).where(User.username == friend).first()
        
            if (person.username in self.current_user.following):
                print("You are already following this person lmao. ")
            else:
                break
        # person has a new follower 
        person.followers.append(self.current_user)
        # current user is following a new person
        self.current_user.following.append(person)
        print("You are now following " + friend)



    def unfollow(self):
        while True:
            friend = input("Who would you like to unfollow? ")
            person = db_session.query(User).where(User.username == friend).first()
        
            if (person not in self.current_user.following):
                print("You have unfollowed this person already. ")
            else:
                break
        # delete followers from the friend
        person.followers.remove(self.current_user)
        # delete following from current user
        self.current_user.following.remove(person)
        db_session().commit()
        print("You are now unfollowing " + friend)



    def tweet(self):
        tweet = input("Create Tweet: ")
        tags = input("Enter your tags seperated by spaces: ")
        tag_list = tags.split()
        timestamp = datetime.now()
        new_tweet = Tweet(tweet, timestamp, self.current_user.username)
        for tag in tag_list:
            new_tag = Tag(tag)
            new_tweet.tags.append(new_tag)
        db_session.add(new_tweet)
        db_session.commit()
        print(new_tweet)
    
             

    # wrong
    def view_my_tweets(self):
        tweets = db_session.query(Tweet).where(Tweet.username == self.current_user.username).all()
        self.print_tweets(tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        # make max values with limit of 5 descending order 
        recent_tweets = db_session.query(Tweet).join(Follower, Tweet.username == Follower.following_id).where(Follower.follower_id == self.current_user.id).order_by(Tweet.timestamp.desc()).limit(5)
        self.print_tweets(recent_tweets)


    def search_by_user(self):
        person = input("Who's tweets would you like to see? Enter their username. ")
        tweets = db_session.query(Tweet).where(Tweet.username == person).all()
        if tweets == None:
            print("There is no user by that name.")
        else:
            self.print_tweets(tweets)

    # have to make sure tag exists and then make sure if some tweets actually have the tag
    def search_by_tag(self):
        tag = input("What tag would you like to view? Enter the tag #___ ")
        # find tweets where tag content equals input
        #tweets1 = db_session.query(Tag).where(Tag.content == tag).all()
        # find tweets where the tags equal this tag 
        tweets2 = db_session.query(Tweet).where(Tweet.tags == tag).all()
        if tweets2 == None:
            print("There are no tweets with this tag.")
        else:
            self.print_tweets(tweets2)
        #tweets = db_session.query(Tag).join(Tweet, Tweet.tags == tag).where((Tag.content == tag) and (Tweet.tags == tag)).all()

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()
        self.startup()
        print("Welcome to ATCS Twitter!")
        
        while self.logged_in == True:
            self.print_menu()
            option = int(input(""))

            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
        self.end()
        

        
        
        
