# FILE: quiz/api.py
from flask import Blueprint, jsonify, request, abort, make_response
from .models import Questionnaire, Question, OpenQuestion, MCQuestion, Choice
from .extensions import db

api_bp = Blueprint('api', __name__)

# ----------------------------
# Endpoints pour les Questionnaires
# ----------------------------
@api_bp.route('/questionnaires', methods=['GET'])
def get_questionnaires():
    questionnaires = Questionnaire.query.all()
    return jsonify([q.to_json() for q in questionnaires]), 200

@api_bp.route('/questionnaires', methods=['POST'])
def create_questionnaire():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Le nom est requis.")
    questionnaire = Questionnaire(name=data['name'])
    db.session.add(questionnaire)
    db.session.commit()
    return jsonify(questionnaire.to_json()), 201

@api_bp.route('/questionnaires/<int:id>', methods=['GET'])
def get_questionnaire(id):
    questionnaire = Questionnaire.query.get_or_404(id)
    questions = questionnaire.questions.all()
    result = questionnaire.to_json()
    result['questions'] = [q.to_json() for q in questions]
    return jsonify(result), 200

@api_bp.route('/questionnaires/<int:id>', methods=['PUT'])
def update_questionnaire(id):
    questionnaire = Questionnaire.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        questionnaire.name = data['name']
    db.session.commit()
    return jsonify(questionnaire.to_json()), 200

@api_bp.route('/questionnaires/<int:id>', methods=['DELETE'])
def delete_questionnaire(id):
    questionnaire = Questionnaire.query.get_or_404(id)
    db.session.delete(questionnaire)
    db.session.commit()
    return jsonify({"message": "Questionnaire supprimé"}), 200

# ----------------------------
# Endpoints pour les Questions
# ----------------------------
@api_bp.route('/questionnaires/<int:questionnaire_id>/questions', methods=['GET'])
def get_questions_for_questionnaire(questionnaire_id):
    questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
    questions = questionnaire.questions.all()
    return jsonify([q.to_json() for q in questions]), 200

@api_bp.route('/questionnaires/<int:questionnaire_id>/questions', methods=['POST'])
def create_question(questionnaire_id):
    Questionnaire.query.get_or_404(questionnaire_id)
    data = request.get_json()
    if not data or 'title' not in data:
        abort(400, description="Le titre est requis.")
    question_type = data.get('question_type', 'open')
    if question_type == 'open':
        question = OpenQuestion(
            title=data['title'],
            ordre=data.get('ordre', 1),
            questionnaire_id=questionnaire_id,
            expected_answer=data.get('expected_answer')
        )
    elif question_type == 'mcq':
        question = MCQuestion(
            title=data['title'],
            ordre=data.get('ordre', 1),
            questionnaire_id=questionnaire_id
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

@api_bp.route('/questions', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    return jsonify([q.to_json() for q in questions]), 200

@api_bp.route('/questions/<int:id>', methods=['GET'])
def get_question(id):
    question = Question.query.get_or_404(id)
    return jsonify(question.to_json()), 200

@api_bp.route('/questions/<int:id>', methods=['PUT'])
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
        # Supprimer les choix existants
        for choice in question.choices.all():
            db.session.delete(choice)
        # Ajouter les nouveaux choix
        for choice_data in data['choices']:
            choice = Choice(
                text=choice_data.get('text', ''),
                is_correct=choice_data.get('is_correct', False),
                question_id=question.id
            )
            db.session.add(choice)
    db.session.commit()
    return jsonify(question.to_json()), 200

@api_bp.route('/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question supprimée"}), 200

# ----------------------------
# Endpoints pour les Choix (pour QCM)
# ----------------------------
@api_bp.route('/questions/<int:question_id>/choices', methods=['GET'])
def get_choices(question_id):
    question = MCQuestion.query.get_or_404(question_id)
    choices = question.choices.all()
    return jsonify([c.to_json() for c in choices]), 200

@api_bp.route('/questions/<int:question_id>/choices', methods=['POST'])
def add_choice(question_id):
    MCQuestion.query.get_or_404(question_id)
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

@api_bp.route('/choices/<int:id>', methods=['PUT'])
def update_choice(id):
    choice = Choice.query.get_or_404(id)
    data = request.get_json()
    if 'text' in data:
        choice.text = data['text']
    if 'is_correct' in data:
        choice.is_correct = data['is_correct']
    db.session.commit()
    return jsonify(choice.to_json()), 200

@api_bp.route('/choices/<int:id>', methods=['DELETE'])
def delete_choice(id):
    choice = Choice.query.get_or_404(id)
    db.session.delete(choice)
    db.session.commit()
    return jsonify({"message": "Option supprimée"}), 200

# ----------------------------
# Gestion des erreurs
# ----------------------------
@api_bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

@api_bp.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": str(error)}), 400)
