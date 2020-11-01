#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import logging
import os
import time

from pyrogram import Client, Filters

from anydlbot import AUTH_USERS, DOWNLOAD_LOCATION
# the logging things
from anydlbot.helper_funcs.display_progress import progress_for_pyrogram
from translation import Translation

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)


# the Strings used for this "thing"

logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(Filters.sticker)
async def DownloadStickersBot(bot, update):
    if update.from_user.id not in AUTH_USERS:
        await update.delete()
        return

    LOGGER.info(update.from_user)
    download_location = DOWNLOAD_LOCATION + "/" + \
        str(update.from_user.id) + "_DownloadStickersBot_" + \
        str(update.from_user.id) + ".png"
    a = await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.DOWNLOAD_START,
        reply_to_message_id=update.message_id
    )
    try:
        c_time = time.time()
        the_real_download_location = await bot.download_media(
            message=update,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.DOWNLOAD_START,
                a,
                c_time
            )
        )
    except (ValueError) as e:
        await bot.edit_message_text(
            text=str(e),
            chat_id=update.chat.id,
            message_id=a.message_id
        )
        return False
    await bot.edit_message_text(
        text=Translation.SAVED_RECVD_DOC_FILE,
        chat_id=update.chat.id,
        message_id=a.message_id
    )
    c_time = time.time()
    await bot.send_document(
        chat_id=update.chat.id,
        document=the_real_download_location,
        # thumb=thumb_image_path,
        # caption=description,
        # reply_markup=reply_markup,
        reply_to_message_id=a.message_id,
        progress=progress_for_pyrogram,
        progress_args=(
            Translation.UPLOAD_START,
            a,
            c_time
        )
    )
    try:
        await bot.send_photo(
            chat_id=update.chat.id,
            photo=the_real_download_location,
            # thumb=thumb_image_path,
            # caption=description,
            # reply_markup=reply_markup,
            reply_to_message_id=a.message_id,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.UPLOAD_START,
                a,
                c_time
            )
        )
    except:
        pass
    os.remove(the_real_download_location)
    await bot.edit_message_text(
        text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG,
        chat_id=update.chat.id,
        message_id=a.message_id,
        disable_web_page_preview=True
    )
