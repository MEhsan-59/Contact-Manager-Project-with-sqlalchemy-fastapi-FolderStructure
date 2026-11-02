from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.contact_api import router as contact_router
from app.api.favorite_api import router as favorite_router
from app.exceptions import AppException
from app.api.group_api import router as group_router
from sqlalchemy.exc import SQLAlchemyError


app = FastAPI(title="Contact Manager API", description="API for managing contacts", version="1.0.0")

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = []
    for error in exc.errors():
        serialized_error = error.copy()
        context = error.get("ctx")
        if context:
            serialized_error["ctx"] = {
                key: str(value) if isinstance(value, Exception) else value
                for key, value in context.items()
            }
        details.append(serialized_error)

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation error occurred in input data.",
                "details": details
            }
        }
    )

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Error occurred while processing data in the database."
            }
        }
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Unknown technical error occurred. Please contact support."
            }
        }
    )

app.include_router(contact_router, prefix="/contacts", tags=["contacts"])
app.include_router(favorite_router, prefix="/favorites", tags=["favorites"])
app.include_router(group_router, prefix="/groups", tags=["groups"])