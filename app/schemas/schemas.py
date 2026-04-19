from pydantic import BaseModel

class DocumentSubmission(BaseModel):
    user_name: str
    content: str