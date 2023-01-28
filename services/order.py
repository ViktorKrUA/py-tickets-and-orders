from datetime import datetime
from django.db.models import QuerySet
from django.db import transaction
from db.models import Order, Ticket
from django.contrib.auth import get_user_model


def create_order(
        tickets: list, username: str, date: datetime = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username).values_list()
    return Order.objects.all()