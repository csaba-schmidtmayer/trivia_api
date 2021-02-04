import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_all_categories():
        categories = Category.query.all()
        return jsonify({
            'success': True,
            'categories': [category.format() for category in categories],
            'total_categories': len(categories)
        })

    @app.route('/questions')
    def get_paginated_questions():
        page = request.args.get('page', 1, type=int)
        questions = Question.query.order_by('id').all()
        paginated_questions = questions[(page-1)*QUESTIONS_PER_PAGE:page*QUESTIONS_PER_PAGE]
        categories = Category.query.all()
        if len(paginated_questions) > 0:
            return jsonify({
                'success': True,
                'questions': [question.format() for question in paginated_questions],
                'total_questions': len(questions),
                'categories': [category.format() for category in categories],
                'current_category': None
            })
        else:
            abort(404, 'The requested page is beyond the valid range.')

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions', methods=['POST'])
    def add_new_question():
        success = True

        question = request.json.get('question', None)
        if question is None:
            abort(400, 'Missing field \'question\'.')

        answer = request.json.get('answer', None)
        if answer is None:
            abort(400, 'Missing field \'answer\'.')

        category = request.json.get('category', None)
        if category is None:
            abort(400, 'Missing field \'category\'.')

        difficulty = request.json.get('difficulty', None)
        if difficulty is None:
            abort(400, 'Missing field \'difficulty\'.')

        existing_question = Question.query.filter(Question.question.ilike(question)).first()
        if existing_question is not None:
            abort(409, 'The question already exists.')

        try:
            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
            new_question.insert()
        except Exception as e:
            db.session.rollback()
            success = False
        finally:
            db.session.close()

        if success:
            return jsonify({
                'success': True
            }), 201
        else:
            abort(500, 'Adding the question to the database was unsuccessful.')

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
    
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''


    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(400)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': error.description
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': error.description
        }), 404

    @app.errorhandler(409)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 409,
            'message': error.description
        }), 409

    @app.errorhandler(500)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': error.description
        }), 500

    return app

    