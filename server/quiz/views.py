from flask import abort, jsonify, make_response, request
from flask_restful import Api, Resource

from .app import app, db
from .models import (Choice, MCQuestion, OpenQuestion, Question, Quiz,
                     valid_data)

api = Api(app, prefix="/api/v1")


class HomeResource(Resource):
    def get(self):
        quizzes = Quiz.query.all()
        return [q.to_json() for q in quizzes], 200

    def post(self):
        quizzes = valid_data(request)
        quizes = []
        for quiz in quizzes:
            if 'name' not in quiz:
                abort(400)

            new_quiz = Quiz(name=quiz['name'])
            quizes.append(new_quiz)
            db.session.add(new_quiz)
            db.session.commit()

            if 'questions' in quiz:
                for question_data in quiz['questions']:
                    if 'title' not in question_data:
                        abort(400)

                    question_type = question_data.get('question_type', 'open')

                    if question_type == 'open':
                        new_question = OpenQuestion(
                            title=question_data['title'],
                            order=question_data.get('order', 1),
                            quiz_id=new_quiz.id,
                            expected_answer=question_data.get('expected_answer')
                        )
                    elif question_type == 'mcq':
                        new_question = MCQuestion(
                            title=question_data['title'],
                            order=question_data.get('order', 1),
                            quiz_id=new_quiz.id
                        )
                        db.session.add(new_question)
                        db.session.commit()

                        if 'choices' in question_data:
                            for choice_data in question_data['choices']:
                                new_choice = Choice(
                                    text=choice_data.get('text', ''),
                                    is_correct=choice_data.get('is_correct', False),
                                    question_id=new_question.id
                                )
                                db.session.add(new_choice)

                    db.session.add(new_question)
                    db.session.commit()

        return [q.to_json() for q in quizes], 201


class QuizListResource(Resource):
    def get(self):
        quizzes = Quiz.query.all()
        return [q.to_json() for q in quizzes], 200

    def post(self):
        data = request.get_json()
        if 'name' not in data:
            abort(400)

        new_quiz = Quiz(name=data['name'])
        db.session.add(new_quiz)
        db.session.commit()
        return new_quiz.to_json(), 201


class QuizResource(Resource):
    def get(self, id):
        quiz = Quiz.query.get(id)
        questions = Question.query.filter_by(quiz_id=id)
        if quiz is None or questions is None:
            abort(404)
        return [quiz.to_json(), [q.to_json() for q in questions]], 200

    def put(self, id):
        quiz = Quiz.query.get(id)
        if quiz is None:
            abort(404)

        data = request.get_json()
        if 'name' in data:
            quiz.name = data['name']

        db.session.commit()
        return {'message': 'Quiz modifié'}, 200

    def delete(self, id):
        quiz = Quiz.query.get(id)
        if quiz is None:
            abort(404)

        db.session.delete(quiz)
        db.session.commit()
        return {'message': 'Quiz supprimée'}, 200


class QuestionListResource(Resource):
    def get(self):
        questions = Question.query.all()
        if questions is None:
            abort(404)
        return [q.to_json() for q in questions], 200


class QuestionResource(Resource):
    def get(self, id):
        question = Question.query.get(id)
        if question is None:
            abort(404)
        return question.to_json(), 200

    def put(self, id):
        question = Question.query.get(id)
        if question is None:
            abort(404)

        data = request.get_json()
        if 'title' in data:
            question.title = data['title']
        if 'order' in data:
            question.order = data['order']
        if question.question_type == 'open' and 'expected_answer' in data:
            question.expected_answer = data['expected_answer']
        elif question.question_type == 'mcq' and 'choices' in data:
            for choice in question.choices.all():
                db.session.delete(choice)
            for choice_data in data['choices']:
                new_choice = Choice(
                    text=choice_data.get('text', ''),
                    is_correct=choice_data.get('is_correct', False),
                    question_id=question.id
                )
                db.session.add(new_choice)

        db.session.commit()
        return question.to_json(), 200

    def delete(self, id):
        question = Question.query.get(id)
        if question is None:
            abort(404)
        db.session.delete(question)
        db.session.commit()
        return {'message': 'Question supprimée'}, 200


class QuizQuestionsResource(Resource):
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if quiz is None:
            abort(404)
        questions = quiz.questions.all()
        return [q.to_json() for q in questions], 200

    def post(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if quiz is None:
            abort(404)

        data = request.get_json()
        if not data or 'title' not in data:
            abort(400)
        
        same_type = Question.query.filter_by(quiz_id=quiz_id).all()
        max_order = max([q.order for q in same_type], default=0)
        order = max_order + 1

        question_type = data.get('question_type', 'open')

        if question_type == 'open':
            new_question = OpenQuestion(
                title=data['title'],
                order=order,
                quiz_id=quiz_id,
                expected_answer=data.get('expected_answer')
            )
        elif question_type == 'mcq':
            new_question = MCQuestion(
                title=data['title'],
                order=order,
                quiz_id=quiz_id
            )
            db.session.add(new_question)
            db.session.commit()

            if 'choices' in data:
                for choice_data in data['choices']:
                    new_choice = Choice(
                        text=choice_data.get('text', ''),
                        is_correct=choice_data.get('is_correct', False),
                        question_id=new_question.id
                    )
                    db.session.add(new_choice)
        else:
            abort(400)

        db.session.add(new_question)
        db.session.commit()
        return new_question.to_json(), 201


class ChoiceListResource(Resource):
    def get(self, question_id):
        question = MCQuestion.query.get(question_id)
        if question is None:
            abort(404)
        return [c.to_json() for c in question.choices], 200

    def post(self, question_id):
        question = MCQuestion.query.get(question_id)
        if question is None:
            abort(404)
        data = request.get_json()
        if not data or 'text' not in data:
            abort(400)
        new_choice = Choice(
            text=data['text'],
            is_correct=data.get('is_correct', False),
            question_id=question_id
        )
        db.session.add(new_choice)
        db.session.commit()
        return new_choice.to_json(), 201


class ChoiceResource(Resource):
    def put(self, id):
        choice = Choice.query.get(id)
        if choice is None:
            abort(404)
        data = request.get_json()
        if 'text' in data:
            choice.text = data['text']
        if 'is_correct' in data:
            choice.is_correct = data['is_correct']
        db.session.commit()
        return choice.to_json(), 200

    def delete(self, id):
        choice = Choice.query.get(id)
        if choice is None:
            abort(404)
        db.session.delete(choice)
        db.session.commit()
        return {'message': 'Option supprimée'}, 200


api.add_resource(HomeResource, '/')
api.add_resource(QuizListResource, '/quizzes')
api.add_resource(QuizResource, '/quizzes/<int:id>')
api.add_resource(QuizQuestionsResource, '/quizzes/<int:quiz_id>/questions')
api.add_resource(QuestionListResource, '/questions')
api.add_resource(QuestionResource, '/questions/<int:id>')
api.add_resource(ChoiceListResource, '/questions/<int:question_id>/choices')
api.add_resource(ChoiceResource, '/choices/<int:id>')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad request"}), 400)
