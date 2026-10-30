
from flask import Flask, request, jsonify
import threading
from werkzeug.serving import make_server
PORT_VPN=  8090
PORT_ONION=8080

VPN_IP_ADDR= '0.0.0.0'

ONION_ADDR= "127.0.0.1"

app_VPN=Flask('vpn')

app_ONION=Flask('onion')

notepad=""

@app_ONION.route(f"/", methods=['GET'])
def handle_get():
    return "",200

@app_ONION.route('/claim', methods=['POST'])
def handle_post_claim():
    try:
        global notepad
        
        token = request.get_data(as_text=True).strip()
        if not token:
            return "Missing Token", 400
        print(f"Token received: {token}")
        notepad=token
        return "",200

    except Exception as e:
        return "Error",400

@app_VPN.route('/claim', methods=['GET'])
def handle_get_claim():
    global notepad
    try:
        if notepad:
            return notepad, 200
        else:
            return "", 200 

    except Exception as e:
        return "Token not found", 404





def start_server(PORT,IP,app):

    server = make_server(IP, PORT, app, threaded=True)

    print(f"-------- Server listening on {IP}:{PORT}-------------")
    
    
    server.serve_forever() 


if __name__== '__main__':
    """1. Onion site
                GET http://<address>.onion/ → 200
        2. Proof of ownership
            POST http://<address>.onion/claim with a token in the body (plain text) → 200
            GET http://<your VPN IP>:8090/claim → the last token received, as plain text
            The onion service and port 8090 on your VPN address must therefore share their state.

        3. Client authorization
            The service must be reachable only by authorized clients: enable v3 client authorization with the course public key (netsec.auth, in the attachments), to be copied into the authorized_clients directory of the service.
            A client without the key must be rejected; the checker uses the course key for parts 1 and 2."""
    
    t_VPN=threading.Thread(target=start_server,args=(PORT_VPN,VPN_IP_ADDR,app_VPN),daemon=True)

    t_ONION=threading.Thread(target=start_server, args=(PORT_ONION,ONION_ADDR,app_ONION),daemon=True)

    t_ONION.start()

    t_VPN.start()
    
    t_ONION.join()

    t_VPN.join()

