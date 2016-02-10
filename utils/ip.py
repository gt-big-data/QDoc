import socket

_ip = None

def _set_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    global _ip
    _ip = s.getsockname()[0]

def get_ip_address():
    # Only get the IP address once because it won't change and it's (relatively) expensive to obtain.
    if _ip is None:
        _set_ip_address()
    return _ip
