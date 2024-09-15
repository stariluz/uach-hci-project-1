from python_event_bus import EventBus

@EventBus.on("new_cli")
def on_event():
    print("Nuevo cliente")