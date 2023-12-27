from website import generator

#Class defines subject name and its confidence level as a private variable
class Subject():
    def __init__(self, name, confidence):
        self.name = name
        self.__hours = 0
        #If the confidence has a string value then convert it to an integer, if confidence is '' print value error
        try:
            self.__confidence = int(confidence)
        except ValueError:
            print('Value error')

    #Returns confidence level
    def get_confidence(self):
        return self.__confidence
    
    #Sets confidence level
    def set_confidence(self, confidence):
        self.__confidence = confidence

    #Returns the amount of revision sessions for the subject
    def get_hours(self):
        return self.__hours
    
    #Sets the amount of revision hours for the subject per week
    def set_hours(self, hours):
        self.__hours = hours

    #When the object is printed its attibutes are printed
    def __str__(self):
        return f'{self.name} Confidence:{self.__confidence} Hours:{self.__hours}'
    


#Function removes empty fields that weren't enterd on the website and calculates the sessions available for a week
def clean_data():
    #Both loops remove unnecessary 4th subject if nothing is inputted
    for subject in subjects:
        if subject.name == '':
            subjects.pop(3)

    #Calls function to work out how many hours available to study each subject in a week
    calculate_hours()
    
#Calculates the hours available to study each subject each week
def calculate_hours():
    revision_hours = []
    weekly_total = 0
    inverse_total = 0
    total_hours = 0

    #Bubble Sort for Subjects, orders them by confidences
    for i in range(0, len(subjects)):
        for j in range(0, len(subjects)-1):
            if(subjects[j].get_confidence() > subjects[j+1].get_confidence()):
                temp = subjects[j]
                subjects[j] = subjects[j+1]
                subjects[j+1] = temp

    #Calculate the total time a student will revise in a week
    for day, available in days_available.items():
        weekly_total += int(available[1])

    #Calculates the total of the reciprocal of confidences
    for subject in subjects:
        inverse_total += 1/subject.get_confidence()

    for subject in subjects:
        #Percentage of study sessions of a subject in a week
        weight = ((1/subject.get_confidence())/inverse_total)
        #How much time to spend revising a subject in a week
        hours = round(weight*weekly_total, 0)
        if(hours == 0):
            hours = 1
        revision_hours.append(hours)

    #Calculate the total time a student will revise in a week
    for hours in revision_hours:
        total_hours += hours
    
    #If there is a difference in session_total and weekly_total the if statements will remove the difference
    if (total_hours > weekly_total):
        difference = abs(total_hours - weekly_total)
        #Takes the difference off the largest value
        revision_hours[-1] -= difference
    elif(total_hours < weekly_total):
        difference = abs(total_hours - weekly_total)
        #Adds the difference to the smallest value
        revision_hours[0] += difference

    #Assigns revision_hours values from local array to subject attributes through a setter method
    for i in range(0, len(subjects)):
        subjects[i].set_hours(revision_hours[i])
        
        print(subjects[i])
    print(days_available)
    #Calls the create_timetable_options function from the other class
    generator.create_timetable_options()
        


#All arrays store data on subjects
subjects = []
#Stores the times the student is available and how long they can revise each day
days_available = {
    'monday': [False, 0],
    'tuesday': [False, 0],
    'wednesday': [False, 0],
    'thursday': [False, 0],
    'friday': [False, 0],
    'saturday': [False, 0],
    'sunday': [False, 0]

}

