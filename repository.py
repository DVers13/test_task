from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from models import User

class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        pass

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self.counter = 1

    def create_user(self, user: User) -> User:
        user.id = self.counter
        self.users[self.counter] = user
        self.counter += 1
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def update_user(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def delete_user(self, user_id: int) -> None:
        if user_id in self.users:
            del self.users[user_id]

class DatabaseUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user(self, user: User) -> User:
        db_user = self.db.query(User).filter(User.id == user.id).first()
        if db_user:
            db_user.full_name = user.full_name
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
