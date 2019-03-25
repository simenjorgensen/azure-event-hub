import json
from flask import Flask, request
from azure.eventhub import EventHubClient, Offset
from ast import literal_eval
import logging
import cherrypy
import os

app = Flask(__name__)

ADDRESS = os.environ.get('ADDRESS')

# Access tokens for event hub namespace, from Azure portal for namespace
USER = os.environ.get('USER')
KEY = os.environ.get('KEY')
CONSUMER_GROUP = os.environ.get('CONSUMER_GROUP')
PARTITION = "0"

if not ADDRESS:
    logging.error("No event hub address supplied")

@app.route('/', methods=['GET', 'POST'])
def get():
    if request.args.get('since') is None:
        since = -1
    else:
        since = request.args.get('since')
    lastoffsetvalue = Offset(since)
    client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
    try:
        receiver = client.add_receiver(CONSUMER_GROUP, PARTITION, prefetch=5000, offset=lastoffsetvalue)
        client.run()
        output = '['
        for event_data in receiver.receive(timeout=1000):
            # parse x:
            last_sn = event_data.sequence_number
            json_string = str(event_data.message)
            json_dict = literal_eval(json_string)
            json_dict.update({"_updated": str(last_sn)})
            output += json.dumps(json_dict) + ','
        output = output.rstrip(',') + ']'
    except KeyboardInterrupt:
        pass
    finally:
        client.stop()

    return output


if __name__ == '__main__':
    cherrypy.tree.graft(app, '/')

    # Set the configuration of the web server to production mode
    cherrypy.config.update({
        'environment': 'production',
        'engine.autoreload_on': False,
        'log.screen': True,
        'server.socket_port': 5000,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
