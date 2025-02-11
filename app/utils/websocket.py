import os
import json
import asyncio
import struct
import websockets
from websockets.exceptions import ConnectionClosed
from websockets.protocol import State

class DhanWebSocketClient:
    def __init__(self):
        self.base_url = "wss://api-feed.dhan.co"
        self.token = os.getenv("DHAN_ACCESS_TOKEN")
        self.client_id = os.getenv("DHAN_CLIENT_ID")
        self.auth_type = "2"
        self.websocket = None
        self.connections = set()  # ✅ Track all active connections

    async def connect(self):
        """Establish WebSocket connection with retry logic."""
        ws_url = f"{self.base_url}?version=2&token={self.token}&clientId={self.client_id}&authType={self.auth_type}"
        print(f"🔌 Connecting to WebSocket: {ws_url}")

        try:
            self.websocket = await websockets.connect(ws_url)
            self.connections.add(self.websocket)  # ✅ Track active connection
            print("✅ WebSocket Connection Established!")
        except Exception as e:
            print(f"❌ WebSocket Connection Error: {e}")
            self.websocket = None

    async def is_connected(self):
        """Check if WebSocket is connected."""
        return self.websocket and self.websocket.state is State.OPEN

    async def subscribe_to_instruments(self, instruments):
        """Subscribe to new instruments."""
        if not await self.is_connected():
            print("⚠️ WebSocket is not connected. Attempting to reconnect...")
            await self.connect()
            if not await self.is_connected():
                print("❌ Unable to subscribe. WebSocket is still not connected.")
                return

        if not instruments:
            print("⚠️ No instruments to subscribe.")
            return

        instrument_list = [
            {"ExchangeSegment": "NSE_EQ", "SecurityId": str(ins["SEM_SMST_SECURITY_ID"])}
            for ins in instruments
        ]

        request_payload = {
            "RequestCode": 15,
            "InstrumentCount": len(instrument_list),
            "InstrumentList": instrument_list
        }

        print(f"📡 Subscribing to {len(instrument_list)} instruments...")
        print(f"➡️ Subscription Request Sent: {json.dumps(request_payload, indent=2)}")

        await self.websocket.send(json.dumps(request_payload))

    async def listen(self):
        """Continuously listen for messages from WebSocket."""
        print("🟢 Listening for incoming WebSocket messages...")

        while True:
            try:
                # ✅ Use recv_streaming() for handling large fragmented messages
                async for message in self.websocket.recv_streaming():
                    if isinstance(message, (bytes, bytearray)):  
                        parsed_data = self.parse_binary_message(message)
                        print(f"📩 Parsed Market Data: {parsed_data}")
                    else:
                        print(f"📩 Received Text Message: {message}")

            except asyncio.TimeoutError:
                print("⏳ No messages received in 30s. Sending PONG to keep connection alive...")
                try:
                    await self.websocket.pong()
                except Exception as e:
                    print(f"⚠️ Failed to send Pong: {e}")

            except ConnectionClosed:
                print("🔴 WebSocket Disconnected! Reconnecting...")
                await asyncio.sleep(5)
                await self.connect()
                return

    def parse_binary_message(self, message):
        """Decode binary WebSocket message from Dhan."""
        try:
            message = bytes(message)
            
            # ✅ Unpack the Response Header (Fix Byte Ranges!)
            response_code, msg_length, exchange_segment, security_id = struct.unpack(">BHB I", message[0:8])

            print(f"📝 Parsed Header: response_code={response_code}, msg_length={msg_length}, exchange_segment={exchange_segment}, security_id={security_id}")

            if response_code == 2:  # ✅ Ticker Data
                last_traded_price = struct.unpack("<f", message[8:12])[0]  # ✅ Read bytes 8-11
                last_trade_time = struct.unpack("<I", message[12:16])[0]  # ✅ Read bytes 12-15

                print(f"📊 Ticker Data: security_id={security_id}, last_traded_price={last_traded_price}, last_trade_time={last_trade_time}")

                return {
                    "response_code": response_code,
                    "security_id": security_id,
                    "exchange_segment": exchange_segment,
                    "last_traded_price": last_traded_price,
                    "last_trade_time": last_trade_time
                }

            elif response_code == 4:  # ✅ Quote Data
                last_traded_price, last_traded_qty, last_traded_time, avg_trade_price, volume = struct.unpack(">fHIfI", message[8:24])
                
                print(f"📊 Quote Data: security_id={security_id}, last_traded_price={last_traded_price}, last_traded_qty={last_traded_qty}, volume={volume}")

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

        except struct.error as e:
            return {"error": f"Failed to decode binary message: {str(e)}", "raw_message": message.hex()}


    async def run(self, instruments):
        """Run WebSocket client with updated instruments."""
        await self.connect()
        await self.subscribe_to_instruments(instruments)
        await self.listen()

# ✅ Instantiate WebSocket client
ws_client = DhanWebSocketClient()
