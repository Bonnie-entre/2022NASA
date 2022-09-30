from fastapi import FastAPI, Response, status, Depends, APIRouter
from fastapi.responses import HTMLResponse
from typing import Optional, List
from .. import models, schemas
from ..database import get_db, connect_cursor
from sqlalchemy.orm import Session

router = APIRouter()


def show_keyword(list_keyword):
    if list_keyword is None:
        return """<h3><span style="color: #296889;"><strong>Keywords:</strong></span></h3><p>none</p>"""
    html_keyword="""<h3><span style="color: #296889;"><strong>Keywords:</strong></span></h3>"""
    
    html_keyword += """<p>"""
    for j in range(len(list_keyword)):
        if j== len(list_keyword)-1:
            html_keyword += f"""<span>{list_keyword[j]}  </span>"""
        else:
            html_keyword += f"""<span>{list_keyword[j]},  </span>"""
        
    html_keyword += """</p>"""
    return html_keyword

def show_outline(outline):
    if outline is None:
        return """<h3><span style="color: #296889;"><strong>Outline:</strong></span></h3><p>nonde</p>"""

    return """<h3><span style="color: #296889;"><strong>Outline:</strong></span></h3>""" + f"""<p>{outline}</p>"""

def show_image(list_pic):
    html = """<h3><span style="color: #296889;"><strong>Pictures:</strong></span></h3>"""
    if list_pic is None:
        html+= """<p>none</p>"""
        return html

    html += """<p>"""
    for j in range(len(list_pic)):
        html += f"""<span><img src="../../static/image/{list_pic[j]}.png" width="60%" style="vertical-align:middle"></img></span>"""
    html += """</p>"""
    print(html)
    return html


@router.get("/files/content")
def one_file_byID(db: Session = Depends(get_db), file_id: str="1"):
    files = db.query(models.Files).filter(models.Files.id==int(file_id)).all()
    return HTMLResponse(content=html_pdf(files[0].filename, files[0].file_title, file_id, show_keyword(files[0].output_keyword), files[0].output_keyword_float, show_outline(files[0].output_outline), show_image(files[0].output_pic)), status_code=200)


@router.get("/filesjson", response_model=List[schemas.FilesBase])
def show_files(db: Session = Depends(get_db),  skip: int=0): #, search: Optional[str]=""    #limit: int=20, #.limit(limit)
    files = db.query(models.Files).offset(skip).all()  #.filter(models.Files.output_outline.contains(search))  #if 該欄 null ，就不會出現該份資料

    return files

def html_pdf(filename, file_title, file_id, file_keyword, keyword_float, file_outline, file_pic) -> str:
    return f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
        </head>
        <body style="margin:0px">
            <div style="display:flex; flex-direction:column; width:100vw; justify-content: center; align-items: center;">
                <header class="header" style="display:flex; flex-direction:row; width:100%; height:8%; justify-content:flex-end; align-items: center; margin:10px; position: fixed; top: 0px;">
                    <div style="display:flex; width:60%; height:100%; padding:10px; justify-content: flex-end;">
                        <input type="search" id="SearchKeyword" placeholder="Enter the keyword..." style="width:40%; margin:4px; padding:5px; border-color:black; border-width:thin; border-radius: 3px;">
                        <button onclick="show_search()"  style="width:12%; margin:4px; padding:5px; border-radius: 8px; border-color:#FF8045; border-width:thin; color:#FF8045; background-color:transparent;">Search</button>
                    </div>
                </header>

                <div class="content" style=" width:90%; height:80%;  position: fixed; top: 12%; overflow-y:scroll;">
                    <h1><span style="color: #296889;"><strong>{file_title}</strong></span></h1>
                    <p>{filename}</p>
                    {file_outline}
                    {file_keyword}
                    <h3><span style="color: #296889;"><strong>Keywords(Detail Result):</strong></span></h3>
                    <p>{keyword_float}</p>
                    {file_pic}

                    <h3><span style="color: #296889;"><strong>Pdf:</strong></span></h3>
                    <object data="../static/file/{filename}" type="application/pdf" width="100%" height="100%"></object>
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
    </html>

    """

# display:flex; flex-direction:column; justify-content:flex-start; align-items: flex-start;