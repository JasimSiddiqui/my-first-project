'''
Second iteration of my schedule project.

Will have 4 available functions to user:
    - Add an event [Completed]
        - User will enter a date in a format that datetime can strip
        - User will enter a time in 24 hour clock and length of event in hours
        - Program will run through the keys of current events to make sure date+time-time is not there [Completed]
        - If slot is empty, will ask user for description of event and add to dictionary [Completed]
        - If slot is not empty, will provide description of events currently occupying timeslot

    - Check a timeslot [Completed]
        - User will enter a date in a format that datetime can strip
        - User will enter a time in 24 hour clock and length of slot in hours
        - Program will run through the keys of current events and return any event that is happening during this timeslot [Completed]

    - Remove an event [Completed]
        - User will enter the description of an event
        - Program will ask whether to remove all instances of event or specific date
        - If specific date is chosen, all instances dates will be printed and the user will enter a respective number to select which date
        - All instances is self explanatory

    - Save & Load file [Completed]
        - Save function
        - Load function (will only run once at start of program)


I will have the program read through the provided file once at the start of the program and add to dictionary in format: 
{'yyyy-mm-ddtste':description} 
where ts and te are time start and time end in hours on the 24 hour clock respectively. 

All functions will be using that dictionary rather then reading and writing (other than the function that reads and function that writes). 

The file will be written similarly, with a comma rather than a colon seperating the keys and description so .split can be used:
yyyy-mm-ddtste,description1
yyyy-mm-ddtste,description2
etc.


'''
#Can get todays date in format yyyy-mm-dd
from datetime import datetime
import os

events = {}

#Reads in the file and fills the events list
def loadin():
    with open('schedule.txt', 'r') as x:
            string = x.readline()
            while string:
                #List of the current string
                time_description_list = string.rstrip().split(',')
                #Adds this list to the events list
                events[time_description_list[0]] = time_description_list[1]
                string = x.readline()

#Overwrites the file with the current events list
def save():
    with open('schedule.txt', 'w') as x:
         for date_and_time in events:
              x.write(f'{date_and_time},{events[date_and_time]}\n')

#Removes event given description of event
def remove_event(description):
    #Returns false if no event description in event
    if description not in events.values():
        print('No event matches description.')
    #If there is more than one key with the value, asks user whether they want to delete all or next instance. Will change this to check current date for next, and add a third option called 'select', which will output all of the dates with the description and ask the user to select one.
    if list(events.values()).count(description) > 1:
        #Adds the key of every element with same description to a list
        keys_to_remove = [event for event in events if events[event] == description]
        
        #Defaults to choose rather than looping for valid input
        x = input('(any other input defaults to choose)\nAll[1] or Choose[2]: ')
        if x == '1':
            #Deletes all keys with same description
            for key in keys_to_remove:
                del events[key]
        else:
            #Print out options
            for key in keys_to_remove:
                print(f'[{keys_to_remove.index(key)}] {key}')
            #Keep asking for key until valid input
            while True:
                try:
                    del events[keys_to_remove[int(input('Which key to remove: '))]]
                    break
                except:
                    print('Please enter a valid choice')
    else:
        #If there's only one, removes that one
        for event in events:
            if events[event] == description:
                del events[event]
                break
    print('Success.')

#Will add an event to events if the timeslot is not occupied
def add_event(timeslot):
    if check_timeslot(timeslot):
        return False
    else:
        events[timeslot] = input('Description of event: ')
        return True
    
#Prints the event(s) occupying given timeslot, returns false if the timeslot is empty
def check_timeslot(timeslot):
    #Fills up with all the descriptions of events overlapping given timeslot
    event_descriptions = [events[event] for event in events if check_overlap(timeslot, event)]
    if event_descriptions:
        #Prints out all the events occuring in given timeslot seperated by ', and ' 
        print('This timeslot is occupied by:', ", and ".join(event_descriptions))
        return True
    else:
        #Empty timeslot
        return False

#Returns True if there is overlap in the provided times, else returns false
def check_overlap(timeslot1, timeslot2):
    #Hardcoded date checking (yyyy-mm-dd) is ten characters
    if timeslot1[:10] == timeslot2[:10]:
        #Hardcoded time overlaps, [10:12] is time start and [12:] is time end
        if int(timeslot1[10:12]) < int(timeslot2[12:]) and int(timeslot2[10:12]) < int(timeslot1[12:]):
            return True
    return False

#Uses datetime to verify given date exists on a calender
def is_valid_date(date_string):
    #Must be ten characters in format yyyy-mm-dd
    if len(date_string) != 10 or date_string[4] != '-' or date_string[7] != '-':
        return False
    try:
        #Makes sure its a valid date
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

#Gets a valid timeslot from user and returns it
def timeslotter():
    #Asks for date until correct input and date exists
    given_date = input('Please enter date in yyyy-mm-dd: ')
    while not is_valid_date(given_date):
        given_date = input('Please enter valid date in yyyy-mm-dd format (including dashes): ')
    #Asks for start time in 24 hour clock until valid input
    while True:
        try:
            given_time = int(input('Enter a time in 24 hour clock (start time): '))
            if given_time < 24 and given_time >= 0:
                break
            print('Must be between 0-23')
        except:
            print('Invalid input. (eg. 3:00pm -> 15)')
    #Asks for length of time that doesn't exceed 24 hour clock until valid input
    while True:
        try:
            given_length = int(input('Enter a length in hours: '))
            if given_length > 0 and given_length + given_time <= 24:
                break
            print('Length + Start time must not exceed 24')
        except:
            print('Invalid input. Must be an integer.')
    #Given length becomes end time
    given_length = str(given_length + given_time)
    given_time = str(given_time)
    #Adding the leading 0s to make sure parsing in check_overlap is valid (ts and te need to be two characters long each)
    if int(given_length) < 10:
        given_length = '0' + given_length
    if int(given_time) < 10:
        given_time = '0' + given_time
    #Returns in the timeslot format (how the keys in events look)
    return (given_date + given_time + given_length)


loadin()
while True:
    choice = input('[1] Add an event\n[2] Check a timeslot\n[3] Remove an event\n[4] Save to File (default)\n[5] Exit\nChoice: ')
    if choice == '1':
        add_event(timeslotter())
    elif choice == '2':
        if check_timeslot(timeslotter()) == False:
            #Printing this here rather than in function since add_event calls check_timeslot too, and it looks ugly/out of place to have 'timeslot is empty' when that runs
            print('Timeslot is empty.')
    elif choice == '3':
        remove_event(input('Description of event to remove: '))
    elif choice == '5':
        print('Quitting program...')
        break
    #Rather than checking inputs with try except, just saves to file on bad input. Same as in remove_event.
    else:
        save()
        print('Saved!')
    # print(events)
    input('[Press enter to continue]')
    os.system('cls')

