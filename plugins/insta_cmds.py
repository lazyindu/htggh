#MIT License

#Copyright (c) 2021 subinps

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from config import Config
from instaloader import Profile
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
import os
from utils import *
import time
from instaloader import Post
from utils import download_insta, upload
import asyncio

USER=Config.USER
OWNER=Config.OWNER
HOME_TEXT_OWNER=Config.HOME_TEXT_OWNER
HELP=Config.HELP
HOME_TEXT=Config.HOME_TEXT
session=f"./{USER}"
STATUS=Config.STATUS

insta = Config.L
buttons=InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/subinps'),
            InlineKeyboardButton("🤖Other Bots", url="https://t.me/subin_works/122")
        ],
        [
            InlineKeyboardButton("🔗Source Code", url="https://github.com/subinps/Instagram-Bot"),
            InlineKeyboardButton("🧩Deploy Own Bot", url="https://heroku.com/deploy?template=https://github.com/subinps/Instagram-Bot")
        ],
        [
            InlineKeyboardButton("👨🏼‍🦯How To Use?", callback_data="help#subin"),
            InlineKeyboardButton("⚙️Update Channel", url="https://t.me/subin_works")
        ]
					
    ]
    )

channels = {
    "@real_MoviesAdda7": "filmygyan",
    # "@telegram_channel_2": "instagram_page_2",
    # Add more Instagram page - Telegram channel pairs as needed
}


from pyrogram import Client, filters
from instaloader import Instaloader, Profile
import os

@Client.on_message(filters.command("scrap") & filters.private)
async def scrap_reels(bot, message):
    try:
        # Parse the command arguments
        args = message.command[1:]
        if len(args) != 2:
            await message.reply_text("Usage: /scrap {username} {number_of_reels}")
            return
        
        username = args[0]
        num_reels = int(args[1])
        
        # Check if the user is logged in
        if 1 not in Config.STATUS:
            await message.reply_text("You are not logged in. Please use /login first.")
            return
        
        # Load the profile and get the reels
        profile = Profile.from_username(insta.context, username)
        reels = [post for post in profile.get_posts() if post.typename == 'GraphVideo'][:num_reels]
        
        # Check if there are enough reels
        if not reels:
            await message.reply_text(f"No reels found for @{username}.")
            return
        
        # Send the reels back to the user
        for reel in reels:
            await bot.send_video(
                chat_id=message.from_user.id,
                video=reel.video_url,
                caption=f"🎥 Reels from @{username}\n\nCaption: {reel.caption}\nLikes: {reel.likes}"
            )
        
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
        print(f"An error occurred: {e}")




# @Client.on_message(filters.command("scrap") & filters.private)
# async def scrap_reels(bot, message):
#     if str(message.from_user.id) != OWNER:
#         await message.reply_text("You are not authorized to use this command.")
#         return

#     # Get the command arguments
#     command_args = message.command[1:]
#     if len(command_args) != 2:
#         await message.reply_text("Usage: /scrap {username} {no_of_reels}")
#         return

#     target_username = command_args[0]
#     try:
#         no_of_reels = int(command_args[1])
#     except ValueError:
#         await message.reply_text("Please provide a valid number for reels.")
#         return

#     # Notify the user that the scraping has started
#     m = await message.reply_text(f"Fetching {no_of_reels} reels from {target_username}...")

#     try:
#         # Load the session
#         insta.load_session_from_file(USER)
        
#         # Fetch the profile using the loaded session
#         profile = Profile.from_username(insta.context, target_username)

#         reels_count = 0  # Counter for fetched reels
#         reels_urls = []  # List to store reels URLs

#         # Iterate through posts and collect reels
#         for post in profile.get_posts():
#             if post.is_video:  # Check if the post is a reel
#                 reels_urls.append(post.video_url)  # Add the reel URL to the list
#                 reels_count += 1

#                 if reels_count >= no_of_reels:  # Stop when the required number is fetched
#                     break

#         if reels_urls:
#             # Prepare the response message with the URLs of the reels
#             response = "\n".join(reels_urls)
#             await m.edit(f"Fetched {len(reels_urls)} reels from {target_username}:\n{response}")
#         else:
#             await m.edit(f"No reels found for {target_username}.")

#     except Exception as e:
#         await m.edit(f"An error occurred: {str(e)}")
#         print(f"An error occurred: {str(e)}")


@Client.on_message(filters.command("automate") & filters.private)
async def automate(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text("You are not authorized to use this command.")
        return

    # Specify the username you want to fetch reels from
    target_username = "filmygyan"  # Replace this with the target username

    # Notify the user that the automation has started
    m = await message.reply_text(f"Fetching reels from {target_username}...")


    # Loop through the posts in the profile
    try:
        insta.load_session_from_file(USER)

        # Fetch the profile using Instaloader
        profile = Profile.from_username(insta.context, target_username)
    
        reels_count = 0  # Counter for fetched reels
        for post in profile.get_posts():
            # Check if the post is a reel (Instagram Reels are video posts)
            if post.is_video:
                reels_count += 1
                # Download the reel
                command = ['instaloader', f'--no-captions', f'--no-metadata-json', f'--no-profile-pic', f'--no-video-thumbnails', f'--dirname-pattern={USER}/reels', post.shortcode]
                await download_insta(command, m, f"{USER}/reels")
                
                # After downloading, upload to Telegram
                await upload(m, bot, message.from_user.id, f"{USER}/reels/{post.shortcode}.mp4")
                
            # Optionally, you can break after fetching a specific number of reels if desired
            if reels_count >= 5:  # Change this number as needed
                break

        await m.edit(f"Successfully fetched {reels_count} reels from {target_username}.")

    except Exception as e:
        await m.edit(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")


# @Client.on_message(filters.command("automate"))
# async def automate_handler(client, message):
#     # Step 1: Verify the user and check if they have the required permissions
#     # if not is_user_authorized(message.from_user.id):
#     #     await message.reply("You are not authorized to use this command.")
#     #     return
    
#     # Step 2: Prompt for Instagram username
#     await message.reply("Please enter the Instagram username you want to automate reels for:")
    
#     # Step 3: Wait for the user's response with the username
#     username_response = await client.wait_for_message(chat_id=message.chat.id, reply_to_message_id=message.message_id)
#     username = username_response.text.strip()

#     # Step 4: Confirm the automation process
#     confirm_markup = InlineKeyboardMarkup(
#         [[InlineKeyboardButton("Yes", callback_data=f"confirm_automate#{username}"),
#           InlineKeyboardButton("No", callback_data="cancel_automate")]]
#     )
#     await message.reply(f"You've selected: {username}. Do you want to proceed?", reply_markup=confirm_markup)

# @Client.on_callback_query(filters.regex(r"confirm_automate#"))
# async def confirm_automate_callback(client, callback_query):
#     username = callback_query.data.split("#")[1]
    
#     await callback_query.answer()  # Acknowledge the callback
    
#     # Step 5: Start the automation process
#     await callback_query.message.edit_text(f"Starting automation for {username}...")

#     # Implement your logic to fetch and post Instagram reels here
#     # This could involve setting up a scheduled task or a loop to fetch reels periodically
#     await automate_instagram_reels(username)

# async def automate_instagram_reels(username):
#     while True:
#         # Fetch reels from the specified Instagram username
#         reels = await fetch_instagram_reels(username)
#         print(f"Loaded reels : {reels}")
#         if reels:
#             for reel in reels:
#                 # Step 6: Post each reel to the specified Telegram channels
#                 print("Posting reel to tg")
#                 await post_to_telegram_channels(reel)
#                 print(f"Posting Done ✅")
#                 print(f"----------")
#                 await asyncio.sleep(5)
#                 print(f"Waiting to 5 sec 🍟")
#                 print(f"----------")
        
#         # Wait for a specified duration before fetching new reels (e.g., 1 hour)
#         await asyncio.sleep(3600)  # Adjust the duration as needed
#         print(f"Waiting to 5 sec 🍟")
# async def fetch_instagram_reels(username):
#     # Your logic to fetch reels from Instagram using instaloader or similar library
#     # Return a list of reels (URLs or file paths)
#     return []  # Replace with actual fetched reels

# async def post_to_telegram_channels(reel):
#     # Your logic to send the reel to the three Telegram channels
#     channels = ['channel1_id', 'channel2_id', 'channel3_id']
#     for channel in channels:
#         await client.send_video(chat_id=channel, video=reel)  # Adjust parameters as needed


# def download_latest_reel(username):
#     profile = Profile.from_username(insta.context, username)
#     print(profile)
#     for post in profile.get_posts():
#         if post.is_video:
#             video_path = f"reels/{username}/{post.shortcode}.mp4"
#             print(f"video_path=> {video_path}")
#             if not os.path.exists(video_path):  # Check if reel has been downloaded before
#                 os.makedirs(f"reels/{username}", exist_ok=True)
#                 insta.download_post(post, target=f"reels/{username}")
#                 return video_path
#     return None

# async def post_reel_to_telegram(bot, channel_username, video_path, caption):
#     try:
#         print(f"trying to post reel to telegram")
#         await bot.send_video(channel_username, video_path, caption=caption)  # Use await directly
#         print(f"Reel posted to {channel_username}")
#     except FloodWait as e:
#         print(f"Rate limit hit! Waiting for {e.x} seconds.")
#         await asyncio.sleep(e.x)  # Use asyncio.sleep for async waiting

# @Client.on_message(filters.command("automate") & filters.private)
# async def automate_reels_posting(bot, message):
#     print(f"initilizing bot to automate")
#     for channel, insta_page in channels.items():
#         video_path = download_latest_reel(insta_page)
#         print(video_path)
#         if video_path:
#             await post_reel_to_telegram(bot, channel, video_path, f"New reel from @{insta_page}!")  # Use await
#         else:
#             print(f"No new reel found for {insta_page}")


@Client.on_message(filters.command("posts") & filters.private)
async def post(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        print(profile)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    await bot.send_message(
            message.from_user.id,
            f"What type of post do you want to download?.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Photos", callback_data=f"photos#{username}"),
                        InlineKeyboardButton("Videos", callback_data=f"video#{username}")
                    ]
                ]
            )
        )
    

@Client.on_message(filters.command("igtv") & filters.private)
async def igtv(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    m=await message.reply_text(f"Fetching IGTV from <code>@{username}</code>")
    profile = Profile.from_username(insta.context, username)
    igtvcount = profile.igtvcount
    await m.edit(
        text = f"Do you Want to download all IGTV posts?\nThere are {igtvcount} posts.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Yes", callback_data=f"yesigtv#{username}"),
                    InlineKeyboardButton("No", callback_data=f"no#{username}")
                ]
            ]
        )
        )
    


@Client.on_message(filters.command("followers") & filters.private)
async def followers(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    profile = Profile.from_username(insta.context, username)
    name=profile.full_name
    m=await message.reply_text(f"Fetching Followers list of <code>@{username}</code>")
    chat_id=message.from_user.id
    f = profile.get_followers()
    followers=f"**Followers List for {name}**\n\n"
    for p in f:
        followers += f"\n[{p.username}](www.instagram.com/{p.username})"
    try:
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=followers)
    except MessageTooLong:
        followers=f"**Followers List for {name}**\n\n"
        f = profile.get_followers()
        for p in f:
            followers += f"\nName: {p.username} :     Link to Profile: www.instagram.com/{p.username}"
        text_file = open(f"{username}'s followers.txt", "w")
        text_file.write(followers)
        text_file.close()
        await bot.send_document(chat_id=chat_id, document=f"./{username}'s followers.txt", caption=f"{name}'s followers\n\nA Project By [XTZ_Bots](https://t.me/subin_works)")
        os.remove(f"./{username}'s followers.txt")


@Client.on_message(filters.command("followees") & filters.private)
async def followees(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    profile = Profile.from_username(insta.context, username)
    name=profile.full_name
    m=await message.reply_text(f"Fetching Followees list of <code>@{username}</code>")
    chat_id=message.from_user.id
    f = profile.get_followees()
    followees=f"**Followees List for {name}**\n\n"
    for p in f:
        followees += f"\n[{p.username}](www.instagram.com/{p.username})"
    try:
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=followees)
    except MessageTooLong:
        followees=f"**Followees List for {name}**\n\n"
        f = profile.get_followees()
        for p in f:
            followees += f"\nName: {p.username} :     Link to Profile: www.instagram.com/{p.username}"
        text_file = open(f"{username}'s followees.txt", "w")
        text_file.write(followees)
        text_file.close()
        await bot.send_document(chat_id=chat_id, document=f"./{username}'s followees.txt", caption=f"{name}'s followees\n\nA Project By [XTZ_Bots](https://t.me/subin_works)")
        os.remove(f"./{username}'s followees.txt")




@Client.on_message(filters.command("fans") & filters.private)
async def fans(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    profile = Profile.from_username(insta.context, username)
    name=profile.full_name
    m=await message.reply_text(f"Fetching list of followees of <code>@{username}</code> who follows <code>@{username}</code>.")
    chat_id=message.from_user.id
    f = profile.get_followers()
    fl = profile.get_followees()
    flist=[]
    fmlist=[]
    for fn in f:
        u=fn.username
        flist.append(u)
    for fm in fl:
        n=fm.username
        fmlist.append(n)

    fans = [value for value in fmlist if value in flist]
    print(len(fans))
    followers=f"**Fans List for {name}**\n\n"
    for p in fans:
        followers += f"\n[{p}](www.instagram.com/{p})"
    try:
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=followers)
    except MessageTooLong:
        followers=f"**Fans List for {name}**\n\n"
        
        for p in fans:
            followers += f"\nName: {p} :     Link to Profile: www.instagram.com/{p}"
        text_file = open(f"{username}'s fans.txt", "w")
        text_file.write(followers)
        text_file.close()
        await bot.send_document(chat_id=chat_id, document=f"./{username}'s fans.txt", caption=f"{name}'s fans\n\nA Project By [XTZ_Bots](https://t.me/subin_works)")
        os.remove(f"./{username}'s fans.txt")


@Client.on_message(filters.command("notfollowing") & filters.private)
async def nfans(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    profile = Profile.from_username(insta.context, username)
    name=profile.full_name
    m=await message.reply_text(f"Fetching list of followees of <code>@{username}</code> who is <b>not</b> following <code>@{username}</code>.")
    chat_id=message.from_user.id
    f = profile.get_followers()
    fl = profile.get_followees()
    flist=[]
    fmlist=[]
    for fn in f:
        u=fn.username
        flist.append(u)
    for fm in fl:
        n=fm.username
        fmlist.append(n)

    fans = list(set(fmlist) - set(flist))
    print(len(fans))
    followers=f"**Followees of <code>@{username}</code> who is <b>not</b> following <code>@{username}</code>**\n\n"
    for p in fans:
        followers += f"\n[{p}](www.instagram.com/{p})"
    try:
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=followers)
    except MessageTooLong:
        followers=f"Followees of <code>@{username}</code> who is <b>not</b> following <code>@{username}</code>\n\n"
        for p in fans:
            followers += f"\nName: {p} :     Link to Profile: www.instagram.com/{p}"
        text_file = open(f"{username}'s Non_followers.txt", "w")
        text_file.write(followers)
        text_file.close()
        await bot.send_document(chat_id=chat_id, document=f"./{username}'s Non_followers.txt", caption=f"{name}'s Non_followers\n\nA Project By [XTZ_Bots](https://t.me/subin_works)")
        os.remove(f"./{username}'s Non_followers.txt")





@Client.on_message(filters.command("feed") & filters.private)
async def feed(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    count=None
    if " " in text:
        cmd, count = text.split(' ')
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    m=await message.reply_text(f"Fetching Posts in Your Feed.")
    chat_id=message.from_user.id
    dir=f"{chat_id}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    if count:
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--no-captions",
            "--no-video-thumbnails",
            "--login", USER,
            "--sessionfile", session,
            "--dirname-pattern", dir,
            ":feed",
            "--count", count
            ]
    else:
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--no-captions",
            "--no-video-thumbnails",
            "--login", USER,
            "--sessionfile", session,
            "--dirname-pattern", dir,
            ":feed"
            ]

    await download_insta(command, m, dir)
    await upload(m, bot, chat_id, dir)



@Client.on_message(filters.command("saved") & filters.private)
async def saved(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    count=None
    if " " in text:
        cmd, count = text.split(' ')
    m=await message.reply_text(f"Fetching your Saved Posts.")
    chat_id=message.from_user.id
    dir=f"{chat_id}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    if count:
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--no-captions",
            "--no-video-thumbnails",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            ":saved",
            "--count", count
            ]
    else:
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--no-captions",
            "--no-video-thumbnails",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            ":saved"
            ]
    await download_insta(command, m, dir)
    await upload(m, bot, chat_id, dir)




@Client.on_message(filters.command("tagged") & filters.private)
async def tagged(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    m=await message.reply_text(f"Fetching the posts in which <code>@{username}</code> is tagged.")
    chat_id=message.from_user.id
    dir=f"{chat_id}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    command = [
        "instaloader",
        "--no-metadata-json",
        "--no-compress-json",
        "--no-profile-pic",
        "--no-posts",
        "--tagged",
        "--no-captions",
        "--no-video-thumbnails",
        "--login", USER,
        "-f", session,
        "--dirname-pattern", dir,
        "--", username
        ]
    await download_insta(command, m, dir)
    await upload(m, bot, chat_id, dir)



@Client.on_message(filters.command("story") & filters.private)
async def story(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    m=await message.reply_text(f"Fetching stories of <code>@{username}</code>")
    chat_id=message.from_user.id
    dir=f"{chat_id}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    command = [
        "instaloader",
        "--no-metadata-json",
        "--no-compress-json",
        "--no-profile-pic",
        "--no-posts",
        "--stories",
        "--no-captions",
        "--no-video-thumbnails",
        "--login", USER,
        "-f", session,
        "--dirname-pattern", dir,
        "--", username
        ]
    await download_insta(command, m, dir)
    await upload(m, bot, chat_id, dir)



@Client.on_message(filters.command("stories") & filters.private)
async def stories(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    m=await message.reply_text(f"Fetching stories of all your followees")
    chat_id=message.from_user.id
    dir=f"{chat_id}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    command = [
        "instaloader",
        "--no-metadata-json",
        "--no-compress-json",
        "--no-profile-pic",
        "--no-captions",
        "--no-posts",
        "--no-video-thumbnails",
        "--login", USER,
        "-f", session,
        "--dirname-pattern", dir,
        ":stories"
        ]
    await download_insta(command, m, dir)
    await upload(m, bot, chat_id, dir)




@Client.on_message(filters.command("highlights") & filters.private)
async def highlights(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    text=message.text
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    m=await message.reply_text(f"Fetching highlights from profile <code>@{username}</code>")
    chat_id=message.from_user.id
    dir=f"{chat_id}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    command = [
        "instaloader",
        "--no-metadata-json",
        "--no-compress-json",
        "--no-profile-pic",
        "--no-posts",
        "--highlights",
        "--no-captions",
        "--no-video-thumbnails",
        "--login", USER,
        "-f", session,
        "--dirname-pattern", dir,
        "--", username
        ]
    await download_insta(command, m, dir)
    await upload(m, bot, chat_id, dir)

