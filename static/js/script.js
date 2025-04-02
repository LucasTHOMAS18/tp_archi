document.addEventListener('DOMContentLoaded', function() {
    let currentQuizId = null;
    let currentQuestionId = null;
    let currentQuestionType = null;

    document.getElementById('button').addEventListener('click', refreshQuizList);
    document.querySelector('#tools #add').addEventListener('click', formQuiz);
    document.querySelector('#tools #del').addEventListener('click', delQuiz);
    document.querySelector('#questionTools #addQuestion').addEventListener('click', selectQuestionType);
    document.querySelector('#questionTools #delQuestion').addEventListener('click', delQuestion);

    document.getElementById('questions').style.display = 'none';
    refreshQuizList();

    function remplirQuiz(repjson) {
        const quizzesElement = document.getElementById('quizzes');
        quizzesElement.innerHTML = '';
        const ul = document.createElement('ul');
        quizzesElement.appendChild(ul);

        repjson.forEach(quiz => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.textContent = quiz.name;
            a.addEventListener('click', () => detailsQuiz(quiz));
            li.appendChild(a);
            ul.appendChild(li);
        });
    }

    function onerror(err) {
        document.getElementById('quizzes').innerHTML = `<b>Impossible de récupérer les quiz !</b>${err}`;
    }

    function refreshQuizList() {
        document.getElementById('currentquiz').innerHTML = '';
        document.getElementById('questions').style.display = 'none';
        document.getElementById('questionsList').innerHTML = '';
        document.getElementById('currentQuestion').innerHTML = '';
        currentQuizId = null;
        currentQuestionId = null;
        currentQuestionType = null;

        fetch('http://127.0.0.1:5000/questionnaires')
            .then(response => {
                if (response.ok) return response.json();
                else throw new Error('Problème ajax: ' + response.status);
            })
            .then(remplirQuiz)
            .catch(onerror);
    }

    function detailsQuiz(quiz) {
        document.getElementById('currentquiz').innerHTML = '';
        formQuiz();
        fillFormQuiz(quiz);
        currentQuizId = quiz.id;

        document.getElementById('questions').style.display = 'block';
        loadQuestions(currentQuizId);
    }

    function loadQuestions(quizId) {
        document.getElementById('questionsList').innerHTML = '';
        document.getElementById('currentQuestion').innerHTML = '';
        currentQuestionId = null;
        currentQuestionType = null;

        fetch(`http://127.0.0.1:5000/questionnaires/${quizId}/questions`)
            .then(response => {
                if (response.ok) return response.json();
                else throw new Error('Problème ajax: ' + response.status);
            })
            .then(displayQuestions)
            .catch(err => {
                document.getElementById('questionsList').innerHTML = `<b>Impossible de récupérer les questions !</b>${err}`;
            });
    }

    function displayQuestions(questions) {
        if (questions.length === 0) {
            document.getElementById('questionsList').innerHTML = '<p>Aucune question pour ce quiz.</p>';
            return;
        }

        const ul = document.createElement('ul');
        document.getElementById('questionsList').appendChild(ul);

        questions.sort((a, b) => a.ordre - b.ordre);

        questions.forEach(question => {
            const questionTypeText = question.question_type === 'open' ? 'Question ouverte' : 'QCM';
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.textContent = `${question.ordre}. ${question.title} (${questionTypeText})`;
            a.addEventListener('click', () => detailsQuestion(question));
            li.appendChild(a);
            ul.appendChild(li);
        });
    }

    function detailsQuestion(question) {
        currentQuestionId = question.id;
        currentQuestionType = question.question_type;

        document.getElementById('currentQuestion').innerHTML = '';

        if (currentQuestionType === 'open') {
            formOpenQuestion(false);
            fillOpenQuestionForm(question);
        } else if (currentQuestionType === 'mcq') {
            formMCQuestion(false);
            fillMCQuestionForm(question);
        }
    }

    class Quiz {
        constructor(name, uri) {
            this.name = name;
            this.uri = uri;
        }
    }

    class Question {
        constructor(title, ordre, question_type, questionnaire_id, uri) {
            this.title = title;
            this.ordre = ordre;
            this.question_type = question_type;
            this.questionnaire_id = questionnaire_id;
            this.uri = uri;
        }
    }

    class OpenQuestion extends Question {
        constructor(title, ordre, questionnaire_id, expected_answer, uri) {
            super(title, ordre, 'open', questionnaire_id, uri);
            this.expected_answer = expected_answer;
        }
    }

    class MCQuestion extends Question {
        constructor(title, ordre, questionnaire_id, choices, uri) {
            super(title, ordre, 'mcq', questionnaire_id, uri);
            this.choices = choices || [];
        }
    }

    class Choice {
        constructor(text, is_correct) {
            this.text = text;
            this.is_correct = is_correct;
        }
    }

    function formQuiz() {
        const currentQuizElement = document.getElementById('currentquiz');
        currentQuizElement.innerHTML = `
            <span>Nom du quiz<input type="text" id="name"><br></span>
            <span><input type="hidden" id="turi"><br></span>
            <span><input type="button" value="${currentQuizId ? 'Modifier Quiz' : 'Enregistrer Quiz'}"><br></span>
        `;
        const button = currentQuizElement.querySelector('input[type="button"]');
        button.addEventListener('click', currentQuizId ? saveModifiedQuiz : saveNewQuiz);
    }

    function fillFormQuiz(q) {
        document.getElementById('name').value = q.name;
        q.uri = q.uri || `http://127.0.0.1:5000/questionnaires/${q.id}`;
        document.getElementById('turi').value = q.uri;
    }

    function selectQuestionType() {
        if (!currentQuizId) {
            alert("Veuillez d'abord sélectionner un quiz.");
            return;
        }

        const currentQuestionElement = document.getElementById('currentQuestion');
        currentQuestionElement.innerHTML = `
            <h4>Nouvelle question</h4>
            <div><label>Type de question:</label><br></div>
            <button>Question Ouverte</button>
            <button>Question à Choix Multiples</button>
        `;

        const buttons = currentQuestionElement.querySelectorAll('button');
        buttons[0].addEventListener('click', () => {
            currentQuestionElement.innerHTML = '';
            formOpenQuestion(true);
        });
        buttons[1].addEventListener('click', () => {
            currentQuestionElement.innerHTML = '';
            formMCQuestion(true);
        });
    }

    function formOpenQuestion(isNew) {
        const currentQuestionElement = document.getElementById('currentQuestion');
        currentQuestionElement.innerHTML = `
            <h4>${isNew ? 'Nouvelle question ouverte' : 'Modifier la question ouverte'}</h4>
            <div><label for="qTitle">Titre:</label><input type="text" id="qTitle"><br></div>
            <div><label for="qOrdre">Ordre:</label><input type="number" id="qOrdre" min="1"><br></div>
            <div><label for="qExpectedAnswer">Réponse attendue (optionnelle):</label><br><textarea id="qExpectedAnswer" rows="3" cols="40"></textarea><br></div>
            <span><input type="hidden" id="qUri"><br></span>
            <span><input type="button" value="${isNew ? 'Ajouter Question' : 'Modifier Question'}" id="saveQuestionButton"><br></span>
        `;
    
        const button = document.getElementById('saveQuestionButton');
        button.addEventListener('click', isNew ? saveNewOpenQuestion : saveModifiedOpenQuestion);
    }

    function fillOpenQuestionForm(q) {
        document.getElementById('qTitle').value = q.title;
        document.getElementById('qOrdre').value = q.ordre;
        document.getElementById('qExpectedAnswer').value = q.expected_answer || '';
        q.uri = q.uri || `http://127.0.0.1:5000/questions/${q.id}`;
        document.getElementById('qUri').value = q.uri;
    }

    function formMCQuestion(isNew) {
        const currentQuestionElement = document.getElementById('currentQuestion');
        currentQuestionElement.innerHTML = `
            <h4>${isNew ? 'Nouvelle question à choix multiples' : 'Modifier la question à choix multiples'}</h4>
            <div><label for="qTitle">Titre:</label><input type="text" id="qTitle"><br></div>
            <div><label for="qOrdre">Ordre:</label><input type="number" id="qOrdre" min="1"><br></div>
            <span><input type="hidden" id="qUri"><br></span>
            <div id="choicesList"><h5>Options:</h5></div>
            <div><button id="addChoice">Ajouter une option</button></div>
            <span><input type="button" value="${isNew ? 'Ajouter Question' : 'Modifier Question'}" id="saveQuestionButton"><br></span>
        `;
    
        document.getElementById('addChoice').addEventListener('click', addChoiceForm);
    
        const button = document.getElementById('saveQuestionButton');
        button.addEventListener('click', isNew ? saveNewMCQuestion : saveModifiedMCQuestion);
    
        if (isNew) {
            addChoiceForm();
        }
    }

    function addChoiceForm() {
        const choiceId = new Date().getTime();
        const choiceDiv = document.createElement('div');
        choiceDiv.className = 'choice-item';
        choiceDiv.dataset.choiceId = choiceId;

        const choiceInput = document.createElement('input');
        choiceInput.type = 'text';
        choiceInput.placeholder = 'Texte de l\'option';
        choiceInput.className = 'choice-text';

        const correctCheckbox = document.createElement('input');
        correctCheckbox.type = 'checkbox';
        correctCheckbox.className = 'choice-correct';

        const removeButton = document.createElement('button');
        removeButton.textContent = 'Supprimer';
        removeButton.addEventListener('click', () => {
            choiceDiv.remove();
        });

        choiceDiv.appendChild(choiceInput);
        choiceDiv.appendChild(document.createTextNode(' Correcte: '));
        choiceDiv.appendChild(correctCheckbox);
        choiceDiv.appendChild(document.createTextNode(' '));
        choiceDiv.appendChild(removeButton);

        document.getElementById('choicesList').appendChild(choiceDiv);
    }

    function fillMCQuestionForm(q) {
        document.getElementById('qTitle').value = q.title;
        document.getElementById('qOrdre').value = q.ordre;
        q.uri = q.uri || `http://127.0.0.1:5000/questions/${q.id}`;
        document.getElementById('qUri').value = q.uri;

        if (q.choices && q.choices.length > 0) {
            q.choices.forEach(choice => {
                const choiceId = new Date().getTime() + Math.random();
                const choiceDiv = document.createElement('div');
                choiceDiv.className = 'choice-item';
                choiceDiv.dataset.choiceId = choiceId;

                const choiceInput = document.createElement('input');
                choiceInput.type = 'text';
                choiceInput.placeholder = 'Texte de l\'option';
                choiceInput.className = 'choice-text';
                choiceInput.value = choice.text;

                const correctCheckbox = document.createElement('input');
                correctCheckbox.type = 'checkbox';
                correctCheckbox.className = 'choice-correct';
                correctCheckbox.checked = choice.is_correct;

                const removeButton = document.createElement('button');
                removeButton.textContent = 'Supprimer';
                removeButton.addEventListener('click', () => {
                    choiceDiv.remove();
                });

                choiceDiv.appendChild(choiceInput);
                choiceDiv.appendChild(document.createTextNode(' Correcte: '));
                choiceDiv.appendChild(correctCheckbox);
                choiceDiv.appendChild(document.createTextNode(' '));
                choiceDiv.appendChild(removeButton);

                document.getElementById('choicesList').appendChild(choiceDiv);
            });
        } else {
            addChoiceForm();
        }
    }

    function collectChoices() {
        const choices = [];
        document.querySelectorAll('.choice-item').forEach(choiceItem => {
            const text = choiceItem.querySelector('.choice-text').value;
            const isCorrect = choiceItem.querySelector('.choice-correct').checked;

            if (text.trim() !== '') {
                choices.push(new Choice(text, isCorrect));
            }
        });
        return choices;
    }

    function saveNewQuiz() {
        const quiz = new Quiz(
            document.getElementById('name').value
        );

        fetch('http://127.0.0.1:5000/questionnaires', {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(quiz)
        })
        .then(response => {
            if (response.ok) return response.json();
            else throw new Error('Problème ajax: ' + response.status);
        })
        .then(data => {
            console.log('Quiz saved successfully');
            currentQuizId = data.id;
            document.getElementById('questions').style.display = 'block';
            refreshQuizList();
        })
        .catch(err => {
            console.log(err);
        });
    }

    function saveModifiedQuiz() {
        const quiz = new Quiz(
            document.getElementById('name').value,
            document.getElementById('turi').value
        );

        fetch(quiz.uri, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'PUT',
            body: JSON.stringify(quiz)
        })
        .then(response => {
            if (response.ok) return response.json();
            else throw new Error('Problème ajax: ' + response.status);
        })
        .then(() => {
            console.log('Quiz updated successfully');
            refreshQuizList();
        })
        .catch(err => {
            console.log(err);
        });
    }

    function saveNewOpenQuestion() {
        console.log('saveNewOpenQuestion called');
        if (!currentQuizId) {
            alert('Erreur: Aucun quiz sélectionné');
            return;
        }
    
        const ordre = parseInt(document.getElementById('qOrdre').value) || 1;
    
        const question = new OpenQuestion(
            document.getElementById('qTitle').value,
            ordre,
            currentQuizId,
            document.getElementById('qExpectedAnswer').value
        );
    
        fetch(`http://127.0.0.1:5000/questionnaires/${currentQuizId}/questions`, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(question)
        })
        .then(response => {
            if (response.ok) return response.json();
            else throw new Error('Problème ajax: ' + response.status);
        })
        .then(data => {
            console.log('Question saved successfully', data);
            loadQuestions(currentQuizId);
        })
        .catch(err => {
            console.log(err);
        });
    }

    function saveNewMCQuestion() {
        console.log('saveNewMCQuestion called');
        if (!currentQuizId) {
            alert('Erreur: Aucun quiz sélectionné');
            return;
        }
    
        const ordre = parseInt(document.getElementById('qOrdre').value) || 1;
        const choices = collectChoices();
    
        if (choices.length === 0) {
            alert('Veuillez ajouter au moins une option pour cette question.');
            return;
        }
    
        const question = new MCQuestion(
            document.getElementById('qTitle').value,
            ordre,
            currentQuizId,
            choices
        );
    
        fetch(`http://127.0.0.1:5000/questionnaires/${currentQuizId}/questions`, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(question)
        })
        .then(response => {
            if (response.ok) return response.json();
            else throw new Error('Problème ajax: ' + response.status);
        })
        .then(data => {
            console.log('Question saved successfully', data);
            loadQuestions(currentQuizId);
        })
        .catch(err => {
            console.log(err);
        });
    }

    function saveModifiedOpenQuestion() {
        if (!currentQuestionId) {
            alert('Erreur: Aucune question sélectionnée');
            return;
        }

        const uri = document.getElementById('qUri').value;
        const ordre = parseInt(document.getElementById('qOrdre').value) || 1;

        const question = {
            title: document.getElementById('qTitle').value,
            ordre: ordre,
            expected_answer: document.getElementById('qExpectedAnswer').value
        };

        fetch(uri, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'PUT',
            body: JSON.stringify(question)
        })
        .then(response => {
            if (response.ok) return response.json();
            else throw new Error('Problème ajax: ' + response.status);
        })
        .then(data => {
            console.log('Question updated successfully');
            loadQuestions(currentQuizId);
        })
        .catch(err => {
            console.log(err);
        });
    }

    function saveModifiedMCQuestion() {
        if (!currentQuestionId) {
            alert('Erreur: Aucune question sélectionnée');
            return;
        }

        const uri = document.getElementById('qUri').value;
        const ordre = parseInt(document.getElementById('qOrdre').value) || 1;
        const choices = collectChoices();

        if (choices.length === 0) {
            alert('Veuillez ajouter au moins une option pour cette question.');
            return;
        }

        const question = {
            title: document.getElementById('qTitle').value,
            ordre: ordre,
            choices: choices
        };

        fetch(uri, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'PUT',
            body: JSON.stringify(question)
        })
        .then(response => {
            if (response.ok) return response.json();
            else throw new Error('Problème ajax: ' + response.status);
        })
        .then(data => {
            console.log('Question updated successfully');
            loadQuestions(currentQuizId);
        })
        .catch(err => {
            console.log(err);
        });
    }

    function delQuiz() {
        if (!currentQuizId) {
            alert('Veuillez d\'abord sélectionner un quiz.');
            return;
        }

        if (!confirm('Êtes-vous sûr de vouloir supprimer ce quiz et toutes ses questions ?')) {
            return;
        }

        const uri = `http://127.0.0.1:5000/questionnaires/${currentQuizId}`;

        fetch(uri, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) return response.json();
            else throw new Error('Problème ajax: ' + response.status);
        })
        .then(() => {
            console.log('Quiz deleted successfully');
            refreshQuizList();
        })
        .catch(err => {
            console.log(err);
        });
    }

    function delQuestion() {
        if (!currentQuestionId) {
            alert('Veuillez d\'abord sélectionner une question.');
            return;
        }

        if (!confirm('Êtes-vous sûr de vouloir supprimer cette question ?')) {
            return;
        }

        const uri = `http://127.0.0.1:5000/questions/${currentQuestionId}`;

        fetch(uri, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) return response.json();
            else throw new Error('Problème ajax: ' + response.status);
        })
        .then(() => {
            console.log('Question deleted successfully');
            loadQuestions(currentQuizId);
            document.getElementById('currentQuestion').innerHTML = '';
        })
        .catch(err => {
            console.log(err);
        });
    }

    function get_data_from_file(request) {
        return request.json();
    }
});