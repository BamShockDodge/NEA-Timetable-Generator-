from website import generator_values
import random

def create_timetable_options():
    #Creates three global timetable variables that can be accessed from any file
    global timetables 
    timetables = []
    #Generates three unique timetable with generate timetable function
    timetables.append(generate_timetable())
    timetables.append(generate_timetable())
    timetables.append(generate_timetable())

   
def generate_timetable():
    #Subject blocks array, which is stores all subject revision sessions
    subject_blocks = []

    #Timetable dictionary which has days of week as keys and array of revision sessions as values
    timetable = {
    'monday': [],
    'tuesday': [],
    'wednesday': [],
    'thursday': [],
    'friday': [],
    'saturday': [],
    'sunday': []
    }
    #Goes through each subject object in subject array
    for subject in generator_values.subjects:
        #Loops through each hour and creates a subject block for each hour
        for i in range(1, int(subject.get_hours()) + 1):
            subject_blocks.append(subject.name)

    #Loops through each key and value in dictionary
    for day, available in generator_values.days_available.items():
        #If the student has checked that days checkbox and is available on that day
        if available[0] == True:
            #They are given revision sessions equivalent to the hours they are available
            for i in range(0, int(available[1])):
                #Random subject is selevted
                subject = random.choice(subject_blocks)
                #Removed from the subject blocks array
                subject_blocks.remove(subject)
                #It is added to the timetable dictionary on as the value corresponding to the days key
                timetable[day].append(subject)
    #Timetable returned
    return timetable
   




        


