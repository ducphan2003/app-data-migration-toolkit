from pydantic import BaseModel
from datetime import datetime


class AITokenLogSchema(BaseModel):
    id: int
    input_tokens: int
    output_tokens: int

    class Config:
        orm_mode = True
