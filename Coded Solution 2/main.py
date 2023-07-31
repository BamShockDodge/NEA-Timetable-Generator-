#imports the function create_app
from website import create_app
#Flask application defined and stored in app
app = create_app()

if __name__ == '__main__': 
    #Flask application is run
    
    app.run(debug=True)