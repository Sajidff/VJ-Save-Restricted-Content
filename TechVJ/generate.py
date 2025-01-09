# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import traceback
from pyrogram.types import Message
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from config import API_ID, API_HASH
from database.db import db

SESSION_STRING_SIZE = 351

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["logout"]))
async def logout(client, message):
    user_data = await db.get_session(message.from_user.id)  
    if user_data is None:
        return 
    await db.set_session(message.from_user.id, session=None)  
    await message.reply("**ʟᴏɢᴏᴜᴛ sᴜᴄᴄᴇssғᴜʟʟʏ**")

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["login"]))
async def main(bot: Client, message: Message):
    user_data = await db.get_session(message.from_user.id)
    if user_data is not None:
        await message.reply("**ʏᴏᴜʀ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ʟᴏɢɢᴇᴅ ɪɴ. ғɪʀsᴛ /logout ʏᴏᴜʀ ᴏʟᴅ sᴇssɪᴏɴ. ᴛʜᴇɴ ᴅᴏ ʟᴏɢɪɴ.**")
        return 
    user_id = int(message.from_user.id)
    phone_number_msg = await bot.ask(chat_id=user_id, text="<b>ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴡʜɪᴄʜ ɪɴᴄʟᴜᴅᴇs ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ</b>\n<b>ᴇxᴀᴍᴘʟᴇ:</b> <code>+13124562345, +9171828181889</code>")
    if phone_number_msg.text=='/cancel':
        return await phone_number_msg.reply('<b>ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ !</b>')
    phone_number = phone_number_msg.text
    client = Client(":memory:", API_ID, API_HASH)
    await client.connect()
    await phone_number_msg.reply("sᴇɴᴅɪɴɢ ᴏᴛᴘ...")
    try:
        code = await client.send_code(phone_number)
        phone_code_msg = await bot.ask(user_id, "ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ғᴏʀ ᴀɴ ᴏᴛᴘ ɪɴ ᴏғғɪᴄɪᴀʟ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ. ɪғ ʏᴏᴜ ɢᴏᴛ ɪᴛ, sᴇɴᴅ ᴏᴛᴘ ʜᴇʀᴇ ᴀғᴛᴇʀ ʀᴇᴀᴅɪɴɢ ᴛʜᴇ ʙᴇʟᴏᴡ ғᴏʀᴍᴀᴛ.\n\nɪғ ᴏᴛᴘ ɪs `12345`, **ᴘʟᴇᴀsᴇ sᴇɴᴅ ɪᴛ ᴀs** `1 2 3 4 5`.\n\n**ᴇɴᴛᴇʀ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴄᴇs**", filters=filters.text, timeout=600)
    except PhoneNumberInvalid:
        await phone_number_msg.reply('`PHONE_NUMBER` **ɪs ɪɴᴠᴀʟɪᴅ.**')
        return
    if phone_code_msg.text=='/cancel':
        return await phone_code_msg.reply('<b>ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ !</b>')
    try:
        phone_code = phone_code_msg.text.replace(" ", "")
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except PhoneCodeInvalid:
        await phone_code_msg.reply('**ᴏᴛᴘ ɪs ɪɴᴠᴀʟɪᴅ.**')
        return
    except PhoneCodeExpired:
        await phone_code_msg.reply('**ᴏᴛᴘ ɪs ᴇxᴘɪʀᴇᴅ.**')
        return
    except SessionPasswordNeeded:
        two_step_msg = await bot.ask(user_id, '**ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀs ᴇɴᴀʙʟᴇᴅ ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴘᴀssᴡᴏʀᴅ.\n\nᴇɴᴛᴇʀ /cancel ᴛᴏ ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴄᴇs**', filters=filters.text, timeout=300)
        if two_step_msg.text=='/cancel':
            return await two_step_msg.reply('<b>ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ !</b>')
        try:
            password = two_step_msg.text
            await client.check_password(password=password)
        except PasswordHashInvalid:
            await two_step_msg.reply('**ɪɴᴠᴀʟɪᴅ ᴘᴀssᴡᴏʀᴅ ᴘʀᴏᴠɪᴅᴇᴅ**')
            return
    string_session = await client.export_session_string()
    await client.disconnect()
    if len(string_session) < SESSION_STRING_SIZE:
        return await message.reply('<b>ɪɴᴠᴀʟɪᴅ sᴇssɪᴏɴ sʀɪɴɢ</b>')
    try:
        user_data = await db.get_session(message.from_user.id)
        if user_data is None:
            uclient = Client(":ᴍᴇᴍᴏʀʏ:", session_string=string_session, api_id=API_ID, api_hash=API_HASH)
            await uclient.connect()
            await db.set_session(message.from_user.id, session=string_session)
    except Exception as e:
        return await message.reply_text(f"<b>ᴇʀʀᴏʀ ɪɴ ʟᴏɢɪɴ:</b> `{e}`")
    await bot.send_message(message.from_user.id, "<b>ᴀᴄᴄᴏᴜɴᴛ ʟᴏɢɪɴ sᴜᴄᴄᴇssғᴜʟʟʏ.\n\nɪғ ʏᴏᴜ ɢᴇᴛ ᴀɴʏ ᴇʀʀᴏʀ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ ᴀᴜᴛʜ ᴋᴇʏ ᴛʜᴇɴ /logout ғɪʀsᴛ ᴀɴᴅ /login ᴀɢᴀɪɴ</b>")


# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
