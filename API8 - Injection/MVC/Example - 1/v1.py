from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        path = request.form['path']
        command = f"dir /b {path}"  # Using 'dir' command on Windows
        print (command)
        output = os.popen(command).read()
        print (output)
       
        return render_template('index.html', output=output, path=path)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
