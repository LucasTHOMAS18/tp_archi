from flask import jsonify, abort, make_response, request

from .app import app, db
from .models import Questionnaire, Question, OpenQuestion, MCQuestion, Choice
from .models import valid_data


@app.route('/', methods=['GET'])
def get_home():
    questionnaires = Questionnaire.query.all()
    return jsonify([q.to_json() for q in questionnaires]), 200


@app.route('/', methods=['POST'])
def load_json_file():
    questionnaires = valid_data(request)

    quizes = []
    for quiz in questionnaires:
        if 'name' not in quiz:
            abort(400)
        
        new_questionnaire = Questionnaire(name=quiz['name'])
        quizes.append(new_questionnaire)
        db.session.add(new_questionnaire)
        db.session.commit()
        
        if 'questions' in quiz:
            for question_data in quiz['questions']:
                if 'title' not in question_data:
                    abort(400)
                
                question_type = question_data.get('question_type', 'open')
                
                if question_type == 'open':
                    new_question = OpenQuestion(
                        title=question_data['title'],
                        ordre=question_data.get('ordre', 1),
                        questionnaire_id=new_questionnaire.id,
                        expected_answer=question_data.get('expected_answer')
                    )
                elif question_type == 'mcq':
                    new_question = MCQuestion(
                        title=question_data['title'],
                        ordre=question_data.get('ordre', 1),
                        questionnaire_id=new_questionnaire.id
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

    return jsonify([q.to_json() for q in quizes]), 201


@app.route('/questionnaires', methods=['GET'])
def get_questionnaires():
    questionnaires = Questionnaire.query.all()
    if questionnaires is None:
        abort(404)

    return jsonify([q.to_json() for q in questionnaires]), 200


@app.route('/questionnaires', methods=['POST'])
def create_questionnaire():
    data = request.get_json()

    if 'name' not in data:
        abort(400)
    
    new_questionnaire = Questionnaire(name=data['name'])
    db.session.add(new_questionnaire)
    db.session.commit()
    return jsonify(new_questionnaire.to_json()), 201


@app.route('/questionnaires/<int:id>', methods=['DELETE'])
def delete_questionnaire(id):
    questionnaire = Questionnaire.query.get(id)
    if questionnaire is None:
        abort(404)
    
    db.session.delete(questionnaire)
    db.session.commit()
    return jsonify({'message': 'Questionnaire supprimée'}), 200


@app.route('/questionnaires/<int:id>', methods=['PUT'])
def update_questionnaire(id):
    questionnaire = Questionnaire.query.get(id)
    if questionnaire is None:
        abort(404)
    
    data = request.get_json()
    if 'name' in data:
        questionnaire.name = data['name']
    
    db.session.commit()
    return jsonify({'message': 'Questionnaire modifié'}), 200


@app.route('/questionnaires/<int:id>', methods=['GET'])
def get_questionnaire(id):
    questionnaire = Questionnaire.query.get(id)
    questions = Question.query.filter_by(questionnaire_id=id)
    if questionnaire is None or questions is None:
        abort(404)

    return jsonify([questionnaire.to_json(), [q.to_json() for q in questions]]), 200


@app.route('/questionnaires/<int:questionnaire_id>/questions', methods=['GET'])
def get_questions_for_questionnaire(questionnaire_id):
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    
    questions = questionnaire.questions.all()
    return jsonify([q.to_json() for q in questions]), 200


@app.route('/questionnaires/<int:questionnaire_id>/questions', methods=['POST'])
def create_question(questionnaire_id):
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    
    data = request.get_json()
    if not data or 'title' not in data:
        abort(400)
    
    question_type = data.get('question_type', 'open')
    
    if question_type == 'open':
        new_question = OpenQuestion(
            title=data['title'],
            ordre=data.get('ordre', 1),
            questionnaire_id=questionnaire_id,
            expected_answer=data.get('expected_answer')
        )
    elif question_type == 'mcq':
        new_question = MCQuestion(
            title=data['title'],
            ordre=data.get('ordre', 1),
            questionnaire_id=questionnaire_id
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
        abort(400, description="Invalid question type")
        
    db.session.add(new_question)
    db.session.commit()
    return jsonify(new_question.to_json()), 201


@app.route('/questions', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    if questions is None:
        abort(404)

    return jsonify([q.to_json() for q in questions]), 200


@app.route('/questions/<int:id>', methods=['GET'])
def get_question(id):
    question = Question.query.get(id)
    if question is None:
        abort(404)

    return jsonify(question.to_json()), 200


@app.route('/questions/<int:id>', methods=['PUT'])
def update_question(id):
    question = Question.query.get(id)
    if question is None:
        abort(404)
    
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
            new_choice = Choice(
                text=choice_data.get('text', ''),
                is_correct=choice_data.get('is_correct', False),
                question_id=question.id
            )
            db.session.add(new_choice)
    
    db.session.commit()
    return jsonify(question.to_json()), 200


@app.route('/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get(id)
    if question is None:
        abort(404)
    
    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question supprimée'}), 200


@app.route('/questions/<int:question_id>/choices', methods=['GET'])
def get_choices(question_id):
    question = MCQuestion.query.get(question_id)
    if question is None:
        abort(404)
    
    return jsonify([c.to_json() for c in question.choices]), 200


@app.route('/questions/<int:question_id>/choices', methods=['POST'])
def add_choice(question_id):
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
    return jsonify(new_choice.to_json()), 201


@app.route('/choices/<int:id>', methods=['PUT'])
def update_choice(id):
    choice = Choice.query.get(id)
    if choice is None:
        abort(404)
    
    data = request.get_json()
    if 'text' in data:
        choice.text = data['text']
    if 'is_correct' in data:
        choice.is_correct = data['is_correct']
    
    db.session.commit()
    return jsonify(choice.to_json()), 200


@app.route('/choices/<int:id>', methods=['DELETE'])
def delete_choice(id):
    choice = Choice.query.get(id)
    if choice is None:
        abort(404)
    
    db.session.delete(choice)
    db.session.commit()
    return jsonify({'message': 'Option supprimée'}), 200


app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad request"}), 400)