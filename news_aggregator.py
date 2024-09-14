from fastapi import FastAPI
from fastapi.responses import HTMLResponse,JSONResponse
import pandas as pd
from fastapi.encoders import jsonable_encoder
import json

app = FastAPI()

df_dct = pd.read_csv('news_art.csv').to_dict(orient='index')

@app.get("/")
def read_root():
    html__index = \
    """
    <html>
        <head>
            <title>DK</title>

            <style>
                body{
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <br>
            <h1>news aggregator :: index</h1>
            <br><hr><br>
            <a href="/articles">articles</a>
            <a href="/article-id">articles-id</a>
            <a href="/search">search</a>
            <a href="/docs" target="_blank">docs-api</a>
            <br>
        </body>
    </html>
    """
    return HTMLResponse(content=html__index)

@app.get("/articles")
def read_articles():
    html__articles = \
    f"""
    <html>
        <head>
            <title>news aggregator :: articles</title>

            <style>
                body{{
                    text-align: center;
                }}
            </style>

        </head>
        <body>
            <br>
            <h1>news aggregator:: articles</h1>
            <br><hr><br>
            <a href="/">index</a>
            <br><hr><br>
            <pre style="text-align:justify;white-space: pre-wrap;">{json.dumps(df_dct,indent=4)}</pre>
            <br>
        </body>
    </html>
    """
    return HTMLResponse(html__articles)

@app.get("/article-id")
def read_article():
    html_content = f"""
    <html>
        <head>
            <title>news aggregator :: article-id</title>

            <style>
                body{{
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <h1>news aggregator :: article-id</h1>
            <br><hr><br>
            <a href="/">index</a><br>
            <br><hr><br>
            <input type="text" id="jsonInput" placeholder="id :: (0 : {len(df_dct.keys())-1})" oninput="updateJson()">
            <br><hr><br>
            <pre id="jsonDisplay" style="text-align:justify;white-space: pre-wrap;"></pre>
            
            <script>
                function updateJson() {{
                    io = document.getElementById('jsonInput').value;
                    fetch(`/article-id/` + io).then(response => response.json()).then(data => document.getElementById('jsonDisplay').innerText = JSON.stringify(data, null, 4)).catch(() => document.getElementById('jsonDisplay').innerText = 'Invalid key or data not found');
                }}
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/article-id/{id}")
def read_article_id(id:int):
    if id in df_dct.keys():
        return JSONResponse(content=df_dct[id])
    else:
        return JSONResponse(content={})


@app.get("/search")
def search_article():
    html__search = f"""
    <html>
        <head>
            <title>news aggregator</title>

            <style>
                body{{
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <center>
            <h1>news aggregator :: search-articles</h1>
            <br><hr><br>
            <a href="/">index</a><br>
            <br><hr><br>
            <select id="searchkey" onchange="searchRecords()">
                <option value="title">title</option>
                <option value="summary">summary</option>
                <option value="publication_date">publication_date</option>
                <option value="source">source</option>
                <option value="url">url</option>
                <option value="category" selected>category</option>
            </select>
            <input type="text" id="searchInput" placeholder="value" oninput="searchRecords()">
            </cemter>
            <br><hr><br>
            <pre id="result" style="text-align:justify;white-space: pre-wrap;"></pre>

            <script>
                function searchRecords() {{
                    key = document.getElementById('searchkey').value;
                    value = document.getElementById('searchInput').value;
                    fetch(`/search/` + key + '/' + value).then(response => response.json()).then(data => {{document.getElementById('result').innerText = JSON.stringify(data, null, 4);}}).catch(error => {{document.getElementById('result').innerText = 'Error: ' + error;}});
                }}
            </script>
        </body>
    </html>
    """
    return HTMLResponse(html__search)


@app.get("/search/{key}/{value}")
def search_article_keyword(key: str, value: str):
    filtered_data = {k: v for k, v in df_dct.items() if value.lower() in v.get(key, "").lower()}

    if filtered_data:
        return JSONResponse(content=jsonable_encoder(filtered_data))
    else:
        return JSONResponse(content={})
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('news_aggregator:app',port=8000, reload=True)