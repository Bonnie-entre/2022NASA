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
    return HTMLResponse(content=html_main(), status_code=200)


def html_main() -> str:
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
                        <button onclick="show_search()"  style="width:12%; margin:4px; padding:5px; border-radius: 8px; border-color:#FF8045; border-width:thin; color:#FF8045; background-color:transparent;">Search</button>
                    </div>
                </header>
                <div class="content" style="display:flex; flex-direction:row; width:100%; height:100%; justify-content:center; align-items: center; background-image: url('../static/image/main.png'); background-repeat: no-repeat; background-size: cover;">
                    <form onsubmit="return upload_files()" style="position:absolute; bottom: 4vh; right: 10px; width: 35%; height: 26vh; overflow-y: scroll;">
                        <div>
                            <label>Select file to upload</label>
                            <input type="file" accept=".pdf" id="fileUploader" style="width: 16vw;" multiple/>
                        </div>
                        <input type="submit" id="submitUploader" value="Submit">
                        <div id="upload_result">
                            <h3 id="result_title" style="visibility: hidden;"><span style="color: #296889;">Upload Result List:</strong></span></h3>
                        </div>
                    </form>
                </div>
                <div class="producer" style="position: fixed; bottom: 0px; display:flex; flex-direction:row; width:100%; height: 6vh; justify-content:center; align-items: center; background-color:#D9D9D9;">
                    <span style="color: white;">Produced by : Cai Yi-Wen, Huang Nian-Hui, Wang Chun-Chieh </span>
                </div>
            </div>
        </body>
        
        <script>
            function show_search(){{
                search_input = document.getElementById("SearchKeyword").value 
                window.open ( "http://127.0.0.1:8000/search?outline=" + search_input + "&keyword=" + search_input, "_blank")             
            }}

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
                    document.getElementById("result_title").style.visibility = "visible";

                    
                }})
                .catch(error => console.log('error', error));

                return false
            }}
        </script>
    </html>

    """
