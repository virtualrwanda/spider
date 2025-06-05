
from flask import Flask, render_template, request
import paramiko

app = Flask(__name__)

# List of hosted apps on the Pi
web_apps = [
    {"name": "Dashboard App", "url": "http://192.168.193.124:8000"}
]

# SSH settings
SSH_HOST = "192.168.193.124"  # or actual Pi IP
SSH_USER = "lion"
SSH_PASS = "1234"

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    error = ''
    if request.method == 'POST':
        command = request.form.get('command', '')

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASS)
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            ssh.close()
        except Exception as e:
            error = str(e)

    return render_template('index.html', apps=web_apps, output=output, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
