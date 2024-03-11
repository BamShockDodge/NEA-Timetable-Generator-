from website import generator_values
import random


def create_timetable_options():
    #Creates global timetable array which can be accessed from anywhere
    global options 
    #Goes through each subject object in subject array
    for subject in generator_values.subjects:
        #Loops through each hour and creates a subject block for each hour
        for i in range(1, int(subject.get_hours()) + 1):
            subject_blocks.append(subject.name)

    #Generates 100,000 revision timetables
    generate_all_timetables()
    #Gets the three best revision timetables and assigns it to the options variable
    options = get_best_timetables()
   
#Stores the revision sessions the student does each week
subject_blocks = []
#Stores the 100,000 revision timetables
timetables = []
#Stores the best 3 revison timetables
options = []

#Generates all 100,000 revision timetables and appends them to the timetables array
def generate_all_timetables():
    for i in range(100000):
        timetables.append(generate_timetable())

    
#Generates a singular revision timetable
def generate_timetable():
    #Creates a copy of all the students revision sessions
    sessions = subject_blocks.copy()
    #Creates an empty revision timetable using a dictionary
    timetable = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": [],
        "saturday": [],
        "sunday": []}

    #Loops through each day in the dictionary
    for day, available in generator_values.days_available.items():
        #If the student checked the checkbox and is available that day
        if available[0] == True:
            #A subject is randomly assigned for each hour the student said they could revise
            for j in range(0, int(available[1])):
                subject = random.choice(sessions)
                timetable[day].append(subject)
                sessions.remove(subject)
    #Returns the generated revision timetable
    return timetable




#Gets the best 3 revision timetable from the 100,000
def get_best_timetables():
    #A list of the best three organisms which contain the revision timetable and the fitness level
    best_organims = [[{}, -1], [{}, -1], [{}, -1]]
    #Iterates through all 100,000 timetables
    for timetable in timetables:
        #Creates an organism with a revision timetable and a fitness level which is calculated using the revision timetable
        organism = [timetable, get_fitness(timetable)]
        #If the fitness level is greater than any fitness level in the best three revision timetables replace that revision timetable with this current one
        for i in range(0, len(best_organims)):
            if organism[1] > best_organims[i][1] and organism not in best_organims:
                best_organims[i] = organism

    #After all the revision timetables are created iterate through the 2D list and add the best three revision timetables to a separate list
    best_timetables = []
    for best_organim in best_organims:
        best_timetables.append(best_organim[0])

    #Return the best three revision timetables
    return best_timetables

#Calculates fitness using revision timetable
def get_fitness(timetable):
    #Default value for fitness is 500
    fitness = 500
    #Stores the schedule of the previous day
    previous_schedule = []
    #Iterates through each day in timetable
    for day, schedule in timetable.items():
        #List of subjects that day
        checked = []
        #Stores repeated subjects in a day
        repeated_subjects = 0
        #Stores subjects that are the same as the previous day
        repeated_schedule = 0
        #Iterates through each subject in schedule
        for subject in schedule:
            #If the current subject is in the checked list repeated_subjects += 1 else the subject is added to checked
            if subject in checked:
                repeated_subjects += 1
            else:
                checked.append(subject)

            #If a subject today is the same as a subject yesterday repeated_schedule += 1
            if subject in previous_schedule:
                repeated_schedule += 1
                
            
        #The amount of repeated subjects that day all squared * 10 is taken away from fitness value
        fitness -= (repeated_subjects**2) * 10

        #The amount of repeated subjects today that appeared yesterday squared * 5 is taken away from the fitness value
        fitness -= (repeated_schedule**2) * 5
            
        #This current schedule becomes the previous schedule for the next iteration
        previous_schedule = schedule

    #If fitness is negative make it 0
    if fitness < 0:
        fitness = 0

    #Return the fitness value
    return fitness




