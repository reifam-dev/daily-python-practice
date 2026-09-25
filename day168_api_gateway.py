"""Day 168 - API Gateway Pattern: a single entry point routes to and
aggregates results from multiple backend services, so a client makes
one call instead of coordinating several - PCPP1 standard."""
from __future__ import annotations
from collections.abc import Callable


def deals_service(deal_id: str) -> dict:
    return {"deal_id": deal_id, "market_value": 12_500_000.0}


def investors_service(deal_id: str) -> list[str]:
    return ["Fund A", "Fund B"]


class UnknownRouteError(Exception):
    pass


class ApiGateway:
    def __init__(self) -> None:
        self.routes: dict[str, Callable] = {}

    def register_route(self, path: str, handler: Callable) -> None:
        self.routes[path] = handler

    def handle_request(self, path: str, *args):
        if path not in self.routes:
            raise UnknownRouteError(f"No route registered for {path}")
        handler = self.routes[path]
        return handler(*args)

    def get_deal_summary(self, deal_id: str) -> dict:
        deal = self.handle_request("/deals", deal_id)
        investors = self.handle_request("/investors", deal_id)
        return {"deal": deal, "investors": investors}


if __name__ == "__main__":
    gateway = ApiGateway()
    gateway.register_route("/deals", deals_service)
    gateway.register_route("/investors", investors_service)
    print(gateway.get_deal_summary("deal-1"))