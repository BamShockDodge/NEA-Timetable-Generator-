from website import CSPValues
import random


def assign_csp_values():
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
    for subject in CSPValues.subjects:
        for i in range(1, subject.get_sessions() + 1):
            subject_blocks.append(subject.name + str(i))

    
    for day, available in CSPValues.days_available.items():
        if available == True:
            for i in range(0, 2):
                subject = random.choice(subject_blocks)
                print(subject)
                subject_blocks.remove(subject)
                timetable[day].append(subject)

    print(timetable)
 
    #Apply heuristics to timetable
    #display timetable to website
    

        


