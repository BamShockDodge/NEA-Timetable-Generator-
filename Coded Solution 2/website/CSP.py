import math

#Class defines subject name and its confidence level as a private variable
class Subject():
    def __init__(self, name, confidence):
        self.name = name
        self.__sessions = 0
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
    def get_sessions(self):
        return self.__sessions
    
    #Sets the amount of revision sessions for the subject
    def set_sessions(self, sessions):
        self.__sessions = sessions

    #When the object is printed its attibutes are printed
    def __str__(self):
        return f'{self.name} Confidence:{self.__confidence} Sessions:{self.__sessions}'
    


#Function removes empty fields that weren't enterd on the website and calculates the sessions available for a week
def clean_data():
    #Both loops remove unnecessary 4th subject if nothing is inputted
    for subject in subjects:
        if subject.name == '':
            subjects.pop(3)

    
    #sessions_available is double the amount of days available
    sessions_available = 0
    for key in days_available.keys():
        if days_available[key] == True:
            sessions_available += 2

    #Calls function to work out how many sessions available each subject has each day.
    calculate_sessions(sessions_available)
    
#Calculates the sessions available for each subject each week
def calculate_sessions(sessions_available):
    inverse_total = 0
    #Calculates the total of the reciprocal of confidences
    for subject in subjects:
        inverse_total += 1/subject.get_confidence()
    
    #Total amount of sessions that are used by all the subjects
    sessions = []
    total_sessions = 0

    for subject in subjects:
        #Total amount of sessions in a week rounded down
        total_sessions += math.floor(((1/subject.get_confidence())/inverse_total) * sessions_available)

        #for each subject its session count is set to the ratio of the reciporcal of confidence to the inverse total times by the sessions available all rounded down
        sessions.append((math.floor(((1/subject.get_confidence())/inverse_total) * sessions_available)))
        
    #Gets the index of the highest session value
    maximum_sessions_index = sessions.index(max(sessions))
    #If there are leftover sessions they will be added to the highest session value
    sessions[maximum_sessions_index] += (sessions_available - total_sessions)

    #Assigns session values from local array to subject attributes through a setter method
    for i in range(0, len(subjects)):
        subjects[i].set_sessions(sessions[i])
        
        print(subjects[i])
        


#All arrays store data on subjects
subjects = []
days_available = {
    'monday': False,
    'tuesday': False,
    'wednesday': False,
    'thursday': False,
    'friday': False,
    'saturday': False,
    'sunday': False

}


