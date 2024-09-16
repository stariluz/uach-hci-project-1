from .main import app, run
from .web_sockets import ws_app, run as ws_run

if __name__=="__main__":
    ws_run()