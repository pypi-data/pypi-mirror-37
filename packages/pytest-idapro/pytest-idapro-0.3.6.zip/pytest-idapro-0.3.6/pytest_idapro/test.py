from ida_netnode import netnode


class MC(type):
    def __new__(cls, *args, **kwargs):
        print("MC new")
        return super(MC, cls).__new__(cls, *args, **kwargs)

class Proxy(netnode):
    def __new__(cls, *args, **kwargs):
        print("Proxy new")
        return super(Proxy, cls).__new__(cls, *args, **kwargs)


nn = Proxy(
