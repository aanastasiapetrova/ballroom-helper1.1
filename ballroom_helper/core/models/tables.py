from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime,
                        ForeignKey, Integer, MetaData, String, Table, Numeric)
from sqlalchemy.orm import registry

metadata = MetaData()

mapper_registry = registry()

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
    Column('club_id', ForeignKey('clubs.id'))
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

athletes = Table(
    'athletes',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('class_st', String(1), nullable=False),
    Column('class_lat', String(1), nullable=False),
    Column('assignment_class_st_date', Date()),
    Column('assignment_class_lat_date', Date()),
    Column('st_base_scores', Integer()),
    Column('st_qualification_scores', Integer()),
    Column('lat_base_scores', Integer()),
    Column('lat_qualification_scores', Integer()),
    Column('qualification_book_id', BigInteger()),
    Column('insurance_id', BigInteger()),
    Column('rusada_certificate_id', BigInteger()),
    Column('sport_category', String(100)),
    Column('assignment_sport_category_date', Date()),
    Column('sport_category_status', Boolean()),
    Column('person_id', ForeignKey('persons.id'))
)

judges = Table(
    'judges',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('has_disciplinary_action', Boolean()),
    Column('fdsarr_judgement_category',String(100)),
    Column('assignment_fdsarr_category_date', Date()),
    Column('sport_judgement_category', String(100)),
    Column('assignment_sport_category_date', Date()),
    Column('sport_judgement_category_status', Boolean()),
    Column('person_id', ForeignKey('persons.id'))
)

coaches = Table(
    'coaches',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('assignment_coach_status_date', Date()),
    Column('person_id', ForeignKey('persons.id'))
)

couples = Table(
    'couples',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('female_id', BigInteger()),
    Column('male_id', ForeignKey('athletes.id'))
)

athlet_coach = Table(
    'athlet_coach',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('athlet_id', ForeignKey('athletes.id'), nullable=False),
    Column('coach_id', ForeignKey('coaches.id'), nullable=False)
)

competitions = Table(
    'competitions',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('organizer', String(255), nullable=False),
    Column('status', String(255)),
    Column('city', String(255)),
    Column('region', Integer()),
    Column('address', String(255)),
    Column('start_date', Date()),
    Column('end_date', Date())
)

groups = Table(
    'groups',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('age_group', String(255), nullable=False),
    Column('program', String(255), nullable=False),
    Column('dances', String(255)),
    Column('participants_amount', Integer()),
    Column('participants_limit', Integer()),
    Column('competition_part_number', Integer()),
    Column('min_age', Integer()),
    Column('max_age', Integer()),
    Column('min_class', String(1)),
    Column('max_class', String(1)),
    Column('competition_id', ForeignKey('competitions.id'), nullable=False)
)

competition_judge = Table(
    'competition_judge',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('competition_id', ForeignKey('competitions.id'), nullable=False),
    Column('judge_id', ForeignKey('judges.id'), nullable=False),
    Column('role', String(255))
)

shedules = Table(
    'shedules',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('group_start', DateTime()),
    Column('group_finish', DateTime()),
    Column('floor', String(1)),
    Column('round', String(10)),
    Column('full_amount', Integer()),
    Column('to_choose_amount', Integer()),
    Column('heats_amount', Integer()),
    Column('group_duration', Integer()),
    Column('competition_id', ForeignKey('competitions.id'), nullable=False),
    Column('group_id', ForeignKey('groups.id'), nullable=False)
)

shedule_judges = Table(
    'shedule_judges',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('judge_abbreviation', String(4)),
    Column('competition_id', ForeignKey('competitions.id'), nullable=False),
    Column('group_id', ForeignKey('groups.id'), nullable=False),
    Column('judge_id', ForeignKey('judges.id'), nullable=False),
)

participants = Table(
    'participants',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('start_number', BigInteger()),
    Column('competition_id', ForeignKey('competitions.id'), nullable=False),
    Column('athlete_id', ForeignKey('athletes.id'))
)

group_participant = Table(
    'group_participants',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('group_id', ForeignKey('groups.id'), nullable=False),
    Column('partcipant_id', ForeignKey('participants.id'))
)

marks = Table(
    'marks',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('dance', String(10)),
    Column('heat_number', Integer()),
    Column('participant_start_number', Integer()),
    Column('mark', Integer()),
    Column('judge_abbreviation', String(10)),
    Column('group_id', ForeignKey('groups.id'), nullable=False),
    Column('partcipant_id', ForeignKey('participants.id'), nullable=False),
)

attestation_results = Table(
    'attestation_results',
    metadata,
    Column('id', BigInteger(), nullable=False, unique=True, primary_key=True, autoincrement=True),
    Column('partcipant_id', ForeignKey('participants.id'), nullable=False),
    Column('group_id', ForeignKey('groups.id')),
    Column('average_score', Numeric())
)

class AttestationResult(object):
    pass


class AthletCoach(object):
    pass


class Athlete(object):
    pass


class Club(object):
    pass


class Coach(object):
    pass


class CompetitionJudge(object):
    pass


class Competition(object):
    pass


class GroupParticipant(object):
    pass


class Group(object):
    pass


class Judge(object):
    pass


class Mark(object):
    pass


class Participant(object):
    pass


class Person(object):
    pass


class SheduleJudge(object):
    pass


class Shedule(object):
    pass

# mapper(models.AthletCoach, athlet_coach)
# mapper(models.Athlete, athletes)
# mapper(models.Club, clubs)
# mapper(models.Coach, coaches)
# mapper(models.CompetitionJudge, competition_judge)
# mapper(models.Competition, competitions)
# mapper(models.Couple, couples)
# mapper(models.GroupParticipant, group_participant)
# mapper(models.Group, groups)
# mapper(models.Judge, judges)
# mapper(models.Mark, marks)
# mapper(models.Participant, participants)
# mapper(Person, persons)
# mapper(models.SheduleJudge, shedule_judges)
# mapper(models.Shedule, shedules)

mapper_registry.map_imperatively(AttestationResult, attestation_results)
mapper_registry.map_imperatively(AthletCoach, athlet_coach)
mapper_registry.map_imperatively(Athlete, athletes)
mapper_registry.map_imperatively(Club, clubs)
mapper_registry.map_imperatively(Coach, coaches)
mapper_registry.map_imperatively(CompetitionJudge, competition_judge)
mapper_registry.map_imperatively(Competition, competitions)
mapper_registry.map_imperatively(GroupParticipant, group_participant)
mapper_registry.map_imperatively(Judge, judges)
mapper_registry.map_imperatively(Group, groups)
mapper_registry.map_imperatively(Mark, marks)
mapper_registry.map_imperatively(Participant, participants)
mapper_registry.map_imperatively(Person, persons)
mapper_registry.map_imperatively(Shedule, shedules)
mapper_registry.map_imperatively(SheduleJudge, shedule_judges)