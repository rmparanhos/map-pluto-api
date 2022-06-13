from pydantic import BaseModel


class Filter(BaseModel):
    attribute: str
    operand: str
    value: str