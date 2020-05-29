from views import assets_view, coins_view, index
from config import API_V1_ADDRESS


def init_routes(app) -> None:
    app.router.add_get('/', index)
    app.router.add_get(f'{API_V1_ADDRESS}/assets/', assets_view)
    app.router.add_get(f'{API_V1_ADDRESS}/coins/', coins_view)
