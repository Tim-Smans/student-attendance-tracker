from pydantic import BaseModel


class PingSchema(BaseModel):
    id: str
