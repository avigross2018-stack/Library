from fastapi import APIRouter, HTTPException, status
from database.member_db import MemberDB, NewMember, UpdateMember
from logger import get_logger

router = APIRouter()
member = MemberDB()
logger = get_logger()

@router.get("/members")
def get_all_members():
    try:
        logger.info("Get all members.")
        return member.get_all_members()
    except Exception as e:
        logger.error(f"Failed to show all members, {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))


@router.post("/members")
def new_member(new_member: NewMember):
    try:
        logger.info("Creating new member.")
        member.create_member(new_member)
    except Exception as e:
        logger.error(f"Failed to create new members, {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))
    

@router.get("/members/{member_id}")
def get_member_by_id(member_id: int):
    try:
        current_member = member.get_member_by_id(member_id)
        if not current_member:
            logger.info("Failed to show member by ID, member does not exist.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member does not exist"
            )
        logger.info("Show member by ID.")
        return current_member
    except Exception as e:
        logger.error(f"Failed to show member by ID., {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))


@router.put("/members/{member_id}")
def update_member(member_id:int, new_data: UpdateMember):
    try:
        data = new_data.model_dump(exclude_unset=True)
        if not data:
            logger.error("Member not updated, No info as given")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No info as given"
            )
        member.update_member(member_id, data)
        logger.info("Member updated.")
    except Exception as e:
        logger.error(f"Failed to update member, {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))


@router.put("/members/{member_id}/deactivate")
def deactivate_member(member_id:int):
    try:
        member.deactivate_member(member_id)
        logger.info("Deactivate member.")
    except Exception as e:
        logger.error(f"failed to deactivate member, {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))


@router.put("/members/{member_id}/activate")
def activate_member(member_id: int):
    try:
        member.activate_member(member_id)
        logger.info("Activate member.")
    except Exception as e:
        logger.error(f"failed to activate member, {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))
