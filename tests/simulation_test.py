from math import e
import signal
import asyncio
import argparse
import numpy as np
from nats.aio.client import Client as NATS
from gym_nats.utils import Channels, numpy_decode, numpy_encode

async def main(loop):
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--host', default='0.0.0.0', required=False)
    parser.add_argument('-p', '--port', default='4222', required=False)
    parser.add_argument('-u', '--user', default=None, required=False)
    parser.add_argument('-a', '--password', default=None, required=False)

    args = parser.parse_args()

    nats = NATS()
    connection_string = "nats://"
    if args.user is not None and args.password is not None:
        connection_string += f"{args.user}:{args.password}@"
    connection_string += f"{args.host}:{args.port}"

    async def error_cb(e):
        print("Error:")
        print(e)

    async def closed_cb():
        print("Connection to NATS is closed.")
        await asyncio.sleep(0.1)
        loop.stop()

    options = {
        "io_loop": loop,
        "error_cb": error_cb,
        "closed_cb": closed_cb
    }

    await nats.connect(connection_string, **options)

    np.random.seed(123)

    async def update_callback(msg):
        print(f"Sent update")
        await nats.publish(msg.reply, numpy_encode(np.array([1, 2, 3]).astype(np.float64)))

    async def reward_callback(msg):
        await nats.publish(msg.reply, numpy_encode(np.array([10]).astype(np.float64)))

    async def action_callback(msg):
        await nats.publish(msg.reply, b'')

    async def reset_callback(msg):
        await nats.publish(msg.reply, b'')

    async def actions_callback(msg):
        await nats.publish(msg.reply, numpy_encode(np.random.randint(0, 1, 2).astype(dtype=np.float64)))

    async def done_callback(msg):
        await nats.publish(msg.reply, numpy_encode(np.array([-1]).astype(np.float64)))

    def signal_handler():
        if nats.is_closed:
            return
        print("Disconnecting...")
        loop.create_task(nats.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)

    await nats.subscribe(Channels.UPDATE.value, cb=update_callback)
    await nats.subscribe(Channels.REWARD.value, cb=reward_callback)
    await nats.subscribe(Channels.ACTION.value, cb=action_callback)
    await nats.subscribe(Channels.RESET.value, cb=reset_callback)
    await nats.subscribe(Channels.ACTIONS.value, cb=actions_callback)
    await nats.subscribe(Channels.DONE.value, cb=done_callback)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()