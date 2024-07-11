from email.policy import default
from os import getenv

from sqlmodel import Field, Session, SQLModel, create_engine, Relationship
from dotenv import load_dotenv

load_dotenv()


class UserTaskLink(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    task_id: int | None = Field(default=None, foreign_key="task.id", primary_key=True)


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str | None = None
    status: str = "new"
    users: list["User"] = Relationship(back_populates="tasks", link_model=UserTaskLink)


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_name: str
    tick_tick_token: str | None = None
    tasks: list[Task] = Relationship(back_populates="users", link_model=UserTaskLink)


engine = create_engine(f"postgresql://postgres:{getenv("POSTGRES_PASSWORD")}@db/{getenv('POSTGRES_DB')}")

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    task_1 = Task(title="Task 1", description="Task 1")
    task_2 = Task(title="Task 2", description="Task 2")
    test_user = User(user_name="testus", tasks=[task_1, task_2])
    with Session(engine) as session:
        session.add(task_1)
        session.add(task_2)
        session.add(test_user)
        session.commit()
