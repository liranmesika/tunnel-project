
class ProxiesList:

    def __init__(self):
        self._proxies = []

    def __repr__(self):
        if len(self._proxies) == 0:
            return "Proxies list is empty\n"
        repr_string = "Proxies list:\n"
        for proxy in self._proxies:
            repr_string += str(proxy) + "\n"
        return repr_string

    def add_proxy(self, proxy):
        self._proxies.append(proxy)

    def remove_proxy(self, ip):
        for i in range(len(self._proxies)):
            if self._proxies[i].get_ip() == ip:
                return self._proxies.pop(i)

    def get_proxy(self, ip):
        for proxy in self._proxies:
            if proxy.get_ip() == ip:
                return proxy
        return None

    def is_contains_proxy(self, proxy_ip):
        server_proxies_ips = [proxy.get_ip() for proxy in self._proxies]
        return proxy_ip in server_proxies_ips
