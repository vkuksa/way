from way.models import Article, Resource


class RecommendationProvider:
    model = {
        'O': {'high': 1, 'neutral': 2, 'low': 3},
        'C': {'high': 1, 'neutral': 2, 'low': 3},
        'E': {'high': 1, 'neutral': 2, 'low': 3},
        'A': {'high': 1, 'neutral': 2, 'low': 3},
        'N': {'high': 3, 'neutral': 2, 'low': 1}
    }
    results = {'O': 0, 'C': 0, 'E': 0, 'A': 0, 'N': 0}
    articles = []
    resources = []
    max_results = 5

    def __init__(self, test_results):
        summary = 0
        for k, v in test_results.items():
            self.results[k] = self.model[k][v['result']]
            summary += self.model[k][v['result']]

        for k, v in self.results.items():
            n = round(v / ((1/self.max_results) * summary))
            self.articles.extend(Article.query.filter_by(tag=RecommendationProvider.__get_domain(k)).limit(n).all())
            self.resources.extend(Resource.query.filter_by(tag=RecommendationProvider.__get_domain(k)).limit(n).all())

    @staticmethod
    def __get_domain(s: str):
        return {
            'O': 'Openness',
            'C': 'Conscientiousness',
            'E': 'Extraversion',
            'A': 'Agreeableness',
            'N': 'Neuroticism'
        }[s]

    def get_articles(self):
        return self.articles

    def get_resources(self):
        return self.resources
