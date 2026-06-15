from fastapi import APIRouter, HTTPException, status
from database.book_db import BookDB, NewBook, UpdateBook
from database.member_db import MemberDB
from logger import get_logger

router = APIRouter()

book = BookDB()
member = MemberDB()


logger = get_logger()


@router.get("/books")
def get_all_books():
    try:
        logger.info("Get all books")
        return book.get_all_books()
    except Exception as e:
        logger.error("Failed to get all members.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))
    

@router.post("/books", 
             status_code=status.HTTP_201_CREATED)
def new_book(new_book: NewBook):
    try:
        book.create_book(new_book)
        logger.info("Created new book.")
    except Exception as e:
        logger.error("Failed to create new book.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )    


@router.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    try:
        data = book.get_book_by_id(book_id)
        if not data:
            logger.error("book does not exist.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="ID does not exist"
            )
        logger.info("Get book by ID.")
        return data
    except Exception as e:
        logger.error(f"Failed to get book by ID, {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )    


@router.put("/books/{book_id}")
def update_book_info(book_id: int, data: UpdateBook):
    update_book = data.model_dump(exclude_unset=True)
    if not update_book:
        logger.error("Failed to update book info, not data has given.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty information")
    try:
        book.update_book_info(book_id, update_book)
        logger.info("Book info updated.")
    except Exception as e:
        logger.error(f"Failed to update book info, {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))



@router.put("/books/{book_id}/borrow/{member_id}")
def member_borrow_book(book_id: int, member_id: int):
    try:
        current_book = book.get_book_by_id(book_id)
        current_member = member.get_member_by_id(member_id)
        member_amount_borrow_books = book.count_active_borrows_by_member(member_id)
        if not current_book:
            logger.error("Failed to borrow, book does not exist.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="book not found")
        
        if current_book["is_available"] == False:
            logger.error("Failed to borrow, book does not available.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="book is not available")
        
        if current_member is None:
            logger.error("Failed to borrow, member does not exist.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="member not found"
            )
        
        if current_member["is_active"] == False:
            logger.error("Failed to borrow, member is not active.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member is not active"
            )
        
        if member_amount_borrow_books["member"] >= 3:
            logger.error("Failed to borrow, member has, member has reached maximum borrows.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member has reached maximum borrows"
            )

        book.set_available(book_id,False, member_id)
        member.increment_borrows(member_id)
        book.update_book_info(book_id, {"borrowed_by_member_id": member_id})
        logger.info(f"Member {member_id} borrow book {book_id}")
    except HTTPException as e:
        raise

    except Exception as e:
        logger.error(f"Failed to borrow book, {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e))
    


@router.put("/books/{book_id}/return/{member_id}")
def member_return_book(book_id: int, member_id: int):
    try:
        current_book = book.get_book_by_id(book_id)
        current_member = member.get_member_by_id(member_id)
        if not current_book:
            logger.error("Failed to return book, book does not exist.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="book not found")
        
        if current_book["is_available"] == True:
            logger.error("Failed to return book, book is not borrowed.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is not borrowed")
        
        if current_member is None:
            logger.error("Failed to return book, member does not exist.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="member not found"
            )
        
        if current_member["is_active"] == False:
            logger.error("Failed to return book, member is not active.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member is not active"
            )
        if current_book["borrowed_by_member_id"] != member_id:
            logger.error("Failed to return book, book is not borrowed by this member.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is not borrowed by this member"
            )
        
        book.set_available(book_id,True, member_id)
        book.update_book_info(book_id, {"is_available": True, "borrowed_by_member_id": None})
        logger.info(f"member {member_id} return book {book_id}")
    except HTTPException as e:
        raise
    
    except Exception as e:
        logger.error(f"Failed to return book, {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e))
    