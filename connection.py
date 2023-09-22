import json
from datetime import datetime
from mongoengine import connect
import configparser

from models import Author, Quote

config = configparser.ConfigParser()
config.read("config.ini")

user_name = config.get("DB", "user")
mongo_pass = config.get("DB", "pass")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")

connect(host=f"mongodb+srv://{user_name}:{mongo_pass}@{db_name}.zfeboae.mongodb.net/?retryWrites=true&w=majority")


with open('authors.json', 'r', encoding='utf-8') as file:
    authors_data = json.load(file)

# Завантаження авторів в базу даних
for author_data in authors_data:
    author = Author.objects(fullname=author_data['fullname']).first()
    if not author:
        author = Author(
            fullname=author_data['fullname'],
            born_date=author_data.get('born_date'),
            born_location=author_data.get('born_location'),
            description=author_data.get('description')
        )
        author.save()

# Завантаження даних з quotes.json
with open('quotes.json', 'r', encoding='utf-8') as file:
    quotes_data = json.load(file)

# Завантаження цитат в базу даних та зв'язок їх з авторами за полем "fullname"
for quote_data in quotes_data:
    author_name = quote_data['author']
    author = Author.objects(fullname=author_name).first()
    if author:
        quote = Quote(
            tags=quote_data['tags'],
            author=author,
            quote=quote_data['quote']
        )
        quote.save()

