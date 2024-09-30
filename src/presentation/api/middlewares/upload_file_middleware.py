from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.datastructures import UploadFile

MAX_FILE_SIZE = 5 * 1024 * 1024


class MaxFileSizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method in ['POST', 'PUT', 'PATCH']:
            body = await request.body()
            content_type = request.headers.get('content-type', '')
            if "multipart/form-data" in content_type:
                try:
                    form = await request.form()
                    for field in form.values():
                        if isinstance(field, UploadFile):
                            if len(await field.read()) > MAX_FILE_SIZE:
                                return JSONResponse(
                                    content={"detail": "File too large"},
                                    status_code=413
                                )
                except Exception as e:
                    return JSONResponse(
                        content={"detail": "Invalid multipart form data"},
                        status_code=400
                    )

        return await call_next(request)
