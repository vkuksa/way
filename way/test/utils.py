import functools
import json

from flask import current_app


def __read_json(filename: str):
    global data
    try:
        content = current_app.open_resource('static/test_data/' + filename + '.json')
        data = json.load(content)
    except OSError:
        print("Could not open/read " + filename + " file")
    except TypeError:
        print("Could not perform reading of " + filename + " file")
    return data


def get_questions():
    return __read_json('questions')


def __calculate_result(score: int, count: int):
    avg = score/count
    if avg == 3:
        return 'neutral'
    return 'low' if avg < 3 else 'high'


def __reducer(a, b):
    domain = b["domain"]
    if a.get(domain) is None:
        a[domain] = {'score': 0, 'count': 0, 'result': 'neutral'}

    a[domain]["score"] += int(b["score"])
    a[domain]["count"] += 1
    a[domain]["result"] = __calculate_result(a[domain]["score"], a[domain]["count"])

    return a


def calculate_scores(answers):
    return functools.reduce(__reducer, answers, {})


def get_results(scores):
    domain_info = __read_json('domain_info')

    ret = {}
    for domain, info in scores.items():
        entry = next(filter(lambda val: val["domain"] == domain, domain_info))
        result = next(filter(lambda val: val["score"] == info["result"], entry["results"]))
        ret[domain] = {
            "title": entry["title"],
            "shortDescription": entry["shortDescription"],
            "description": entry["description"],
            "scoreText": result["score"],
            "text": result["text"],
            "count": info["count"],
            "score": info["score"],
        }

    return ret

