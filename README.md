# smartmirror

from pprint import pprint
from news import source
from news import news

all_news = list()
preferred_news = list()

Get list of sources from 'news.py' and append to all_news
<
for src in news.News.sources:
    news_src = source.Source(src)
    all_news.append(news_src)

# Get list of preferred sources from 'news.py', get all corresponding
# articles of the preferred sources and append to preferred_news
# TODO Function
for src in news.News.preferred_sources:
    news_src = source.Source(src)
    news_src.get_articles(src)
    preferred_news.append(news_src)

# Print all available sources, change 'all_news' to 'preferred_news'
# for preferred
#
# 'source_id': Returns id of source
# 'name': Returns name of source
# 'articles': Returns all articles of corresponding source (preferred_news only)
# TODO Function
for news in all_news:
    pprint(news.source['name'])

# Print all articles from preferred news
# TODO Function
for news in preferred_news:
    pprint(news.source['name'])
    pprint(news.source['articles'])

# Print a single article from a specific preferred news source based on
# the article id
# TODO Wrap in function. Better referencing
article = preferred_news[0].get_article_by_id(2)
article_id = article['article_id']
title = article['title']
description = article['description']

print('Article ID: ')
pprint(article_id)
print('Title: ')
pprint(title)
print('Description: ')
pprint(description)
