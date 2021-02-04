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
        self.database_path = "postgres://postgres:postgres@{}/{}".format('localhost:5432', self.database_name)
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

    def test_get_all_categories(self):
        """Test case for successful GET /categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    def test_get_questions_first_page(self):
        """Test case for successful GET /questions?page=1"""
        res = self.client().get('/questions?pages=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']) == 10)
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'], None)

    def test_questions_over_index_404(self):
        """Test case for 404 error GET /questions?page=1000"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'The requested page is beyond the valid range.')

    def test_add_question_success(self):
        """Test case for successfully creating a new question in the database"""
        res = self.client().post(
            '/questions',
            json={
                'question': 'Which country is the only remaining grand duchy?',
                'answer': 'Luxembourg',
                'category': 3,
                'difficulty': 3
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_missing_field_when_adding_question(self):
        """Test case for 400 error when missing a field in the POST body"""
        res = self.client().post(
            '/questions',
            json={
                'question': 'Which country is the only remaining grand duchy?',
                'answer': 'Luxembourg',
                'difficulty': 3
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Missing field \'category\'.')

    def test_adding_existing_question(self):
        """Test case for 409 error when trying to add question that already exists in the database"""
        res = self.client().post(
            '/questions',
            json={
                'question': 'The Taj Mahal is located in which Indian city?',
                'answer': 'Agra',
                'category': 3,
                'difficulty': 2
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 409)
        self.assertEqual(data['message'], 'The question already exists.')

    def test_search_question(self):
        """Test case for successful question search"""
        res = self.client().post('/questions', json={'searchTerm': 'cage'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']) == 1)
        self.assertEqual(data['current_category'], None)

    def test_get_questions_by_category_success(self):
        """Test case for successful GET /categories/1/questions"""
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']) == 3)
        self.assertEqual(data['current_category'], 1)

    def test_get_questions_by_category_422(self):
        """Test case for unsuccessful GET /categories/50/questions"""
        res = self.client().get('/categories/50/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'The requested category does not exist.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()