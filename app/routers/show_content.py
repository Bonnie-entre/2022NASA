from fastapi import FastAPI, Response, status, Depends, APIRouter
from fastapi.responses import HTMLResponse
from typing import Optional, List
from .. import models, schemas
from ..database import get_db, connect_cursor
from sqlalchemy.orm import Session

router = APIRouter()


def show_keyword(list_keyword):
    if list_keyword is None:
        return """<p>none</p>"""
    html_keyword=""""""
    
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

def keywordTuple_to_twoList(target):
    key_name = []
    key_weight = []

    for i in range(len(target)):
        target[i] = target[i].replace("(", "")
        target[i] = target[i].replace(")", "")
        target[i] = target[i].replace(",", "")
        target[i] = target[i].replace('\'', "")
        first, second = target[i].split(" ")
        key_name.append(first)
        key_weight.append(float(second))
    
    print(key_name)
    print(key_weight)

    return key_name, key_weight

@router.get("/files/content")
def one_file_byID(db: Session = Depends(get_db), file_id: str="1"):
    files = db.query(models.Files).filter(models.Files.id==int(file_id)).all()

    list_key_name, list_key_weight = keywordTuple_to_twoList(files[0].output_keyword_float)

    return HTMLResponse(content=html_pdf(files[0].filename, files[0].file_title, file_id, show_keyword(files[0].output_keyword), files[0].output_keyword_float, show_outline(files[0].output_outline), show_image(files[0].output_pic), list_key_name, list_key_weight), status_code=200)


@router.get("/filesjson", response_model=List[schemas.FilesBase])
def show_files(db: Session = Depends(get_db),  skip: int=0): #, search: Optional[str]=""    #limit: int=20, #.limit(limit)
    files = db.query(models.Files).offset(skip).all()  #.filter(models.Files.output_outline.contains(search))  #if 該欄 null ，就不會出現該份資料

    return files

def html_pdf(filename, file_title, file_id, file_keyword, keyword_float, file_outline, file_pic, key_word_js, key_word_float_js) -> str:
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
                    <h3><span style="color: #296889;"><strong>Keywords:</strong></span></h3>
                    <script src="https://www.amcharts.com/lib/4/core.js"></script>
                    <script src="https://www.amcharts.com/lib/4/charts.js"></script>
                    <script src="https://www.amcharts.com/lib/4/themes/animated.js"></script>
                    <script src="https://www.amcharts.com/lib/4/themes/dataviz.js"></script>
                    <div id="chartdiv"></div>
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
            
            
            am4core.useTheme(am4themes_animated);
            am4core.useTheme(am4themes_dataviz);

            // Create chart instance
            var chart = am4core.create("chartdiv", am4charts.PieChart);
            try{{
                kewyword = {key_word_js}
                kewyword_float = {key_word_float_js}
                console.log(kewyword)
                console.log(kewyword_float)

                // Add data
                chart.data = [{{
                    "_keyword": kewyword[0],
                    "_keyword_value": kewyword_float[0],
                    "url": "http://127.0.0.1:8000/search?outline=" + kewyword[0] + "&keyword=" + kewyword[0],
                    }},
                    {{
                    "_keyword": kewyword[1],
                    "_keyword_value": kewyword_float[1],
                    "url": "http://127.0.0.1:8000/search?outline=" + kewyword[1] + "&keyword=" + kewyword[1],
                    }},
                    {{
                    "_keyword": kewyword[2],
                    "_keyword_value": kewyword_float[2],
                    "url": "http://127.0.0.1:8000/search?outline=" + kewyword[2] + "&keyword=" + kewyword[2],
                    }},
                    {{
                    "_keyword": kewyword[3],
                    "_keyword_value": kewyword_float[3],
                    "url": "http://127.0.0.1:8000/search?outline=" + kewyword[3] + "&keyword=" + kewyword[3],
                    }},
                    {{
                    "_keyword": kewyword[4],
                    "_keyword_value": kewyword_float[4],
                    "url": "http://127.0.0.1:8000/search?outline=" + kewyword[4] + "&keyword=" + kewyword[4],
                    }},
                    {{
                    "_keyword": kewyword[5],
                    "_keyword_value": kewyword_float[5],
                    "url": "http://127.0.0.1:8000/search?outline=" + kewyword[5] + "&keyword=" + kewyword[5],
                    }},
                    {{
                    "_keyword": kewyword[6],
                    "_keyword_value": kewyword_float[6],
                    "url": "http://127.0.0.1:8000/search?outline=" + kewyword[6] + "&keyword=" + kewyword[6],
                    }},
                    {{
                    "_keyword": kewyword[7],
                    "_keyword_value": kewyword_float[7],
                    "url": "http://127.0.0.1:8000/search?outline=" + kewyword[7] + "&keyword=" + kewyword[7],
                    }},
                    {{
                    "_keyword": kewyword[8],
                    "_keyword_value": kewyword_float[8],
                    "url": "http://127.0.0.1:8000/search?outline=" + kewyword[8] + "&keyword=" + kewyword[8],
                    }},
                    {{
                    "_keyword": kewyword[9],
                    "_keyword_value": kewyword_float[9],
                    "url": "http://127.0.0.1:8000/search?outline=" + kewyword[9] + "&keyword=" + kewyword[9],
                    }} 
                    ];

                // Add and configure Series
                var pieSeries = chart.series.push(new am4charts.PieSeries());

                pieSeries.dataFields.value = "_keyword_value";
                pieSeries.dataFields.category = "_keyword";
                pieSeries.slices.template.propertyFields.url = "url";
                pieSeries.slices.template.urlTarget = "_blank";

            }}
            catch(e){{
                console.log(e)
            }}
        
        </script>
        <style lang="scss" scoped>
           body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
            }}

            #chartdiv {{
            width: 100%;
            height: 350px;
            }}

           
        </style>
    </html>

    """

# display:flex; flex-direction:column; justify-content:flex-start; align-items: flex-start;