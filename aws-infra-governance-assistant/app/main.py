from fastapi import FastAPI

from app.api.routes import router

# Creating FastAPI instance
app = FastAPI(
    title="AWS Infra Governance Assistant",
    version="1.0.0"
)

# Mapping routes to the instance
app.include_router(router)