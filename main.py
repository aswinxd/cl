import asyncio
import os
import shutil
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from pytgcalls.exceptions import NoActiveGroupCall

# Initialize Pyrogram Client
app = Client("assistant")

# Initialize GroupCallFactory
group_call = GroupCallFactory(app).get_file_group_call()

# Command to play music
@app.on_message(filters.command("play"))
async def play_music(client, message):
    if message.reply_to_message and message.reply_to_message.audio:
        audio = message.reply_to_message.audio
        file_path = await message.reply_to_message.download()
        try:
            await group_call.start(message.chat.id)
            await group_call.join(message.chat.id, file_path)
        except NoActiveGroupCall:
            await message.reply_text("No active group call.")
        os.remove(file_path)

# Run the assistant client
async def run():
    await app.start()
    await app.idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
