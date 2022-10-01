from fastapi import FastAPI, Response, status, Depends, APIRouter, UploadFile
from fastapi.responses import HTMLResponse
from typing import Optional, List
from .. import models, schemas
from ..database import get_db, connect_cursor, SessionLocal
from sqlalchemy.orm import Session

import imp
from io import StringIO
from os import listdir
from os.path import isfile, join
import PyPDF2
from PyPDF2 import PdfFileReader
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from ..nlp_model import insert_db, Text_outline, hack_utils

router = APIRouter()

summarize = Text_outline.Summarize()

@router.get("/upload")  
def upload_page():
    return HTMLResponse(content=html_page(), status_code=200)


@router.post("/upload/multifiles", status_code=status.HTTP_201_CREATED, response_model=List[schemas.FilesBase])  
async def upload_files(files: List[UploadFile], db: Session = Depends(get_db)):   #, db: Session = Depends(get_db)
    next_file_id = init_id = insert_db.get_next_fileID()
    print(f'next_file_id sart at:{next_file_id}')

    # Get & Save the Upload File
    list_filename = []
    
    for file in files:
        print(file.filename)
        try:
            contents = file.file.read()
            with open(f"static/file/{file.filename}", 'wb') as f:    #f"files/{get_next_fileID()}"
                f.write(contents)
        except Exception as e:
            return {"message": e}
        finally:
            file.file.close()
            list_filename.append(file.filename)

    # Call NLP model to train it
    try:
        for file in list_filename:
            print(f"#{next_file_id} filename={file}")
            pdfFileObj =  open(f"static/file/{file}", 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            pdf_one_line_text = hack_utils.pdf2text(pdfReader)
            PDF_string = StringIO()
            parser = PDFParser(pdfFileObj)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, PDF_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
            pdf_sum = summarize.summarize(pdf_one_line_text)
            pdf_title = summarize.title(pdf_one_line_text)
            pdf_final_text = hack_utils.pdf_string_prep(PDF_string.getvalue())
            key_word = hack_utils.find_key_word(pdf_final_text)
            hack_utils.to_chart(key_word, next_file_id)     
            

            _keyword=[]
            _output_keyword_float=[]
            for i in range(len(key_word)):
                x = '%s' % (key_word[i],)
                _keyword.append(key_word[i][0])
                _output_keyword_float.append(x)
            _output_pic = [f"{next_file_id}"]  

            insert_db.create_files(SessionLocal(), file, pdf_title, pdf_sum,  _keyword, _output_keyword_float, _output_pic)
            next_file_id+=1
    except Exception as e:
        return {"train model & save err message": f"when process file_id={next_file_id}, error:{e}"}
    files = db.query(models.Files).filter(models.Files.id>=init_id).all()    #>init_id
    
    return files

# @router.post("/", status_code=status.HTTP_201_CREATED)
# def add_files(post: schemas.FilesBase, db: Session = Depends(get_db)):
#     new_post = models.Files(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post    

def html_page() -> str:
    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
        </head>
        <body>
            <header class="header" style="font-size: 30px; font-weight:400; padding:30px; color:white; background:#5E9BC9;">
                2022 NASA
            </header>
            <div class="content">
                <h2><span style="color: #296889;"><strong>Upload Files</strong></span></h2>
                <p>&nbsp;</p>
                <h3><span style="color: #296889;"><strong>Pdf:</strong></span></h3>
            </div>

            <form  onsubmit="return upload_files()">
                <div>
                    <label>Select file to upload</label>
                    <input type="file" id="fileUploader" multiple/>
                </div>
                <input type="submit" id="submitUploader" value="Submit">
                <div id="upload_result">
                    <h3><span style="color: #296889;">Result List:</strong></span></h3>
                </div>
            </form>
        </body>

        <script>
            function upload_files(){{
                var input = document.getElementById('fileUploader')

                var data = new FormData()

                for (const file of input.files) {{
                    data.append('files', file, file.name)
                }}

                var requestOptions = {{
                    method: 'POST',
                    body: data,
                }}

                document.getElementById("submitUploader").disabled = true;
                fetch("http://127.0.0.1:8000/upload/multifiles", requestOptions)
                .then(response => response.json())
                .then((result) => {{
                    console.log(`Upload file num=${{result.length}}`)

                    for(var i=0; i<result.length; i++ ){{
                        //Result Filename - a tag
                        var createA = document.createElement('a');
                        var createAText = document.createTextNode(result[i].filename);
                        var _href = "http://127.0.0.1:8000/files/content?file_id=" + (result[i].id).toString()
                        createA.setAttribute('href', _href);
                        createA.setAttribute('target', "_blank");
                        createA.appendChild(createAText);

                        // Result Outline - span tag
                        var para = document.createElement("p");
                        para.innerHTML = result[i].file_title


                        //Append to Div
                        document.getElementById("upload_result").appendChild(createA)
                        document.getElementById("upload_result").appendChild(para)
                    }}

                    
                    document.getElementById("submitUploader").disabled = false;
                }})
                .catch(error => console.log('error', error));

                return false
            }}
        </script>
    </html>

    """
