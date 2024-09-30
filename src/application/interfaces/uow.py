from typing import Protocol, runtime_checkable


@runtime_checkable
class UoW(Protocol):
    async def commit(self) -> None:
        ...

    async def flush(self) -> None:
        ...

    async def rollback(self) -> None:
        ...
