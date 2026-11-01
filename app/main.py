from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.contact_api import router as contact_router
from app.api.favorite_api import router as favorite_router
from app.exceptions import ContactError

app = FastAPI(title="Contact Manager API", description="API for managing contacts", version="1.0.0")
@app.exception_handler(ContactError)
def contact_error_handler(request: Request, exc: ContactError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(contact_router, prefix="/contacts", tags=["contacts"])
app.include_router(favorite_router, prefix="/favorites", tags=["favorites"])