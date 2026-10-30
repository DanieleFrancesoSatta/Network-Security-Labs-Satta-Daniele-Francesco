
from flask import Flask, request, jsonify
PORT=  8080

IP_ADDR= '0.0.0.0'


app=Flask(__name__)

notepad={}
next_id=0

@app.route('/')
def handle_ROOT():
    return "",200

@app.route('/echo')
def handle_echo():
    msg= request.args.get('msg')
    return jsonify({'msg': msg})
    

@app.route('/notes', methods=['POST'])
def handle_post_notes():
    
    if not request.is_json:
        return jsonify({"error": "Unsupported Media Type"}), 415

    dati = request.get_json(silent=True)

    if dati is None:
        return jsonify({"error": "Malformed JSON"}), 400
    
    text=dati.get('text')
    if not isinstance(text,str):
        return jsonify({"error": "Missing or non-string text"}), 400

    
    global next_id
    id=next_id
    notepad[next_id] = text
    next_id=next_id+1
    return jsonify({'id': id}),201
    

@app.route('/notes/<int:id>', methods=['GET'])
def handle_get_notes(id):
    
    if id not in notepad:
        return jsonify({"error": "Not found"}), 404
    return jsonify({'id': id, 'text': notepad[id]})


@app.route('/notes/<int:id>', methods=['DELETE'])
def handle_delete(id):
    if id in notepad:
        del notepad[id]
        
        return "",204
    else:
        return jsonify({"error": "Not found"}), 404

if __name__== '__main__':
    app.run(host=IP_ADDR, port=PORT)

