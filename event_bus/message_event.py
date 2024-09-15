from python_event_bus import EventBus

@EventBus.on("message")
def on_message_event(message):
    print(f"Message event. {message}")
    
@EventBus.on("qt5_message")
def on_qt5_message_event(message):
    print(f"QT5. {message}")

@EventBus.on("ws_message")
def on_ws_message_event(message):
    print(f"WS. {message}")


