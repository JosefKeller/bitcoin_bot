import fastapi
import database
import pydantic_models
import config

api = fastapi.FastAPI()


@api.get('/hello')
def api_hello():
    return {"hello":'from api!'}
