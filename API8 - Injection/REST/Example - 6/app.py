from flask import Flask, request
from pathlib import Path
import subprocess

app = Flask(__name__)
path = Path(__file__)

@app.route("/dns")
def page():

    hostname = request.values.get(hostname)
    cmd = 'nslookup ' + hostname

    return subprocess.check_output(cmd, shell=True)