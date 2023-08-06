import http.client
import random

VATSIM_STATUS_HOST = "status,vatsim,net"


def choose_server():
    return random.choice(get_status_servers())


def get_status_servers():
    """
    get a set of all available status servers live

    heads up, vatsim gets angry if you hit this too often, so make sure you cache the result on your side

    :return `set` of possible URLs that can be fetched to get the wazzup:
    """
    conn = http.client.HTTPSConnection(VATSIM_STATUS_HOST)

    headers = {
        'Cache-Control': "no-cache",
        'User-Agent': "vatstat python library"
    }

    conn.request("GET", "", headers=headers)

    res = conn.getresponse()
    data = res.read()

    possible_servers = set()

    for line in iter(data.splitlines()):
        if line.startswith("url0="):
            possible_servers.add(line.split("=")[1])

    return possible_servers
