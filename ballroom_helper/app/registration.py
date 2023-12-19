from tkinter import *
from tkinter import ttk

from ballroom_helper.repositories.competition_repository import CompetitionRepository
from ballroom_helper.repositories.group_repository import GroupRepository
from ballroom_helper.core.models.tables import Competition, Group
from ballroom_helper.core.db.session import get_session

class RegistrationWindow:
    def __init__(self, master):
        self.master = master
        self._competition = None

    
    @staticmethod
    def get_competitions(repo):
        return repo.get_items().scalars().all()
    

    def create_competition_frame(self, master_frame, competition_repo):
        select_competition_frame = LabelFrame(master_frame, text="Cоревнование")

        competitions = RegistrationWindow.get_competitions(competition_repo)

        select_competition_label = ttk.Label(select_competition_frame, text="Выберите соревнование: ")
        select_competition_label.pack(side=LEFT, padx=10, pady=10)

        self.selected_competition_combobox = ttk.Combobox(
            select_competition_frame,
            values=[f'{comp.id} - {comp.name} г. {comp.city}' for comp in competitions],
            state="readonly",
            width=50
            )
        self.selected_competition_combobox.pack(side=LEFT, padx=10, pady=10)
        	
        self.selected_competition_combobox.current(0)

        submit_competition_selection_button = ttk.Button(
            select_competition_frame,
            text="OK",
            command=self.select_competition
            )
        submit_competition_selection_button.pack(side=LEFT, padx=10, pady=10)

        select_competition_frame.pack(anchor=NW, fill=X, padx=10, pady=10)

        return select_competition_frame
    

    def create_registration_frame(self, master_frame):
        registration_frame = Frame(master_frame)
        participants_frame = LabelFrame(registration_frame, text="Участники")

        self.create_groups_frame(registration_frame)

        part_label = ttk.Label(participants_frame, text="Label")
        part_label.pack()

        participants_frame.pack(side=LEFT, fill=X, padx=10, pady=10)
        registration_frame.pack(fill=X)

        return registration_frame
    

    def create_groups_frame(self, master_frame):
        columns = ("id", "name", "participants_amount")
        groups_frame = LabelFrame(master_frame, text="Группы соревнования")
        groups_list = [
            (item.id, f"{item.name} {item.age_group}", item.participants_amount) for item in self.group_repo.get_items().scalars().all()
            ]
    

        groups_list_table = ttk.Treeview(master_frame, columns=columns, show="headings")
        groups_list_table.pack(side=LEFT, fill=Y, padx=10, pady=10)

        groups_list_table.heading("id", text="Номер группы")
        groups_list_table.heading("name", text="Название группы")
        groups_list_table.heading("participants_amount", text="Участников")

        for group in groups_list:
            groups_list_table.insert("", END, values=group)

        groups_frame.pack(side=LEFT, fill=X)

        return groups_frame
    
    
    def select_competition(self):
        self._competition = self.selected_competition_combobox.get().split(" - ")[0]
        selected_competition = self.competition_repo.get_item(self._competition)
        if selected_competition.status != "active":
            self.competition_repo.update_item(self._competition, {"status": "active"})
            print(selected_competition.name)
    

    def initialize(self):
        self.competition_repo = CompetitionRepository(Competition, next(get_session()))
        self.group_repo = GroupRepository(Group, next(get_session()))

        main = ttk.Frame(self.master)

        competition_frame = self.create_competition_frame(main, self.competition_repo)

        groups_frame = self.create_registration_frame(main)

        return main