import pickle
from twisted.internet import reactor, protocol
from utils import SERVER_PORT, DISCONNECT_MESSAGE, Commands


class Client(protocol.Protocol):

    def dataReceived(self, data):
        print(f"\nMessage from server:\n{data.decode()}")
        if data.decode() == DISCONNECT_MESSAGE:
            reactor.stop()
            return

        wrong_command = True
        while wrong_command:
            command = input("\n" + 50 * "=" + "\n\nEnter command:\n")
            if command in [item.value for item in Commands]:
                wrong_command = False

            if command == Commands.ADD_PROXY.value:
                self.add_proxy_command_handler(command)
            elif command == Commands.REMOVE_PROXY.value:
                self.remove_proxy_command_handler(command)
            elif command == Commands.SETUP_TOR.value or command == Commands.TEARDOWN_TOR.value:
                self.tor_command_handler(command)
            elif command == Commands.CONNECT_URL_VIA_PROXY.value:
                self.connect_via_proxy_command_handler(command)
            elif command == Commands.CONNECT_URL_VIA_TOR.value:
                self.connect_via_tor_command_handler(command)
            elif command == Commands.QUIT.value:
                self.quit_command_handler(command)
            else:
                print("Wrong command, try Again")

    def add_proxy_command_handler(self, command):
        ip = input("Enter proxy IP:\n")
        port = input("Enter proxy port:\n")
        protocol = input("Enter protocol:\n")
        user = input("Enter user:\n")
        password = input("Enter password:\n")

        command_dict = {"command": command, "ip": ip, "port": port, "protocol": protocol,
                        "user": user, "password": password}
        self.transport.write(pickle.dumps(command_dict))

    def remove_proxy_command_handler(self, command):
        ip = input("Enter proxy IP:\n")
        command_dict = {"command": command, "ip": ip}
        self.transport.write(pickle.dumps(command_dict))

    def tor_command_handler(self, command):
        command_dict = {"command": command}
        self.transport.write(pickle.dumps(command_dict))

    def connect_via_proxy_command_handler(self, command):
        proxies = input("Enter proxy IP:\n")
        url = input("Enter url:\n")
        command_dict = {"command": command, "proxy_ip": proxies, "url": url}
        self.transport.write(pickle.dumps(command_dict))

    def connect_via_tor_command_handler(self, command):
        url = input("Enter url:\n")
        command_dict = {"command": command, "url": url}
        self.transport.write(pickle.dumps(command_dict))

    def quit_command_handler(self, command):
        command_dict = {"command": command}
        self.transport.write(pickle.dumps(command_dict))


class ClientFactory(protocol.ClientFactory):

    def buildProtocol(self, addr):
        return Client()


def main():
    print("Start Client")
    reactor.connectTCP("localhost", SERVER_PORT, ClientFactory())
    reactor.run()


if __name__ == '__main__':
    main()


