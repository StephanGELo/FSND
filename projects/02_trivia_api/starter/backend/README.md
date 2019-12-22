# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## Endpoint Library
#### GET '/categories'
- General:
  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  - Request Arguments: None
  - Returns an object with a single key, categories, that contains an object of id: category_string key:value pairs.

- Sample: ``` curl http://127.0.0.1:5000/categories ```
```
  {
    "categories": [
      {
        "id": 1, 
        "type": "Science"
      }, 
      {
        "id": 2, 
        "type": "Art"
      }, 
      {
        "id": 3, 
        "type": "Geography"
      }, 
      {
        "id": 4, 
        "type": "History"
      }, 
      {
        "id": 5, 
        "type": "Entertainment"
      }, 
      {
        "id": 6, 
        "type": "Sports"
      }
    ], 
    "success": true
  }

```

#### GET '/questions'
- General: 
  - Retrieve a dictionary of questions in which the keys are the id, the question, the answer, the difficulty and the category of each question.
  - Retrieve a dictionary of categories in which the key is the id and the value is the corresponding string of the category
  - Request Arguments: Page number
  - Returns a list of questions, a list of categories, the total number of questions, the current category and a succcess value.
  - Results are paginated in groups of 10.
- Sample: ``` curl http://127.0.0.1:5000/questions  ```
```
  {
    "categories": [
      {
        "id": 1, 
        "type": "Science"
      }, 
      {
        "id": 2, 
        "type": "Art"
      }, 
      {
        "id": 3, 
        "type": "Geography"
      }, 
      {
        "id": 4, 
        "type": "History"
      }, 
      {
        "id": 5, 
        "type": "Entertainment"
      }, 
      {
        "id": 6, 
        "type": "Sports"
      }
    ], 
    "current_category": "", 
    "questions": [
      {
        "answer": "Apollo 13", 
        "category": 5, 
        "difficulty": 4, 
        "id": 2, 
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      }, 
      {
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      }, 
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }, 
      {
        "answer": "Muhammad Ali", 
        "category": 4, 
        "difficulty": 1, 
        "id": 9, 
        "question": "What boxer's original name is Cassius Clay?"
      }, 
      {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }, 
      {
        "answer": "George Washington Carver", 
        "category": 4, 
        "difficulty": 2, 
        "id": 12, 
        "question": "Who invented Peanut Butter?"
      }, 
      {
        "answer": "Lake Victoria", 
        "category": 3, 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
      }, 
      {
        "answer": "The Palace of Versailles", 
        "category": 3, 
        "difficulty": 3, 
        "id": 14, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
      }
    ], 
    "success": true, 
    "total_questions": 19
  }

```
#### DELETE '/questions/{question_id}'
- General:
  - Deletes a question given a specific question id.
  - Request Arguments: An integer corresponding to the question id to be deleted.
  - Returns an object containing the corresponding question id deleted, a list of the updated questions after the required question has been deleted, the total questions remaining and a success value.
- Sample: ``` curl -X DELETE 'http://127.0.0.1:5000/questions/14' ```
```
  {
    "deleted": 14,
    "questions": [
      {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      },
      {
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 4,
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      },
      {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      },
      {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      },
      {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
      },
      {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      },
      {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
      },
      {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
      },
      {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
      },
      {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
      }
    ],
    "success": true,
    "total_questions": 18
  }

```


#### POST '/questions'
- General: 
  - Adds a new question with the corresponding values for the answer, the difficulty level and the category.
  - Request Arguments: a string of question, answer and category and  an integers for difficulty.
  - Returns an object containing a success value.
- Sample: ``` curl -X POST http://127.0.0.1:5000/questions -H 'Content-Type: application/json' -d '{"question":"What is science?", "answer": "Science", "difficulty":1, "category":"6"}' ```
```
  {"success":true}
```
#### POST '/questions/search'
- General:
  - Searches for a question based on a given string of characters.
  - Request Arguments: a string of characters
  - Returns an object containing a list of questions which contains the search term , the current_category, a success value and the total questions. The list will have the values for the question, answer, the category and the difficulty.
- Sample: ``` curl -X POST http://127.0.0.1:5000/questions/search -H 'Content-Type: application/json' -d '{"searchTerm":"soccer"}' ```
```
  {
    "current_category": "",
    "questions": [
      {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      },
      {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }
    ],
    "success": true,
    "total_questions": 2
  }
```

#### GET '/categories/<int:category_id>/questions'
- General:
  - Fetches all questions corresponding to a particular category.
  - Request Arguments: A category id.
  - Returns an object containing the current category and a list of questions with keys as id, question, answer, category, difficulty and their corresponding values.
- Sample: ``` curl -X GET http://127.0.0.1:5000/categories/3/questions ```
```
  {
    "current_category": [
      "Geography"
    ],
    "questions": [
      {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
      },
      {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
      }
    ],
    "success": true,
    "total_questions": 2
  }

```  

#### POST '/quizzes'
- General: 
  - Get a random unique question based on a specific category or based on all categories.
  - Request Arguments: Category Id (id = 0 for All) and a list of previous questions, if any.
  - Returns a random question with the corresponding answer, category and difficulty within the given category and a list of previously.
- Sample: ``` curl -X POST http://127.0.0.1:5000/quizzes -H 'Content-Type: application/json' -d '{"previous_questions": [1],"quiz_category": {"type": "click", "id": 0}}' ```
```
  {
    "previous_questions": [
      1,
      {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
      }
    ],
    "question": {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    "success": true,
    "total_questions": 5
  }
```
- Game Play Mechanics
  - When a specific category id( 1 to 6) is selected when playing the quiz, the final score will be given based on the number of questions available in the specific category. If 'All' categories are selected for the quiz, then the final score will be given after a set of 5 questions have been answered.

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
