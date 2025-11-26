from pydantic import BaseModel


class ImageSearchResponse(BaseModel):
    status: str
    status_code: int
    message: str
    data: dict
