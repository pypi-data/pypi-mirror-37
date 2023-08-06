# -*- coding: utf-8 -*-
import json

from flask import Flask, request, jsonify
import socket
from univider.settings import app_user
from univider.logger import Logger

app = Flask(__name__)
logger = Logger(__name__).getlogger()

@app.route("/crawl", methods=['GET', 'POST'])
def crawl():
    # parse needs
    data = request.get_data()
    params = json.loads(data)
    node = socket.gethostname()
    # authentication
    if (params.has_key("user") and params.has_key("secret") and params["secret"] == app_user.get(params["user"])):
        # handle needs
        from univider.fetcher import Fetcher
        fetcher = Fetcher()
        result = fetcher.fetch_page_with_cache(params)
    else:
        if (params.has_key("user")):
            logger.info(params["user"] + ' Authentication failed ' )
        else:
            logger.info('Unknown user Authentication failed '+str(params))
        result = {
            'status': 'error',
            'node' : node,
            'description': 'Authentication failed.'
        }

    # return needs
    return jsonify(result)
    # return result["html"].decode('gbk')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5010,debug=False)

def main():
    app.run(host='0.0.0.0',port=5010,debug=False)