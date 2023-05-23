from src.config.schemas import ORJSONSchema


class CitySchema(ORJSONSchema):
    id: int
    name: str

    class Config:
        orm_mode = True
