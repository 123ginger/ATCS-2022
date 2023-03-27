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
                print("Please enter a new username: ")
        user = user(handle, password)
        self.logged_in = True
        self.current_user = user
        db_session.add(user)



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
        option = input("1. Login \n 2. Register User 3. Exit" )
        if option == 1:
            self.login()
        if option == 2:
            self.register_user
        if option == 3:
            self.end()



    def follow(self):
        while True:
            friend = input("Who would you like to follow? ")
            person = db_session.query(User).where(User.username == friend)
        
            if (person in self.current_user.following):
                print("You are already following this person lmao. ")
            else:
                break
        follower = Follower(self.current_user.id, person.id)
        db_session().add(follower)
        db_session().commit()
        print("You are now following " + friend)



    def unfollow(self):
        while True:
            friend = input("Who would you like to unfollow? ")
            person = db_session.query(User).where(User.username == friend)
        
            if (person not in self.current_user.following):
                print("You have unfollowed this person already. ")
            else:
                break
        db_session().delete(person)
        db_session().commit()
        print("You are now unfollowing " + friend)

    def tweet(self):
        pass
    
    def view_my_tweets(self):
        pass
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        pass

    def search_by_user(self):
        pass

    def search_by_tag(self):
        pass

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
        

        
        
        
