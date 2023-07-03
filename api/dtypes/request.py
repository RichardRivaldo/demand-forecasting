from pydantic import BaseModel


class Request(BaseModel):
    menu_group: str
    n_weeks: int
    include_deals: bool
