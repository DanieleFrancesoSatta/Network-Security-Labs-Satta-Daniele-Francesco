from flask import Flask, jsonify, request, make_response
import uuid
import threading
import ssl
from werkzeug.serving import make_server
host_address ="0.0.0.0"

TLS_SERVER_PORT = 8443

session= {}

certificate_authentication_port= 8443

mTSL_Port=8444
cert_path = "server.crt"
key_path = "server.key"

app_main = Flask('main')
app_mtls= Flask('mtsl')


def save_session(user):
    try:
        token = str(uuid.uuid4())
        session[token]=user
        resp= make_response("",200)
        
        resp.set_cookie('session', token, secure=True, httponly=True)
        return resp
    except Exception as e:
        raise (e)
    
@app_main.route('/', methods=['GET'])
def index():
    return "",200

@app_main.route('/login', methods=['POST'])
def login():
    try:

        data = request.get_json()
        if not data:
            return "",400

        user= data.get('user')
        password= data.get('password')
        if (password == 'netsec'):
            resp= save_session(user)
            
            return resp
        else:
            return   "",401  
    except Exception as e:
        print(f"Login Error: {e}")
        return "",400


@app_main.route('/me', methods=['GET'])
def getMe():
    userID= request.cookies.get('session')
    if not userID:
        return "", 401
    else:
        return jsonify({"user": session[userID]})


def avvia_server(app, host, port, ssl_contesto):
    
    server = make_server(host, port, app, ssl_context=ssl_contesto, threaded=True)

    print(f"------------Server Linstening on {host}:{port}----------")
    
    
    server.serve_forever() 


@app_mtls.route('/whoami')
def whoami():
    sock = request.environ.get('werkzeug.socket')
    if not sock:
        return "", 500
    
    client_cert =sock.getpeercert()
    if not client_cert:
        return "", 401
    
    client_cn = dict(x[0] for x in client_cert['subject'])['commonName']
    return client_cn, 200



if __name__ == '__main__':
    context8433= ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context8433.load_cert_chain(certfile=cert_path,keyfile=key_path)

    context8444 = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context8444.load_cert_chain(certfile=cert_path, keyfile=key_path)


    context8444.verify_mode = ssl.CERT_REQUIRED 
    context8444.load_verify_locations(cafile="ca.crt") 



    thread_8443 = threading.Thread(target=avvia_server, args=(app_main, host_address, certificate_authentication_port, context8433),daemon=True)
    
    thread_8444 = threading.Thread(target=avvia_server, args=(app_mtls, host_address, mTSL_Port, context8444),daemon=True)

    thread_8443.start()
    thread_8444.start()

    thread_8443.join()
    thread_8444.join()