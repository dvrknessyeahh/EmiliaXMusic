# this module i created only for playing music using audio file, idk, because the audio player on play.py module not working
# so this is the alternative
# audio play function

from os import path

from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from callsmusic import callsmusic, queues

import converter
from downloaders import youtube

from config import (
    DURATION_LIMIT,
    UPDATES_CHANNEL,
    GROUP_SUPPORT,
    BOT_USERNAME,
)
from handlers.play import convert_seconds
from helpers.filters import command, other_filters
from helpers.gets import get_url, get_file_name


@Client.on_message(command(["stream", f"stream@{BOT_USERNAME}"]) & other_filters)
async def stream(_, message: Message):

    lel = await message.reply("🔁 **memproses** suara...")
    costumer = message.from_user.mention

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="ɢʀᴏᴜᴘ",
                        url=f"https://t.me/{GROUP_SUPPORT}"),
                    InlineKeyboardButton(
                        text="ᴄʜᴀɴɴᴇʟ",
                        url=f"https://t.me/{UPDATES_CHANNEL}")
                ]
            ]
        )

    audio = message.reply_to_message.audio if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            return await lel.edit(f"❌ **musik dengan durasi lebih dari** `{DURATION_LIMIT}` **menit, tidak dapat diputar !**")

        file_name = get_file_name(audio)
        title = audio.title
        duration = convert_seconds(audio.duration)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        return await lel.edit("❗ **balas ke file audio telegram.**")
    else:
        return await lel.edit("❗ **balas ke file audio telegram.**")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo="https://telegra.ph/file/2fd3ee6fc59e88c61e4a5.png",
            caption=f"💡 **Track ditambahkan ke antrian »** `{position}`\n\n🏷 **Nama:** [{title[:40]}](https://t.me/{GROUP_SUPPORT})\n⏱ **Durasi:** `{duration}`\n🎧 **Permintaan dari:** {costumer}",
            reply_markup=keyboard,
        )
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
            photo="https://telegra.ph/file/2fd3ee6fc59e88c61e4a5.png",
            caption=f"🏷 **Nama:** [{title[:40]}](https://t.me/{GROUP_SUPPORT})\n⏱ **Durasi:** `{duration}`\n💡 **Status:** `Playing`\n" \
                   +f"🎧 **Permintaan dari:** {costumer}",
            reply_markup=keyboard,
        )
        return await lel.delete()
