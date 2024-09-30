import uuid
from pathlib import Path
import aiofiles
from src.domain.entities.upload import UploadResponse
from src.domain.exceptions.base import InternalServerError
from src.main.config import MEDIA_DIR, BASE_DIR, settings


class UploadService:
    def __init__(self):
        self._backend_url = settings.backend_url

    async def upload_file(self, file: bytes, filename: str, file_dir: str = '') -> UploadResponse:
        try:
            save_dir = Path(MEDIA_DIR) / file_dir
            save_dir.mkdir(parents=True, exist_ok=True)

            file_stem = Path(filename).stem
            file_ext = Path(filename).suffix

            new_filename = f"{file_stem}_{uuid.uuid4().hex[:5]}{file_ext}"
            file_path = save_dir / new_filename

            async with aiofiles.open(file_path, "wb") as writer:
                await writer.write(file)

            relative_file_path = file_path.relative_to(MEDIA_DIR.parent)
            return UploadResponse(url=f"{self._backend_url}/{relative_file_path}")
        except Exception as e:
            raise InternalServerError(f"Failed to upload file: {e}")

    async def delete_file(self, file_path: str) -> bool:
        try:
            file_path_relative = file_path.replace(self._backend_url, "")
            path = BASE_DIR / file_path_relative.strip("/")

            if path.exists():
                path.unlink()
            else:
                print(f"File not found and cannot be deleted: {file_path_relative}")
            return True
        except Exception as e:
            raise InternalServerError(f"Failed to delete file: {e}")
