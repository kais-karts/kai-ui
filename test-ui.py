import threading
# import keyboard
from pynput import keyboard
from flask import Flask, request, render_template
from flask_socketio import SocketIO 
from flask_socketio import emit 
import asyncio
import websockets

app = Flask(__name__)
socketio = SocketIO(app)
item = 0


def item_pickup(item: int) -> None:
    """
    Updates the UI when a new item is picked up
    """
    socketio.emit('item_pickup', {'item': item})


def item_hit(item: int) -> None:
    """
    Updates UI when player is hit with item
    """
    socketio.emit('item_hit', {'item': item})

def item_use(duration: float) -> None:
    """
    Updates UI when player uses an item
    """
    socketio.emit('item_use', {'duration': duration})

async def handler(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            response = f"Server received: {message}"
            await websocket.send(response)  # Send response back to client
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")


def flask():
    # Run Flask (via SocketIO) in the main thread
    socketio.run(app, port=8000, debug=True, use_reloader=False)

def on_press(key):
    global item
    try:
        char = key.char
        if char.isdigit():
            item = int(char)
            if item >= 8:
                item = 7
    except AttributeError:
        if key == keyboard.Key.enter:
            print("Item Pickup")
            item_pickup(item)
        elif key == keyboard.Key.space:
            print("Item Hit")
            item_hit(item)
        elif key == keyboard.Key.shift:
            print("Item Use")
            item_use(item)
        else:
            print(f"Unrecognized trigger key: {key}")

def main():
    """
    The main function will set up the keyboard listener in a separate thread
    so that we can still run the Flask app in the main thread.
    """
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    # Run the keyboard listener in a background thread
    threading.Thread(target=main, daemon=True).start()
    flask()
    # main()
