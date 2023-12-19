from core.db.session import get_session
from repositories.person_repository import PersonRepository
from core.models.tables import Person

repo = PersonRepository(Person, next(get_session()))
data = repo.get_items().scalars().all()

for iter in data:
    print(iter.first_name, iter.second_name, iter.last_name)