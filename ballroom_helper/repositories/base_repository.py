from sqlalchemy import select, insert, update, delete, func, Result
from sqlalchemy.orm import Session, Query

class BaseRepository:
    def __init__(self, model, session: Session):
        self.model = model
        self.session: Session = session

    
    def get_items(self):
        return self.session.execute(select(self.model))
    

    def order_by(self, query, field):
        return self.session.execute(query.order_by(field))
    

    def inner_join(self, query, join_models):
        for model in join_models:
            query = query.join(model)
        return self.session.execute(query)


    def get_item(self, id):
        result = self.session.get(self.model, id)
        return result
    

    def add_item(self, object):
        self.session.add(object)
        self.session.commit()
        return object
    

    def delete_item(self, id):
        item = self.session.query(self.model).filter(self.model.id == id).first()
        self.session.delete(item)
        self.session.commit()
    
    
    def filter_items(self, filter_data):
        query = select(self.model)
        for param, value in filter_data.items():
            column = getattr(self.model, param, None)
            if value is not None:
                query = query.filter(column == value)
        return self.session.execute(query.order_by(self.model.id)).scalars().all()
    

    def update_item(self, id, update_data):
        result = self.session.execute(update(self.model).where(self.model.id == id).values(**update_data).returning(self.model))
        self.session.commit()
        return result.scalar_one()