from app.parsers import ryanair_parser
from app.services.notifier import notify_users
from app.db.db import get_all_subscribers

def parse():
    print("🔁 Scheduler запущено")

    users = get_all_subscribers()
    if not users:
        print("❗ Немає підписок")
        return

    all_results = []

    for user in users:
        user_id, month, price = user
        for origin in ["BTS", "BUD", "VIE"]:
            tickets = ryanair_parser.get_ryanair_tickets(origin, month, price)
            all_results.extend([(user_id, ticket) for ticket in tickets])

    # відправка результатів
    for user_id, ticket_text in all_results:
        notify_users(user_id, ticket_text)
