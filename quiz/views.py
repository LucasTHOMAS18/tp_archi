# FILE: quiz/views.py
from flask import jsonify, abort, make_response, request
from .app import app, db
from .models import Questionnaire, Question, OpenQuestion, MCQuestion, Choice

@app.route('/questionnaires', methods=['GET'])
def get_questionnaires():
    quizzes = Questionnaire.query.all()
    return jsonify([q.to_json() for q in quizzes]), 200

@app.route('/questionnaires', methods=['POST'])
def create_questionnaire():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Le nom du questionnaire est requis.")
    quiz = Questionnaire(name=data['name'])
    db.session.add(quiz)
    db.session.commit()
    return jsonify(quiz.to_json()), 201

@app.route('/questionnaires/<int:id>', methods=['GET'])
def get_questionnaire(id):
    quiz = Questionnaire.query.get_or_404(id)
    questions = quiz.questions.all()
    result = quiz.to_json()
    result['questions'] = [q.to_json() for q in questions]
    return jsonify(result), 200

@app.route('/questionnaires/<int:id>', methods=['PUT'])
def update_questionnaire(id):
    quiz = Questionnaire.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        quiz.name = data['name']
    db.session.commit()
    return jsonify(quiz.to_json()), 200

@app.route('/questionnaires/<int:id>', methods=['DELETE'])
def delete_questionnaire(id):
    quiz = Questionnaire.query.get_or_404(id)
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"message": "Questionnaire supprimé"}), 200

@app.route('/questionnaires/<int:quiz_id>/questions', methods=['GET'])
def get_questions_for_quiz(quiz_id):
    quiz = Questionnaire.query.get_or_404(quiz_id)
    questions = quiz.questions.all()
    return jsonify([q.to_json() for q in questions]), 200

@app.route('/questionnaires/<int:quiz_id>/questions', methods=['POST'])
def create_question(quiz_id):
    Questionnaire.query.get_or_404(quiz_id)
    data = request.get_json()
    if not data or 'title' not in data:
        abort(400, description="Le titre de la question est requis.")
    qtype = data.get('question_type', 'open')
    if qtype == 'open':
        question = OpenQuestion(
            title=data['title'],
            ordre=data.get('ordre', 1),
            questionnaire_id=quiz_id,
            expected_answer=data.get('expected_answer')
        )
    elif qtype == 'mcq':
        question = MCQuestion(
            title=data['title'],
            ordre=data.get('ordre', 1),
            questionnaire_id=quiz_id
        )
        db.session.add(question)
        db.session.commit()
        if 'choices' in data:
            for choice_data in data['choices']:
                choice = Choice(
                    text=choice_data.get('text', ''),
                    is_correct=choice_data.get('is_correct', False),
                    question_id=question.id
                )
                db.session.add(choice)
    else:
        abort(400, description="Type de question invalide")
    db.session.add(question)
    db.session.commit()
    return jsonify(question.to_json()), 201

@app.route('/questions/<int:id>', methods=['GET'])
def get_question(id):
    question = Question.query.get_or_404(id)
    return jsonify(question.to_json()), 200

@app.route('/questions/<int:id>', methods=['PUT'])
def update_question(id):
    question = Question.query.get_or_404(id)
    data = request.get_json()
    if 'title' in data:
        question.title = data['title']
    if 'ordre' in data:
        question.ordre = data['ordre']
    if question.question_type == 'open' and 'expected_answer' in data:
        question.expected_answer = data['expected_answer']
    elif question.question_type == 'mcq' and 'choices' in data:
        for choice in question.choices.all():
            db.session.delete(choice)
        for choice_data in data['choices']:
            choice = Choice(
                text=choice_data.get('text', ''),
                is_correct=choice_data.get('is_correct', False),
                question_id=question.id
            )
            db.session.add(choice)
    db.session.commit()
    return jsonify(question.to_json()), 200

@app.route('/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question supprimée"}), 200

@app.route('/questions/<int:question_id>/choices', methods=['GET'])
def get_choices(question_id):
    question = MCQuestion.query.get_or_404(question_id)
    choices = question.choices.all()
    return jsonify([c.to_json() for c in choices]), 200

@app.route('/questions/<int:question_id>/choices', methods=['POST'])
def add_choice(question_id):
    question = MCQuestion.query.get_or_404(question_id)
    data = request.get_json()
    if not data or 'text' not in data:
        abort(400, description="Le texte de l'option est requis.")
    choice = Choice(
        text=data['text'],
        is_correct=data.get('is_correct', False),
        question_id=question_id
    )
    db.session.add(choice)
    db.session.commit()
    return jsonify(choice.to_json()), 201

@app.route('/choices/<int:id>', methods=['PUT'])
def update_choice(id):
    choice = Choice.query.get_or_404(id)
    data = request.get_json()
    if 'text' in data:
        choice.text = data['text']
    if 'is_correct' in data:
        choice.is_correct = data['is_correct']
    db.session.commit()
    return jsonify(choice.to_json()), 200

@app.route('/choices/<int:id>', methods=['DELETE'])
def delete_choice(id):
    choice = Choice.query.get_or_404(id)
    db.session.delete(choice)
    db.session.commit()
    return jsonify({"message": "Option supprimée"}), 200

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": str(error)}), 400)
