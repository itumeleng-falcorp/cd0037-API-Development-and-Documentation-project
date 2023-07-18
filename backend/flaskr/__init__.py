import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    @app.route("/categories", methods=["POST"])
    def create_category():
        body = request.get_json()
        new_type = body.get("type", None)
        try:
            category = Category(
                type=new_type,
            )
            category.insert()
            selection = Category.query.order_by(Category.id).all()
            current_category = paginate(request, selection)
            return jsonify(
                {
                    "success": True,
                    "created": category.id,
                    "categories": current_category,
                    "total_categories": len(Category.query.all()),
                }
            )
        except:
            abort(422)

    @app.route("/categories")
    def retrieve_categories():
        selection = Category.query.order_by(Category.id).all()
        categories = [category.format() for category in selection]
        if len(categories) == 0:
            abort(404)
        return jsonify(
            {
                "success": True,
                "categories": categories,
                "total_categories": len(Category.query.all()),
            }
        )

    @app.route("/questions")
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate(request, selection)
        categories = Category.query.order_by(Category.id).all()
        current_categories = [category.format() for category in categories]
        if len(current_questions) == 0:
            abort(404)
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": current_categories,
                "current_category": current_categories[0],
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate(request, selection)
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )
        except:
            abort(422)

    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)
        new_rating = body.get("rating", None)

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category,
                rating=new_rating
            )
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate(request, selection)

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(405)

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()
        search_term = body.get("searchTerm", None)
        try:
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search_term))
            )
            current_questions = paginate(request, selection)
            categories = Category.query.order_by(Category.id).all()
            current_categories = [category.format() for category in categories]
            if len(current_questions) == 0:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(current_questions),
                    "categories": current_categories,
                    "current_category": current_categories[0],
                }
            )
        except:
            abort(422)

    @app.route("/categories/<int:category_id>/questions")
    def retrieve_question_by_category(category_id):
        try:
            selection = Question.query.order_by(Question.id).filter(
                Question.category == category_id
            )
            current_questions = paginate(request, selection)
            if len(current_questions) == 0:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(selection.all()),
                }
            )
        except:
            abort(422)

    @app.route("/quizzes", methods=["POST"])
    def retrieve_question_by_category1():
        body = request.get_json()
        questions = body.get("previous_questions", None)
        category = body.get("quiz_category", None).get("type", None).get("id", None)
        try:
            selection = Question.query.order_by(Question.id).filter(
                Question.category == category, ~Question.id.in_(questions)
            )
            current_questions = paginate(request, selection)
            if len(current_questions) == 0:
                abort(404)
            selected_question = random.choice(current_questions)
            return jsonify(
                {
                    "success": True,
                    "question": selected_question,
                }
            )
        except:
            abort(404)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "Method not allowed"}),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "Internal Server Error"}
            ),
            500,
        )

    return app