import hashlib

async def app(scope, receive, send):
    if scope["type"] != "http":
        return

    method = scope["method"]
    path = scope["path"]
    version = str(scope.get("http_version", "1.1"))

    # --- GET / ---
    if method == "GET" and path == "/":
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({"type": "http.response.body", "body": b"OK\n"})
        return

    # GET /proto
    if method == "GET" and path == "/proto":
        if version.startswith("3"):
            body = b"HTTP/3"
        elif version.startswith("2"):
            body = b"HTTP/2"
        else:
            body = b"HTTP/1.1"

        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({"type": "http.response.body", "body": body})
        return



    if method == "POST" and path=="/hash":
        more_body=True
        body=b""
        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)

        body_hashed= hashlib.sha256(body).hexdigest().encode()

        print(f"Recived message: {body}")
        print(f"Hashed and sent message: {body_hashed}")

        await send({
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [(b"content-type", b"text/plain")],
                })
        await send({"type": "http.response.body", "body": body_hashed})