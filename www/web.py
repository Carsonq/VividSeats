# -*- coding: utf-8 -*-
__author__ = 'carson.qin'

from Challenge import create_app

web = create_app()

if __name__ == "__main__":
    web.run(use_reloader=False, threaded=True, port=5000, host='0.0.0.0')
