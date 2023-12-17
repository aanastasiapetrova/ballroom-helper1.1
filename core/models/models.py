from sqlalchemy import MetaData, Table, BigInteger, Integer, Boolean, Column, Date, ForeignKey, String

metadata = MetaData()

persons = Table(
    'persons',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('first_name', String(255), nullable=False),
    Column('second_name', String(255)),
    Column('last_name', String(255), nullable=False),
    Column('birth_date', Date()),
    Column('gender', Boolean()),
    Column('is_active', Boolean()),
    Column('club_id', ForeignKey("clubs.id"))
)

clubs = Table(
    'clubs',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('name', String(255)),
    Column('city', String(255)),
    Column('region', Integer()),
    Column('director_id', BigInteger())
)
