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

app = Client("music_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# Command to play a song
@app.on_message(filters.command("play"))
async def play_song(client, message):
    # Get the song name from the command
    song_name = " ".join(message.command[1:])
    
    # Search for the song on YouTube
    url = await search_youtube(song_name)
    if url:
        # Start streaming the song
        await start_streaming(message.chat.id, url)
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
async def start_streaming(chat_id, url):
    try:
        await app.send_audio(chat_id, audio=url)
    except Exception as e:
        print(e)


# Run the bot
async def main():
    await app.start()
    print("Bot started successfully!")
    await asyncio.gather(app.idle())

if __name__ == "__main__":
    asyncio.run(main())
