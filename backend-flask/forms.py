import pydantic

class User(pydantic.BaseModel):
    steam_id: int = pydantic.Field(2)

class TestForm(pydantic.BaseModel):
    value: str = "lol"
