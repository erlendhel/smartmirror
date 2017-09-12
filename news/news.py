from news import source
from news import article as ArticleImport
from pprint import pprint

#
# Contains lists to specify which sources of news can be accessed and also which
# sources are preferred by the user

#
# Functions:
# set_all_sources
# set_preferred_sources


class News(object):

    all_sources = list()
    pref_sources = list()

    sources = [
        'bbc-news',
        'bbc-sport',
        'bloomberg',
        'buzzfeed',
        'cnn',
        'ign',
        'the-new-york-times',
        'business-insider',
        'daily-mail',
        'engadget',
        'espn',
        'financial-times',
        'fortune',
        'fox-sports',
        'mirror',
        'national-geographic',
        'techcrunch',
        'techradar',
        'the-new-york-times',
        'time'
    ]

    preferred_sources = [
        'time',
        'bbc-news',
        'espn'
    ]

    # TODO: Function to change preferred_sources

    # Sets all sources corresponding to dict: 'sources'
    # Returns type: list
    def set_all_sources(self):
        for src in self.sources:
            news_src = source.Source(src)
            self.all_sources.append(news_src)
        return self.all_sources

    # Sets sources corresponding to dict: 'preferred_sources'
    # Returns type: list
    def set_preferred_sources(self):
        for src in self.preferred_sources:
            news_src = source.Source(src)
            news_src.init_articles(src)
            self.pref_sources.append(news_src)
        return self.pref_sources

    # Function that returns a exhaustive list of all articles from
    # preferred sources.
    # Returns type: list
    def get_all_articles(self):
        articles = list()
        for src in self.pref_sources:
            for article in src.source['articles']:
                articles.append(article)
        return articles

    def get_articles_by_source(self, preferred_news, source_id):
        for news in preferred_news:
            if news.source['source_id'] == source_id:
                articles = news.source['articles']
                return articles

    # Function to get a single article based on given article_id
    # Returns type: NewsArticle
    def get_article_by_id(self, article_id):
        for src in self.pref_sources:
            for art in src.source['articles']:
                if art['article_id'] == article_id:
                    article = art
                    return article

