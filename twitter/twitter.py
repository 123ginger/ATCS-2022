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
            handle = input("\nWhat will your twitter handle be? ")
            password = input("Enter a password: ")
            password_check = input("Re-enter your password: ")
            check = db_session.query(User).where(User.username == handle).first()
            if check == None and password == password_check:
                break
            elif password != password_check:
                print("\nThose passwords don't match. Try again. ")
            elif check != None:
                print("\nThat username is already taken. Try again. ")
        user = User(handle, password)
        self.logged_in = True
        self.current_user = user
        db_session.add(user)
        db_session.commit()
        print("Welcome to ATCS Twitter!")


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
                print("\nWelcome to ATCS Twitter!")
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
        print("\nWelcome to ATCS Twitter!")
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
        
            if (person in self.current_user.following):
                print("You are already following this person lmao. ")
            elif person == None:
                print("Please enter a valid username.")
            else:
                break
        person.followers.append(self.current_user)
        self.current_user.following.append(person)
        db_session().commit()
        print("You are now following " + friend)


    def unfollow(self):
        name = input("Who would you like to unfollow? ")
        person = db_session.query(Follower).where((Follower.following_id == name) and (Follower.follower_id == self.current_user.username)).first()
        if(person == None):
            print("You don't follow " + name)
        else:
            db_session.delete(person)
            db_session.commit()
            print("You are no longer following " + name)

    def tweet(self):
        timestamp = datetime.now()
        tweet = input("Create Tweet: ")
        tags = input("Enter your tags seperated by spaces: ")
        tag_list = tags.split()
        new_tweet = Tweet(tweet, timestamp, self.current_user.username)
        for tag in tag_list:
            new_tag = Tag(tag)
            new_tweet.tags.append(new_tag)
        db_session.add(new_tweet)
        db_session.commit()
        print(new_tweet)
    
             
    def view_my_tweets(self):
        tweets = db_session.query(Tweet).where(Tweet.username == self.current_user.username).all()
        self.print_tweets(tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        recent_tweets = db_session.query(Tweet).join(Follower, Tweet.username == Follower.following_id).where(Follower.follower_id == self.current_user.username).order_by(Tweet.timestamp.desc()).limit(10)
        self.print_tweets(recent_tweets)


    def search_by_user(self):
        person = input("Who's tweets would you like to see? Enter their username. ")
        tweets = db_session.query(Tweet).where(Tweet.username == person).all()
        people = db_session.query(User).where(User.username == person).first()
        
        if tweets == None:
             print("There is no user by that name.")
        elif people == None:
            print("There is no user by that name.")
        else:
            self.print_tweets(tweets)


    def search_by_tag(self):
        tag = input("What tag would you like to view? Enter the tag #___ ")
        tweets1 = db_session.query(Tweet).join(Tweet.tags).where(Tag.content == tag).all()
        tag_exist = db_session.query(Tag).where(Tag.content == tag).first()
        
        if tweets1 == None:
            print("There are no tweets with this tag.")
        elif tag_exist == None:
            print("There are no tweets with this tag.")
        else:
            self.print_tweets(tweets1)
    

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()
        self.startup()
        
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
        

        
        
        
