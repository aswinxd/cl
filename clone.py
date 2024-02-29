import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory

# Load environment variables from .env file
load_dotenv()

app = Client(session_name=os.getenv("SESSION_NAME"), api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"))

# Create a Group Call Factory
group_call_factory = GroupCallFactory(app)

@app.on_message(filters.command("start", prefixes="!"))
async def start(client, message):
    group_call = group_call_factory.get_group_call()

    if not message.chat.id in group_call.full_chat.id:
        await group_call.join(message.chat.id)
        await message.reply("Bot joined the chat")
    else:
        await message.reply("Bot is already in the chat")

@group_call.on_playout_ended
async def playout_ended(group_call, source):
    await app.send_message(group_call.full_chat.id, f"Finished playing {source['input']}")
    # You can add logic here to play the next song in a playlist

@app.on_message(filters.command("play", prefixes="!"))
async def play(client, message):
    group_call = group_call_factory.get_group_call()

    if not group_call.is_connected:
        await message.reply("Bot is not connected to a voice chat")
        return

    # You can replace this with the actual source from Youtube, Spotify, etc.
    audio_source = "song.mp3"

    await group_call.start_playout(audio_source)
    await message.reply(f"Started playing {audio_source}")

@app.on_message(filters.command("stop", prefixes="!"))
async def stop(client, message):
    group_call = group_call_factory.get_group_call()

    if group_call.is_connected:
        await group_call.stop_playout()
        await message.reply("Stopped playing")
    else:
        await message.reply("Bot is not playing anything")

app.run()
