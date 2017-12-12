import flask
import json
import os
import hbase_manager

PROD_PATH = os.environ.get('PROD')
CLUSTER_CONFIG_PATH = PROD_PATH + '/conf/cluster_conf.json'
CLUSTER_CONFIG = json.loads(open(CLUSTER_CONFIG_PATH).read())
MASTER_HOST = CLUSTER_CONFIG['masterHost']
WEB_APP_PORT = CLUSTER_CONFIG['webAppPort']
HBASE_PORT = CLUSTER_CONFIG['hbaseThriftPort']

class Server(flask.Flask):

    def __init__(self, import_name):
        super(Server, self).__init__(import_name)
        self.hbase = hbase_manager.HBaseManager()

app = Server('Lyrics Web App')

@app.route("/")
def hello():
    return flask.render_template('index.html')

@app.route('/vendor/<path:path>')
def send_static(path):
    split_path = path.split('/')
    path, filename = os.path.join(*split_path[:-1]), split_path[-1]
    return flask.send_from_directory(os.path.join('static/vendor', path), filename)

if __name__ == "__main__":
    app.run(host=MASTER_HOST, port=WEB_APP_PORT)