# About the project

This is a trivia game where you can answer questions in all kinds of categories and get points. The questions database is not large, but you can add to it if you want to

# How to install

The project is in 2 parts: frontend and backend.
For the backend, you first need to install python3 on your system, then install PostgreSQL.

Create a new database in psql with this command:
CREATE DATABASE trivia;

After then, move to the backend folder and install the libraries in the requirements.txt file with this command:
pip install -r requirements.txt

When you're done, type those commands if you're on windows:
set FLASK_APP=flaskr
flask run

At this point, the flask server should be running on port 5000

For our frontend application, you need to install Node.js.
After installing it, Go to the frontend folder and type those commands:
npm install (Only once)
npm start

The frontend app will launch at port 3000.

Enjoy the game.

# API Documentation

## Introduction
This is a RESTful API that allows you to access the database of the questions and categories for the trivia project. You can also use it to search for questions in the database, add more questions, and play the game.

## Getting started

### The base URl

Since you can clone this and host it yourself, the base URL is really dependent on where you'll host the project. But if you host it on your machine, the base URL should be localhost:5000 under default settings.

## Errors

Here is a list of the errors you might encounter when using the API:

1. 404: Not found.
2. 422: You sent the message correctly, but the server couldn't process your request.
3. 405: Method not allowed.

Sample response:
{"error":404,"message":"Resource not found","success":false}

## Endpoints


### GET /categories

curl localhost:5000/categories

Sends back all categories with their ids.

Sample responce:
{"categories":{"1":"Science","2":"Art","3":"Geography","4":"History","5":"Entertainment","6":"Sports"},"success":true}

### GET /questions

Returns the questions for a specified page, as well as the total number of questions.

curl localhost:5000/questions?page=1

Sample response:

{"categories":{"1":"Science","2":"Art","3":"Geography","4":"History","5":"Entertainment","6":"Sports"},"current_category
":null,"questions":[{"answer":"Maya Angelou","category":4,"difficulty":2,"id":5,"question":"Whose autobiography is entit
led 'I Know Why the Caged Bird Sings'?"},{"answer":"Edward Scissorhands","category":5,"difficulty":3,"id":6,"question":"
What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},{"answer
":"Muhammad Ali","category":4,"difficulty":1,"id":9,"question":"What boxer's original name is Cassius Clay?"},{"answer":
"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the only team to play in every soccer World Cup tourna
ment?"},{"answer":"Uruguay","category":6,"difficulty":4,"id":11,"question":"Which country won the first ever soccer Worl
d Cup in 1930?"},{"answer":"George Washington Carver","category":4,"difficulty":2,"id":12,"question":"Who invented Peanu
t Butter?"},{"answer":"Lake Victoria","category":3,"difficulty":2,"id":13,"question":"What is the largest lake in Africa
?"},{"answer":"The Palace of Versailles","category":3,"difficulty":3,"id":14,"question":"In which royal palace would you
 find the Hall of Mirrors?"},{"answer":"Agra","category":3,"difficulty":2,"id":15,"question":"The Taj Mahal is located i
n which Indian city?"},{"answer":"Escher","category":2,"difficulty":1,"id":16,"question":"Which Dutch graphic artist\u20
13initials M C was a creator of optical illusions?"}],"success":true,"total_questions":23}

### DELETE /questions/question_id

Deletes the question and returns the id of the deleted question.

curl -X DELETE http://localhost:5000/questions/16?page=2

Sample response:
{"deleted":"16","success":true}

### POST /questions

Creates a new question.
You need to provide  it with a question, an answer, difficulty, and a category.
Question and answers are of the type str, while difficulty, and category are of the type int.

### GET /categories/cat_id/questions

Returns questions only from the category you selected, as well as the total number of questions for that category.

curl localhost:5000/categories/1/questions

Sample response:
{"current_category":"1","questions":[{"answer":"The Liver","category":1,"difficulty":4,"id":20,"question":"What is the h
eaviest organ in the human body?"},{"answer":"Alexander Fleming","category":1,"difficulty":3,"id":21,"question":"Who dis
covered penicillin?"},{"answer":"Blood","category":1,"difficulty":4,"id":22,"question":"Hematology is a branch of medici
ne involving the study of what?"}],"success":true,"total_questions":3}


### POST /quizzes
Returns a random question from a category. It will not get questions that have been already asked.
This is used when playing the game.

when requesting:
quiz_category is of type int, and previous_questions are of type array.

### POST /questions/search

Returns questions that contain the search word. (Not case sensitive).

When requestion:
Request body: is of type string.
