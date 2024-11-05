from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import instaloader
import os

# Your bot's token from BotFather
bot = Client("instagram_reels_bot", bot_token="7921162807:AAEwyG8ZK5HJC6-6fr7kapJeWa_y_FYg7Hs", api_id="13323016", api_hash="68e791e616100248b0a53ae86a661a12")

# Initialize Instaloader
loader = instaloader.Instaloader()

# Replace with the Instagram username of the public account you want to fetch reels from
public_account = "filmygyan"

@bot.on_message(filters.command("lazy") & filters.private)
async def fetch_reels(bot, message):
    await message.reply_text("Fetching reels from Instagram...")

    # Load the public profile
    profile = instaloader.Profile.from_username(loader.context, public_account)
    
    # Iterate over the posts and filter for videos (reels)
    reels = [post for post in profile.get_posts() if post.typename == "GraphVideo"]

    if not reels:
        await message.reply_text("No reels found on this account.")
        return

    # Send each reel to your Telegram channel
    for reel in reels:
        try:
            # Send video URL
            await bot.send_message("-1001895607162", reel.video_url)
            if reel.caption:
                await bot.send_message("-1001895607162", reel.caption)
        except Exception as e:
            await message.reply_text(f"Failed to send reel: {e}")

    await message.reply_text("All reels have been sent to the channel.")

# Start the bot
bot.run()
