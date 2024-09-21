from typing import Generic, TypeVar

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class Interactor(Generic[InputDTO, OutputDTO]):
    pass
