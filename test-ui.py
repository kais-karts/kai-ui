import asyncio
import websockets
import threading
import json
from pynput import keyboard

# from ui_comms import item_pickup, item_hit, players_update, send_debuff, use_buff, init

connected_clients = set()   # To store active websocket connections
broadcast_lock = asyncio.Lock()
item = 0
item_type = "buff"
map_locs = [
    [{"x":2, "y":3, "rank":1, "id": 6},{"x":53, "y":125, "rank":2, "id": 5},{"x":25, "y":50, "rank":3, "id": 4},{"x":0, "y":60, "rank":4, "id": 3},{"x":7, "y":23, "rank":5, "id": 2},{"x":16, "y":35, "rank":6, "id": 1},],
    [{"x":2, "y":3, "rank":1, "id": 5},{"x":53, "y":125, "rank":2, "id": 6},{"x":25, "y":50, "rank":3, "id": 3},{"x":0, "y":60, "rank":4, "id": 4},{"x":7, "y":23, "rank":5, "id": 1},{"x":16, "y":35, "rank":6, "id": 2},],
    [{"x":2, "y":3, "rank":1, "id": 4},{"x":53, "y":125, "rank":2, "id": 5},{"x":25, "y":50, "rank":3, "id": 6},{"x":0, "y":60, "rank":4, "id": 3},{"x":7, "y":23, "rank":5, "id": 2},{"x":16, "y":35, "rank":6, "id": 1},],
]
index = 0

# ---------------- WEBSOCKET SERVER ----------------
async def handler(websocket, path):
    print("Client connected")
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            print(f"Received: {message}")
            # Optionally respond back
            response = f"Server received: {message}"
            await websocket.send(response)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)

async def websocket_server():
    print("Websocket server listening on ws://localhost:5000")
    async with websockets.serve(handler, "localhost", 5000):
        await asyncio.Future()  # run forever


# ---------------- BROADCAST FUNCTION ----------------
async def broadcast(msg: str):
    """
    Broadcasts a JSON-encoded string to all connected websocket clients.
    """
    async with broadcast_lock:
        tasks = []
        for ws in connected_clients:
            tasks.append(ws.send(msg))
        await asyncio.gather(*tasks, return_exceptions=True)


# ---------------- KEYBOARD HANDLING ----------------
async def on_press_async(key):
    global item
    global item_type
    global index
    global map_locs

    try:
        # If the key is an alphanumeric character
        char = key.char
        if char.isdigit():
            item = int(char)
            # Bound the item to 7 if >= 8
            if item >= 8:
                item = 7
        elif char == "d":
            item_type = "debuff"
        elif char == "b":
            item_type = "buff"

    except AttributeError:
        # Handle special keys
        if key == keyboard.Key.enter:
            # Example: item pickup
            msg = json.dumps({
                "action": "item_pickup",
                "item_type": item_type,
                "item": item,
            })
            print(f"[Keyboard] -> item_pickup (item={item})")
            await broadcast(msg)

        elif key == keyboard.Key.space:
            # Example: item hit
            duration = 5
            msg = json.dumps({
                "action": "item_hit",
                "item": item,
                "duration": duration,
            })
            print(f"[Keyboard] -> item_hit (duration={duration})")
            await broadcast(msg)

        elif key == keyboard.Key.shift:
            # Example: use_buff
            duration = 10
            msg = json.dumps({
                "action": "use_buff",
                "item": item,
                "duration": duration
            })
            print(f"[Keyboard] -> use_buff (item={item}, duration={duration})")
            await broadcast(msg)

        elif key == keyboard.Key.ctrl:
            # Example: send_debuff
            msg = json.dumps({
                "action": "send_debuff",
            })
            print("[Keyboard] -> send_debuff")
            await broadcast(msg)

        elif key == keyboard.Key.alt_l:
            # Example: players_update
            rank_data = {"player1": 1, "player2": 2}  # sample data
            msg = json.dumps({
                "action": "players_update",
                "player_status": rank_data
            })
            print(f"[Keyboard] -> players_update {rank_data}")
            await broadcast(msg)
        elif key == keyboard.Key.tab:
            print("index",index,"\n \n")
            msg = json.dumps({
                "action": "players_update",
                "player_status": map_locs[index]
            })
            print(f"[Keyboard] -> players_update {map_locs[index]}")
            index += 1
            if index >= 3:
                index = 0
            await broadcast(msg)

        else:
            # Unrecognized special key
            print(f"Unrecognized trigger key: {key}")


def on_press_wrapper(key, loop):
    """
    Schedules the on_press_async coroutine on the active event loop
    from a separate (blocking) thread.
    """
    asyncio.run_coroutine_threadsafe(on_press_async(key), loop)


def keyboard_func(loop):
    listener = keyboard.Listener(on_press=lambda key: on_press_wrapper(key, loop))
    listener.start()
    listener.join()


# ---------------- MAIN ENTRY POINT ----------------
def main():
    loop = asyncio.get_event_loop()
    # Start websocket server task
    server_task = loop.create_task(websocket_server())

    # Start keyboard listener in a separate thread
    t = threading.Thread(target=keyboard_func, args=(loop,), daemon=True)
    t.start()

    print("Press ENTER, SPACE, SHIFT, CTRL, ALT, or digits (0-7).")
    # Keep the loop running indefinitely
    loop.run_forever()


if __name__ == "__main__":
    main()
