"""Entry point for generic Python HTTP runner: uvicorn main:app.

Imports the pre-built Flask app from app.py and wraps it as ASGI.
"""

import os

from asgiref.wsgi import WsgiToAsgi

from app import app as _flask_app

app = WsgiToAsgi(_flask_app)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
