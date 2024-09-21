from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncContextManager, TypeVar, TypeAlias, Callable, Awaitable

from src.application.interfaces.interactor import Interactor

GenericInputDTO = TypeVar("GenericInputDTO")
GenericOutputDTO = TypeVar("GenericOutputDTO")

InteractorCallable: TypeAlias = Callable[[GenericInputDTO], Awaitable[GenericOutputDTO]]
InteractorPicker: TypeAlias = Callable[
    [Interactor], InteractorCallable[GenericInputDTO, GenericOutputDTO]
]


class InteractorFactory(ABC):
    @asynccontextmanager
    def pick_user_interactor(self, picker: InteractorPicker[GenericInputDTO, GenericOutputDTO]) -> AsyncContextManager[
        InteractorCallable[GenericInputDTO, GenericOutputDTO]]:
        raise NotImplementedError
