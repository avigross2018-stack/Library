from fastapi import APIRouter, HTTPException, status
from database.book_db import BookDB, NewBook, UpdateBook


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
    

@router.post("/books", 
             status_code=status.HTTP_201_CREATED)
def new_book(new_book: NewBook):
    try:
        book.create_book(new_book)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )    


@router.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    try:
        book.get_book_by_id(book_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )    


@router.put("/books/{book_id}")
def update_book_info(book_id: int, data: UpdateBook):
    update_book = data.model_dump(exclude_unset=True)
    if not update_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty information")
    try:
        book.update_book_info(book_id, update_book)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e))



@router.put("/books/{book_id}/borrow/{member_id}")
def member_borrow_book(book_id: int, member_id: int):
    try:
        book.set_available(book_id,False, member_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e))
    


@router.put("/books/{book_id}/return/{member_id}")
def member_return_book(book_id: int, member_id: int):
    try:
        book.set_available(book_id,True, member_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e))
    