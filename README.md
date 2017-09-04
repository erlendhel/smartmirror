# smartmirror
Documentation and usage of smartmirror repository

# Usage/Testing of News

TODO: Make functions

#### Required imports:
<pre><code>from pprint import pprint
from news import news
</pre></code>

#### Initialize list of preferred_news *REQUIRED*
<pre><code>test = news.News()
preferred_news = test.set_preferred_sources()
</pre></code>

#### Iterating through preferred_news returns everything from preferred_news
##### Code
<pre><code>for news in preferred_news:
    pprint(news.source)
</pre></code>
##### Output
<pre><code>{'articles': [{'article_id': 'business-insider0',
               'description': 'MEMPHIS, Tenn. (AP) — Harvey spread its misery '
                              'into the Deep South as a likely tornado damaged '
                              'homes and toppled trees in a rural area of '
                              'northwest Alabama and areas around the region '
                              'faced flooding fears.',
               'published': '2017-09-01T10:25:00Z',
               'title': 'Harvey is causing tornadoes and flooding across the '
                        'Deep South'},
              {'article_id': 'business-insider1',
               'description': 'Friday is packed with economic news\xa0on US...',
               'published': '2017-09-01T09:57:00Z',
               'title': "Here's your full preview of the jobs report on a big "
                        "day for America's economy"},
              {'article_id': 'business-insider2',
               'description': 'MOSCOW (Reuters) - Russian President '
                              'Vladimir...',
               'published': '2017-09-01T08:47:00Z',
               'title': 'Putin warns that North Korea is on the verge of a '
                        "'large-scale conflict'"},
              {'article_id': 'business-insider3',
               'description': 'Here is what you need to know...',
               'published': '2017-09-01T10:41:00Z',
               'title': '10 things you need to know before the opening bell'},
              {'article_id': 'business-insider4',
               'description': 'Dozens of tech-industry titans are joining...',
               'published': '2017-09-01T04:43:04Z',
               'title': "'I stand with the Dreamers': Mark Zuckerberg and "
                        'dozens of tech giants are urging Trump to protect '
                        'immigrants covered by Obama-era policy'},
              {'article_id': 'business-insider5',
               'description': 'Stock market volatility — or the lack...',
               'published': '2017-09-01T10:03:00Z',
               'title': 'The creator of the VIX says the market is looking at '
                        'volatility all wrong'},
              {'article_id': 'business-insider6',
               'description': "Robert Mueller, the FBI's special counsel in...",
               'published': '2017-09-01T00:47:51Z',
               'title': 'Robert Mueller is reportedly bringing an IRS '
                        'financial crimes unit into the Russia investigation'},
              {'article_id': 'business-insider7',
               'description': 'As eastern Texas saw its first clear skies '
                              'and...',
               'published': '2017-08-31T22:20:00Z',
               'title': 'Incredible satellite photos show Texas before and '
                        'after Harvey flooded the region'},
              {'article_id': 'business-insider8',
               'description': 'LONDON – Yngve Slyngstad, the CEO of...',
               'published': '2017-09-01T07:48:58Z',
               'title': "The head of the world's biggest sovereign wealth fund "
                        'is worried about global trade'},
              {'article_id': 'business-insider9',
               'description': 'The National Labor Relations Board has filed '
                              'an...',
               'published': '2017-09-01T01:10:54Z',
               'title': 'Federal labor officials are going after Tesla over '
                        "alleged workers' rights violations"}],
 'name': 'Business Insider',
 'path': None,
 'source_id': 'business-insider'}
{'articles': [{'article_id': 'national-geographic0',
               'description': 'Newly revealed images shed light on her '
                              'research breakthroughs, how she became famous, '
                              'and the photographer she loved.',
               'published': '2017-09-01T04:02:28Z',
               'title': 'How Jane Goodall Changed What We Know About Chimps'},
              {'article_id': 'national-geographic1',
               'description': 'Excavations in El Salvador recently unearthed '
                              "the remains of some of the region's oldest "
                              'societies.',
               'published': '2017-09-01T03:24:32Z',
               'title': 'Ancient Remains Offer Clues About Early Americans'},
              {'article_id': 'national-geographic2',
               'description': 'Set sail with seafaring photographers around '
                              'the globe.',
               'published': '2017-08-31T20:41:26Z',
               'title': 'Stunning Sailing Adventures Around the World'},
              {'article_id': 'national-geographic3',
               'description': 'The heavy, trunk-nosed animal squirmed and '
                              'wiggled, making the rescue a difficult one.',
               'published': '2017-08-31T18:48:00Z',
               'title': 'Tapir Breaks Out of Zoo, Gets Stuck in Palace Pond'},
              {'article_id': 'national-geographic4',
               'description': 'No matter your interest, the Great Lakes state '
                              'has got you covered.',
               'published': '2017-08-31T16:32:00Z',
               'title': 'A Perfect Michigan Spot for Every Type of Traveler'},
              {'article_id': 'national-geographic5',
               'description': 'Scientists are unsure if warming temperatures '
                              'are causing the bizarre invertebrates to '
                              'spread.',
               'published': '2017-08-31T12:07:36Z',
               'title': 'Mysterious, Brain-Like Blob Found in Lagoon'},
              {'article_id': 'national-geographic6',
               'description': 'Three decades after the groundbreaking '
                              'researcher was killed in Rwanda, the ape '
                              'population is growing—but is under rising '
                              'pressure.',
               'published': '2017-08-31T04:53:50Z',
               'title': 'The Gorillas Dian Fossey Saved Are Facing New '
                        'Challenges'},
              {'article_id': 'national-geographic7',
               'description': '100 years after the inkblots were created, '
                              'studies show they reveal something about us.',
               'published': '2017-08-31T04:53:43Z',
               'title': 'The Rorschach Test Is More Accurate Than You Think'},
              {'article_id': 'national-geographic8',
               'description': 'The United States has some pretty peculiar '
                              'regulations when it comes to wildlife—real or '
                              'imagined.',
               'published': '2017-08-31T04:01:00Z',
               'title': "You Can't Kill Bigfoot in Washington and More Odd "
                        'Animal Laws'},
              {'article_id': 'national-geographic9',
               'description': 'The Netherlands has become an agricultural '
                              'giant by showing what the future of farming '
                              'could look like.',
               'published': '2017-08-31T04:01:00Z',
               'title': 'This Tiny Country Feeds the World'}],
 'name': 'National Geographic',
 'path': None,
 'source_id': 'national-geographic'}
 
 etc ...
</pre></code>

#### Iterating to get specific values from the list, possible keys: source_id, name, path, articles
##### Code
<pre><code>for news in preferred_news:
    pprint(news.source['source_id'])
    pprint(news.source['name'])
    pprint(news.source['path'])
</pre></code>
##### Output
<pre><code>'business-insider'
'Business Insider'
None
'national-geographic'
'National Geographic'
None
'espn'
'ESPN'
None
</pre></code>

#### Get a specific source from preferred_news. Valid values as source_id: sources listed in preferred_news in news.py
##### Code
<pre><code>for news in preferred_news:
    if news.source['source_id'] == 'espn':
        pprint(news.source['name'])
        pprint(news.source['path'])
</pre></code>
##### Output
<pre><code>'ESPN'
None
</pre></code>

#### Get articles from a specific source. Current valid sources: espn, national-geographic, business-insider
##### Code
<pre><code>articles_by_source = test.get_articles_by_source(preferred_news, 'national-geographic')
</pre></code>

#### Iterate through list of articles. Allowed keys: article_id, title, description, published
##### Code
<pre><code>for article in articles_by_source:
    pprint(article['article_id'] + ', ' + article['title'])
</pre></code>
##### Output
<pre><code>'national-geographic0, How Jane Goodall Changed What We Know About Chimps'
'national-geographic1, Ancient Remains Offer Clues About Early Americans'
'national-geographic2, Stunning Sailing Adventures Around the World'
'national-geographic3, Tapir Breaks Out of Zoo, Gets Stuck in Palace Pond'
'national-geographic4, A Perfect Michigan Spot for Every Type of Traveler'
'national-geographic5, Mysterious, Brain-Like Blob Found in Lagoon'
'national-geographic6, The Gorillas Dian Fossey Saved Are Facing New Challenges'
'national-geographic7, The Rorschach Test Is More Accurate Than You Think'
</pre></code>

#### Get a single article by article_id. article_id is of the form: espn3, national-geographic2, business-insider5 etc.
##### Code
<pre><code>article = test.get_article_by_id('espn3')
</pre></code>

#### Raw print of article:
##### Code
<pre><code>pprint(article)
</pre></code>
#### Output
<pre><code>{'article_id': 'espn3',
 'description': "It's not supposed to take this much work for the graceful, "
                'dominant Roger Federer. But after consecutive five-set '
                "struggles, he has left his devout fans wondering what's "
                'wrong.',
 'published': '2017-09-01T02:13:21Z',
 'title': 'Panic meter running high for Federer fans'}
</pre></code>

#### Print specific values of article. Allowed keys: article_id, title, description, published
##### Code
<pre><code>pprint(article['article_id'] + ', ' + article['title'])
</pre></code>
##### Output
<pre><code>'espn3, Panic meter running high for Federer fans'
</pre></code>
