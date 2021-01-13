# tgfilestream - A Telegram bot that can stream Telegram files to users over HTTP.
# Copyright (C) 2019 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.'
import logging

from telethon import TelegramClient, events, Button

from .paralleltransfer import ParallelTransferrer
from .config import (
    session_name,
    api_id,
    api_hash,
    public_url,
    start_message,
    group_chat_message
)
from .util import pack_id, get_file_name

log = logging.getLogger(__name__)

client = TelegramClient(session_name, api_id, api_hash)
transfer = ParallelTransferrer(client)


@client.on(events.NewMessage)
async def handle_message(evt: events.NewMessage.Event) -> None:
    if not evt.is_private:
        await evt.reply(group_chat_message)
        return
    if not evt.file:
        channel_link = "https://t.me/Discovery_Updates"
        group_link = "https://t.me/linux_repo"
        dev_link = "https://t.me/AbirHasan2005"
        keyboard = [
            [  
                Button.url("Updates Channel", channel_link), 
                Button.url("Support Group", group_link)
            ],
            [
                Button.url("Developer", dev_link)
            ]
        ]
        await evt.reply(start_message,buttons=keyboard,parse_mode='md')
        return
    url_button = [
        [
            Button.url("Download Now", f"{public_url}/{str(pack_id(evt))}/{get_file_name(evt)}")
        ],
        [
            Button.url("Join Bots Updates Channel", "https://t.me/Discovery_Updates")
        ]
    ]
    await evt.reply(f"Bruh!\nYour Link Generated.\n\nDownload Link: `{public_url}/{str(pack_id(evt))}/{get_file_name(evt)}`\n\n__(Tap to Copy!)__",buttons=url_button,parse_mode="md")
    log.info(f"Replied with link for {evt.id} to {evt.from_id} in {evt.chat_id}")
    log.debug(f"Link to {evt.id} in {evt.chat_id}: {url}")
