from typing import Optional, Type
from fastapi import FastAPI
from sanic import Sanic
from sanic.config import Config
from core.config import get_settings
from core.db_factory import DBFactory
from infrastructure.sqlite3.session import init_db as init_sqlite
from infrastructure.mongodb.session import init_db as init_mongo

settings = get_settings()

class AppFactory:
    """Factory for creating web applications with different frameworks"""
    
    @staticmethod
    def create_app(framework: str = "fastapi", db: str = "sqlite") -> Optional[Type]:
        """Create a web application based on the specified framework
        
        Args:
            framework: Web framework to use ("fastapi" or "sanic")
            db: Database to use ("sqlite" or "mongo")
        """
        # Set database type for DBFactory
        DBFactory.set_db_type(db)
        
        if framework.lower() == "fastapi":
            return AppFactory._create_fastapi_app(db)
        elif framework.lower() == "sanic":
            return AppFactory._create_sanic_app(db)
        else:
            raise ValueError(f"Unsupported framework: {framework}")

    @staticmethod
    def _create_fastapi_app(db: str) -> FastAPI:
        from presentation.api.v1.post_router import router as post_router
        
        app = FastAPI(
            title=settings.PROJECT_NAME,
            openapi_url=f"{settings.API_V1_STR}/openapi.json"
        )
        
        @app.on_event("startup")
        async def startup_event():
            if db == "sqlite":
                init_sqlite()
            elif db == "mongo":
                await init_mongo()
        
        # Include routers
        app.include_router(post_router, prefix=settings.API_V1_STR)
        
        return app

    @staticmethod
    def _create_sanic_app(db: str) -> Sanic:
        from presentation.sanic.routes.post_routes import bp as post_bp
        from presentation.sanic.routes.comment_routes import bp as comment_bp
        from presentation.sanic.middleware.error_handler import ErrorHandler
        
        # Configure Sanic
        config = Config()
        config.update({
            "API_VERSION": "v1",
            "API_TITLE": settings.PROJECT_NAME,
            "API_DESCRIPTION": "A flexible blog service with hexagonal architecture",
            "API_TERMS_OF_SERVICE": "Use with caution",
            "API_CONTACT_EMAIL": "your.email@example.com",
            "API_LICENSE_NAME": "MIT",
            "CORS_ORIGINS": "*",
            "CORS_ALLOW_HEADERS": "*",
            "CORS_ALLOW_METHODS": "*",
        })
        
        app = Sanic(settings.PROJECT_NAME, config=config)
        
        # Add error handlers
        error_handler = ErrorHandler()
        app.error_handler = error_handler
        
        @app.before_server_start
        async def init_db(app, _):
            if db == "sqlite":
                init_sqlite()
            elif db == "mongo":
                await init_mongo()
        
        # Register blueprints with versioned prefix
        app.blueprint(post_bp, url_prefix=f"{settings.API_V1_STR}/posts")
        app.blueprint(comment_bp, url_prefix=f"{settings.API_V1_STR}/comments")
        
        return app
