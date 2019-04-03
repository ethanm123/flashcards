import os
import hashlib
current_user = ""
import random

class user(): #basic user class
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return "Username: {0} Password: {1}".format(self.name, self.password) #for troubleshooting

    def get_details(self): #setting a username and password, also adding that to the document of users
        self.name = input("Please enter a username")
        self.password = input("Please enter a password")
        os.makedirs("./users/"+self.name)
        file = open("userdetails.txt", "a")
        m = hashlib.sha256()
        m.update(self.password.encode("utf-8"))

        file.write(self.name + "\n")
        file.close()
        f = open("userdetails.txt", "ab")
        f.write(m.hexdigest().encode("utf-8"))
        f.close()
        f = open("userdetails.txt", "a")
        f.write("\n")
        f.close()
        choice = input("Would you like to start a new topic? Enter yes or no")
        if choice.lower() == "yes":
            self.add_topic()
        else:
            exit()

    def add_topic(self): #allowing the user to create a file for their new topic
        new_topic = input(f"{self.name}, please enter the name for your new topic")
        f = open("./users/"+self.name+"/"+new_topic+".txt", "w+")
        f.close()
        choice = input("Would you like to add another topic? Enter y or n")
        if choice.lower() == "y":
            self.add_topic()
        else:
            exit(1)

    def edit_topic(self): #allowing people to add questions
        topic_to_edit = input("Please enter the name of a topic to edit.")
        try: #looking to see if the file exists
            f = open("./users/" + self.name + "/" +topic_to_edit + ".txt", "w")
        except:
            exit("Couldn't find a file with that name.") #Exiting if it cant find one

        while True:
            question = input("Please enter a question. Enter quit to exit.") #Telling the person to enter the thing they want to enter
            if question.lower() == "quit":#allowing the user to exit the program
                f.close()
                exit(1)
            else:   f.write(question + "\n") #if not exiting, writing to the file
            answer = input("Please enter the answer for that question") #getting answer and writing to the file
            f.write(answer + "\n")

    def do_next(self):
        user_choice = input("Please enter what you would like to do next. Enter add to add a topic, or edit to edit a topic. Enter test to get a test on a topic")
        if user_choice.lower() == "add":
            self.add_topic()
        elif user_choice.lower() == "edit":
            self.edit_topic()
        elif user_choice.lower() == "test":
            self.quiz()
        else:
            print("You didn't select a valid option. Exiting...")
            exit(0)

    def quiz(self):
        user_choice = input("Please enter the subject that you want to revise")
        f = open("./users/" + self.name+ "/"+user_choice + ".txt", "r")
        lineList = f.readlines()
        while True:
            while True:
                i = random.randint(0, (len(lineList) -1))
                if i % 2 == 0:
                    break
                else: continue

            user_answer = input("Question: " + lineList[i]+ " or you can enter quit to stop.")
            if  user_answer.lower() == "quit":
                exit(0)
            correct_answer = lineList[i+1]
            if user_answer.lower() in correct_answer.lower():
                print("You got it right! Next question coming up!")
            else:
                print(user_answer, " ", correct_answer)
                print("You got it wrong. The correct answer was: " + correct_answer)



def start(): #starting the program, will run at the start and call other things based on the user input.
    print("Hi there, welcome to flashcards!")
    user_choice = input("Please enter what you'd like to do. Type add to add a new user, or login to enter your username and password.")
    if user_choice.lower() == "add":
        add_user()
    elif user_choice.lower() == "login":
        login()
    else:
        exit("Enter a valid option next time!")


def login(): #if user chooses to login to an existing user
    global current_user
    user_input_name = input("Please enter your username")
    f = open("userdetails.txt", "r")
    fileList = f.readlines()
    j = 0
    for i in fileList: #looping through the file.

        if i.strip() == user_input_name: #checking if the line currently on is the line with the username required
            pass_in_file=fileList[j + 1] #looking for the password
            m = hashlib.sha256()
            user_input_password = input("Please enter your password") #asking for the user to input their password
            m.update(user_input_password.encode("utf-8"))
            if m.hexdigest() == pass_in_file.strip():
                print("You successfully logged in") #logs in if its right
                current_user = user(i.strip(), user_input_password)
                current_user.do_next()
                break
            elif user_input_password != pass_in_file: #if its incorrect itll ask again
                user_input_password = input("Incorrect password, please try again. If you get it wrong once more, the program will close")
                m = hashlib.sha256()
                m.update(user_input_password.encode("utf-8"))
                print(m.hexdigest(), pass_in_file.strip())
                if m.hexdigest() == pass_in_file.strip(): #if its correct, log in
                    current_user = user(i.strip(), user_input_password)
                    current_user.do_next()
                    print("You successfully logged in")
                    break
                else:
                    exit()#if not correct, closes the program
        j = j + 1  # adding one to the line count
    return user_input_name

def add_user():
    new_user = user("x", "y") #need to define something to make the class in the first place
    new_user.get_details()#getting the username and password

start()