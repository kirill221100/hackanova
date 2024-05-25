from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from db.db_setup import init_db
from config import config
from routes.user import user_router
from routes.team import team_router
from routes.tag import tag_router


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=db_lifespan, debug=config.DEBUG, title='ToDo')
app.include_router(user_router, prefix='/user', tags=['user'])
app.include_router(team_router, prefix='/team', tags=['team'])
app.include_router(tag_router, prefix='/tag', tags=['tag'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
