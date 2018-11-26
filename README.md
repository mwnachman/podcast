
# podcast
The backend of the podcastListener application

## Set-Up local dev environment:
- Install python3 virtual env `python3 -m venv venv`
- Activate it `source venv/bin/activate`
- Install requirements `pip install -r requirements.txt`
- Add to the /static_db directory the following files: (TO DO)

## Running locally:
- Make sure that your virtual environment is active
- From the command line, set the environment variables:  
  `export FLASK_APP=manager`
  `export FLASK_ENV=development`
- From the root directory, initialize and seed the local database:
  `python3 seed_data.py`
- Run the flask app:  
  `flask run`
- Go to http://127.0.0.1:5000/ to see a welcome message.

## Tests:
- To run tests, from the root directory run:
  `flask test`
- New test files should have names starting with "test"
