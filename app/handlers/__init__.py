from .handlers_search import router as search_router
from .handlers_general import router as general_router  

def register_handlers(dp):
    dp.include_router(general_router)
    dp.include_router(search_router)
