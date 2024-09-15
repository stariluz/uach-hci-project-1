from python_event_bus import EventBus

@EventBus.on("connect")
def on_connect_event(message):
    print(f"Connection. {message}")
