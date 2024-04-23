from fastapi import FastAPI
from fastapi_pagination import add_pagination
from workout_api.routers import api_router as router

app = FastAPI(title="WorkoutApi")
app.include_router(router=router)

if __name__ == 'main':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)

add_pagination(app)