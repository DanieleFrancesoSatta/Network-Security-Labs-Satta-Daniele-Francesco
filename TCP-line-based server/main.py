
import threading
import sys
from pydoc import resolve
from selectors import SelectSelector
from typing import reveal_type
from xmlrpc import client, server
import csv
import socket
IP_ADDRESS = "0.0.0.0"

PORT = 9001
keys_values_dict={}

def handle_client(connection, client_address,lock):
    buffer = ""
    while True:

        data = connection.recv(1024)
        if not data:
            break
        msg = data.decode()
        print(msg)

        buffer += msg

        while '\n' in buffer:
            riga, buffer = buffer.split("\n", 1)
            riga = riga.rstrip("\r")
            responce = process_command(str(riga),lock)

            connection.send(responce.encode() + b"\n")


def process_command(command,lock):
    tmp=command.split(" ",1)[0]

    match tmp:
        case "PING":
            return ("PONG")
        case "SET":
            try:

                lock.acquire(blocking=True)


                key_value = command.split(" ", 1)[1]
                key = key_value.split(" ", 1)[0]
                value = key_value.split(" ", 1)[1]
                if not value:
                    return ("ERR")
                store_key( key, value)
                lock.release()
                print(f"[{key}]--> ({value})")
                return "OK"
            except Exception as e:
                lock.release()
                return ("ERR")
        case "ECHO":
            try:
                msg= command.split(" ",1)[1]
                return (msg)
            except:
                return ("ERR")
        case "GET":
            try:
                lock.acquire()
                key= command.split(" ",1)[1]
                if key not in keys_values_dict:
                    lock.release()
                    return ("NOT_FOUND")
                else:
                    lock.release()
                    return keys_values_dict[key]
            except Exception as e:
                lock.release()
                return ("ERR")
        case _:
            return ("ERR")





def store_key(key,value):
    keys_values_dict[key]=value

def get_key(key):
    return keys_values_dict[key]

def connect_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((IP_ADDRESS, PORT))
        server.listen(5)
        return server
    except Exception as e:
        print(f"Connection error: {e}")
        raise Exception(f"Connection error: {e}")



def start_server():
    threads=[]
    lock=threading.Lock()

    try:
        try:

            server = connect_server()
            while True:
                connection, client_address = server.accept()
                thread=threading.Thread(target=handle_client, args=(connection, client_address,lock))
                threads.append(thread)
                print(f"Connection from: {client_address}")
                thread.start()


        except Exception as e:
            print(f"Connection error: {e}")


    except KeyboardInterrupt:
        connection.close()
        print("Server closed")
    finally:
        connection.close()

if __name__ == "__main__":
    start_server()
