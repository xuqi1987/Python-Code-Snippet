import socket
from flask import Flask
app = Flask(__name__)

serverip = "136.17.76.243"
@app.route('/hostname/<name>')
def hostname(name):
	addr = socket.gethostbyname(name)
    	return addr 


@app.route('/synergy/server/<ip>')
def synergy_server(ip):
	if len(ip) >0:
		serverip=ip
	return serverip

@app.route('/synergy/<ip>')
def synergy_get_server(ip):
	return serverip



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8999)
