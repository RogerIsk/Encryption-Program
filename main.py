#Libaries used in the program:: - we put them here to shorten the code and make the code more readable

import datetime                         # allows us to work with dates and times
import weather                          # allows us to work with the weather.py file which helps us to get the weather data
import json                             # allows us to work with JSON files
import time                             # allows us to work with time / different frin datetime
import os                               # allows us to interact with the operating system
from cryptography.fernet import Fernet  # allows us to encrypt and decrypt data
try:
    from flask_bcrypt import Bcrypt         # allows us to hash passwords
except ImportError:
    print("Error: flask_bcrypt module not found. Please install it.")
    exit(1)
from stringcolor import cs              # allows us to color the text in the terminal

#======================================================================================================
#Global variables - variables that are used in multiple functions:: - we put them here to shorten the code and make the code more readable

usernames = ""                          # variables that store the username inputed by the user
passwords = ""                          # variables that store the password inputed by the user
message = ""                            # variable that stores the message inputed by the user
messages = ""                           # variable that stores the message inputed by the user in the register_account function
messages_list = []                      # list that stores the messages
credentials = {}                        # dictionary that stores the credentials
key = Fernet.generate_key()             # generate a key for the encryption globaly
fernet = Fernet(key)                    # create a Fernet instance with the key globaly
encMessages = ""                        # variable that stores the encrypted messages
bcrypt = Bcrypt()                       # create an instance of the Bcrypt class                                                           
name_input = ""                         # variable that stores the name inputed by the user after logging in
data = []                               # list that stores the data from the JSON file
JSON_FILE = './users.json'              # variable that stores the path to the JSON file for easier use later in the code

#======================================================================================================
# Functions::

clear = lambda: os.system('clear')      # define a "clear" function that clears the terminal from previous lines
clear()                                 # call the clear function to clear the terminal

def main_menu_ui():         # Function that shows the main menu choices - User Interface (Graphical part of the main menu) - ONLY PRINTING
    print(cs("Welcome to the encryption program. \n" , "blue"))             # print the welcome message
    weather.main()                                                          # call the weather.main() function to get the weather data
    print("\n")                                                             # print a new line 
    print("╔" + "═" * 14 + "╗")                                             # print the top border of the main menu
    print("║ 1. Login     ║" , "\n║ 2. Register  ║" , "\n║ 3. Exit      ║") # print the choices of the main menu
    print("╚" + "═" * 14 + "╝\n")                                           # print the bottom border of the main menu

def main_menu_logic():      # Function that works as the main menu of the program (logical part of the main menu)
    main_menu_ui()          # Call and show the main menu choices
    main_menu_choice = ""   # variable that stores the choice of the user in the main menu
    while True:             # loop that runs until the user enters a valid choice from the main menu options (login, register, exit)
        main_menu_choice = input("Enter your choice: ").lower()             # ask the user to enter a choice - it gets lowercased to make it easier to compare
        clear()                                                             #
        main_menu_ui()                                                      # call the main menu UI to show the choices again after clearing the terminal
        if main_menu_choice == 'login' or main_menu_choice == '1':          # if the user enters 'login' or '1' - the program will allow the user to login
            clear()                                                         #
            logging_in()                                                    # the logging_in function will be called so the the user can input their username and password
            logged_in_menu_logic()                                          # call the logged_in_menu_logic function to show the choices after logging in
        elif main_menu_choice == 'register' or main_menu_choice == '2':     # if the user enters 'register' or '2' - the program will allow the user to register
            clear()                                                         #
            register_account()                                              # the register_account function will be called so the user can register a new account
        elif main_menu_choice == 'exit' or main_menu_choice == '3':         # if the user enters 'exit' or '3' - the program will stop running
            clear()                                                         #
            print(cs("Exiting program", "magenta") , end='', flush=True)    # print the message that the program is exiting
            print(print_letters_appart(20 * '.'))                           # print the dots separately to make the program look like it's exiting
            time.sleep(0.5)                                                 # wait for 0.5 seconds before exiting (all special effects basically)
            clear()                                                         #
            exit()                                                          # this is where the program finally stops running
        elif (not main_menu_choice.strip or main_menu_choice != 'login' or 'register' or # if the user enters something other than 'login' or 'register' or 'exit' or '1' or '2' or '3'
            'exit' or '1' or '2' or '3' ()):                                # here a sick technique is used allowing us to write the condition in multiple lines for better readability       
            print("Please enter a valid choice.")                           # print the message that the user needs to enter a valid choice
            time.sleep(1)                                                   #
            clear()                                                         #
            main_menu_ui()                                                  # call the main menu UI to show the choices again so the user can see and choose what to enter
            continue                                                        # continue the loop until the user enters a valid choice
        break                                                               # break the loop when the user enters a valid choice

def register_account():     # Function that lets you register a new account
    global messages, usernames, passwords                         # like this we are able to use the variables in the function without giving them values
    while True:                                                   # loop that runs until the user enters a valid username
        usernames = input(cs("Enter a new username: ", "cyan"))   # ask the user to enter a new username and color the text in cyan
        if not usernames.strip():                                 # if the username is blank '.strip()' removes the whitespace from the string
            print("Username cannot be blank. Please try again.")  # print the message that the username cannot be blank
            time.sleep(1)                                         #
            clear()                                               #
            continue                                              # continue the loop until the user enters a valid username
        else:                                                     # we put else just to complete the if statement, we don't need it
            break                                                 # break the loop when the user enters a valid username
    while True:                                                   # loop that runs until the user enters a valid password
        passwords = input(cs("Enter a new password: ", "cyan"))   # ask the user to enter a new password and color the text in cyan
        if not passwords.strip():                                 # if the password is blank '.strip()' removes the whitespace from the string
            print("Password cannot be blank. Please try again.")  # print the message that the password cannot be blank
            time.sleep(1)                                         
            clear()                                               
            continue                                              
        else:                                                      
            hashed_passwords = bcrypt.generate_password_hash(passwords).decode('utf-8')  # Hash the password - convert the password to a string and stores it in the variable
            clear()
            break 
    while True:
        global encMessages
        print('Would you like to enter an initial message? (yes/no): ')
        initial_message = input().lower()                                 # ask the user if they want to enter an initial message and lower the input
        if not initial_message.strip():                                   # if the input is blank '.strip()' removes the whitespace from the string
            print('Yes or no? ')                                          #
            time.sleep(1)                                                 #
            clear()                                                       #
        if initial_message.startswith('y'):                                      # if the user enters 'yes' - the program will allow the user to enter a message
            clear()                                                       #
            messages = input(f"Hi {cs(usernames.title(), 'cyan')}, enter the message you want to encrypt: ") # ask the user to enter a message
            adding_date_to_message()                                      # add the date and time to the message
            clear()                                                       #
            encryption_function()                                         # encrypt the message
            print(cs("Encrypting: ", "green"), end='', flush=True)        # print the message that the program is encrypting the message (a visual effect)
            print(print_letters_appart(encMessages))                      # print the dots separately to make the program look like it's encrypting the message and loading
            print(cs("\nMessage added!" , "yellow"))                      #   
            time.sleep(2)                                                 #      
            break                                                         # break the loop when the user enters a valid message
        elif initial_message.startswith('n'):                                     # if the user enters 'no' - the program will not allow the user to enter a message
            clear()                                                       #
            break                                                         # break the loop when the user enters 'no'
        elif initial_message != 'yes' or initial_message != 'no':         # if the user enters something other than 'yes' or 'no'
            print('Would you like to enter an initial message? (yes/no): ')
            clear() 

    credentials = { # With this code we store the usernames, passwords, messages and keys of the user in the credentials dictionary
    'username': usernames,         # Store the username
    'password': hashed_passwords,  # Store the hashed password
    'messages': encMessages.decode('utf-8'),          # Store the message
    'key': key.decode('utf-8')}    # Convert the key to a string and store it
    
    load_user_data()                              # Load the user data from the JSON file before registration
    data.append(credentials)                      # adding the new credentials to the list
    with open(JSON_FILE, 'w') as output_file:     # Write the data back to the JSON file
        json.dump(data, output_file, indent=2)    # We use dump to store/trasfer the data to the JSON file

    print(cs("\nRegistration successful!" , "yellow"))                   #
    time.sleep(2)                                                        #
    clear()                                                              #
    print(cs("Redirecting to main menu", "orange"), end='', flush=True)  #
    print(print_letters_appart(20 * '.'))                                # - All of these lines are just for the visual effect of the program
    time.sleep(0.5)                                                      #
    clear()                                                              #
    print("You can now login with your new account. ")                   #
    time.sleep(3)                                                        #
    clear()                                                              #
    main_menu_logic()                                                    # calling the main menu logic function to show the choices again after registration

def logging_in():           # Function that lets you login to your account
    load_user_data()                                                     # Load the user data from the JSON file before login, allows us to work with the data
    global usernames, passwords, name_input                              # like this we are able to use the variables in the function without giving them values again, we save space
    while True:                                                          # loop that runs until the user enters a valid username
        name_input = input(cs("Enter your username: ", "cyan"))          # ask the user to enter their username and color the text in cyan
        if not name_input.strip():                                       # if the username is blank '.strip()' removes the whitespace from the string
            print("The username cannot be blank. Please try again.")     # print the message that the username cannot be blank
            time.sleep(1)                                                #
            clear()                                                      #
            continue                                                     # continue the loop until the user enters a valid username
        elif name_input in [user['username'] for user in data]:          # if the username is in the data list
            passwords_input = input(cs("Enter your password: ", "cyan")) # ask the user to enter their password and color the text in cyan
            if not passwords_input.strip():                              # if the password is blank '.strip()' removes the whitespace from the string
                print("Password cannot be blank. Please try again.")     # print the message that the password cannot be blank
                time.sleep(1)                                            
                clear()                                                  
                continue                                                 # we check if the password corresponds to the usernames password in the json file
            elif bcrypt.check_password_hash([user['password'] for user in data if user['username'] == name_input][0], passwords_input): 
                print(cs("Logging in", "yellow"), end='', flush=True)    # print the message that the program is logging in the user (if the password is correct)
                print(print_letters_appart(20 * '.'))                    
                time.sleep(0.5)
                clear()
                break
            else:
                print(cs("Incorrect password >:()", "red"))              # print the message that the password is incorrect
            logging_in()                                                 # call the logging_in function to allow the user to enter the username and password again
        else:                                                            # if the username is not in the data list
            while True:                                                  # loop that runs until the user enters a valid choice
                print(cs("Non-existent username >:()", "red"))           # print the message that the username does not exist
                print("\nWould you like to register? (yes/no) ")         # ask the user if they want to register
                question = input().lower()                               # ask the user to enter 'yes' or 'no' and lower the input
                if not question.strip():                                 # if the input is blank '.strip()' removes the whitespace from the string
                    print("Yes or no?")                                  # print the message that the user needs to enter 'yes' or 'no'
                    time.sleep(1)                                        #
                    clear()                                              #
                elif question.startswith("y"):                                  # if the user enters 'yes' - the program will allow the user to register
                    clear()                                              #
                    print("Redirecting to registration page", end='', flush=True) # print the message that the program is redirecting to the registration page
                    print(print_letters_appart(20 * '.'))                #
                    clear()                                              #
                    register_account()                                   # call the register_account function to allow the user to register
                    break                                                # break the loop when the user enters 'yes'
                elif question.startswith("n"):                                   # if the user enters 'no' - the program will not allow the user to register
                    clear()                                              #
                    print("Redirecting to main menu", end='', flush=True)# print the message that the program is redirecting to the main menu
                    print(print_letters_appart(20 * '.'))                #
                    clear()                                              #
                    main_menu_logic()                                    # call the main_menu_logic function to show the choices again after logging in
                    break                                                # break the loop when the user enters 'no'
                else:                                                    # if the user enters something other than 'yes' or 'no'
                    print("Invalid input. Please enter 'yes' or 'no'.")  # print the message that the user needs to enter 'yes' or 'no'
                    time.sleep(1)                                        #
                    clear()                                              #

def logged_in_menu_ui():    # Function that shows the logged in menu choices - User Interface (Graphical part of the logged in menu) - ONLY PRINTING
    print(cs("Welcome to the encryption program. \n" , "blue"))             
    print( 'Logged in as:' , (cs(f"{name_input.title()} \n", "cyan")))
    weather.main()                                                          # call the weather.main() function to get the weather data
    print("\n")                                                             # print a new line 
    print("╔" + "═" * 22 + "╗")
    print("║ 1. Display message   ║" , "\n║ 2. Add Message       ║" , "\n║ 3. Delete Message    ║")
    print("║ 4. Delete Account    ║" , "\n║ 5. Log out           ║" , "\n║ 6. Exit              ║")
    print("╚" + "═" * 22 + "╝\n")

def logged_in_menu_logic():     # Function that works at the program menu once logged in (logical part of it)
    logged_in_menu_ui()         # Call and show the logged in menu choices
    global messages, fernet, name_input
    import cryptography
    while True:                 # loop that runs until the user enters a valid choice from the main menu options
        logged_in_choice = input("Enter your choice: ").lower()             # ask the user to enter a choice - it gets lowercased to make it easier to compare

        if logged_in_choice in ['display messages', '1']:                   # if user enters 'display messages' or '1' - the program will display the messages from that user -
            clear()
            load_user_data()                                    # Load the user data from the JSON file, allows us to work with the data
            messages_string = read_messages_from_json()[0]      # Calls the function read_messages_from_json to access messages starting from index [0]
            messages_list = messages_string.split('\n')         # Split the string (all the messages together, separated by \n) into individual messages
            print(cs("Displaying messages", "magenta"))
            for message in messages_list:                       # Apply the following to every single message:
                try:
                    decrypted_message = fernet.decrypt(message.encode()).decode()       # Convert message from string to bytes, decrypt message and converting it to string again
                    print(decrypted_message)                                            # Print decrypted message
                except cryptography.fernet.InvalidToken:                                # If there is no valid key, will return the following error message:
                    print("Error: Unable to decrypt message. Invalid token.")
            input("\nPress Enter to continue...")
            clear()                                                         # Clear terminal
            logged_in_menu_logic()                                          # Go back to the start of the logged in menu
            break

        elif logged_in_choice in ['add message', '2']:                      # if user enters 'add messages' or '2' - runs the option to add messages
            clear()
            messages = input(cs("Enter a new message: ", "cyan"))           # Ask user to input a new message
            print(cs("Encrypting: ", "green"), end='', flush=True)                      
            adding_date_to_message()                                        # add the date and time to the message
            write_to_json()                                                 # Access the JSON file for writing
            encryption_function()                                           # encrypt the message
            add_message_in_json(name_input, encMessages)                    # Add message to the JSON file
            print(print_letters_appart(encMessages))                        # Print encrypted message
            print(cs("\nMessage added!", "yellow"))
            time.sleep(2)
            clear()
            logged_in_menu_logic()                                          # Go back to the start of logged in menu
            break

        elif logged_in_choice in ['delete message', '3']:                   # if user enters 'delete message' or '3' - runs the option to delete messages
            clear()
            load_user_data()                                                # Access the JSON file for reading
            messages_list = read_messages_from_json()                       # Access the messages from the JSON file
            delete_messages()                                               # calls the function to delete messages
            break

        elif logged_in_choice in ['delete account', '4']:                   # if user enters 'delete account' or '4' - runs the option to delete account
            clear()
            delete_account()                                                # calls the function to delete account

        elif logged_in_choice in ['log out', '5']:                          # if user enters 'log out' or '5' - logs out of current account
            clear()
            print(cs("Logging out", "magenta"), end='', flush=True)         # Prints "Logging out" in a fancy way
            print(print_letters_appart(20 * '.'))                           # Nice text effects....
            time.sleep(0.5)
            clear()
            print(cs("Redirecting to main menu", "orange"), end='', flush=True)
            print(print_letters_appart('..........\n\n'))
            clear()
            main_menu_logic()                                               # Go back to main menu

        elif logged_in_choice in ['exit', '6']:                             # if user enters 'exit' or '6' - exit the program
            print(cs("Exiting program", "magenta"), end='', flush=True)     # Nice texts effects...
            print(print_letters_appart(20 * '.'))
            time.sleep(1.5)
            clear()                                                         # clear terminal
            exit()                                                          # exit the program

def load_user_data():       # Function that loads the user data from the JSON file
    global data, encMessages                                 
    if os.path.exists(JSON_FILE) and os.stat(JSON_FILE).st_size != 0: # Check if the JSON file exists and is not empty
        with open(JSON_FILE) as json_file:                            # Open the JSON file in read mode
            data = json.load(json_file)                               # Load the data from the JSON file
            if isinstance(data, dict):                                # If 'data' is a dictionary, convert it to a list
                data = [data]                                         # This is done to make the data easier to work with
    else:                                                             #
        data = []                                                     # If the file doesn't exist or is empty, start with an empty list

def read_from_json():       # Function that reads the data from the JSON file
    with open(JSON_FILE, 'r') as json_file: # Open the JSON file in read mode
        data = json.load(json_file)         # Load the data from the JSON file
    return data                             # Return the data

def write_to_json():        # Function that writes the data to the JSON file
    global JSON_FILE, data                    # we have to use JSON_FILE and data as global variables - otherwise it doesnt work
    with open(JSON_FILE, 'w') as json_file:   # Open the JSON file in write mode
        json.dump(data, json_file, indent=2)  # Write the data to the JSON file

def read_messages_from_json(): # Function that reads the messages from the JSON file / specifically the messages of the logged in user
    global JSON_FILE, data, name_input, key  # 
    with open(JSON_FILE, 'r') as json_file:  # Open the JSON file in read mode
        data = json.load(json_file)          # Load the data from the JSON file
        messages = [user['messages'] for user in data if user['username'] == name_input]  # Extracting only the "messages" field from the loggedin user's dictionary 
    return messages                          # Return the messagesa

def add_message_in_json(name_input, messages):   # Function that adds the message to the JSON file
    global data                                  # we have to use data as a global variable - otherwise it doesnt work
    for user in data:                            # Loop through the data list
        if user['username'] == name_input:       # If the username matches the logged in user
            if 'messages' in user:               # If the user has messages
                if isinstance(messages, str):    # Ensure messages is a byte string
                    messages = messages.encode() # Convert messages to bytes
                user['messages'] = (user.get('messages', '').encode() + b'\n' + messages).decode() # Add the new message to the existing messages
            else:                                # If the user has no messages
                user['messages'] = messages      # Add the message to the user's dictionary
            write_to_json()                      # Write the data back to the JSON file
            break                                # Break the loop

def delete_messages():                                # Function that deletes the messages
    global name_input, messages_list, data            # we have to use name_input, messages_list and data as global variables - otherwise it doesnt work
    import cryptography                               # Import the cryptography module in the function to avoid errors
    clear()                                           
    print("\nSelect the message you want to delete:") 
    load_user_data()                                  # Load the user data from the JSON file
    messages_string = read_messages_from_json()[0]    # Get the first (and only) item in the list
    messages_list = messages_string.split('\n')       # Split the string into individual messages
    for i, message in enumerate(messages_list):       # Loop through the messages list
        try:
            decrypted_message = fernet.decrypt(message.encode()).decode() # Decrypt the message
            print(f"{i+1}. {decrypted_message}")                          # Print the decrypted message
        except cryptography.fernet.InvalidToken:                          # If the message cannot be decrypted
            print("Error: Unable to decrypt message. Invalid token.")     # Print an error message
    # rest of the function...
    choice = input("Enter the number of the message you want to delete (or 'q' to cancel): ") 
    if choice == 'q':                                 # If the user enters 'q' - cancel the deletion
        clear()                                       # Clear the terminal before returning to the logged in menu
        logged_in_menu_logic()                        # Go back to the start of the logged in menu
    try:
        index = int(choice) - 1                       # Convert the choice to an integer and subtract 1 to get the index
        if index < 0 or index >= len(messages_list):  # If the index is out of range
            print("Invalid choice. Please try again.")# Print an error message
            time.sleep(2)                             # Wait for 2 seconds before returning to the delete_messages function
            delete_messages()                         # Return to the delete_messages function
            return                                    # Return to prevent further execution
        else:
            del messages_list[index]                  # Delete the message at the specified index
            print("Message deleted successfully.")    # Print the message that the message was deleted successfully
            for user in data:                         # Loop through the data list
                if user['username'] == name_input:    # If the username matches the logged in user
                    user['messages'] = '\n'.join(messages_list) # Join the messages list into a string
                    write_to_json()                   # Update the JSON file with the modified messages list
                    time.sleep(2)                     # Wait for 2 seconds before returning to the logged in menu
                    delete_messages()                 # Return to the delete_messages function
    except ValueError:                                # If the user enters a non-integer value
        print("Invalid choice. Please try again.")    # Print an error message
        delete_messages()                             # Return to the delete_messages function

def encryption_function():                          # Function that encrypts the message
    global messages, encMessages, fernet            # we have to use messages, encMessages and fernet as global variables - otherwise it doesnt work
    encMessages = fernet.encrypt(messages.encode()) # Encrypt the message and store it in the variable
    return encMessages                              # Return the encrypted message as bytes

def print_letters_appart(string):         # Function that prints out string characters one by one
    for char in string:                   # loop that runs through the characters in the string
        time.sleep(0.03)                  # wait for 0.03 seconds before printing the next character
        print(char, end=' ', flush=True)  # print the character and flush the output buffer
    return ''                             # return an empty string

def adding_date_to_message():             # Function that adds the date and time to the message
    global messages
    messages += f" - Message created at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" # Add the date and time to the message
    messages_list.append(fernet.encrypt(messages.encode()).decode('utf-8'))                       # Encrypt and add the message to the list       

def delete_account():                      # Function that deletes the account of the logged in user
    global name_input, data, JSON_FILE     # we have to use name_input, data and JSON_FILE as global variables - otherwise it doesnt work
    while True:                            # loop that runs until the user enters a valid choice
        confirmation = input("Are you sure you want to delete your account? (yes/no): ").lower() # ask the user if they want to delete their account and lower the input
        if confirmation.startswith('y'):                                          # if the user enters 'yes' - the program will delete the account
            data = [user for user in data if user['username'] != name_input]      # Delete the user from the data list
            write_to_json()                                                       # Write the data back to the JSON file
            print(cs("Account deleted successfully!", "yellow"))                  # print the message that the account was deleted successfully
            time.sleep(2)   
            clear()    
            print(cs("Redirecting to main menu", "orange"), end='', flush=True)   # print the message that the program is redirecting to the main menu
            print(print_letters_appart(20 * '.'))                                 # print the dots separately to make the program look like it's redirecting
            time.sleep(0.5)                                                       # wait for 0.5 seconds before redirecting to the main menu
            clear()
            main_menu_logic()                # call the main_menu_logic function to show the choices again after deleting the account
            break                            # break the loop when the user enters 'yes'
        elif confirmation.startswith('n'):   # if the user enters 'no' - the program will not delete the account
            clear()  
            logged_in_menu_logic()      # call the logged_in_menu_logic function to show the choices again after not deleting the account
            break                       # break the loop when the user enters 'no'
        else:                           # if the user enters something other than 'yes' or 'no'
            print("Invalid input. Please enter 'yes' or 'no'.")   # print the message that the user needs to enter 'yes' or 'no'
            time.sleep(1)   
            clear()                     # wait for 1 second before clearing the terminal

def load_key():                         # Function that loads the encryption key from the file
    key_file = "encryption_key.txt"     # variable that stores the path to the file with the encryption key
    if os.path.exists(key_file):        # if the file with the encryption key exists
        with open(key_file, "rb") as f: # open the file in read mode
            key = f.read()              # read the key from the file
    else:                               # if the file with the encryption key does not exist
        key = Fernet.generate_key()     # generate a new key
        with open(key_file, "wb") as f: # open the file in write mode
            f.write(key)                # write the key to the file
    return key                          # return the key

key = load_key()                        # load the encryption key
fernet = Fernet(key)                    # create a Fernet instance with the key

main_menu_logic()                       # This is where the program starts.
