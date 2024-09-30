from datetime import datetime, timedelta
import jwt

from src.application.user.dto import PayloadDTO
from src.domain.exceptions.jwt import JWTError, JWTExpiredError, JWTMissingError, JWTSignatureError, JWTDecodeError


class JWTService:
    def __init__(
            self,
            secret_key: str,
            algorithm: str = "HS256",
            expires_in_minutes: int = 60
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_in_minutes = expires_in_minutes

    def encode(self, payload: PayloadDTO) -> str:
        try:
            payload_dict = payload.__dict__.copy()
            payload_dict['exp'] = datetime.utcnow() + timedelta(minutes=self.expires_in_minutes)
            return jwt.encode(payload_dict, self.secret_key, algorithm=self.algorithm)
        except Exception as e:
            raise JWTError(f"Failed to encode JWT: {str(e)}")

    def decode(self, token: str) -> PayloadDTO:
        if not token:
            raise JWTMissingError("Token is missing")

        try:
            decoded_payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return PayloadDTO(**decoded_payload)
        except jwt.ExpiredSignatureError:
            raise JWTExpiredError("Token has expired")
        except jwt.InvalidSignatureError:
            raise JWTSignatureError("Invalid token signature")
        except jwt.DecodeError:
            raise JWTDecodeError("Failed to decode token")
        except Exception as e:
            raise JWTError(f"Failed to process token: {str(e)}")
