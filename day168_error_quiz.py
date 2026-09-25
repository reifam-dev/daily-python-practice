"""Day 168 - API Gateway Pattern: Error Quiz. Find and fix three bugs."""
def deals_service(deal_id: str) -> dict:
    return {"deal_id": deal_id, "market_value": 12_500_000.0}


def investors_service(deal_id: str) -> list:
    return ["Fund A", "Fund B"]


class ApiGateway:
    def __init__(self):
        self.routes = {}

    def register_route(self, path: str, handler) -> None:
        self.routes[path] = handler

    def handle_request(self, path: str, *args):
        handler = self.routes[path]
        return handler(args)

    def get_deal_summary(self, deal_id: str) -> dict:
        deal = self.handle_request("/deals", deal_id)
        investors = self.handle_request("/investors", deal_id)
        return {"deal": deal, "investors": investors}


if __name__ == "__main__":
    gateway = ApiGateway()
    gateway.register_route("/deals", deals_service)
    gateway.register_route("/investors", investors_service)
    print(gateway.get_deal_summary("deal-1"))