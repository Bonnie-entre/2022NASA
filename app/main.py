from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from . import models
from .database import engine
from .routers import search, show_content, upload

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(show_content .router)
app.include_router(search.router)
app.include_router(upload.router)


@app.get("/")
async def root():
    return HTMLResponse(content=html_content(), status_code=200)


def html_content() -> str:
    return f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
        </head>
        <body style="margin:0px">
            <div style="display:flex; flex-direction:column; width:100vw; height: 100vh; justify-content: center; align-items: center;">
                <header class="header" style="display:flex; flex-direction:row; width:100%; height:8%; justify-content:flex-end; align-items: center; margin:10px;">
                    <div style="display:flex; width:60%; height:100%; padding:10px; justify-content: flex-end;">
                        <input type="search" id="SearchKeyword" placeholder="Enter the keyword..." style="width:40%; margin:4px; padding:5px; border-color:black; border-width:thin; border-radius: 3px;">
                        <button style="width:12%; margin:4px; padding:5px; border-radius: 8px; border-color:#FF8045; border-width:thin; color:#FF8045; background-color:transparent;">Search</button>
                    </div>
                </header>
                <div class="content" style="display:flex; flex-direction:row; width:100%; height:100%; justify-content:center; align-items: center; background-image: url('../static/image/main.png'); background-repeat: no-repeat; background-size: cover;">
                    <form  onsubmit="return upload_files()" style="position:absolute; bottom: 6vh; right: 10px;">
                        <div>
                            <label>Select file to upload</label>
                            <input type="file" accept=".pdf" id="fileUploader" multiple/>
                        </div>
                        <input type="submit" id="submitUploader" value="Submit">
                        <div id="upload_result">
                            <h3><span style="color: #296889;">Result List:</strong></span></h3>
                        </div>
                    </form>
                </div>
                <div class="producer" style="display:flex; flex-direction:row; width:100%; height: 6vh; justify-content:center; align-items: center; background-color:#D9D9D9;">
                    <span style="color: white;">Produced by : Cai Yi-Wen, Huang Nian-Hui, Wang Chun-Chieh </span>
                </div>
            </div>
        </body>
        
        <script>
            function show_search(){{
                search_input = document.getElementById("SearchKeyword").value 
                window.location.href = "http://127.0.0.1:8000/search?outline=" + search_input + "&keyword=" + search_input                
            }}
        </script>
    </html>

    """

# <div class="content" style="display:flex; flex-direction:row; width:100%; justify-content:flex-start; align-items: center;">
#                     <img src="static/image/1-1.png" width="40%" style="display: flex; align-items: center; margin: 30px;"></img>
#                     <div class="content_right" style="display:flex; flex-direction:column; width="50% margin: 30px;">
#                         <img src="static/image/main2.png" width="40%" style="display:flex; align-items: center; margin: 30px;"></img>
#                         <form  onsubmit="return upload_files()">
#                             <div>
#                                 <label>Select file to upload</label>
#                                 <input type="file" id="fileUploader" multiple/>
#                             </div>
#                             <input type="submit" id="submitUploader" value="Submit">
#                             <div id="upload_result">
#                                 <h3><span style="color: #296889;">Result List:</strong></span></h3>
#                             </div>
#                         </form>
#                     </div>
#                 </div>


# <div style="display:flex; justify-content: flex-start; font-size: 26px; font-weight:400; padding:10px; color:blue; width:30%;">
#                         <span>2022 NASA</span>
#                     </div>
# <div>
#                             <h2>Problem Name, Team Name</h2>
#                             <p><span>Solution<span></p>
#                         </div>