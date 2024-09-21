from datetime import datetime, timedelta
import jwt

from src.application.user.dto import PayloadDTO


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
        payload_dict = payload.__dict__.copy()
        payload_dict['exp'] = datetime.utcnow() + timedelta(minutes=self.expires_in_minutes)
        return jwt.encode(payload_dict, self.secret_key, algorithm=self.algorithm)

    def decode(self, token: str) -> PayloadDTO:
        try:
            decoded_payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return PayloadDTO(**decoded_payload)
        except jwt.ExpiredSignatureError:
            raise ValueError("Срок действия токена истек")
        except jwt.DecodeError:
            raise ValueError("Неверный токен")
