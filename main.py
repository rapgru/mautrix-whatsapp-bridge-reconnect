#!/bin/python3
import asyncio
import json
import os
import sys
from asyncio import sleep

from nio import AsyncClient, LoginResponse

async def main() -> None:
    # open the file in read-only mode
    client = AsyncClient(os.environ['HOMESERVER'])
    client.access_token = os.environ['ACCESS_TOKEN']
    client.user_id = os.environ['USER_ID']
    client.device_id = os.environ['DEVICE_ID']

    # Now we can send messages as the user
    room_id = os.environ['ROOM_ID']

    await client.room_send(
        room_id,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": "ping"
        }
    )

    lastString = "ping"
    timeout = 10
    while lastString == "ping" and timeout > 0:
        timeout = timeout - 1
        await sleep(1)
        sync_response = await client.sync(1000)
        if len(sync_response.rooms.join) > 0:
            joins = sync_response.rooms.join
            events = joins[room_id].timeline.events

            lastString = events[len(events) - 1].body

    if lastString != "Connection to WhatsApp OK":
        await client.room_send(
            room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": "reconnect"
            }
        )

    await client.close()


asyncio.get_event_loop().run_until_complete(main())


