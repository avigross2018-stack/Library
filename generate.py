import json
from database.book_db import BookDB, NewBook
from database.member_db import MemberDB, NewMember

def gen_books():
    with open("books.json", "r") as f:
        data = json.load(f)

    book = BookDB()
    for d in data:
        new = NewBook(**d)
        book.create_book(new)



def gen_members():
    with open("members.json", "r") as f:
        data = json.load(f)

    member = MemberDB()
    for d in data:
        new = NewMember(**d)
        member.create_member(new)


gen_books()