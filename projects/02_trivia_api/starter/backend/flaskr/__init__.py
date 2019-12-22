import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, list):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in list]
  actual_questions = questions[start:end]

  return actual_questions


def create_app(test_config=None):
  #create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  
  '''
  @TODO 1: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  
  '''
  @TODO 2: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-ALlow-Headers', 'GET, POST, DELETE')
    return response
  '''
  @TODO 3: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    
    if len(formatted_categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': formatted_categories
    })

  '''
  @TODO 4: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, questions)
    num_of_questions = len(questions)
    
    if len(current_questions) == 0:
      abort (404)

    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': num_of_questions,
      'categories': formatted_categories,
      'current_category': ''
    })

  '''
  @TODO 5: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)
      
      question.delete()
      remaining_questions = Question.query.order_by(Question.id).all()
      questions = paginate_questions(request, remaining_questions)
      num_of_questions = len(remaining_questions)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions':questions,
        'total_questions':num_of_questions
      })

    except:
      abort(422)
      
  '''
  @TODO 6: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def post_search_question():
    body = request.get_json()

    if 'searchTerm' in body:
      return search_questions(body['searchTerm'])
    else:
      return add_question(body)
  
  def add_question(body):
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    
    try:
      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      question.insert()
      return jsonify({
        'success': True,
      })
    
    except:
      abort(422)

  '''
  @TODO 7: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm', None)

    try:
      if search_term:
        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        current_questions = paginate_questions(request, questions)
        num_of_questions = len(questions)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': num_of_questions,
          'current_category': ''
        })
      else:
        abort(404)
    except:
      abort(422)
      
  '''
  @TODO 8: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    try:
      questions = Question.query.filter(Question.category==category_id).all()
      current_questions = paginate_questions(request, questions)
      actual_category = [(Category.query.get(category_id).format()['type'])]
      num_of_questions = len(current_questions)

      return jsonify ({
        'success': True,
        'questions': current_questions,
        'total_questions': num_of_questions,
        'current_category': actual_category
      })
    except:
      abort(404)

  '''
  @TODO 9: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    body = request.get_json()
    previous_questions = body['previous_questions']
    quiz_category = body['quiz_category']

    try:
      #Retrieve a random question if a category has been selected
      if quiz_category['id'] > 0:
        total_questions = 0
        questions = Question.query.filter(Question.category==str(quiz_category['id'])).all()
        formatted_questions = [question.format() for question in questions]
        total_questions = len(formatted_questions)
        selected_question = random.choice(formatted_questions)
       #Check if there is any previous question
        if len(previous_questions) == 0:
          return jsonify({
            "success": True,
            "question": selected_question,
            "previous_questions": previous_questions.append(selected_question)
          }) 
        #Otherwise, check if selected question exists in previous questions
        else:
          while (selected_question['id'] in previous_questions):
            formatted_questions.remove(selected_question)
            selected_question = random.choice(formatted_questions)
            #Condition to prevent a request error from ocurring
            if len(formatted_questions) == 1:
              return jsonify({
                "success": True,
                "question": selected_question,
                "previous_questions": previous_questions,
                "total_questions": total_questions
              })
          #If selected question does not exist in previous questions, append it and return it to the frontend
          previous_questions.append(selected_question)
          return jsonify({
            "success": True,
            "question": selected_question,
            "previous_questions": previous_questions,
            "total_questions": total_questions
          })
      #Retrieve a random question if All categories have been selected
      else:
        selected_question = []
        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]
        selected_question = random.choice(formatted_questions)
    
        while selected_question['id'] in previous_questions:
          selected_question = random.choice(formatted_questions)

        previous_questions.append(selected_question)

        return jsonify({
          "success": True,
          "question": selected_question,
          "previous_questions": previous_questions,
          "total_questions": 5
        })
    except:
      abort(404)
      
  '''
  @TODO 10: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request"
    }), 400

  @app.errorhandler(404)
  def non_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource Not Found"
    }), 404

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method Not Allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable"
    }), 422
  
  @app.errorhandler(500)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Servor Error"
    }), 500

  return app

    