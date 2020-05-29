from flask import render_template, Blueprint, g, request, jsonify, url_for
from flask_login import login_required, current_user

import json
import way.test.utils
from way import db
from way.models import Article, Resource, TestResult, DomainResult

test = Blueprint('test', __name__)


def __load_questions():
    if 'questions' not in g:
        g.questions = way.test.utils.get_questions()


def __get_questions():
    __load_questions()
    questions = g.get('questions', [])
    return questions


@test.route("/test/inventory")
def inventory():
    return jsonify(__get_questions())


@test.route("/test/start")
@login_required
def start():
    return render_template('start_test.html', title='Start Test')


@test.route("/test/<int:test_id>", methods=['GET', 'POST'])
@login_required
def load(test_id):
    if request.method == 'POST':
        data = json.loads(request.get_json())
        scores = way.test.utils.calculate_scores(data)

        test_result = TestResult(user_id=current_user.id)
        for domain, info in scores.items():
            domain_result = DomainResult(domain=domain, score=info["score"], count=info["count"], result=info["result"])
            db.session.add(domain_result)
            db.session.commit()
            setattr(test_result, domain + '_id', domain_result.id)
        db.session.add(test_result)
        db.session.commit()

        return url_for('test.result', test_id=test_id)
    if request.method == 'GET':
        return render_template('test_entry.html', title='Test', test_id=test_id)


@test.route("/test/<int:test_id>/result")
@login_required
def result(test_id):
    test_result = TestResult.query.get(test_id)
    test_data = test_result.to_dict()
    results = way.test.utils.get_results(test_data)
    articles = Article.query.limit(5).all()  # TODO: add simple model for recommendations
    resources = Resource.query.limit(5).all()
    return render_template('test_results.html', title='Test Results', articles=articles, resources=resources,
                           data=results, legend='Test result')


@test.route("/test/test2")
def testorino2():
    res = """[
    {
      "domain": "A",
      "facet": "1",
      "score": "3"
    },
    {
      "domain": "A",
      "facet": "1",
      "score": "3"
    },
    {
      "domain": "E",
      "facet": "1",
      "score": "3"
    },
    {
      "domain": "E",
      "facet": "2",
      "score": "3"
    },
    {
      "domain": "O",
      "facet": "1",
      "score": "3"
    },
    {
      "domain": "N",
      "facet": "2",
      "score": "3"
    },
    {
      "domain": "C",
      "facet": "2",
      "score": "3"
    }
  ]"""
    answers = json.loads(res)
    scores = way.test.utils.calculate_scores(answers)

    print(scores)

    test_result = TestResult(user_id=current_user.id)
    for domain, info in scores.items():
        domain_result = DomainResult(domain=domain, score=info["score"], count=info["count"], result=info["result"])
        db.session.add(domain_result)
        db.session.commit()
        setattr(test_result, domain + '_id', domain_result.id)
    db.session.add(test_result)
    db.session.commit()

    results = way.test.utils.get_results(scores)
    return render_template('test.html', data=results)
