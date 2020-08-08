# Mikhail Pisman
# https://github.com/mike-pisman/To_Do_List
# To_Do_List
# Required: SQLAlchemy==1.3.16

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


# Load a SQL database, and create engine for it
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


# Class for table and rows
class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)  # ID of a task
    task = Column(String, default='default_value')  # Description of a task
    deadline = Column(Date, default=datetime.today())  # Deadline of a task

    def __repr__(self):
        return self.task


# Main class for printing menu
def main():
    Base.metadata.create_all(engine)
    # Start  session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Print Menu
    while True:
        # Print Menu options
        print("\n"
              "1) Today's tasks",
              "2) Week's tasks",
              "3) All tasks",
              "4) Missed tasks",
              "5) Add task",
              "6) Delete task",
              "0) Exit", sep="\n")
        # Get user choice
        command = int(input(">").strip())

        # 1) Today's tasks
        if command == 1:
            print("\nToday", "{dt.day} {dt:%b}".format(dt=datetime.now()))  # Print today's date (i.e. 19 Apr)
            rows = session.query(Task).filter(Task.deadline == datetime.today().date()).all()  # Get the rows
            if len(rows) > 0:
                print(*rows, sep="\n")  # Print each task
            else:
                print("Nothing to do!")  # If there are no tasks for today

        # 2) Week's tasks
        if command == 2:
            # Print tasks for next 7 days starting today
            for day in range(7):
                t = datetime.today().date() + timedelta(days=day)
                rows = session.query(Task).filter(Task.deadline == t).all()
                # For each day print Day of Week, Day, and Month (i.e. Monday 19 Apr:)
                print("\n{dt:%A} {dt.day} {dt:%b}:".format(dt=t))
                if rows:
                    for i, row in enumerate(rows, 1):
                        print("{}. {}".format(i, row.task))  # Print each task enumerated
                else:
                    print("Nothing to do!")  # If no task were found for that day of the week

        # 3) All tasks
        if command == 3:
            # Print all tasks from the table
            print("\nAll tasks:")
            rows = session.query(Task).order_by(Task.deadline).all()
            if len(rows) > 0:
                for i, row in enumerate(rows, 1):
                    # Print ID, name, deadline (i.e 1. First Task. 19 Apr)
                    print("{}. {}. {dt.day} {dt:%b}".format(i, row.task, dt=row.deadline))
            else:
                print("Nothing to do!")  # If the table is empty

        # 4) Missed tasks
        if command == 4:
            # Print all tasks from the table with deadline before today's date
            print("\nMissed tasks:")
            rows = session.query(Task).order_by(Task.deadline < datetime.today().date()).all()
            if len(rows) > 0:
                for i, row in enumerate(rows, 1):
                    # Print ID, name, deadline (i.e 1. First Task. 19 Apr)
                    print("{}. {}. {dt.day} {dt:%b}".format(i, row.task, dt=row.deadline))
            else:
                print("Nothing is missed!")  # If no tasks were found

        # 5) Add task
        if command == 5:
            # Get user input (task and deadline)
            task = input("\nEnter task\n>")  # Task Description
            deadline = datetime.strptime(input("Enter deadline\n>"), "%Y-%m-%d")  # Task Deadline i.e. 2020-08-13
            new_task = Task(task=task, deadline=deadline)  # Create new task object
            session.add(new_task)  # ASs row to the table
            session.commit()
            print("The task has been added!")

        # 6) Delete task
        if command == 6:
            # Print all tasks from the table
            print("\nChoose the number of the task you want to delete::")
            rows = session.query(Task).order_by(Task.deadline).all()
            if len(rows) > 0:
                for i, row in enumerate(rows, 1):
                    # Print ID, name, deadline (i.e 1. First Task. 19 Apr)
                    print("{}. {}. {dt.day} {dt:%b}".format(i, row.task, dt=row.deadline))
            else:
                print("Nothing to delete!")  # If the table is empty

            # Ask user for the ID of a task to delete
            task = rows[int(input("\n>")) - 1]
            session.delete(task)  # Delete the row from the table
            session.commit()
            print("The task has been deleted!")

        # 0) Exit
        if command == 0:
            # Stop the Loop and clear the table
            session.query(Task).delete()
            session.commit()
            print("\nBye!")
            break

if __name__ == '__main__':
    main()
