from database.db_connection import get_connection, create_tables
from pydantic import BaseModel


class MemberDB:
    def __init__(self):
        pass

    def create_member(self, data):
        pass


    def  get_all_members(self):
        pass


    def get_member_by_id(self, id):
        pass


    def update_member(self, id, data):
        pass


    def deactivate_member(self, id):
        pass


    def  activate_member(self, id):
        pass


    def increment_borrows(self, id):
        pass


    def count_active_members(self):
        pass


    def get_top_member(self):
        pass