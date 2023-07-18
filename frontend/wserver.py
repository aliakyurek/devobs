import json

from flask import (
    Flask,
    render_template,
)
import common
import logging
import pandas as pd
from backend.device_manager import DeviceManager
import time
import humanize

app = Flask(__name__)
app.logger.setLevel(logging.getLogger().level)
logging.getLogger('werkzeug').setLevel(logging.getLogger().level)

# Flask routes and endpoints
@app.route('/api/devices')
def devices():
    # conn = common.connect_to_db()
    # Query to retrieve data from the database
    # query = "SELECT * FROM devices"
    # df = pd.read_sql(query, conn)
    # conn.close()
    df = DeviceManager.get_instance().cache
    if df is not None:
        return df.to_json(orient="split")
    else:
        return "{}"

@app.route('/api/devices/<int:device_id>/prompt')
def get_device_prompt(device_id):
    dm = DeviceManager.get_instance()
    prompt = dm.devices[device_id].get_prompt()
    return json.dumps(prompt)

@app.route('/')
def home():
    dm = DeviceManager.get_instance()
    last_update=humanize.naturaltime(dm.cache_time-time.time())
    return render_template("app.html", version=common.VERSION, last_update=last_update)

def main():
    app.run(port=5000)

