from sqlalchemy import select, insert, update, delete, func, Result
from sqlalchemy.orm import Session, Query

class BaseRepository:
    def __init__(self, model, session: Session):
        self.model = model
        self.session: Session = session

    
    def get_items(self):
        return self.session.execute(select(self.model))