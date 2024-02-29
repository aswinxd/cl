import os
import asyncio
import youtube_dl
from pyrogram import Client, filters
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Initialize Pyrogram client
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
userbot_session = os.getenv("USERBOT_SESSION")

app = Client("music_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# Command to start the bot
@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply("Hello! I'm a music bot. Use the /play command to play a song.")


# Command to play a song
@app.on_message(filters.command("play"))
async def play_song(client, message):
    # Get the song name from the command
    song_name = " ".join(message.command[1:])
    print(f"Received command to play: {song_name}")
    
    # Search for the song on YouTube
    url = await search_youtube(song_name)
    if url:
        print(f"URL for song '{song_name}': {url}")
        # Start streaming the song
        await start_streaming(app, message.chat.id, url)
        await message.reply(f"Streaming song: {song_name}")
    else:
        await message.reply("Song not found on YouTube")


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
async def start_streaming(client, chat_id, url):
    try:
        await client.join_chat(chat_id)
        print(f"Joining chat {chat_id} for streaming")
        await client.send_audio(chat_id, audio=url)
        print("Streaming started successfully")
    except Exception as e:
        print(e)


# Run the bot
async def main():
    await app.start()
    print("Bot started successfully!")
    await asyncio.sleep(1)  # Wait for the bot to fully connect
    await start_userbot_session()
    await asyncio.get_event_loop().run_forever()  # Keep the event loop running


# Start the userbot session
async def start_userbot_session():
    userbot = Client(name=userbot_session, api_id=api_id, api_hash=api_hash)
    await userbot.start()


if __name__ == "__main__":
    asyncio.run(main())
