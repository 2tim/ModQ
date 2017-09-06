import json
import newspaper
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


bb_paper = newspaper.build('http://www.bloomberg.com', memoize_articles=False)
reuters_paper = newspaper.build('http://www.reuters.com', memoize_articles=False)

articles = {}
try:
    with open("articles.json", 'r') as a:
        articles = json.load(a)
except FileNotFoundError as e:
    articles = {}

previous = set(articles.keys())
for article in bb_paper.articles + reuters_paper.articles:
    if article.url not in previous:
        try:
            article.download()
            article.parse()
            articles[article.url] = article.text
        except newspaper.article.ArticleException as e:
            print(e)
            print("Could not get article at: {}".format(article.url))
            articles[article.url] = article.text
json.dump(articles, open("articles.json", "w"))
client = language.LanguageServiceClient()
users = json.load(open("user.json", 'r'))

matched = {k.get("name"): list() for k in users.get("users", [])}

# The text to analyze
for url, t in articles.items():

    document = types.Document(
        content=t,
        type=enums.Document.Type.PLAIN_TEXT)

    entities = client.analyze_entities(document).entities

    for entity in entities:
        for user in users.get("users", []):
            for c in user.get("companies"):
                #TODO: decide if this is the proper match
                if c.lower() == entity.name.lower():
                    # print(user.get("name")+' is interested in '+c+' and might like '+url+" with salience "+str(entity.salience))
                    matched[user.get("name")].append((url, entity.salience))

# sorted_match = sorted(matched.items(), key=lambda x: x[1][1])
for k, v in matched.items():
    s_sorted = sorted(v, key=lambda x: x[1],reverse=True)
    print(k+" might like:\n"+"\n\t".join(map(str, s_sorted[:3])))
