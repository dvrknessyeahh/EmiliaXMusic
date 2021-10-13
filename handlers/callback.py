# (C) KennedyProject github.com/KennedyProject

from time import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import authorized_users_only
from config import ALIVE_EMOJI as alv
from config import BOT_NAME as bn, BOT_IMG, BOT_USERNAME, OWNER_NAME, GROUP_SUPPORT, UPDATES_CHANNEL, ASSISTANT_NAME
from handlers.play import cb_admin_check


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>👋 **Hello {message.from_user.mention}**</b> ❗
**🤖 Perkenalkan saya [{BOT_NAME}](https://t.me/{BOT_USERNAME}) Adalah Bot Canggih Yang Dibuat Untuk Memutar Musik Di Obrolan Suara Grup Telegram
Saya Memiliki Banyak Fitur Praktis Seperti:

➡️ Memutar Musik.
➡️ Mendownload Lagu.
➡️ Mencari Lagu Yang ingin di Putar atau di Download
➡️ Fitur Keamanan dan Lainnya

👩‍💻 Bot ini dikelola oleh {OWNER_NAME}

✏️ Tekan » /help « Untuk Melihat Daftar Perintah Yang Saya Punya**""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ​ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "ʀᴇᴘᴏ​​", url="https://github.com/EmiliaTzy/EmiliaXMusic"
                    ),
                    InlineKeyboardButton(
                        "ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/{GROUP_SUPPORT}")
                ],[
                    InlineKeyboardButton(
                        "ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ​ ❓​", callback_data="cbguide"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("cbabout"))
async def cbabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>❓ **About  [{bn}](https://t.me/{BOT_USERNAME})**</b> 

➠ **Kekuatan penuh bot untuk memutar musik di grup!

➠ Bekerja dengan pyrogram

➠ Menggunakan Python 3.9.7

➠ Dapat memutar dan mengunduh musik atau video dari YouTube

➠ Saya dapat membuatmu senang

➠ Info selebihnya tekan /help

__{bn} lisensi dibawah GNU General Public License v.3.0__

• Updates channel @{UPDATES_CHANNEL}
• Group Support @{GROUP_SUPPORT}
• Assistant @{ASSISTANT_NAME}
• Here is my [Owner](https://t.me/{OWNER_NAME})**

❓ Ingin membuat musik bot Anda sendiri? coba klik tombol Source !""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "sᴏᴜʀᴄᴇ​​", url="https://github.com/KennedyProject/KennedyXMusic"
                    ),
                    InlineKeyboardButton(
                        "ʙᴀᴄᴋ​", callback_data="cbadvanced"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} Disini menu bantuan !</b>

**Pada menu ini Anda dapat membuka beberapa menu perintah yang tersedia, di setiap menu perintah juga terdapat penjelasan singkat masing-masing perintah **

💡 Bot by @{OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Perintah Dasar", callback_data="cbbasic"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 Perintah Admin", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 Perintah Sudo", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📔 Perintah Fun", callback_data="cbfun"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbguide"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} perintah dasar untuk bot

[PENGATURAN GRUP]
/play (judul) - memutar musik melalui youtube
/ytp (judul) - putar musik secara langsung
/stream (membalas audio) - memutar musik melalui balasan ke audio
/playlist - lihat daftar antrian
/song (judul) - unduh musik dari youtube
/search (judul) - mencari musik dari youtube secara detail
/saavn (judul) - unduh musik dari saavn
/video (judul) - unduh musik dari youtube secara detail
/lirik (judul) - cari lirik
/shazam (audio balasan) - untuk mengidentifikasi nama lagu
/q (teks balasan) - untuk membuat stiker tanda kutip
/id - untuk menunjukkan id atau id obrolan Anda
[ LAGI ]
/alive - periksa status bot
/start - memulai bot

💡 Bot by @{OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await query.edit_message_text(
        f"""**{alv} Hallo saya [{bn}](https://t.me/{BOT_USERNAME})**

{alv} **Saya bekerja dengan baik**

{alv} **Bot : 6.0 LATEST**

{alv} **My Master : [{OWNER_NAME}](https://t.me/{OWNER_NAME})**

{alv} **Service Uptime : `{uptime}`**

**Terima kasih banyak sudah menggunakan saya ♥️**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ᴀʙᴏᴜᴛ", callback_data="cbabout"
                    ),
                    InlineKeyboardButton(
                        "ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} Perintah anggota dalam grup

/player - lihat status pemutaran
/pause - menjeda pemutaran musik
/resume - melanjutkan musik yang dijeda
/skip - lompat ke lagu berikutnya
/end - bisukan musiknya
/userbotjoin - undang asisten untuk bergabung dengan grup
/musicplayer (on / off) - nyalakan / matikan pemutar musik di grup Anda

💡 Bot by @{OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} **perintah untuk sudo**

**/userbotleaveall - hapus asisten dari semua grup
/gcast - mengirim pesan global melalui asisten
/rmd - hapus file yang diunduh
/ uptime - untuk melihat uptime dan waktu mulai bot diluncurkan
jika menggunakan heroku
/penggunaan - untuk memeriksa dyno heroku
/update - untuk membangun, perbarui bot Anda
/restart - restart/boot ulang bot Anda
/setvar (var) (nilai) - untuk memperbarui variabel nilai Anda di heroku
/delvar (var) - untuk menghapus var Anda di heroku.

💡 Bot by @{OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbfun"))
async def cbfun(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} **Perintah fun**

**/truth - check yourself
/dare - check it yourself
/q - to make quotes text
/paste - pasting your text or document to pastebin into photo

💡 Bot by @{OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "BACK", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**BAGAIMANA MENGGUNAKAN BOT INI :**

**1.) Pertama, tambahkan ke grup Anda.
2.) Kemudian jadikan sebagai admin dengan semua izin kecuali admin anonim.
3.) Tambahkan @{ASSISTANT_NAME} ke grup Anda atau ketik /userbotjoin untuk mengundang asisten.
4.) Aktifkan obrolan suara terlebih dahulu sebelum memutar musik.

💡 Bot by @{OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 List Perintah", callback_data="cbhelp"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Close", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()
