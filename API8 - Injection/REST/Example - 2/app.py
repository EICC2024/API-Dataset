import os

from flask import Flask

app = Flask(__name__)


@app.get("/uptime", defaults={"flag": None})
@app.get("/uptime/<string:flag>")
def display_uptime(flag):
    command = "uptime"
    if flag:
        command += f" -{flag}"

    output = os.popen(command).read()

    return {"output": output}