from interface.newsapi import NewsAPI
from news import article as ArticleImport

apiKey = '437cc86718154f9592f4f135401caf7f'
apiParams = {}
api = NewsAPI(apiKey)
# List which contains all news sources from newsApi, used for referencing
newsSources = api.sources(apiParams)

#
# Defines object 'Source' which contains any news source
# in dictionary 'source'.
#
# Format 'source':
# {
#  'articles': list()
#  'name': str
# }
#
#


class Source(object):

    source = {}

    def __init__(self, source_id):

        if source_id is None:
            self.source = None
        else:
            self.source = {
                'source_id': source_id,
                'name': self.init_name(source_id),
                'path': None,
                'articles': None
            }

    # Function to get the name of the source given by the id in the newsSources list
    # Returns type: str
    def init_name(self, source_id):

        for newsSource in newsSources:
            if newsSource['id'] == source_id:
                name = newsSource['name']
                return name

    # Function to get articles for the source given by the id
    def init_articles(self, source_id):

        # Edit 'params' according to: status, sortBy
        params = {}
        article_num = 0
        articles = list()

        for article in api.articles(source_id, params):
            article_id = source_id + str(article_num)
            title = article['title']
            description = article['description']
            published = article['publishedAt']
            article = ArticleImport.NewsArticle()
            a = article.set_article(article_id, title, description, published)
            articles.append(a)
            article_num += 1

        self.source['articles'] = articles

