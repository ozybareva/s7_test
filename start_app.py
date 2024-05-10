import uvicorn
from application.application import App

app = App()

uvicorn.run(app.start())
