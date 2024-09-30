from abc import ABC
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

    @asynccontextmanager
    def pick_style_interactor(self, picker: InteractorPicker[GenericInputDTO, GenericOutputDTO]) -> AsyncContextManager[
        InteractorCallable[GenericInputDTO, GenericOutputDTO]]:
        raise NotImplementedError

    @asynccontextmanager
    def pick_tag_interactor(self, picker: InteractorPicker[GenericInputDTO, GenericOutputDTO]) -> AsyncContextManager[
        InteractorCallable[GenericInputDTO, GenericOutputDTO]]:
        raise NotImplementedError

    @asynccontextmanager
    def pick_workout_interactor(self, picker: InteractorPicker[GenericInputDTO, GenericOutputDTO]) -> \
            AsyncContextManager[
                InteractorCallable[GenericInputDTO, GenericOutputDTO]]:
        raise NotImplementedError

    @asynccontextmanager
    def pick_avatar_interactor(self, picker: InteractorPicker[GenericInputDTO, GenericOutputDTO]) -> \
            AsyncContextManager[
                InteractorCallable[GenericInputDTO, GenericOutputDTO]]:
        raise NotImplementedError
