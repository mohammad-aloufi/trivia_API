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
        self.database_path = "postgres://{}/{}".format('postgres:post2021@localhost:5433', self.database_name)
        setup_db(self.app, self.database_path)

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

    def test_search(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'actor'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_on_search(self):
        res = self.client().post('/questions/search', json ={'searchTerm': ''})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_404_getting_non_existing_category(self):
        res = self.client().get('/categories/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    def test_delete_question(self):
        q = Question(question='testing question', answer='testing answer', difficulty=1, category=1)
        q.insert()
        id =q.id
        res = self.client().delete('/questions/{}'.format(id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_405_on_question(self):
        res = self.client().get('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'This method is not allowed')

    def test_questions_by_cat(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


        def test_404_on_questions_by_cat(self):
            res = self.client().get('/categories/1000/questions')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Resource not found')

    def test_quiz(self):
        res = self.client().post('/quizzes', json ={'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': '1'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


        def test_404_on_quiz(self):
            res = self.client().post('/quizzes', json={'previous_questions': []})
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Resource not found')


    def test_question_pages(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


        def test_404_on_pages(self):
            res = self.client().get('/quizzes')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()