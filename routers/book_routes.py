from fastapi import APIRouter, HTTPException, status
from database.book_db import BookDB, NewBook


router = APIRouter()

book = BookDB()

@router.get("/books")
def get_all_books():
    try:
        return book.get_all_books()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))
    

@router.post("/books")
def new_book(new_book: NewBook):
    pass


@router.get("/books/{id}")
def get_book_by_id(id: int):
    pass


@router.put("/books/{id}")
def update_book_info(id: int, data):
    pass


@router.put("/books/{id}/borrow/{member_id}")
def member_borrow_book(id: int, member_id: int):
    pass


@router.put("/books/{id}/return/{member_id}")
def member_return_book(id: int, member_id: int):
    pass