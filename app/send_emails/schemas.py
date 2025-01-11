from pydantic import BaseModel, EmailStr
from fastapi_mail import MessageType

class EmailSchema(BaseModel):
    subject: str
    email: EmailStr
    body: str
    body_type: MessageType