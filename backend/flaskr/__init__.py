import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):

    question = request.args.get('page', 1, type=int)

    start = (question - 1) * QUESTIONS_PER_PAGE

    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

# Setting up CORS, allowing * for origins

    CORS(app)


# Use after_request to set headers

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def categories():
        # Return all categories
        try:
            cat = Category.query.all()
            return jsonify({'success': True,
                            'categories': {i.id: i.type for i in cat}})
        except:
            abort(422)

    @app.route('/questions/<question_id>', methods=['DELETE'])
    def del_question(question_id):
        # Delete a question, and return the deleted id
        q = Question.query.get(question_id)
        print(q.id)
        try:
            q.delete()
            return jsonify({'success': True, 'deleted': question_id})
        except:
            abort(422)

    @app.route('/questions')
    def get_questions():
        '''
        Return questions with pagination to endpoint,
        as well as number of questions and current category
        '''
        selection = Question.query.order_by(Question.id).all()
        cats = Category.query.order_by(Category.type).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)
        return jsonify({'success': True,
                        'questions': current_questions,
                        'categories': {i.id: i.type for i in cats},
                        'current_category': None,
                        'total_questions': len(Question.query.all())})

    @app.route('/questions/search', methods=['POST'])
    def search():
        # Search the db for a keyword we got from the data object
        data = request.get_json()
        term = data.get('searchTerm')
        if term:
            results = Question.query.filter(
                Question.question.ilike(f'%{term}%')).all()
            return jsonify({'success': True,
                            'questions': [question.format()
                                          for question in results],
                            'total_questions': len(results),
                            'current_category': None})

        abort(404)

    @app.route('/questions', methods=['POST'])
    def new_question():
        '''
        Create a new question
        according to the data we got from the data object,
        then return the new question's id
        '''
        data = request.get_json()

        try:
            new_q = Question(question=data.get('question'), answer=data.get(
                'answer'), difficulty=data.get('difficulty'), category=data.get('category'))
            new_q.insert()
        except:
            abort(422)
        return jsonify({'success': True, 'created': new_q.id})

    @app.route('/quizzes', methods=['POST'])
    def quiz():
        '''
        Get category and previous question from the endpoint,
        then return a random question from that category.
        Same question won't be repeated in same session hopefully
        '''
        data = request.get_json()
        if 'quiz_category' not in data and 'previous_questions' not in data:
            abort(422)

        if data.get('quiz_category')['type'] == 'click':
            questions = Question.query.filter(
                Question.id.notin_((data.get('previous_questions')))).all()
        else:
            questions = Question.query.filter_by(category=data.get('quiz_category')['id']).filter(
                Question.id.notin_((data.get('previous_questions')))).all()

        new_question = questions[random.randrange(
            0, len(questions))].format() if len(questions) > 0 else None

        return jsonify({'success': True, 'question': new_question})

    @app.route('/categories/<cat_id>/questions')
    def q_by_cat(cat_id):
        # Get questions only in a specific category
        try:
            q = Question.query.filter(Question.category == str(cat_id)).all()
            if len(q) == 0:
                abort(404)

            return jsonify({'success': True,
                            'questions': [question.format()
                                          for question in q],
                            'total_questions': len(q),
                            'current_category': cat_id})
        except:
            abort(404)

    @app.errorhandler(404)
    def not_found(error):
        # 404 error handler
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def cant_process(error):
        # 422 error handler
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Request could not be completed'
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        # 405 error handler
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'This method is not allowed'
        }), 405

    return app
