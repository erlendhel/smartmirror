# smartmirror
Documentation and usage of smartmirror repository

# Usage/Testing of News

TODO: Make functions

Required imports:
<pre><code>from pprint import pprint
from news import source
from news import news
</pre></code>

For testing lists 'all_news' and 'preferred_news' are used
<pre><code>all_news = list()
preferred_news = list()
</pre></code>

Get list of sources from 'news.py' and append to all_news:
<pre><code>for src in news.News.sources:
    news_src = source.Source(src)
    all_news.append(news_src)
    </pre></code>
    
Get list of preferred sources from 'news.py', get all corresponding articles of the preferred sources and append to preferred_news:
<pre><code>for src in news.News.preferred_sources:
    news_src = source.Source(src)
    news_src.get_articles(src)
    preferred_news.append(news_src)
</pre></code>

Print all available sources, change 'all_news' to 'preferred_news' for preferred.
Possible key values: 'source_id', 'name', 'articles'
<pre><code>for news in all_news:
    pprint(news.source['name'])
</pre></code>

Print all articles from preferred news:
<pre><code>for news in preferred_news:
    pprint(news.source['name'])
    pprint(news.source['articles'])
</pre></code>

Print a single article from a specific preferred news source based on article id:
<pre><code>article = preferred_news[0].get_article_by_id(2)
article_id = article['article_id']
title = article['title']
description = article['description']
published = article['published']

print('Article ID: ')
pprint(article_id)
print('Title: ')
pprint(title)
print('Description: ')
pprint(description)
print('Published at: ')
pprint(published)
</pre></code>
