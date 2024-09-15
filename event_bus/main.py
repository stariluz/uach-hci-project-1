from python_event_bus import EventBus
from . import message_event

def init():
    EventBus.call("message", "Event bus is running")

if __name__== "__main__":
    init()