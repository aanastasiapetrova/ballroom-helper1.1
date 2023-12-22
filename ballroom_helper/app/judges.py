from tkinter import *
from tkinter import ttk

from ttkwidgets import CheckboxTreeview

from ballroom_helper.core.db.session import get_session
from ballroom_helper.core.models.tables import (Club, Competition,
                                                CompetitionJudge, Group, Judge,
                                                Person, Shedule, SheduleJudge, GroupParticipant, Participant)
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

class JudgeWindow:
    def __init__(self, master):
        self.master = master
        self._competition = 0
        self._part = 0
        self._registration_group = 0


    
    @staticmethod
    def get_competitions(repo):
        return repo.get_items().scalars().all()
    

    def create_competition_frame(self, master_frame, competition_repo):
        select_competition_frame = LabelFrame(master_frame, text="Cоревнование")

        competitions = JudgeWindow.get_competitions(competition_repo)

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
    

    def create_registration_frame(self, master_frame):
        common_frame = Frame(master_frame)
        registration_frame = LabelFrame(common_frame, text="Регистрация")
        judges_frame = LabelFrame(common_frame, text="Участники")

        self.create_groups_frame(registration_frame)
        self.create_judges_frame(judges_frame)

        registration_frame.pack(side=LEFT, fill=X, padx=10, pady=10)
        judges_frame.pack(side=LEFT, fill=X, padx=10, pady=10)
        common_frame.pack(anchor=CENTER)

    
    def create_judges_frame(self, master_frame):
        registration_participants_frame = Frame(master_frame)

        self.get_judges()

        registration_label = Label(registration_participants_frame, text="НАЗНАЧИТЬ НА СУДЕЙСТВО")

        name_input_frame = Frame(registration_participants_frame)
        name_label = Label(name_input_frame, text="Введите фамилию и имя судьи: ")
        self.name_entry = ttk.Entry(name_input_frame)
        name_button = ttk.Button(
            name_input_frame,
            text="OK",
            #command=self.search_athletes
            )
        reset_button = ttk.Button(
            name_input_frame,
            text="Сбросить",
            #command=self.reset_athletes
            )
        
        judges_frame = Frame(registration_participants_frame)
        columns = ("id", "name", "fdsarr_judgment_category", "club")
        self.judges_table = CheckboxTreeview(judges_frame, columns=columns)

        self.judges_table.heading("id", text="ID")
        self.judges_table.heading("name", text="Имя судьи")
        self.judges_table.heading("fdsarr_judgment_category", text="ФТСАРР")
        # self.judges_table.heading("sport_judgment_category", text="Спортивная")
        self.judges_table.heading("club", text="Клуб")

        self.judges_table.column("id", width=50, anchor=CENTER)
        self.judges_table.column("name", width=180, anchor=CENTER)
        self.judges_table.column("fdsarr_judgment_category", width=100, anchor=CENTER)
        # self.judges_table.column("sport_judgment_category", width=120, anchor=CENTER)
        self.judges_table.column("club", width=180, anchor=CENTER)

        # self.athletes_table.bind("<<TreeviewSelect>>", self.select_athlete_to_register)

        self.judges_table.delete(*self.judges_table.get_children())
        for judge in self.judges_list:
            self.judges_table.insert("", END, values=judge)

        registration_label.pack()

        name_input_frame.pack(side=TOP)
        name_label.pack(side=LEFT, padx=10, pady=10)
        self.name_entry.pack(side=LEFT, padx=10, pady=10)
        name_button.pack(side=LEFT, padx=10, pady=10)
        reset_button.pack(side=LEFT, padx=10, pady=10)

        self.judges_table.pack(side=LEFT, fill=Y)
        judges_frame.pack(side=BOTTOM, fill=Y, padx=10, pady=10)

        registration_participants_frame.pack(side=LEFT, fill=X, padx=10, pady=10)

        return registration_participants_frame


    def get_judges(self):
        session = next(get_session())
        judges_query = session.query(Judge.id, Person.first_name, Person.last_name, Judge.fdsarr_judgement_category, Club.name, Club.city)
        judges_data = self.person_repo.inner_join(judges_query, [Judge, Club])

        self.judges_list = [[data.id, f"{data.first_name} {data.last_name}", data.fdsarr_judgement_category, f'"{data.name}", г. {data.city}'] for data in judges_data.all()]

    
    def get_selected_competition_judges(self):
        self.judges_table.delete(*self.judges_table.get_children())

        this_competition_judges = self.competition_judges_repo.filter_items({"competition_id": self._competition})
        this_competition_judges_ids = [comp_judge.judge_id for comp_judge in this_competition_judges]

        self.judges_list = [judge for judge in self.judges_list if judge[0] in this_competition_judges_ids]

        for judge in self.judges_list:
            self.judges_table.insert("", END, values=judge)

    
    def create_groups_frame(self, master_frame):
        registration_group_frame = Frame(master_frame)
        groups = self.group_repo.filter_items({"competition_id": self._competition})

        part_frame = Frame(registration_group_frame)
        part_groups_label = Label(registration_group_frame, text="ГРУППЫ ОТДЕЛЕНИЯ")
        part_label = Label(part_frame, text="Введите отделение: ")
        self.part_combobox = ttk.Combobox(
            part_frame)
        part_button = ttk.Button(
            part_frame,
            text="OK",
            command=self.get_groups
        )
    

        columns = ("id", "name", "participants_amount", "dances", "part")
        groups_frame = Frame(registration_group_frame)

        self.groups_list_table = ttk.Treeview(groups_frame, columns=columns, show="headings")

        self.groups_list_table.heading("id", text="Номер группы")
        self.groups_list_table.heading("name", text="Название группы")
        self.groups_list_table.heading("participants_amount", text="Участников")
        self.groups_list_table.heading("dances", text="Программа")
        self.groups_list_table.heading("part", text="Отделение")

        self.groups_list_table.column("id", width=50, anchor=CENTER)
        self.groups_list_table.column("name", width=310, anchor=CENTER)
        self.groups_list_table.column("participants_amount", width=80, anchor=CENTER)
        self.groups_list_table.column("dances", width=200, anchor=CENTER)
        self.groups_list_table.column("part", width=80, anchor=CENTER)

        self.groups_list_table.bind("<<TreeviewSelect>>", self.select_registration_group)

        part_groups_label.pack()
        part_frame.pack(side=TOP, padx=10, pady=10)
        part_label.pack(side=LEFT, padx=10, pady=10)
        self.part_combobox.pack(side=LEFT, fill=X, padx=10, pady=10)
        part_button.pack(side=LEFT, padx=10, pady=10)
        self.groups_list_table.pack(side=LEFT, fill=Y)
        groups_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10)
        registration_group_frame.pack(side=LEFT)

        return registration_group_frame
    

    def create_registered_judges_frame(self, master_frame):
        reg_list_frame = LabelFrame(master_frame, text="Список назначенных судей")

        selected_group_frame = Frame(reg_list_frame)
        selected_group_label = ttk.Label(selected_group_frame, text="Выбранная группа: ")
        self.selected_group_value_label = ttk.Label(selected_group_frame)


        button_frame = Frame(reg_list_frame)
        registration_button = ttk.Button(
            button_frame,
            text="Зарегистрировать",
            command=self.register
        )
        cancel_registration_button = ttk.Button(
            button_frame,
            text="Снять",
            command=self.cancel_register
        )

        registration_list_frame = Frame(reg_list_frame)
        columns = ("group_id", "judge_id", "judge_name", "fdsarr_judgement_category", "judge_club")
        self.registration_list_table = ttk.Treeview(registration_list_frame, columns=columns, show="headings")
        
        self.registration_list_table.heading("group_id", text="Номер группы")
        self.registration_list_table.heading("judge_id", text="ID судьи")
        self.registration_list_table.heading("judge_name", text="Имя судьи")
        self.registration_list_table.heading("fdsarr_judgement_category", text="Категория ФТСАРР")
        self.registration_list_table.heading("judge_club", text="Клуб судьи")

        self.registration_list_table.column("group_id", anchor=CENTER)
        self.registration_list_table.column("judge_id", anchor=CENTER)
        self.registration_list_table.column("judge_name", anchor=CENTER)
        self.registration_list_table.column("fdsarr_judgement_category", anchor=CENTER)
        self.registration_list_table.column("judge_club", anchor=CENTER)

        # self.registration_list_table.bind("<<TreeviewSelect>>", self.get_data_for_number)

        form_collegue_button = ttk.Button(
            button_frame,
            text="Коллегия",
            command=self.form_collegue
        )
        
        selected_group_label.pack(side=LEFT)
        self.selected_group_value_label.pack(side=LEFT)
        selected_group_frame.pack(fill=BOTH, padx=10)

        registration_button.pack(side=LEFT)
        cancel_registration_button.pack(side=LEFT)
        form_collegue_button.pack(side=LEFT)
        button_frame.pack(pady=5)

        self.registration_list_table.pack(anchor=W, fill=BOTH)
        registration_list_frame.pack(anchor=CENTER, fill=BOTH, padx=10)

        reg_list_frame.pack(anchor=CENTER, fill=BOTH, padx=10, pady=10)

    
    def form_collegue(self):
        registered = self.shedule_judge_repo.filter_items({"competition_id": self._competition, "group_id": self._registration_group})
        result_list = []
        it = 0

        for item in registered:
            it += 1
            for judge in self.registered_judges_data:
                if item.judge_id == judge[1]:
                    result_list.append([it, item.judge_abbreviation, *judge[2:]])
        
        participants = self.group_paricipants_repo.filter_items({"group_id": self._registration_group})
        participants_ids = [part.partcipant_id for part in participants]

        session = next(get_session())
        query = session.query(Participant).filter(Participant.id.in_(participants_ids)).all()
        numbers_list = [item.start_number for item in query]

        dances_list = (self.group_repo.get_item(self._registration_group).dances).split(', ')
        
        get_collegue_list(
            1,
            result_list,
            self.selected_competition_combobox.get().split(" - ")[1],
            self.selected_group_value_label["text"],
            self._registration_group
        )
        
        for judge in result_list:
            get_marks_list(
                1,
                numbers_list,
                dances_list,
                self.selected_competition_combobox.get().split(" - ")[1],
                self.selected_group_value_label["text"],
                [judge[2], judge[1]],
                self._registration_group
            )


    def register(self):
        judges_to_register = []
        for check in self.judges_table.get_checked():
            item = self.judges_table.item(check)["values"]
            judges_to_register.append(SheduleJudge(competition_id=self._competition, group_id=self._registration_group, judge_id=item[0]))
        for item in judges_to_register:
            self.shedule_judge_repo.add_item(item)
        self.get_registred_judges()


    def cancel_register(self):
        judges_to_cancel_register = []
        for check in self.judges_table.get_checked():
            item = self.judges_table.item(check)["values"]
            shedule_judge_item = self.shedule_judge_repo.filter_items({"group_id": self._registration_group, "competition_id": self._competition, "judge_id": item[0]})
            if shedule_judge_item:
                judges_to_cancel_register.extend(shedule_judge_item)
        for item_ in judges_to_cancel_register:
            self.shedule_judge_repo.delete_item(item_.id)
        self.get_registred_judges()

    

    def select_registration_group(self, event):
        self.get_registred_judges()
    


    def get_registred_judges(self):
        self.registration_list_table.delete(*self.registration_list_table.get_children())

        for selection in self.groups_list_table.selection():
            item = self.groups_list_table.item(selection)
            self._registration_group = item["values"][0]
            self.selected_group_value_label["text"] = item["values"][1]

        shedule_judge_objects = self.shedule_judge_repo.filter_items({"group_id": self._registration_group})
        judges_ids = [id_.judge_id for id_ in shedule_judge_objects]

        self.registered_judges_data = [[self._registration_group, *judge] for judge in self.judges_list if judge[0] in judges_ids]

        for judge in self.registered_judges_data:
            self.registration_list_table.insert("", END, values=judge)

    
    def get_groups(self):
        self._part = int(self.part_combobox.get())

        groups = self.group_repo.filter_items({"competition_id": self._competition, "competition_part_number": self._part})
        groups_list = [
            (item.id, f"{item.name} ({item.program})", item.participants_amount, item.dances, item.competition_part_number) for item in groups
            ]

        self.groups_list_table.delete(*self.groups_list_table.get_children())
        for group in groups_list:
            self.groups_list_table.insert("", END, values=group)
    

    def select_competition(self):
        self._competition = self.selected_competition_combobox.get().split(" - ")[0]

        groups = self.group_repo.filter_items({"competition_id": self._competition})
        
        selected_competition = self.competition_repo.get_item(self._competition)
        if selected_competition.status != "active":
            self.competition_repo.update_item(self._competition, {"status": "active"})

        self.get_selected_competition_judges()

        self.part_combobox["values"] = list(set([group.competition_part_number for group in groups]))
    


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

        judges = ttk.Frame(self.master)

        self.create_competition_frame(judges, self.competition_repo)

        self.create_registration_frame(judges)

        self.create_registered_judges_frame(judges)

        return judges