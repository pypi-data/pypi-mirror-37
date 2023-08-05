from .cofan import *
import sys
import argparse

parser = argparse.ArgumentParser(description='Serve files over http.')
parser.add_argument(
        '-a', '--addr', type=str, action='store', default='localhost:8000',
        help='http bind address in the form <ip>:<port>'
    )
parser.add_argument(
        'root', action='store', nargs='?', default='.',
        help='root directory to serve through http'
    )


args = parser.parse_args()

addr = args.addr.split(':')
addr[1] = int(addr[1])
root = args.root

provider = Patterner()
icons = Iconer()
if pathlib.Path(root).is_dir():
    browser = Filer(root, iconer=icons)
else:
    browser = Ziper(root, iconer=icons)

provider.add('__icons__/', icons)
provider.add('', browser)

handler = BaseHandler(provider)

srv = Server(tuple(addr), handler)
print('serving {} at {}:{}'.format(pathlib.Path(root).resolve(), *addr))
try:
    srv.serve_forever()
except KeyboardInterrupt:
    pass
