from fastapi import FastAPI
from server.routes import auth_routes, news_routes, user_routes, external_server_routes, category_routes, \
    user_notification_routes, article_routes, blocked_keyword_routes, article_preference_routes, \
    article_read_history_routes
from server.scheduler.news_sync_scheduler import start_news_sync_scheduler

app = FastAPI(
    title="News Aggregation",
    description="A RESTful API for news aggregation"
)

app.include_router(auth_routes.router)
app.include_router(news_routes.router)
app.include_router(user_routes.router)
app.include_router(external_server_routes.router)
app.include_router(category_routes.router)
app.include_router(user_notification_routes.router)
app.include_router(article_routes.router)
app.include_router(blocked_keyword_routes.router)
app.include_router(article_preference_routes.router)
app.include_router(article_read_history_routes.router)
start_news_sync_scheduler()


@app.get("/")
def read_root():
    return {"message": "Welcome to the News Aggregation API!"}