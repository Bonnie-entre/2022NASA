from fastapi import FastAPI, Response, status, Depends, APIRouter
from fastapi.responses import HTMLResponse
from typing import Optional, List
from .. import models, schemas
from ..database import get_db, connect_cursor
from sqlalchemy.orm import Session

router = APIRouter(
    # prefix="/files"
)

# def show_keyword(obj_keyword):
#     html_keyword=""
#     for i in range(len(obj_keyword)):
#         if obj_keyword[i].output_keyword is None:
#             continue

#         list_keyword = obj_keyword[i].output_keyword
#         for j in range(len(list_keyword)):
#             html_keyword += f"""<p>{list_keyword[j]}</p>"""
    
#     print(html_keyword)
#     return html_keyword

def show_keyword(list_keyword):
    if list_keyword is None:
        return """<h3><span style="color: #296889;"><strong>Keywords:</strong></span></h3><p>none</p>"""
    html_keyword="""<h3><span style="color: #296889;"><strong>Keywords:</strong></span></h3>"""
    
    html_keyword += """<p>"""
    for j in range(len(list_keyword)):
        html_keyword += f"""<span>{list_keyword[j]}  </span>"""
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
        html += f"""<span><img src="../../static/image/{list_pic[j]}.jpg" width="60%" style="vertical-align:middle"></img></span>"""
    html += """</p>"""
    print(html)
    return html


@router.get("/files/content")
def one_file_byID(db: Session = Depends(get_db), file_id: str="1"):
    files = db.query(models.Files).filter(models.Files.id==int(file_id)).all()
    return HTMLResponse(content=html_pdf(files[0].filename, file_id, show_keyword(files[0].output_keyword), show_outline(files[0].output_outline), show_image(files[0].output_pic)), status_code=200)


@router.get("/files", response_model=List[schemas.FilesBase])
def show_files(db: Session = Depends(get_db),  skip: int=0): #, search: Optional[str]=""    #limit: int=20, #.limit(limit)
    files = db.query(models.Files).offset(skip).all()  #.filter(models.Files.output_outline.contains(search))  #if 該欄 null ，就不會出現該份資料
    # print(files[0].filename)
    # show_keyword(files[1].output_keyword)
    # show_keyword(files)
    # return HTMLResponse(content=html_content(), status_code=200)
    return files

def html_pdf(filename, file_id, file_keyword, file_outline, file_pic) -> str:
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
            <h2><span style="color: #296889;"><strong>{filename}</strong></span></h2>
            <p>&nbsp;</p>
            {file_outline}
            {file_keyword}
            {file_pic}
            <h3><span style="color: #296889;"><strong>Pdf:</strong></span></h3>
            <object data="../static/file/{file_id}.pdf" type="application/pdf" width="100%" height="100%"></object>
            </div>
        </body>
    </html>

    """

