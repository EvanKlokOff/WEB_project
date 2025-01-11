from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.send_emails.schemas import EmailSchema
from app.send_emails.utils import send_email_background
router = APIRouter(
    prefix='/email'
)

@router.post("/send")
async def send_with_template(email: EmailSchema) -> JSONResponse:
    html = "<p>Hi this test mail, thanks for using Fastapi-mail</p>"
    await send_email_background(email)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
