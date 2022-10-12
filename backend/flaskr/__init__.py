import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
   
    @app.route('/categories')
    def get_all_categories():
        categories = Category.query.all()
        formatted_categories = {}

        
        for category in categories:
            formatted_categories[category.id]=category.type
            
        if len(formatted_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.all()
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        
        formatted_questions= [question.format() for question in questions]
        formatted_categories = {category.id:category.type for category in categories}

        paginated_questions = formatted_questions[start:end]
              
        if len(paginated_questions) == 0:
            abort(404)
        

        return jsonify({
            'success': True,
            'questions':paginated_questions,
            'total_number_of_questions':len(formatted_questions),
            'categories': formatted_categories
        })
        
    
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def remove_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
                
            question.delete()
            return jsonify({
                'success': True,
                'id': question.id
            })
        except:
            abort(422)
            
    @app.route('/questions', methods=['POST'])
    def add_new_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        
        try:
            new_question = Question(question = new_question, answer = new_answer, category = new_category, difficulty = new_difficulty)
            new_question.insert()
            return jsonify({
                'success':True,
                'id': new_question.id
            })
            
        except:
            abort(422)
            
    @app.route('/questions/search', methods=['POST'])
    def get_search():
        body = request.get_json()
        search_term = body.get('searchTerm',None)
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        search_questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
        formatted_searched_question = [question.format() for question in search_questions][start:end]
        return jsonify({
            'success': True,
            'questions':formatted_searched_question
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_question_by_category(category_id):
        categorized_questions = Question.query.filter(Question.category == category_id).all()
        category = Category.query.filter(Category.id == category_id).all()
        
        for cat in category:
            question_category = cat.type
            
        formatted_categorized_question = [question.format() for question in categorized_questions]
        if len(formatted_categorized_question) == 0:
            abort(404)
        return jsonify({
            'success': True,
             question_category:formatted_categorized_question,
            'questions' : formatted_categorized_question,
            'current_category' : question_category
        })
    
    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        body = request.get_json()
        quizCategory = body.get('quiz_category')
        previousQuestion = body.get('previous_questions')

        try:
            if quizCategory['id'] == 0:
                questions = Question.query.all()
                quiz_question =[question.format() for question in questions]
            else:
                questions = Question.query.filter_by(
                    category=quizCategory['id']).all()
                quiz_question =[question.format() for question in questions]
            

            randomIndex = random.randint(0, len(quiz_question)-1)
            nextQuestion = questions[randomIndex]

            return jsonify({
                'success': True,
                'question': {
                        "answer": nextQuestion.answer,
                        "category": nextQuestion.category,
                        "difficulty": nextQuestion.difficulty,
                        "id": nextQuestion.id,
                        "question": nextQuestion.question
                    },
            })

        except:
            abort(404)
        
    @app.errorhandler(404)
    def not_found_handler(error):
        return jsonify({
            'success':False,
            'error': 404,
            'message': 'resource not found'
        }), 404
    
    @app.errorhandler(422)
    def not_found_handler(error):
        return jsonify({
            'success':False,
            'error': 422,
            'message': 'unprocessable'
        }), 422
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message':'method not allowed'
        }), 405

    return app
