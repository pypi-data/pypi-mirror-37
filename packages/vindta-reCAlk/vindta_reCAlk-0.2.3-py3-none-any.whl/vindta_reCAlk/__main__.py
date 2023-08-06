#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import

def main():
    from numpy.random import randint
    import threading
    import webbrowser

    from vindta_reCAlk import app

    port = 7523

    url = "http://localhost:{:d}/".format(port)
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()

    app.run(port=port, debug=False)


if __name__ == '__main__':
    main()
