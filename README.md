THE TRIVIA 
the trivia is a quiz app that connects the user to many quz questions, it is entertaining and educative. it allows the user to craete a new quiz, delete an existing quiz or pick from a randomized category of quizzes.

all backend follows PEP* style guidelines

GETTING STARTED

prerequisites and local development:
developer should have node and python3 installed

backend

for the backend we use flask and sqlalchemy for the Models .
all neccessary packages and dependencies are located in the requirement file. it can be run by pip3 install -r requirements.txt; in the backend directory.
 to run use:
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

this should start the development server

frontend

from the frontend directory, use:
npm install to install all react dependencies

and npm start to start the app

API REFERENCE
base URL:
http://127.0.0.1/ or localhost

errors

status code 404
returns:
{
'success':False,
'error': 404,
'message': 'resource not found'
}

status code 422
returns:
{
'success':False,
'error': 422,
'message': 'unprocessable'
}

status code 405
returns: {
'success':False,
'error': 405,
'message': 'method not allowed'
}


resource endpoint

GET '/categories'

fetches a dictionary of categories which the keys are the ids and the values is the corresponding string of the category

request arguments: none
returns: an object with a single key, categories, that contains an object of id:category_string

{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}

GET '/questions'

fetches a dictionary of keys  questions and total number of questions. the question key which is a paginated list of objects containing two key value pairs. keys: category and question with their corresponding values. each page contains 10 questions

request argument: none
returns: 
{
  "questions": [
    {
      "category": "Art", 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }.....
   ],
   "total_number_of_questions": 19
}


GET '/categories/{id}/questions'
this returns questions based on a given category

request arguement: id of the category

returns:
an object whose key is the category_type containing the id of the question and the question itself

{
  
  "Art": {
    "16": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?", 
    "17": "La Giaconda is better known as what?", 
    "18": "How many paintings did Van Gogh sell in his lifetime?", 
    "19": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  }
}

DELETE '/questions/{id}'

this deletes the question based on the id
request argument:takes in the id of the question



Authors
Udacity, Olanrewaju Awe

Aknowledgemnt
 The wonderful team at Udacity, Stack Overflow, MY brain