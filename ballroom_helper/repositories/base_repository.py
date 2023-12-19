from sqlalchemy import select, insert, update, delete, func, Result
from sqlalchemy.orm import Session, Query

class BaseRepository:
    def __init__(self, model, session: Session):
        self.model = model
        self.session: Session = session

    
    def get_items(self):
        return self.session.execute(select(self.model))
    

    def get_item(self, id):
        result = self.session.get(self.model, id)
        return result
    

    def add_item(self, object):
        self.session.add(self.model(object))
        self.session.commit()
        return self.model(object)
    

    def update_item(self, id, update_data):
        result = self.session.execute(update(self.model).where(self.model.id == id).values(**update_data).returning(self.model))
        self.session.commit()
        return result.scalar_one()