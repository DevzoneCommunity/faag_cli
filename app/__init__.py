from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.config import AppConfig, Constants, generate_settings
from app.controller import private_fast_app
from app.schemas import CommonResponseSchema
from app.utils.logger import logger


def create_fast_app() -> FastAPI:
    app_settings: AppConfig = generate_settings()
    base_app = FastAPI(**app_settings.fastapi_kwargs)
    base_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return base_app


sample_app: FastAPI = create_fast_app()

# Add all your public routes here
# sample_app.include_router(
#     router=sample_public_router,
#     prefix=f"{Constants.BASE_SLUG}/public",
# )


@sample_app.get(f"{Constants.BASE_SLUG}/public/ping", tags=["Health Check"])
def ping():
    function_name = "Ping - Health Check"
    logger.info(
        message=f"Enter - {function_name}",
        function_name=function_name,
    )
    return JSONResponse(
        CommonResponseSchema(message="Health check ping working for public", status="Ok").dict(),
        status_code=status.HTTP_200_OK,
    )


sample_app.mount(f"{Constants.BASE_SLUG}/private", private_fast_app)
