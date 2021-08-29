from enum import Enum

SERVER_PORT = 9999
DISCONNECT_MESSAGE = "Goodbye client!"


class Commands(Enum):
    ADD_PROXY = "1"
    REMOVE_PROXY = "2"
    SETUP_TOR = "3"
    TEARDOWN_TOR = "4"
    CONNECT_URL_VIA_PROXY = "5"
    CONNECT_URL_VIA_TOR = "6"
    QUIT = "7"

