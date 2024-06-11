import websocket
import json



class ShogunBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.ws = None

    def on_message(self, ws, message):
        print(f"Received message: {message}")
        # Add battle logic here

    def on_open(self, ws):
        print("Connection opened")
        self.login()

    def login(self):
        login_payload = {
            'act': 'login',
            'name': self.username,
            'pass': self.password
        }
        self.ws.send(json.dumps(login_payload))

    def run(self):
        self.ws = websocket.WebSocketApp(
            "ws://sim.smogon.com:8000/showdown/websocket",
            on_message=self.on_message,
            on_open=self.on_open
        )
        self.ws.run_forever()

if __name__ == "*":
    bot = ShogunBot("your_username", "your_password")
    bot.run()