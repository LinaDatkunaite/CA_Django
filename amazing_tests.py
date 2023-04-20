import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from library.models import Book

b = Book.objects.all()
for book in b:
    print(book.title)

b = Book.objects.filter(book_id=1).values()
print(b)