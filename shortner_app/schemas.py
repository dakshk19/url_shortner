from pydantic import BaseModel

class url(BaseModel):

    body: str

    class config:

        orm_mode=True
