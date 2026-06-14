from fastapi import APIRouter, HTTPException, status
from database.book_db import BookDB, NewBook, UpdateBook


router = APIRouter()

book = BookDB()


@router.get("/reports/summary")
def total_books():
    try:
        total_books =  book.count_total_books()
        available_books = book.count_available_books()
        borrowed_books = book.count_borrowed_books()
        return [total_books[0], available_books[0], borrowed_books[0]]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))


@router.get("/reports/books-by-genre")
def count_by_genre(genre: str):
    try:
        return book.count_by_genre(genre)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))
