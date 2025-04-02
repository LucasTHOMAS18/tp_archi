from .app import db


class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"<Questionnaire ({self.id}) {self.name}>"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    ordre = db.Column(db.Integer)
    question_type = db.Column(db.String(20))  # 'open' ou 'mcq'
    questionnaire_id = db.Column(
        db.Integer, db.ForeignKey("questionnaire.id")) 
    questionnaire = db.relationship(
        "Questionnaire", backref=db.backref("questions", lazy="dynamic"))
    
    __mapper_args__ = {
        'polymorphic_on': question_type,
        'polymorphic_identity': 'base'
    }

    def __init__(self, title, ordre, questionnaire_id):
        self.title = title
        self.ordre = ordre
        self.questionnaire_id = questionnaire_id
    
    def __repr__(self):
        return f"<Question ({self.id}) {self.title}>"
    
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "ordre": self.ordre,
            "questionnaire_id": self.questionnaire_id,
            "question_type": self.question_type
        }


class OpenQuestion(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    expected_answer = db.Column(db.Text, nullable=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'open'
    }
    
    def __init__(self, title, ordre, questionnaire_id, expected_answer=None):
        super().__init__(title, ordre, questionnaire_id)
        self.expected_answer = expected_answer
        
    def to_json(self):
        json_data = super().to_json()
        json_data.update({
            "expected_answer": self.expected_answer
        })
        return json_data


class MCQuestion(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'mcq'
    }
    
    def __init__(self, title, ordre, questionnaire_id):
        super().__init__(title, ordre, questionnaire_id)
        
    def to_json(self):
        json_data = super().to_json()
        json_data.update({
            "choices": [choice.to_json() for choice in self.choices]
        })
        return json_data


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('mc_question.id'))
    question = db.relationship("MCQuestion", backref=db.backref("choices", lazy="dynamic"))
    
    def __init__(self, text, is_correct, question_id):
        self.text = text
        self.is_correct = is_correct
        self.question_id = question_id
        
    def to_json(self):
        return {
            "id": self.id,
            "text": self.text,
            "is_correct": self.is_correct
        }


def valid_data(request):
    data = get_data_from_file(request)
    
    if 'questionnaires' in data:
        return data['questionnaires']