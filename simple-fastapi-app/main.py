import socket
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    hostname = socket.gethostname()
    html_content = f"""
    <html>
        <head>
            <title>Simple Application</title>
            <style>
                body {{
                    background-color: #0072c9;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}
                div {{
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div>
                <h1>Hello, world!</h1>
                <h2>This is {hostname}</h2>
            </div>
        </body>
    </html>
    """
    return html_content
