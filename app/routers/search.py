from fastapi import FastAPI, Response, status, Depends, APIRouter
from fastapi.responses import HTMLResponse
from typing import Optional, List
from .. import models, schemas
from ..database import get_db, connect_cursor
from sqlalchemy.orm import Session


router = APIRouter()    #prefix="/files"


# @router.get("/", response_model=List[schemas.FilesBase])
# def show_files(db: Session = Depends(get_db),  limit: int=10, skip: int=0): #, search: Optional[str]=""
#     files = db.query(models.Files).limit(limit).offset(skip).all()  #.filter(models.Files.output_outline.contains(search))  #if 該欄 null ，就不會出現該份資料
#     return files

def show_titles(posts):  #filename ideally
    html=''
    for i in range(len(posts)):
        post = dict(posts[i])
        html+=f"""<p><span><a href="/files/content?file_id={post['id']}">{post['filename']}</span></p>"""
    return html


# search1 for outline(dont fit well)
# search2 for keyword(totally equal)
@router.get("/search", response_model=List[schemas.FilesBase])  # without ( outline is null || keyword is null )
def show_files(db: Session = Depends(get_db),  outline: Optional[str]="", keyword: Optional[str]=""):   #limit: int=10, skip: int=0,
    cursor = connect_cursor()
    cursor.execute(f"""select * from files where output_outline like '%{outline}%' or '{keyword}'=ANY(output_keyword) """ ) # or, not and
    posts = cursor.fetchall()
    # print(dict(posts[0])['id'])
    # return posts
    return HTMLResponse(content=html_search_result(show_titles(posts)), status_code=200)


def html_search_result(titles) -> str:
    return f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
        </head>
        <body>
            <header class="header" style="font-size: 30px; font-weight:400; padding:30px; color:white; background:#5E9BC9;">
                2022 NASA
            </header>
            
            <div class="content">
            <h3><span style="color: #296889;">Search Result</span></h3>
            <p>&nbsp;</p>
            {titles}
            
            </div>
        </body>
    </html>

    """

