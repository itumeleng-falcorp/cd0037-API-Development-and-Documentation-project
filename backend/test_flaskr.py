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
        self.client = self.app.test_client()

        # setup_db(self.app, self.database_path)
        self.new_question = {
            "question": "Who is your favourite player?",
            "answer": "Kevin",
            "difficulty": 5,
            "category": 6,
            "rating": 5
        }

        self.search = {"searchTerm": "favourite"}

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    TODO
    Write at least one test for each test for successful
    operation and for expected errors.
    """

    # Test retrieve categories
    def test_retrieve_categories(self):
        """Test GET /categories"""
        res = self.client.get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["total_categories"])

    # Test retrieve questions
    def test_retrieve_questions(self):
        """Test GET /questions"""
        res = self.client.get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])

    # Test 404 retrieve questions
    def test_404_retrieve_questions(self):
        """Test GET /questions?page=1000"""
        res = self.client.get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # Test delete question
    def test_delete_question(self):
        """Test DELETE /questions/<question_id>"""
        res = self.client.delete("/questions/5")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 5)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    # Test 422 delete question
    def test_422_if_question_does_not_exist(self):
        res = self.client.delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # Test create question
    def test_create_new_question(self):
        """Test POST /questions"""
        res = self.client.post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(len(data["questions"]))

    # Test 405 create question
    def test_405_if_question_creation_not_allowed(self):
        """Test POST /questions"""
        res = self.client.post("/questions/12", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")

    # Test search questions
    def test_search_questions(self):
        """Test POST /questions/search"""
        res = self.client.post("/questions/search", json=self.search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])

    # Test 422 search questions
    def test_422_search_questions(self):
        """Test POST /questions/search"""
        res = self.client.post("/questions/search", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # Test retrieve question by category
    def test_retrieve_question_by_category(self):
        """Test GET /categories/<category_id>/questions"""
        res = self.client.get("/categories/6/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(len(data["questions"]))

    # Test 422 retrieve question by category
    def test_422_retrieve_question_by_category(self):
        """Test GET /categories/<category_id>/questions"""
        res = self.client.get("/categories/7/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # Test get quiz question
    def test_get_quiz_question(self):
        """Test POST /quizzes"""
        quiz_data = {
            "previous_questions": [],
            "quiz_category": {
                "type": {"type": "Who is you favourite player?", "id": "6"},
            },
        }
        res = self.client.post("/quizzes", json=quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    # Test get quiz question
    def test_404_get_quiz_question(self):
        """Test POST /quizzes"""
        quiz_data = {
            "previous_questions": [],
            "quiz_category": {
                "type": {"type": "Doesn't Exist", "id": "10"},
            },
        }
        res = self.client.post("/quizzes", json=quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
