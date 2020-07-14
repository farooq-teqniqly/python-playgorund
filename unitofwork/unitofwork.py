from abc import ABC, abstractmethod
from typing import Any
from enum import IntFlag


class UnitOfWorkState(IntFlag):
    NEW = (1,)
    STARTED = (2,)
    COMMITTED = (3,)
    REVERSED = (4,)
    ERROR = 5


class AbstractUnitOfWork(ABC):
    def __init__(self):
        self.state = UnitOfWorkState.NEW

    @abstractmethod
    def __enter__(self) -> Any:
        self.state = UnitOfWorkState.STARTED

    @abstractmethod
    def commit(self):
        self.state = UnitOfWorkState.COMMITTED

    @abstractmethod
    def rollback(self):
        self.state = UnitOfWorkState.REVERSED

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type or exc_val or exc_tb:
            self.rollback()
            self.state = UnitOfWorkState.ERROR | UnitOfWorkState.REVERSED
            return

        if self.state != UnitOfWorkState.COMMITTED:
            self.rollback()


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, tx_name: str):
        self._tx_name = tx_name
        super().__init__()

    def commit(self):
        print(f"Committing transaction {'{self._tx_name}'}...")
        super().commit()

    def rollback(self):
        print(f"Rolling back transaction {'{self._tx_name}'}...")
        super().rollback()

    def __enter__(self):
        print(f"Transaction '{self._tx_name}' started.")
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Exiting transaction '{self._tx_name}'.")
        super().__exit__(exc_type, exc_val, exc_tb)
