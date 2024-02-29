from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid
from py_tgcalls import PyTgCalls
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Client(
    "my_bot",
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

pytgcalls = PyTgCalls(app)

# Dictionary to store active group calls
active_group_calls = {}

@app.on_message(filters.command("start"))
async def start(bot, update):
    await update.reply_text("Hello! I am your Group Calls Streaming bot. Use /help to see available commands.")

@app.on_message(filters.command("help"))
async def help(bot, update):
    help_text = """
    Available commands:
    /play <link>: Play audio from supported platforms.
    /pause: Pause the currently playing track.
    /resume: Resume the paused track.
    /stop: Stop the current playback and leave the call.
    """
    await update.reply_text(help_text)

@app.on_message(filters.command("play"))
async def play(bot, update):
    try:
        # Check if the user is in a group
        if update.chat.type != "group" and update.chat.type != "supergroup":
            await update.reply_text("Please add me to a group to use this command.")
            return

        # Get the provided link from the message
        link = update.command[1]
        
        # Check the type of link and handle accordingly (e.g., YouTube, Spotify, etc.)
        # Stream the content using Py-Tgcalls

        # For demonstration, let's just reply with the link being played
        await update.reply_text(f"Streaming: {link}")

        # Start streaming in the group call
        chat_id = update.chat.id
        if chat_id not in active_group_calls:
            active_group_calls[chat_id] = pytgcalls.join_group_call(chat_id)
        
        # For demonstration, let's assume we're using some placeholder audio file
        audio_file = "path_to_audio_file.mp3"
        await active_group_calls[chat_id].start_audio(audio_file)
        
    except IndexError:
        await update.reply_text("Please provide a valid link.")

@app.on_message(filters.command("pause"))
async def pause(bot, update):
    # Pause the currently playing track in the group call
    chat_id = update.chat.id
    if chat_id in active_group_calls:
        await active_group_calls[chat_id].pause_audio()
        await update.reply_text("Track paused.")
    else:
        await update.reply_text("No active playback.")

@app.on_message(filters.command("resume"))
async def resume(bot, update):
    # Resume the paused track in the group call
    chat_id = update.chat.id
    if chat_id in active_group_calls:
        await active_group_calls[chat_id].resume_audio()
        await update.reply_text("Track resumed.")
    else:
        await update.reply_text("No active playback.")

@app.on_message(filters.command("stop"))
async def stop(bot, update):
    # Stop the current playback and leave the call
    chat_id = update.chat.id
    if chat_id in active_group_calls:
        await active_group_calls[chat_id].stop_audio()
        del active_group_calls[chat_id]
        await update.reply_text("Playback stopped.")
    else:
        await update.reply_text("No active playback.")

# Add more handlers for other commands and functionalities

app.run()
