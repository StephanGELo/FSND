import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "What would get if you mix all light together?",
            "answer": "White", 
            "category": "1",
            "difficulty": 3
        }

        self.quiz_question_category = {
            'previous_questions': [],
            'quiz_category': {'type': 'Sports', 'id': 6}
        }

        self.quiz_question_all = {
            'previous_questions': [],
            'quiz_category': {'type': 'click', 'id': 0}
        }

        self.quiz_question_wrong_category = {
            'previous_questions': [],
            'quiz_category': {'type': 'unclick', 'id': 7}
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # #Tests for endpoint to get all categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_404_if_category_does_not_exist(self):
        res = self.client().get('/categories/500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'],' Resource Not Found')
       
    # #Tests for endpoint to get paginated questions
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'],'')
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=500', json={'category':6})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    
    # #Tests for endpoint to delete a question using a question id
    def test_delete_question(self):
        res = self.client().delete('/questions/14')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 14).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 14)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # #Tests for endpoint to post a new question
    def test_add_new_question(self):
        
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_405_if_adding_question_not_allowed(self):
        res = self.client().post('/questions/500', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    #Tests for endpoint to search for questions
    def test_search_for_questions(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'soccer'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(data['questions'][0]['question'], "Which is the only team to play in every soccer World Cup tournament?")

    def test_search_for_questions_without_results(self):
        res = self.client().post('questions/search', json={'searchTerm': 'Tree'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)
    
    #Tests for endpoint to retrieve questions based on a category id
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/6/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(len(data['questions']))

    def test_404_get_questions_by_category_with_no_valid_category(self):
        res = self.client().get('/categories/7/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    
    #Tests for endpoint to play quiz
    def test_get_question_for_quiz_by_category(self):
        res = self.client().post('/quizzes', json=self.quiz_question_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['previous_questions'])
    
    def test_get_question_for_quiz_by_All(self):
        res = self.client().post('/quizzes', json=self.quiz_question_all)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['previous_questions'])

    def test_404_get_question_for_quiz_with_no_results(self):
        res = self.client().post('/quizzes', json=self.quiz_question_wrong_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()