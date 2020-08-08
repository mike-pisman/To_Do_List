from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

def main():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("\n1) Today's tasks", "2) Week's tasks", "3) All tasks", "4) Add task", "0) Exit", sep="\n")
        command = int(input(">").strip())
        if command == 0:
            session.query(Task).delete()
            session.commit()
            print("\nBye!")
            break

        if command == 1:
            print("\nToday", "{dt.day} {dt:%b}".format(dt=datetime.now()))
            rows = session.query(Task).filter(Task.deadline == datetime.today().date()).all()
            if len(rows) > 0:
                print(*rows, sep="\n")
            else:
                print("Nothing to do!")

        if command == 2:
            for day in range(7):
                t = datetime.today().date() + timedelta(days=day)
                rows = session.query(Task).filter(Task.deadline == t).all()

                print("\n{dt:%A} {dt.day} {dt:%b}:".format(dt=t))
                if rows:
                    for i, row in enumerate(rows, 1):
                        print("{}. {}".format(i, row.task))
                else:
                    print("Nothing to do!")

        if command == 3:
            print("\nAll tasks:")
            rows = session.query(Task).order_by(Task.deadline).all()
            if len(rows) > 0:
                for i, row in enumerate(rows, 1):
                    print("{}. {}. {dt.day} {dt:%b}".format(i, row.task, dt=row.deadline))
            else:
                print("Nothing to do!")

        if command == 4:
            task = input("\nEnter task\n>")
            deadline = datetime.strptime(input("Enter deadline\n>"), "%Y-%m-%d")
            new_task = Task(task=task, deadline=deadline)
            session.add(new_task)
            session.commit()
            print("The task has been added!")

if __name__ == '__main__':
    main()
