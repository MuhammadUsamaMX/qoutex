import json
from quotexpy.ws.channels.base import Base
from quotexpy.expiration import get_expiration_time_quotex

class Time_Buy(Base):
    """Class for placing pending orders based on trade start time on Quotex."""

    name = "time_buy"

    def __call__(self, order_type: str, asset: str, duration: int, trade_start_time: int, amount: int, request_id: int):
        """Place a pending order based on trade start time."""
        option_type = 100 if "_otc" not in asset.strip().lower() else 1
        duration = get_expiration_time_quotex(trade_start_time, duration)

        payload = {
            "openType": 1 if order_type == "call" else 0,
            "asset": asset,
            "openPrice": "",  # You can specify the open price here if needed
            "timeframe": duration,
            "command": order_type,
            "amount": amount,
        }
        data = f'42["pending/create",{json.dumps(payload)}]'
        self.send_websocket_request(data)

        response = self.get_websocket_response()

        # Handle the response
        if response:
            parsed_response = json.loads(response)
            # You can do further processing of the response here
            print("Time_Buy order response:", parsed_response)
        else:
            print("No response received for Time_Buy order request.")
