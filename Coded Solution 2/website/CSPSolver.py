from website import CSPValues
import random




def assign_csp_values():
    global timetable1
    global timetable2
    global timetable3
    timetable1 = generate_timetable()
    timetable2 = generate_timetable()
    timetable3 = generate_timetable()
    

   
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
    for subject in CSPValues.subjects:
        #Loops through each hour
        for i in range(1, int(subject.get_hours()) + 1):
            subject_blocks.append(subject.name)
    print(subject_blocks)

    for day, available in CSPValues.days_available.items():
        if available[0] == True:
            for i in range(0, int(available[1])):
                subject = random.choice(subject_blocks)
                subject_blocks.remove(subject)
                timetable[day].append(subject)

    return timetable
   




        


