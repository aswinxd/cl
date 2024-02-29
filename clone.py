import os
import asyncio
import youtube_dl
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory, GroupCall
from pytgcalls.exceptions import GroupCallNotFound
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Initialize Pyrogram client
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
userbot_session = os.getenv("USERBOT_SESSION")

app = Client("music_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# Initialize GroupCallFactory
group_call_factory = GroupCallFactory(app)


# Command to play a song
@app.on_message(filters.command("play"))
async def play_song(client, message):
    # Get the song name from the command
    song_name = " ".join(message.command[1:])
    
    # Search for the song on YouTube
    url = await search_youtube(song_name)
    if url:
        # Start streaming the song
        group_call = await start_streaming(message.chat.id, url)
        if group_call:
            await message.reply(f"Streaming song: {song_name}")
        else:
            await message.reply("Failed to start streaming")
    else:
        await message.reply("Song not found on YouTube")


# Command to clone the bot
@app.on_message(filters.command("clone"))
async def clone(client, message):
    # Extract the token from the command arguments
    if len(message.command) != 2:
        await message.reply_text("Usage: /clone <token>")
        return
    token = message.command[1]

    # Set the bot token as environment variable
    os.environ["BOT_TOKEN"] = token

    # Run initialization
    await app.start()
    await message.reply_text("Bot successfully cloned!")


# Search for a song on YouTube
async def search_youtube(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extractaudio': True,
        'audioformat': 'mp3',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch1:{song_name}", download=False)
            if 'entries' in info:
                return info['entries'][0]['url']
        except Exception as e:
            print(e)
            return None


# Start streaming the song
async def start_streaming(chat_id, url):
    try:
        group_call = group_call_factory.get_file_group_call()
        await group_call.join(chat_id)
        success = await group_call.start_audio(url, repeat=False)
        if success:
            return group_call
        else:
            return None
    except GroupCallNotFound:
        return None


# Run the bot
async def main():
    await app.start()
    print("Bot started successfully!")
    await asyncio.sleep(1)  # Wait for the bot to fully connect
    await start_userbot_session()
    await app.idle()


# Start the userbot session
async def start_userbot_session():
    userbot = Client(session_name=userbot_session, api_id=api_id, api_hash=api_hash)
    await userbot.start()


if __name__ == "__main__":
    asyncio.run(main())
