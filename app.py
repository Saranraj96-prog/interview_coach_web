"""
AI Interview Coach - Flask Web App
Reuses the same OOP classes from ai_interview_coach.py and serves them
through a real HTML/CSS front end.

Run:
    pip install flask
    python app.py
Then open: http://127.0.0.1:5000
"""

from abc import ABC, abstractmethod
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# ---------- Same OOP structure as the console version ----------
class Question:
    def __init__(self, text, category, keywords):
        self.__text = text
        self.__category = category
        self.__keywords = keywords

    def get_text(self):
        return self.__text

    def get_category(self):
        return self.__category

    def get_keywords(self):
        return self.__keywords

    def to_dict(self):
        return {"text": self.__text, "category": self.__category}


class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, answer: str, question: Question) -> tuple:
        pass


class KeywordEvaluator(Evaluator):
    def evaluate(self, answer: str, question: Question) -> tuple:
        answer_lower = answer.lower()
        keywords = question.get_keywords()
        matched = [kw for kw in keywords if kw.lower() in answer_lower]
        missing = [kw for kw in keywords if kw.lower() not in answer_lower]
        score = round((len(matched) / len(keywords)) * 10, 1) if keywords else 5.0
        if len(answer.split()) < 5:
            score = min(score, 3.0)
        feedback = f"Matched concepts: {matched if matched else 'None'}. "
        feedback += f"Try to also mention: {missing}." if missing else "Great, you covered all key points!"
        return score, feedback


class QuestionBank:
    def __init__(self):
        self.__questions = [
            Question("Tell me about yourself.", "HR",
                      ["background", "skills", "experience", "goal"]),
            Question("What is Object-Oriented Programming?", "Technical",
                      ["class", "object", "inheritance", "encapsulation", "polymorphism"]),
            Question("Difference between list and tuple in Python?", "Technical",
                      ["mutable", "immutable", "list", "tuple"]),
            Question("What is your greatest strength?", "HR",
                      ["strength", "example", "workplace"]),
            Question("Why should we hire you?", "HR",
                      ["skills", "value", "company", "contribute"]),
        ]

    def get_all_questions(self):
        return self.__questions


bank = QuestionBank()
evaluator = KeywordEvaluator()
questions = bank.get_all_questions()


# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("index.html", questions=[q.to_dict() for q in questions])


@app.route("/evaluate", methods=["POST"])
def evaluate_answer():
    data = request.get_json()
    q_index = int(data["index"])
    answer = data["answer"]

    question = questions[q_index]
    score, feedback = evaluator.evaluate(answer, question)

    return jsonify({"score": score, "feedback": feedback})


if __name__ == "__main__":
    app.run(debug=True)
