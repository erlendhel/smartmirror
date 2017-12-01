#
# Defines object 'NewsArticle' which contains a single article
# in dictionary 'article'.
#
# Format 'article':
# {
#  'title': str
#  'description': str
#  'published: str
# }
#


class NewsArticle(object):

    article = {}
    # Function to clean article response from api
    # Returns type: dict
    def set_article(self, article_id, title, description, published):
        self.article = {
            'article_id': article_id,
            'title': title,
            'description': description,
            'published': published
        }
        return self.article
