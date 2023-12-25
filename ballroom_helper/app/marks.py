from tkinter import *
from tkinter import ttk

from ttkwidgets import CheckboxTreeview

from ballroom_helper.core.db.session import get_session
from ballroom_helper.core.models.tables import (Club, Competition,
                                                CompetitionJudge, Group, Judge,
                                                Person, Shedule, SheduleJudge, GroupParticipant, Participant, Mark, AttestationResult)
from ballroom_helper.repositories.competition_judge_repository import \
    CompetitionJudgeRepository
from ballroom_helper.repositories.competition_repository import \
    CompetitionRepository
from ballroom_helper.repositories.group_repository import GroupRepository
from ballroom_helper.repositories.judge_repository import JudgeRepository
from ballroom_helper.repositories.person_repository import PersonRepository
from ballroom_helper.repositories.shedule_judge_repository import \
    SheduleJudgeRepository
from ballroom_helper.repositories.shedule_repository import SheduleRepository
from ballroom_helper.reports.collegue import get_collegue_list
from ballroom_helper.reports.marks_blank import get_marks_list
from ballroom_helper.repositories.group_participant_repository import GroupParticipantRepository
from ballroom_helper.repositories.participant_repository import ParticipantRepository
from ballroom_helper.repositories.mark_repository import MarkRepository
from ballroom_helper.repositories.result_repository import ResultRepository


class MarksWindow:
    def __init__(self, master_frame):
        self.master = master_frame
        self._competition = 0
        self._dance = 0
        self._registration_group = 0
        self._participants = [[1, 1]]


    @staticmethod
    def get_competitions(repo):
        return repo.get_items().scalars().all()
    

    def create_competition_frame(self, master_frame, competition_repo):
        select_competition_frame = LabelFrame(master_frame, text="Cоревнование")

        competitions = MarksWindow.get_competitions(competition_repo)

        select_competition_label = ttk.Label(select_competition_frame, text="Выберите соревнование: ")
        select_competition_label.pack(side=LEFT, padx=10, pady=10)

        self.selected_competition_combobox = ttk.Combobox(
            select_competition_frame,
            values=[f'{comp.id} - {comp.name} г. {comp.city}' for comp in competitions],
            state="readonly",
            width=50
            )
        self.selected_competition_combobox.pack(side=LEFT, padx=10, pady=10)
        	
        submit_competition_selection_button = ttk.Button(
            select_competition_frame,
            text="OK",
            command=self.select_competition
            )
        submit_competition_selection_button.pack(side=LEFT, padx=10, pady=10)

        select_competition_frame.pack(anchor=NW, fill=X, padx=10, pady=10)

        return select_competition_frame
    

    def create_groups_frame(self, master_frame):
        select_group_frame = LabelFrame(master_frame, text="Группа")

        select_group_label = ttk.Label(select_group_frame, text="Выберите группу: ")
        select_group_label.pack(side=LEFT, padx=10, pady=10)

        self.selected_group_combobox = ttk.Combobox(
            select_group_frame,
            values=[],
            state="readonly",
            width=50
            )
        self.selected_group_combobox.pack(side=LEFT, padx=10, pady=10)

        submit_group_selection_button = ttk.Button(
            select_group_frame,
            text="OK",
            command=self.select_group
            )
        submit_group_selection_button.pack(side=LEFT, padx=10, pady=10)

        select_group_frame.pack(anchor=NW, fill=X, padx=10, pady=10)
    
    
    def create_dances_frame(self, master_frame):
        select_dance_frame = LabelFrame(master_frame, text="Танец")

        select_dance_label = ttk.Label(select_dance_frame, text="Выберите танец: ")
        select_dance_label.pack(side=LEFT, padx=10, pady=10)

        self.selected_dance_combobox = ttk.Combobox(
            select_dance_frame,
            values=[],
            state="readonly",
            width=50
            )
        self.selected_dance_combobox.pack(side=LEFT, padx=10, pady=10)

        submit_dance_selection_button = ttk.Button(
            select_dance_frame,
            text="OK",
            command=self.select_participants
            )
        submit_dance_selection_button.pack(side=LEFT, padx=10, pady=10)

        select_dance_frame.pack(anchor=NW, fill=X, padx=10, pady=10)

    
    def create_participant_frame(self, master_frame):
        select_part_frame = LabelFrame(master_frame, text="Участник")

        select_part_label = ttk.Label(select_part_frame, text="Выберите участника: ")
        select_part_label.pack(side=LEFT, padx=10, pady=10)

        self.selected_part_combobox = ttk.Combobox(
            select_part_frame,
            values=[],
            state="readonly",
            width=50
            )
        self.selected_part_combobox.pack(side=LEFT, padx=10, pady=10)

        submit_part_selection_button = ttk.Button(
            select_part_frame,
            text="OK",
            command=self.select_participant
            )
        submit_part_selection_button.pack(side=LEFT, padx=10, pady=10)

        select_part_frame.pack(anchor=NW, fill=X, padx=10, pady=10)
    

    def create_marks_frame(self, master_frame):
        marks_frame = LabelFrame(master_frame, text="Оценки")

        participant_frame = Frame(marks_frame)
        selected_participant_label = ttk.Label(participant_frame, text="Выбранный участник: ")
        selected_participant_label.pack(side=LEFT)
        self.selected_participant_value = ttk.Label(participant_frame)
        self.selected_participant_value.pack(side=LEFT)
        participant_frame.pack(anchor=NW, fill=X, padx=10, pady=10)

        dance_frame = Frame(marks_frame)
        selected_dance_label = ttk.Label(dance_frame, text="Выбранный танец: ")
        selected_dance_label.pack(side=LEFT)
        self.selected_dance_value = ttk.Label(dance_frame)
        self.selected_dance_value.pack(side=LEFT)
        dance_frame.pack(anchor=NW, fill=X, padx=10, pady=10)

        marks_values_frame = Frame(marks_frame)
        input_marks_label = ttk.Label(marks_values_frame, text="Введите оценки судей в порядке возрастания ID:")
        input_marks_label.pack(side=LEFT)
        self.input_marks_entry = ttk.Entry(marks_values_frame)
        self.input_marks_entry.pack(side=LEFT, padx=10)
        input_button = ttk.Button(
            marks_values_frame,
            text="OK",
            command=self.add_dance_marks
        )
        result_button = ttk.Button(
            marks_values_frame,
            text="Результат",
            command=self.get_result
        )
        input_button.pack(side=LEFT, padx=10)
        result_button.pack(side=LEFT, padx=10)
        marks_values_frame.pack(anchor=NW, fill=X, padx=10, pady=10)

        marks_frame.pack(anchor=NW, fill=X, padx=10, pady=10)


    def add_dance_marks(self):
        abbr = ['A(1)', 'B(2)', 'C(3)', 'D(4)', 'E(5)']
        marks = self.input_marks_entry.get().split()
        part_start_number = self.selected_participant_value["text"]
        part_id = self.participant_repo.filter_items({"competition_id": self._competition, "start_number": part_start_number})[0].id
        dance = self.selected_dance_value["text"]

        marks_list = []

        for i in range(len(abbr)):
            print(i)
            marks_list.append(Mark(
                dance=dance,
                participant_start_number=part_start_number,
                mark=marks[i],
                group_id=self._registration_group,
                partcipant_id=part_id,
                judge_abbreviation=abbr[i]))
        
        self.mark_repo.add_items(marks_list)
    
    
    def get_result(self):
        part_start_number = self.selected_participant_value["text"]
        part_id = self.participant_repo.filter_items({"competition_id": self._competition, "start_number": part_start_number})[0].id
        participant_marks = self.mark_repo.filter_items({
            "group_id": self._registration_group,
            "participant_start_number": part_start_number,
            "partcipant_id": part_id})
        sum_ = 0
        for mark in participant_marks:
            sum_ += mark.mark
        result = AttestationResult(
            partcipant_id=part_id,
            average_score=sum_/len(participant_marks),
            group_id=self._registration_group
        )
        self.resilt_repo.add_item(result)



    def select_competition(self):
        self._competition = self.selected_competition_combobox.get().split(" - ")[0]
        groups = self.group_repo.filter_items({"competition_id": self._competition})
        self.selected_group_combobox["values"] = [f"{group.id} - {group.name}" for group in groups]

    
    def select_group(self):
        self._registration_group = self.selected_group_combobox.get().split(" - ")[0]
        dances = self.group_repo.get_item(self._registration_group).dances.split(", ")
        self.selected_dance_combobox["values"] = dances

    
    def select_participants(self):
        participants = self.group_paricipants_repo.filter_items({"group_id": self._registration_group})
        participants_ids = [part.partcipant_id for part in participants]

        session = next(get_session())
        query = session.query(Participant).filter(Participant.id.in_(participants_ids)).all()
        self._participants = [[item.id, item.start_number] for item in query]
        print(self._participants)
        participants_nums = [item[1] for item in self._participants]
        print(participants_nums)
        self.selected_part_combobox["values"] = participants_nums
    
    
    def select_participant(self):
        self.selected_participant_value["text"] = self.selected_part_combobox.get()
        self.selected_dance_value["text"] = self.selected_dance_combobox.get()


    def initialize(self):
        self.competition_repo = CompetitionRepository(Competition, next(get_session()))
        self.group_repo = GroupRepository(Group, next(get_session()))
        self.person_repo = PersonRepository(Person, next(get_session()))
        self.judges_repo = JudgeRepository(Judge, next(get_session()))
        self.competition_judges_repo = CompetitionJudgeRepository(CompetitionJudge, next(get_session()))
        self.shedule_repo = SheduleRepository(Shedule, next(get_session()))
        self.shedule_judge_repo = SheduleJudgeRepository(SheduleJudge, next(get_session()))
        self.group_paricipants_repo = GroupParticipantRepository(GroupParticipant, next(get_session()))
        self.participant_repo = ParticipantRepository(Participant, next(get_session()))
        self.mark_repo = MarkRepository(Mark, next(get_session()))
        self.resilt_repo = ResultRepository(AttestationResult, next(get_session()))

        marks = ttk.Frame(self.master)

        self.create_competition_frame(marks, self.competition_repo)

        self.create_groups_frame(marks)

        self.create_dances_frame(marks)

        self.create_participant_frame(marks)

        self.create_marks_frame(marks)

        # self.create_registration_frame(judges)

        # self.create_registered_judges_frame(judges)

        return marks