from dataclasses import dataclass


@dataclass
class CreateUpload:
    file: bytes
    filename: str
    filedir: str


@dataclass
class UploadResponse:
    url: str
