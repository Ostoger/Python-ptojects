from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()


class User(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class Plan:
    state = None
    session = None
    task_queue = {}
    menu_option = ["1) Today's tasks", "2) Week's tasks", "3) All tasks",
                   "4) Missed tasks", "5) Add task", "6) Delete task", "0) Exit"]

    def __init__(self):
        self.db_init()
        self.back_to_menu()

    def back_to_menu(self):
        self.state = "main menu"
        self.show_menu()

    def db_init(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        self.session = session()

    def set_state(self, state):
        self.state = state

    def main_menu(self, user_input=None):
        if self.state == "main menu":
            self.show_menu()
        elif self.state == "choose option":
            if user_input == "1":
                self.today_tasks()
            elif user_input == "2":
                self.week_tasks()
            elif user_input == "3":
                self.all_tasks()
            elif user_input == "4":
                self.missed_tasks()
            elif user_input == "5":
                self.add_task(user_input)
            elif user_input == "6":
                self.delete_task(user_input)
            elif user_input == "0":
                self.exit()
        elif self.state == "enter task":
            self.add_task(user_input)
        elif self.state == "enter deadline":
            self.add_deadline(user_input)
        elif self.state == "delete row":
            self.delete_task(user_input)

    def show_menu(self):
        for i in self.menu_option:
            print(i)
        self.set_state("choose option")

    def all_tasks(self):
        all_tasks = self.session.query(User.task, User.deadline).order_by(User.deadline).all()
        print('\nAll tasks:')
        if not all_tasks:
            print('Nothing to do!\n')
        else:
            for number, task in enumerate(all_tasks):
                print(f'{number + 1}. {task[0]}. {task[1].strftime("%#d %b")}')
            print('\n')
        self.back_to_menu()

    def today_tasks(self):
        today = datetime.today()
        today_tasks = self.session.query(User).filter(User.deadline == today.date()).all()
        print(f'\nToday, {today.strftime("%d %b")}:')
        if not today_tasks:
            print('Nothing to do!\n')
        else:
            for number, task in enumerate(today_tasks):
                print(f'{number + 1}. {task}')
            print('\n')
        self.back_to_menu()

    def week_tasks(self):
        for days in range(7):
            week_days = datetime.today() + timedelta(days=days)
            print(f'{week_days.strftime("%A")} {week_days.day} {week_days.strftime("%b")}')
            rows = self.session.query(User).filter(User.deadline == week_days.date()).all()
            if not rows:
                print("Nothing to do!\n")
            else:
                for number, task in enumerate(rows):
                    print(f'{number + 1}. {task}\n')
        self.back_to_menu()

    def missed_tasks(self):
        print("Missed tasks:")
        today = datetime.today()
        rows = self.session.query(User.task, User.deadline). \
            filter(User.deadline < today.date()).all()
        if not rows:
            print("Nothing is missed!")
        else:
            for number, task in enumerate(rows):
                print(f'{number + 1}. {task[0]}. {task[1].strftime("%#d %b")}')
        print('')
        self.back_to_menu()

    def add_task(self, user_input=None):
        if self.state != "enter task":
            print("\nEnter task")
            self.set_state("enter task")
        elif self.state == "enter task":
            self.set_state("enter task")
            self.task_queue["task"] = user_input
            self.set_state("enter deadline")
            print("\nEnter deadline")

    def add_deadline(self, user_input=None):
        self.task_queue["deadline"] = datetime.strptime(user_input, "%Y-%m-%d")
        new_task = User(task=self.task_queue["task"], deadline=self.task_queue["deadline"])
        self.session.add(new_task)
        self.session.commit()
        print("The task has been added!\n")
        self.back_to_menu()

    def delete_task(self, user_input=None):
        if self.state != "delete row":
            today = datetime.today()
            rows_to_delete = self.session.query(User) \
                .filter(User.deadline <= today).order_by(User.deadline)
            if not rows_to_delete:
                print("Nothing to delete")
            else:
                print("Choose the number of the task you want to delete:")
                for row in rows_to_delete:
                    date = row.deadline.strftime("%#d %b")
                    print(f'{row.id}. {row.task}. {date}\n')
                    self.set_state("delete row")
        elif self.state == "delete row":
            today = datetime.today()
            rows_to_delete_ = self.session.query(User) \
                .filter(User.deadline <= today).order_by(User.deadline)
            specific_row = rows_to_delete_[int(user_input) - 1]
            self.session.delete(specific_row)
            print("The task has been deleted!\n")
            self.session.commit()
            self.back_to_menu()

    def exit(self):
        self.session.close()
        print("\nBye!")
        self.set_state("exit")


to_do_list = Plan()
while True:
    if to_do_list.state == "exit":
        break
    else:
        provided_input = input()
        to_do_list.main_menu(provided_input)
