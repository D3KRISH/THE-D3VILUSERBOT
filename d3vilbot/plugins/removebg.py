import os
import requests
import PIL.ImageOps
from PIL import Image, ImageDraw, ImageFont

from . import *

TEMP_DIR = os.environ.get("TEMP_DIR", "./temp/")

def convert_toimage(image, filename=None):
    filename = filename or os.path.join("./temp/", "temp.jpg")
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(filename, "jpeg")
    os.remove(image)
    return filename


def convert_tosticker(response, filename=None):
    filename = filename or os.path.join("./temp/", "temp.webp")
    image = Image.open(response)
    if image.mode != "RGB":
        image.convert("RGB")
    image.save(filename, "webp")
    os.remove(response)
    return filename


@bot.on(mafia_cmd(pattern="(rmbg|srmbg) ?(.*)"))
@bot.on(sudo_cmd(pattern="(rmbg|srmbg) ?(.*)", allow_sudo=True))
async def remove_background(event):
    if Config.REMOVE_BG_API is None:
        return await eod(
            event,
            "You need to set  `REMOVE_BG_API`  for this module to work..."
        )
    cmd = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    message_id = await reply_id(event)
    if event.reply_to_msg_id and not input_str:
        reply_message = await event.get_reply_message()
        mafiaevent = await edit_or_reply(event, "`Analysing...`")
        file_name = os.path.join(TEMP_DIR, "rmbg.png")
        try:
            await event.client.download_media(reply_message, file_name)
        except Exception as e:
            await edit_or_reply(mafiaevent, f"`{str(e)}`")
            return
        else:
            await mafiaevent.edit("`Removing Background of this media`")
            file_name = convert_toimage(file_name)
            response = ReTrieveFile(file_name)
            os.remove(file_name)
    elif input_str:
        mafiaevent = await edit_or_reply(event, "`Removing Background of this media`")
        response = ReTrieveURL(input_str)
    else:
        await edit_or_reply(
            event,
            "`Reply to any image or sticker with rmbg/srmbg to get background less png file or webp format or provide image link along with command`"
        )
        return
    contentType = response.headers.get("content-type")
    remove_bg_image = "D3vilBot.png"
    if "image" in contentType:
        with open("D3vilBot.png", "wb") as removed_bg_file:
            removed_bg_file.write(response.content)
    else:
        await edit_or_reply(mafiaevent, f"`{response.content.decode('UTF-8')}`")
        return
    if cmd == "srmbg":
        file = convert_tosticker(remove_bg_image, filename="HellBot.webp")
        await event.client.send_file(
            event.chat_id,
            file,
            reply_to=message_id,
        )
    else:
        file = remove_bg_image
        await event.client.send_file(
            event.chat_id,
            file,
            force_document=True,
            reply_to=message_id,
        )
    await mafiaevent.delete()


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": Config.REMOVE_BG_API,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": Config.REMOVE_BG_API,
    }
    data = {"image_url": input_url}
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True,
    )

CmdHelp("removebg").add_command(
  "rmbg", "<reply to image/stcr> or <link>", "`Removes Background of replied image or sticker and sends output as a file. Need` REMOVE_BG_API `to be set in Heroku Config Vars."
).add_command(
  "srmbg", "<reply to img/stcr> or <link>", f"Same as {hl}rmbg but sends output as a sticker. Need REMOVE_BG_API to be set in Heroku Config Vars."
).add_info(
  "Remove Background."
).add_warning(
  "✅ Harmless Module."
).add()
