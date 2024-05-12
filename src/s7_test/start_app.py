import uvicorn
from s7_test.application.application import App

app = App()

uvicorn.run(app.start())
