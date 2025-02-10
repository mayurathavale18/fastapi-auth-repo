import os
import json
import asyncio
import struct  # Required for binary parsing
import websockets

class DhanWebSocketClient:
    def __init__(self):
        self.base_url = "wss://api-feed.dhan.co"
        self.token = os.getenv("DHAN_ACCESS_TOKEN")
        self.client_id = os.getenv("DHAN_CLIENT_ID")
        self.auth_type = "2"
        self.websocket = None

    async def connect(self):
        """Establish WebSocket connection."""
        ws_url = f"{self.base_url}?version=2&token={self.token}&clientId={self.client_id}&authType={self.auth_type}"
        print(f"🔌 Connecting to WebSocket: {ws_url}")

        try:
            self.websocket = await websockets.connect(ws_url)
            print("✅ WebSocket Connection Established!")
        except Exception as e:
            print(f"❌ WebSocket Connection Failed: {e}")
            return

    async def subscribe_to_instruments(self, instruments):
        """Subscribe to new instruments."""
        if not self.websocket:
            print("⚠️ WebSocket is not connected. Reconnecting...")
            await self.connect()
            if not self.websocket:
                return

        if not instruments:
            print("⚠️ No instruments to subscribe.")
            return

        # Prepare subscription message
        instrument_list = [
            {"ExchangeSegment": ins["SEM_EXM_EXCH_ID"], "SecurityId": ins["SEM_SMST_SECURITY_ID"]}
            for ins in instruments
        ]

        request_payload = {
            "RequestCode": 15,  # Subscribe to ticker feed
            "InstrumentCount": len(instrument_list),
            "InstrumentList": instrument_list
        }

        print(f"📡 Subscribing to {len(instrument_list)} instruments...")
        await self.websocket.send(json.dumps(request_payload))

    async def listen(self):
        """Continuously listen for messages from WebSocket."""
        print("🟢 Listening for incoming WebSocket messages...")

        while True:
            try:
                message = await self.websocket.recv()

                if isinstance(message, bytes):  # Check if the response is binary
                    parsed_data = self.parse_binary_message(message)
                    print(f"📩 Parsed Market Data: {parsed_data}")
                else:
                    print(f"📩 Received Text Message: {message}")

            except websockets.exceptions.ConnectionClosed:
                print("🔴 WebSocket Disconnected! Reconnecting...")
                await asyncio.sleep(5)
                await self.connect()
                return

    def parse_binary_message(self, message):
        """Decode binary WebSocket message from Dhan."""
        try:
            # Read Response Code (1 byte) + Message Length (2 bytes) + Exchange Segment (1 byte) + Security ID (4 bytes)
            response_code, msg_length, exchange_segment, security_id = struct.unpack(">BHBI", message[:8])

            if response_code == 2:  # Ticker Data (LTP)
                last_traded_price = struct.unpack(">f", message[8:12])[0]
                return {
                    "response_code": response_code,
                    "security_id": security_id,
                    "exchange_segment": exchange_segment,
                    "last_traded_price": last_traded_price
                }

            elif response_code == 4:  # Quote Data (Full Trade Data)
                last_traded_price, last_traded_qty, last_traded_time, avg_trade_price, volume = struct.unpack(">fHIfI", message[8:24])
                return {
                    "response_code": response_code,
                    "security_id": security_id,
                    "exchange_segment": exchange_segment,
                    "last_traded_price": last_traded_price,
                    "last_traded_qty": last_traded_qty,
                    "last_traded_time": last_traded_time,
                    "avg_trade_price": avg_trade_price,
                    "volume": volume
                }

            return {"unknown_binary_message": message.hex()}

        except Exception as e:
            return {"error": f"Failed to decode binary message: {str(e)}"}

    async def run(self, instruments):
        """Run WebSocket client with updated instruments."""
        await self.connect()
        await self.subscribe_to_instruments(instruments)
        await self.listen()

# ✅ Instantiate WebSocket client
ws_client = DhanWebSocketClient()
