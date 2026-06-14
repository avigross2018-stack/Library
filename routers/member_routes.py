from fastapi import APIRouter, HTTPException, status
from database.member_db import MemberDB, NewMember, UpdateMember


router = APIRouter()
member = MemberDB()


@router.get("/members")
def get_all_members():
    try:
        return member.get_all_members()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))


@router.post("/members")
def new_member(new_member: NewMember):
    try:
        member.create_member(new_member)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))
    

@router.get("/members/{member_id}")
def get_member_by_id(member_id: int):
    try:
        current_member = member.get_member_by_id(member_id)
        if not current_member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member does not exist"
            )
        return current_member
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))


@router.put("/members/{member_id}")
def update_member(member_id:int, new_data: UpdateMember):
    try:
        data = new_data.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No info as given"
            )
        member.update_member(member_id, data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))


@router.put("/members/{member_id}/deactivate")
def deactivate_member(member_id:int):
    try:
        member.deactivate_member(member_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))


@router.put("/members/{member_id}/activate")
def activate_member(member_id: int):
    try:
        member.activate_member(member_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=str(e))
