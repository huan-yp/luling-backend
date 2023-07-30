
import requests
import newspaper

from newspaper import Article

def get_raw_content(url):
    headers = {"Content-Type": "text/html; charset=utf-8"}
    response = requests.get(url, headers=headers)
    content_type = response.headers["Content-Type"]
    charset = content_type[content_type.find('=') + 1:]
    print(response.content.decode(charset))
    return response.content

def search_content(url, content):
    pass


if __name__ == "__main__":
    print(newspaper.languages())
    url = "http://47.109.84.142:8001"
    article = Article(url, language="zh")
    article.download()
    article.parse()
    print(article.authors)
    print(article.publish_date)
    article.nlp()
    print(article.keywords)
    print(article.text)
    print(article.summary)
    print(article.html)
    # get_raw_content("")