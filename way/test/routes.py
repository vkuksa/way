from flask import render_template, Blueprint, g, request, jsonify, url_for
from flask_login import login_required, current_user

import json
import way.test.utils
import way.recommendations.utils
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
    latest_user_test = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.id.desc()).first()
    latest_test = TestResult.query.order_by(TestResult.id.desc()).first()
    test_id = latest_user_test.id if latest_user_test else latest_test.id
    return render_template('start_test.html', title='Start Test', test_id=test_id)


@test.route("/test/<int:test_id>", methods=['GET', 'POST'])
@login_required
def load(test_id):
    if request.method == 'POST':
        data = json.loads(request.get_json())
        print(data)
        scores = way.test.utils.calculate_scores(data)
        print(scores)

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
    results = None
    previous_data = None
    articles = None
    resources = None

    test_results = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.id.desc()).all()
    if len(test_results) >= 1:
        recent_result = test_results[0]
        recent_data = recent_result.to_dict()
        print(recent_data)
        rp = way.recommendations.utils.RecommendationProvider(recent_data)
        articles = rp.get_articles()
        resources = rp.get_resources()

        if len(test_results) >= 2:
            previous_result = test_results[1]
            previous_data = previous_result.get_scores()

        results = way.test.utils.get_results(recent_data)
    return render_template('test_results.html', title='Test Results', articles=articles, resources=resources,
                           data=results, previous_data=previous_data, legend='Test result')
