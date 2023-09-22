from time import sleep
from models import Author, Quote
from connection import connect
from connection import user_name, mongo_pass, db_name

connect(host=f"mongodb+srv://{user_name}:{mongo_pass}@{db_name}.zfeboae.mongodb.net/?retryWrites=true&w=majority")

while True:
    command = input("Введіть команду (наприклад, name: Steve Martin), для завершення програми введіть команду 'exit': ")

    if command == 'exit':
        break

    parts = command.split(':')
    if len(parts) != 2:
        print("Неправильний формат команди. Використовуйте name:, tag: або tags:")
        continue

    field, value = parts[0].strip(), parts[1].strip()
    results = []  # Створюємо список для зберігання результатів запитів

    if field == 'name':
        author = Author.objects(fullname=value).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                results.append(quote.quote)  # Додаємо результат до списку

        else:
            print(f"Автор {value} не знайдений")

    elif field == 'tag':
        quotes = Quote.objects(tags=value)
        for quote in quotes:
            results.append(quote.quote)  # Додаємо результат до списку

    elif field == 'tags':
        tags = value.split(',')
        quotes = Quote.objects(tags__in=tags)
        for quote in quotes:
            results.append(quote.quote)  # Додаємо результат до списку

    else:
        print("Непідтримувана команда. Використовуйте name:, tag: або tags:")
