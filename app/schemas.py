from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class FilesBase(BaseModel):
    id: int
    filename: str
    file_title: Optional[str] = None
    output_outline: Optional[str] = None
    output_keyword: Optional[List[str]] = None
    output_keyword_float: Optional[List[str]] = None
    output_pic: Optional[List[str]] = None
    class Config:
        orm_mode = True

class FilesCreate(FilesBase):
    pass

# class UploadFile(BaseModel):
#     filename: str
    # output_outline: Optional[str] = None
    # output_keyword: Optional[List[str]] = None
    # output_pic: Optional[List[str]] = None
        

# model the data return when post
# class Post(FilesBase):
#     id: int
    # input_time: datetime
    

