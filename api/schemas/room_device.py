from pydantic import BaseModel

class RoomDeviceSchema(BaseModel):
    room_name: str
    device_identifier: str 

    class Config:
        from_attributes = True