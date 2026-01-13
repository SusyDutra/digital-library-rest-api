# main.py
from fastapi import FastAPI
from app.controllers.book_controller import router as book_router
from app.controllers.user_controller import router as user_router
from app.controllers.loan_controller import router as loan_router
from app.controllers.author_controller import router as author_router
from app.middleware.logging import LoggingMiddleware
from app.logging_config import configure_logging, get_logger

# Configure logging
configure_logging()
logger = get_logger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Digital Library API",
        version="1.0.0",
        description="API REST for digital library management"
    )

    app.add_middleware(LoggingMiddleware)

    app.include_router(book_router, prefix="/api/v1", tags=["Livros"])
    app.include_router(author_router, prefix="/api/v1", tags=["Autores"])
    app.include_router(user_router, prefix="/api/v1", tags=["Usuários"])
    app.include_router(loan_router, prefix="/api/v1", tags=["Empréstimos"])

    logger.info("Digital Library API started")
    return app

app = create_app()
