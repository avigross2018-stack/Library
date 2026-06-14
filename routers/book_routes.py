from fastapi import APIRouter, HTTPException, status
from database.book_db import BookDB, NewBook, UpdateBook
from database.member_db import MemberDB


router = APIRouter()

book = BookDB()
member = MemberDB()

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
        current_book = book.get_book_by_id(book_id)
        current_member = member.get_member_by_id(member_id)
        member_amount_borrow_books = book.count_active_borrows_by_member(member_id)
        if not current_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="book not found")
        
        if current_book["is_available"] == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="book is not available")
        
        if current_member is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="member not found"
            )
        
        if current_member["is_active"] == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member is not active"
            )
        
        if member_amount_borrow_books["member"] >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member has reached maximum borrows"
            )

        book.set_available(book_id,False, member_id)
        member.increment_borrows(member_id)
        book.update_book_info(book_id, {"borrowed_by_member_id": member_id})
    except HTTPException as e:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e))
    


@router.put("/books/{book_id}/return/{member_id}")
def member_return_book(book_id: int, member_id: int):
    try:
        current_book = book.get_book_by_id(book_id)
        current_member = member.get_member_by_id(member_id)
        if not current_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="book not found")
        
        if current_book["is_available"] == True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is not borrowed")
        
        if current_member is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="member not found"
            )
        
        if current_member["is_active"] == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member is not active"
            )
        if current_book["borrowed_by_member_id"] != member_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is not borrowed by this member"
            )
        
        book.set_available(book_id,True, member_id)
        book.update_book_info(book_id, {"is_available": True, "borrowed_by_member_id": None})
    except HTTPException as e:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e))
    