from tkinter import *
from tkinter import ttk

from ballroom_helper.repositories.competition_repository import CompetitionRepository
from ballroom_helper.repositories.group_repository import GroupRepository
from ballroom_helper.repositories.group_participant_repository import GroupParticipantRepository
from ballroom_helper.repositories.athlete_repository import AthleteRepository
from ballroom_helper.repositories.person_repository import PersonRepository
from ballroom_helper.repositories.coach_repository import CoachRepository
from ballroom_helper.repositories.participant_repository import ParticipantRepository
from ballroom_helper.core.models.tables import Competition, Group, Athlete, Person, Club, Coach, AthletCoach, Participant, GroupParticipant
from ballroom_helper.core.db.session import get_session
from ballroom_helper.reports.registration_number import get_number
from ballroom_helper.reports.registration_convert import get_convert
from ballroom_helper.reports.registrations_list import get_group_list
from ballroom_helper.reports.group_participants_list import get_group_registration_list

class RegistrationWindow:
    def __init__(self, master):
        self.master = master
        self._competition = 0
        self._part = 0
        self._registration_group = 0
        self._participant = 0
        self._number = []

    
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
        participants_frame = LabelFrame(common_frame, text="Участники")

        self.create_groups_frame(registration_frame)
        self.create_participants_frame(participants_frame)

        registration_frame.pack(side=LEFT, fill=X, padx=10, pady=10)
        participants_frame.pack(side=LEFT, fill=X, padx=10, pady=10)
        common_frame.pack(anchor=CENTER)

    
    def create_participants_frame(self, master_frame):
        registration_participants_frame = Frame(master_frame)

        athletes_list = self.get_athletes()

        registration_label = Label(registration_participants_frame, text="ЗАРЕГИСТРИРОВАТЬ НА УЧАСТИЕ")

        name_input_frame = Frame(registration_participants_frame)
        name_label = Label(name_input_frame, text="Введите фамилию и имя учаcтника: ")
        self.name_entry = ttk.Entry(name_input_frame)
        name_button = ttk.Button(
            name_input_frame,
            text="OK",
            command=self.search_athletes
            )
        reset_button = ttk.Button(
            name_input_frame,
            text="Сбросить",
            command=self.reset_athletes
            )
        
        athletes_frame = Frame(registration_participants_frame)
        columns = ("id", "name", "club", "coach")
        self.athletes_table = ttk.Treeview(athletes_frame, columns=columns, show="headings")

        self.athletes_table.heading("id", text="ID")
        self.athletes_table.heading("name", text="Имя спортсмена")
        self.athletes_table.heading("club", text="Клуб")
        self.athletes_table.heading("coach", text="Тренер")

        self.athletes_table.column("id", width=50, anchor=CENTER)
        self.athletes_table.column("name", width=250, anchor=CENTER)
        self.athletes_table.column("club", width=160, anchor=CENTER)
        self.athletes_table.column("coach", width=240, anchor=CENTER)

        self.athletes_table.bind("<<TreeviewSelect>>", self.select_athlete_to_register)

        self.athletes_table.delete(*self.athletes_table.get_children())
        for athlete in athletes_list:
            self.athletes_table.insert("", END, values=athlete)

        registration_label.pack()

        name_input_frame.pack(side=TOP)
        name_label.pack(side=LEFT, padx=10, pady=10)
        self.name_entry.pack(side=LEFT, padx=10, pady=10)
        name_button.pack(side=LEFT, padx=10, pady=10)
        reset_button.pack(side=LEFT, padx=10, pady=10)

        self.athletes_table.pack(side=LEFT, fill=Y)
        athletes_frame.pack(side=BOTTOM, fill=Y, padx=10, pady=10)

        registration_participants_frame.pack(side=LEFT, fill=X, padx=10, pady=10)

        return registration_participants_frame
    

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
        list_button = ttk.Button(
            part_frame,
            text="Список",
            command=self.get_registration_list
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
        list_button.pack(side=LEFT, padx=10, pady=10)
        self.groups_list_table.pack(side=LEFT, fill=Y)
        groups_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10)
        registration_group_frame.pack(side=LEFT)

        return registration_group_frame
    

    def select_registration_group(self, event):
        self.registration_list_table.delete(*self.registration_list_table.get_children())

        for selection in self.groups_list_table.selection():
            item = self.groups_list_table.item(selection)
            self._registration_group = item["values"][0]
            self.selected_group_value_label["text"] = item["values"][1]

        group_participants = self.group_participant_repository.filter_items({"group_id": int(self._registration_group)})
        self.group_participants_list = [part.partcipant_id for part in group_participants]

        participants = self.participants_repo.get_items().scalars().all()
        participants_list = [[part.id, part.start_number, part.athlete_id] for part in participants]

        self.group_participants_list = [[self._registration_group, item[0], item[1], item[2]] for item in participants_list if item[0] in self.group_participants_list]
    
        for item in self.group_participants_list:
            for athlete in self.athletes_list:
                if item[2] == athlete[0]:
                    item[3] = athlete[1]
                    item.append(athlete[2])

        for part in self.group_participants_list:
            self.registration_list_table.insert("", END, values=part)

    
    def select_athlete_to_register(self, event):
        for selection in self.athletes_table.selection():
            item = self.athletes_table.item(selection)
            self._participant = item["values"][0]
            self.selected_participant_value_label["text"] = item["values"][1]
    

    def create_registration_list_frame(self, master_frame):
        reg_list_frame = LabelFrame(master_frame, text="Список регистрации")

        selected_group_frame = Frame(reg_list_frame)
        selected_group_label = ttk.Label(selected_group_frame, text="Выранная группа: ")
        self.selected_group_value_label = ttk.Label(selected_group_frame)

        selected_participant_frame = ttk.Frame(reg_list_frame)
        selected_participant_label = ttk.Label(selected_participant_frame, text="Выбранный участник: ")
        self.selected_participant_value_label = ttk.Label(selected_participant_frame)

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
        columns = ("group_id", "participant_id", "participant_number", "participant_name", "participant_club")
        self.registration_list_table = ttk.Treeview(registration_list_frame, columns=columns, show="headings")
        
        self.registration_list_table.heading("group_id", text="Номер группы")
        self.registration_list_table.heading("participant_id", text="ID участника")
        self.registration_list_table.heading("participant_number", text="Стартовый номер")
        self.registration_list_table.heading("participant_name", text="Имя участника")
        self.registration_list_table.heading("participant_club", text="Клуб участника")

        self.registration_list_table.column("group_id", anchor=CENTER)
        self.registration_list_table.column("participant_id", anchor=CENTER)
        self.registration_list_table.column("participant_number", anchor=CENTER)
        self.registration_list_table.column("participant_name", anchor=CENTER)
        self.registration_list_table.column("participant_club", anchor=CENTER)

        self.registration_list_table.bind("<<TreeviewSelect>>", self.get_data_for_number)

        form_number_button = ttk.Button(
            button_frame,
            text="Номер",
            command=self.form_number
        )
        
        selected_group_label.pack(side=LEFT)
        self.selected_group_value_label.pack(side=LEFT)
        selected_group_frame.pack(fill=BOTH, padx=10)

        selected_participant_label.pack(side=LEFT)
        self.selected_participant_value_label.pack(side=LEFT)
        selected_participant_frame.pack(fill=BOTH, padx=10, pady=5)

        registration_button.pack(side=LEFT)
        cancel_registration_button.pack(side=LEFT)
        form_number_button.pack(side=LEFT)
        button_frame.pack(pady=5)

        self.registration_list_table.pack(anchor=W, fill=BOTH)
        registration_list_frame.pack(anchor=CENTER, fill=BOTH, padx=10)

        reg_list_frame.pack(anchor=CENTER, fill=BOTH, padx=10, pady=10)

    
    def get_data_for_number(self, event):
        for selection in self.registration_list_table.selection():
            item = self.registration_list_table.item(selection)
            self._number = item["values"]
            print(self._number)


    def form_number(self):
        groups = self.group_participant_repository.filter_items({"partcipant_id": self._number[1]})
        groups_ids = [group.group_id for group in groups]
        group_names = []
        for group in groups_ids:
            group = self.group_repo.get_item(group)
            group_names.append([group.id, group.competition_part_number, group.name, group.dances])

        groups_for_number = ", ".join([group[2] for group in group_names])
        get_number(
            1,
            self._number[2],
            self._number[3],
            self._number[4],
            self.selected_competition_combobox.get().split(" - ")[1],
            groups_for_number,
            self._registration_group
            )
        
        get_convert(
            1,
            self._number[2],
            self._number[3],
            self._number[4],
            self.selected_competition_combobox.get().split(" - ")[1],
            self.selected_group_value_label["text"],
            self._registration_group
        )
            
        get_group_list(
            1,
            group_names,
            self.selected_competition_combobox.get().split(" - ")[1],
            self._number[3],
            self._number[1]
        )

    
    def get_registration_list(self):
        participants = self.registration_list_table.get_children()
        registration_list = []
        it = 0
        for part in participants:
            it += 1
            item = [it]
            item.extend(self.registration_list_table.item(part)["values"][2:])
            registration_list.append(item)
        
        print(registration_list)

        get_group_registration_list(
            1,
            registration_list,
            self.selected_competition_combobox.get().split(" - ")[1],
            self.selected_group_value_label["text"],
            self._registration_group
        )


    def register(self):
        register_participant = GroupParticipant(group_id=self._registration_group, partcipant_id=self._participant)
        added_participant = self.group_participant_repository.add_item(register_participant)
        register_group = self.group_repo.update_item(self._registration_group, {"participants_amount": len(self.group_participants_list)+1})
        self.get_groups()


    def cancel_register(self):
        participant_to_cancel = self.group_participant_repository.filter_items({"group_id": self._registration_group, "partcipant_id": self._participant})[0]
        self.group_participant_repository.delete_item(participant_to_cancel.id)
        register_group = self.group_repo.update_item(self._registration_group, {"participants_amount": len(self.group_participants_list)-1})
        self.get_groups()
        self.select_registration_group()


    def get_athletes(self):
        session = next(get_session())
        athletes_query = session.query(Athlete.id, Person.first_name, Person.last_name, Club.name, Club.city)
        athletes_data = self.person_repo.inner_join(athletes_query, [Athlete, Club])

        coaches_query = session.query(Coach.id, Person.first_name, Person.last_name, AthletCoach.athlet_id)
        coaches_data = self.coach_repo.inner_join(coaches_query, [Person, AthletCoach])
        coaches_list = list(coaches_data.all())

        self.athletes_list = [[data.id, f"{data.first_name} {data.last_name}", f'"{data.name}", г. {data.city}'] for data in athletes_data.all()]
        for athlete in self.athletes_list:
            for coach in coaches_list:
                if athlete[0] == coach[3]:
                    if len(athlete) == 3:
                        athlete.append([f"{coach[1]} {coach[2]}"])
                    else:
                        if f"{coach[1]} {coach[2]}" not in athlete[3]:
                            athlete[3].append(f"{coach[1]} {coach[2]}")
        for athlete in self.athletes_list:
            if len(athlete) == 4:
                athlete[3] = ", ".join(athlete[3])
        

        return self.athletes_list
    

    def search_athletes(self):
        self.athletes_table.delete(*self.athletes_table.get_children())
        name = self.name_entry.get()
        print(self.name_entry.get())

        filtered_data = [athlet for athlet in self.athletes_list if name in athlet[1]]
        print(filtered_data)

        for item in filtered_data:
            self.athletes_table.insert("", END, values=item)

    
    def reset_athletes(self):
        self.athletes_table.delete(*self.athletes_table.get_children())
        athletes = self.get_athletes()

        for item in athletes:
            self.athletes_table.insert("", END, values=item)
    

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

        self.part_combobox["values"] = list(set([group.competition_part_number for group in groups]))
    

    def initialize(self):
        self.competition_repo = CompetitionRepository(Competition, next(get_session()))
        self.group_participant_repository = GroupParticipantRepository(GroupParticipant, next(get_session()))
        self.group_repo = GroupRepository(Group, next(get_session()))
        self.athletes_repo = AthleteRepository(Athlete, next(get_session()))
        self.coach_repo = CoachRepository(Coach, next(get_session()))
        self.participants_repo = ParticipantRepository(Participant, next(get_session()))
        self.person_repo = PersonRepository(Person, next(get_session()))

        main = ttk.Frame(self.master)

        self.create_competition_frame(main, self.competition_repo)

        self.create_registration_frame(main)

        self.create_registration_list_frame(main)

        return main