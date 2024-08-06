from sort_db import sort_db, sort_known
from sort_readme import sort_readme
from maskt2ipv4 import maskt2ipv4
from make_amnezia import make_amnezia
from make_wireguard import make_wireguard
from make_route_bat import make_route_bat


if __name__ == '__main__':
    # maskt2ipv4()
    sort_readme()
    sort_known()
    sort_db()
    make_amnezia()
    make_wireguard()
    make_route_bat()