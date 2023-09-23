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
        return f'{self.name}:{self.__confidence}'
    


#Function removes empty fields that weren't enterd on the website and calculates the sessions available for a week
def clean_data():
    #Both loops remove unnecessary 4th subject if nothing is inputted
    for subject in subjects:
        if subject.name == '':
            subjects.remove(subject)

    
    #sessions_available is double the amount of days available
    sessions_available = 0
    for key in days_available.keys():
        if days_available[key] == True:
            sessions_available += 2

    #Calls function to work out how many sessions available each subject has each day.
    calculate_sessions(sessions_available)
    
#Calculates the sessions available for each subject each week
def calculate_sessions(sessions_available):
    InverseTotal = 0
    for subject in subjects:
        InverseTotal += 1/subject.get_confidence()
    
    for subject in subjects:
        subject.set_sessions(round(((1/subject.get_confidence())/InverseTotal) * sessions_available, 0))
        print(subject.get_sessions())

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


