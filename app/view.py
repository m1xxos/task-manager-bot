from sqlmodel import select, Session

import model


class User:
    def __init__(self, user_id):
        self._engine = model.engine
        self._user_id = user_id

    def get_user(self):
        with Session(self._engine) as session:
            statement = select(model.User).where(model.User.id == self._user_id)
            result = session.exec(statement).one()
        return result

    def create_user(self, user_name: str):
        if self.get_user():
            return "User already exists"

        new_user = model.User(id=self._user_id, user_name=user_name, tasks=[])
        with Session(self._engine) as session:
            session.add(new_user)
            session.commit()
        return "User created"

    def create_task(self, title: str, description: str):
        with Session(self._engine) as session:
            statement = select(model.User).where(model.User.id == self._user_id)
            _user = session.exec(statement).one()
            _user.tasks.append(model.Task(title=title, description=description))
            session.commit()
            session.refresh(_user)
            task = _user.tasks[-1].title
        return task
