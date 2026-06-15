from fastapi import APIRouter, HTTPException, status
from database.book_db import BookDB, NewBook, UpdateBook
from database.member_db import MemberDB
from logger import get_logger

router = APIRouter()

book = BookDB()
member = MemberDB()
logger = get_logger()


@router.get("/reports/summary")
def total_summary_books():
    try:
        total_books =  book.count_total_books()
        available_books = book.count_available_books()
        borrowed_books = book.count_borrowed_books()
        logger.info("Show books summary.")
        return [total_books, available_books, borrowed_books]
    except Exception as e:
        logger.error("Failed to show books summary")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))


@router.get("/reports/books-by-genre")
def count_by_genre(genre: str):
    try:
        logger.info(f"Show count books by genre {genre}")
        return book.count_by_genre(genre)
    except Exception as e:
        logger.error(f"Failed to show count books by genre {genre}, {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))


@router.get("/reports/top-member")
def top_active_member():
    try:
        logger.info("Show top active member.")
        return member.get_top_member()
    except Exception as e:
        logger.error(f"Failed to show top active member, {str(e)}.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))