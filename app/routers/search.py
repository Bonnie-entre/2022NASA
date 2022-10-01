from fastapi import FastAPI, Response, status, Depends, APIRouter
from fastapi.responses import HTMLResponse
from typing import Optional, List
from .. import models, schemas
from ..database import get_db, connect_cursor
from sqlalchemy.orm import Session


router = APIRouter()    #prefix="/files"

def show_titles(posts):  #filename ideally
    html=''
    for i in range(len(posts)):
        post = dict(posts[i])
        html+=f"""<p><span><a href="/files/content?file_id={post['id']}" class="file_tiltle">{post['file_title']}</a></span></p>
                    <p><span>{post['filename']} - {post['output_outline']}</span></p>
                """
    return html

@router.get("/files")
def show_files(db: Session = Depends(get_db)): #, search: Optional[str]=""    #limit: int=20, #.limit(limit)
    # files = db.query(models.Files).offset(skip).all()  #.filter(models.Files.output_outline.contains(search))  #if 該欄 null ，就不會出現該份資料
    cursor = connect_cursor()
    cursor.execute(f"""select * from files""" ) # or, not and
    posts = cursor.fetchall()
    return HTMLResponse(content=html_search_result(show_titles(posts)), status_code=200)

# search1 for outline(dont fit well)
# search2 for keyword(totally equal)
@router.get("/search")  # without ( outline is null || keyword is null )
def show_files(db: Session = Depends(get_db),  outline: Optional[str]="", keyword: Optional[str]=""):   #limit: int=10, skip: int=0,
    cursor = connect_cursor()
    if(len(outline)==0 & len(keyword)==0):
        cursor.execute(f"""select * from files""" )
    else:
        cursor.execute(f"""select * from files where output_outline like '%{outline}%' or '{keyword}'=ANY(output_keyword) """ ) # or, not and
    posts = cursor.fetchall()
    return HTMLResponse(content=html_search_result(show_titles(posts)), status_code=200)


def html_search_result(titles) -> str:
    return f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
        </head>
        <body style="margin:0px">
            <div style="display:flex; flex-direction:column; width:100vw; height: 100vh; justify-content: center; align-items: center;">
                <header class="header" style="display:flex; flex-direction:row; width:100%; height:8%; justify-content:flex-end; align-items: center; margin:10px; position: fixed; top: 0px;">
                    <div style="display:flex; width:60%; height:100%; padding:10px; justify-content: flex-end;">
                        <input type="search" id="SearchKeyword" placeholder="Enter the keyword..." style="width:40%; margin:4px; padding:5px; border-color:black; border-width:thin; border-radius: 3px;">
                        <button onclick="show_search()"  style="width:12%; margin:4px; padding:5px; border-radius: 8px; border-color:#FF8045; border-width:thin; color:#FF8045; background-color:transparent;">Search</button>
                    </div>
                </header>
            
                <div class="content" style="display:flex; flex-direction:column; width:80%; height:80%; justify-content:flex-start; align-items: flex-start;  position: fixed; top: 12%; overflow-y:scroll;">
                    <h3><span style="color: #296889; font-size:36px;" class="search_result">Search Result</span></h3>
                    {titles}
                </div>

                <div class="producer" style="position: fixed; bottom: 0px; display:flex; flex-direction:row; width:100%; height: 6vh; justify-content:center; align-items: center; background-color:#D9D9D9;">
                    <span style="color: white;">Produced by : Cai Yi-Wen, Huang Nian-Hui, Wang Chun-Chieh </span>
                </div>
            </div>
        </body>

        <script>
            function show_search(){{
                search_input = document.getElementById("SearchKeyword").value 
                window.location.href =  "http://127.0.0.1:8000/search?outline=" + search_input + "&keyword=" + search_input          
            }}
        </script>

        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@700&display=swap');
            .search_result{{
                font-family: 'Zilla Slab', serif;
            }}
            .file_tiltle{{
                font-family: 'Zilla Slab', serif;
                font-size: 24px;
            }}
        </style>
    </html>

    """

