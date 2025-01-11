from fastapi import BackgroundTasks
from app.send_emails.schemas import EmailSchema
from app.send_emails.my_utils import send_message, create_message

def send_email_background(background_tasks: BackgroundTasks, mail: EmailSchema):
    background_tasks.add_task()
    pass
