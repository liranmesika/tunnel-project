
class Proxy:

    def __init__(self, ip, port, protocol, user, password):
        self._ip = ip
        self._port = port
        self._protocol = protocol
        self._user = user
        self._password = password

    def __repr__(self):
        return f"(ip={self._ip}, port={self._port}, protocol={self._protocol}, " \
               f"user={self._user}, password={self._password})"

    def get_ip(self):
        return self._ip

    def get_port(self):
        return self._port

    def get_protocol(self):
        return self._protocol

    def get_user(self):
        return self._user

    def get_password(self):
        return self._password
