from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return "{}. {}".format(self.id, self.task)

def main():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("\n1) Today's tasks", "2) Add task", "0) Exit", sep="\n")
        command = int(input().strip())
        if command == 0:
            session.query(Task).delete()
            session.commit()
            print("\nBye!")
            break

        elif command == 1:
            print("\nToday:")
            rows = session.query(Task).all()
            if len(rows) > 0:
                print(*rows, sep="\n")
            else:
                print("Nothing to do!")

        elif command == 2:
            print("\nEnter task")
            new_row = Task(task=input())
            session.add(new_row)
            session.commit()
            print("The task has been added!")

if __name__ == '__main__':
    main()
