# About my first project on GitHub

This is a simple project with limited features. 
- **Add event:** After selecting this option, the user is prompted to enter a date in the format yyyy-mm-dd until it is validated by the datetime package,
then they enter a start time for the event on the 24 hour clock using only integers, and a length of the event in hours (again, using only integers). If this timeslot
is empty, they are prompted to enter a description and this event is added to a list of events. If the timeslot is not empty, the descriptions of all events occupying the timeslot are printed.
- **Remove event:** After selecting this option, the user is prompted to enter a description of an event. If this description exists in the list of events, the event is removed. If there are more than one timeslots with the same description, the user is prompted to select removing all of them or one of their choice.
- **Check timeslot:** After selecting this option, the user is prompted the same as in **Add event** to get a timeslot, and if the timeslot is not empty the descriptions of all events occupying the timeslot are printed.
- **Save to file:** The user can select this option to save their changes to the events list to schedule.txt
- **Exit:** This quits the program
