import pickle
import requests
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Factory
from utils import SERVER_PORT, DISCONNECT_MESSAGE, Commands
from .proxy import Proxy
from .proxies_list import ProxiesList
from .tor import Tor


PROXY_PATH = "{protocol}://{host}:{port}"
PROXY_PATH_WITH_CREDENTIALS = "{protocol}://{user}:{password}@{host}:{port}"
TOR_PORT = 9050


class ClientsAmount:

    def __init__(self):
        self.clients_amount = 0

    def get(self):
        return self.clients_amount

    def add(self):
        self.clients_amount += 1

    def subtract(self):
        self.clients_amount -= 1


class Server(protocol.Protocol):

    def __init__(self, proxies_list, tor, clients_amount):
        self.clients_amount = clients_amount
        self.command_dict = {}
        self.proxies_list = proxies_list
        self.tor = tor

    def add_proxy_command_handler(self):
        print(100 * "=" + "\n\nAdd Proxy Command:\n")
        proxy = Proxy(self.command_dict["ip"], self.command_dict["port"], self.command_dict["protocol"],
                      self.command_dict["user"], self.command_dict["password"])
        self.proxies_list.add_proxy(proxy)
        print(f"Server added proxy {proxy}:\n\n{self.proxies_list}")
        self.transport.write(f"Server added proxy {proxy}".encode())

    def remove_proxy_command_handler(self):
        print(100 * "=" + "\n\nRemove Proxy Command:\n")
        proxy_ip = self.command_dict["ip"]
        proxy_removed = self.proxies_list.remove_proxy(proxy_ip)
        if proxy_removed:
            print(f"Server removed proxy {proxy_removed}:\n\n{self.proxies_list}")
            self.transport.write(f"Server removed proxy {proxy_removed}".encode())
        else:
            print(f"Server does not contain this proxy")
            self.transport.write(f"Server does not contain this proxy".encode())

    def setup_tor_command_handler(self):
        print(100 * "=" + "\n\nSetup Tor Command:\n")
        if self.tor.is_tor_set_up():
            print(f"Tor is already setup\n")
            self.transport.write(f"Tor is already setup".encode())
            return
        self.tor.setup()
        print(f"Server setup Tor\n")
        self.transport.write(f"Server setup Tor".encode())

    def teardown_tor_command_handler(self):
        print(100 * "=" + "\n\nTeardown Tor Command:\n")
        if not self.tor.is_tor_set_up():
            print(f"Tor is already teardown\n")
            self.transport.write(f"Tor is already teardown".encode())
            return
        self.tor.teardown()
        print(f"Server teardown Tor\n")
        self.transport.write(f"Server teardown Tor".encode())

    def run_requests_command(self, url, proxies=None):
        if proxies is None:
            proxies = {}
        print(f"Server run command:\nrequests.get(url={url}, proxies={proxies})\n")
        try:
            response = requests.get(url=url, proxies=proxies)
            print("Command ended successfully\n")
            self.transport.write(f"Response from {url}:\n{response.json()}".encode())
        except requests.exceptions.RequestException as exception:
            print(f"Command failed: {exception}\n")
            self.transport.write(f"Server failed to connect {url}".encode())

    def connect_via_proxy_command_handler(self):
        print(100 * "=" + "\n\nConnect URL via Proxy Command:\n")
        proxy_ip = self.command_dict["proxy_ip"]

        # empty proxies_list, connect URL directly, without proxies
        if proxy_ip == "":
            print(f"Empty proxies list\n")
            self.run_requests_command(self.command_dict["url"])
            return
        if not self.proxies_list.is_contains_proxy(proxy_ip):
            print(f"Server does not contain this proxy\n")
            self.transport.write(f"Server does not contain this proxy".encode())
            return
        proxy = self.proxies_list.get_proxy(proxy_ip)
        proxy_path = PROXY_PATH_WITH_CREDENTIALS.format(protocol=proxy.get_protocol(),
                                                        user=proxy.get_user(),
                                                        password=proxy.get_password(),
                                                        host=proxy.get_ip(),
                                                        port=proxy.get_port())
        self.run_requests_command(self.command_dict["url"], {"http": proxy_path, "https": proxy_path})

    def connect_via_tor_command_handler(self):
        print(100 * "=" + "\n\nConnect URL via Tor Command:\n")
        if not self.tor.is_tor_set_up():
            print(f"Tor is currently teardown, client should setup it first\n")
            self.transport.write(f"Tor is currently teardown, you should setup it first".encode())
            return
        proxy_path = PROXY_PATH.format(protocol="socks5h",
                                       host="localhost",
                                       port=TOR_PORT)
        self.run_requests_command(self.command_dict["url"], {"http": proxy_path, "https": proxy_path})

    def quit_command_handler(self):
        print(100 * "=" + "\n\nQuit Command:\n")
        print(f"Client asked to quit, send a disconnect message\n")
        self.transport.write(DISCONNECT_MESSAGE.encode())

    def connectionMade(self):
        print(100 * "=" + "\n\nConnection from new client\n")
        self.clients_amount.add()
        print(f"There are currently {self.clients_amount.get()} clients connected\n")
        self.transport.write("Welcome client!\n\nAvailable commands:\n"
                             "1 - For add new proxy to server\n"
                             "2 - For remove proxy from server\n"
                             "3 - For setup Tor\n"
                             "4 - For teardown Tor\n"
                             "5 - For connect URL via proxy\n"
                             "6 - For connect URL via Tor\n"
                             "7 - For quit".encode())

    def connectionLost(self, reason):
        print(100*"=" + "\n\nClient disconnected from server\n")
        print(f"Connection lost reason:\n{reason}\n")
        self.clients_amount.subtract()
        print(f"There are currently {self.clients_amount.get()} clients connected\n")

    def dataReceived(self, data):
        self.command_dict = pickle.loads(data)
        command = self.command_dict["command"]
        if command == Commands.ADD_PROXY.value:
            self.add_proxy_command_handler()
        elif command == Commands.REMOVE_PROXY.value:
            self.remove_proxy_command_handler()
        elif command == Commands.SETUP_TOR.value:
            self.setup_tor_command_handler()
        elif command == Commands.TEARDOWN_TOR.value:
            self.teardown_tor_command_handler()
        elif command == Commands.CONNECT_URL_VIA_PROXY.value:
            self.connect_via_proxy_command_handler()
        elif command == Commands.CONNECT_URL_VIA_TOR.value:
            self.connect_via_tor_command_handler()
        elif command == Commands.QUIT.value:
            self.quit_command_handler()
        else:
            print("Wrong command, try Again\n")


class ServerFactory(Factory):

    def __init__(self):
        self.proxies_list = ProxiesList()
        self.tor = Tor()
        self.clients_amount = ClientsAmount()

    def buildProtocol(self, addr):
        return Server(self.proxies_list, self.tor, self.clients_amount)


def main():
    print("Start Server\n")
    reactor.listenTCP(SERVER_PORT, ServerFactory())
    reactor.run()


if __name__ == '__main__':
    main()
