from functools import partial
from html import escape

from telegram import Bot, Update, User, TelegramError, Message
from telegram.error import Unauthorized
from telegram.ext import MessageHandler, Filters, CommandHandler

from bots.models import TelegramBot
from telebaka_anonymous_chat.models import User


def start(bot: Bot, update: Update, bot_instance: TelegramBot):
    if bot_instance.settings.get('no_autoadd'):
        return update.message.reply_text(bot_instance.settings['no_autoadd'])
    User.objects.update_or_create(user_id=update.effective_user.id, bot=bot_instance)
    update.effective_message.reply_text('You\'ve joined the chat')


def stop(bot: Bot, update: Update, bot_instance: TelegramBot):
    User.objects.filter(user_id=update.effective_user.id, bot=bot_instance).delete()
    update.effective_message.reply_text('You\'ve left the chat')


def message(bot: Bot, update: Update, bot_instance: TelegramBot):
    user = User.objects.filter(user_id=update.effective_user.id).first()
    if not user:
        return

    th = update.message.text_html
    if th and th.startswith('/') and not th.startswith('/sign '):
        return update.message.reply_text('Command was not found', quote=True)

    uids = User.objects.filter(bot=bot_instance)\
                       .exclude(user_id=update.effective_user.id)\
                       .values_list('user_id', flat=True)
    media_counted = False
    for uid in uids:
        try:
            m = update.message  # type: Message
            r = None
            if m.forward_from or m.forward_from_chat or m.forward_from_message_id or m.forward_signature:
                m.forward(uid)
            elif hasattr(m, 'audio') and m.audio:
                a = m.audio
                r = bot.send_audio(uid, a.file_id, a.duration, a.performer, a.title, m.caption_html, parse_mode='html')
            elif hasattr(m, 'document') and m.document:
                if m.document.mime_type == 'video/mp4':
                    if user.media_sent >= 10:
                        return m.reply_text('Hourly limit of 10 stickers/gifs is reached', quote=True)
                    if not media_counted:
                        user.media_sent += 1
                        user.save()
                        media_counted = True
                d = m.document
                r = bot.send_document(uid, d.file_id, d.file_name, m.caption_html, parse_mode='html')
            elif hasattr(m, 'photo') and m.photo:
                p = m.photo
                r = bot.send_photo(uid, p[-1].file_id, m.caption_html, parse_mode='html')
            elif hasattr(m, 'sticker') and m.sticker:
                if user.media_sent >= 10:
                    return m.reply_text('Hourly limit of 10 stickers/gifs is reached', quote=True)
                if not media_counted:
                    user.media_sent += 1
                    user.save()
                    media_counted = True
                s = m.sticker
                r = bot.send_sticker(uid, s.file_id)
            elif hasattr(m, 'video') and m.video:
                v = m.video
                r = bot.send_video(uid, v.file_id, v.duration, m.caption_html, parse_mode='html')
            elif hasattr(m, 'voice') and m.voice:
                v = m.voice
                r = bot.send_voice(uid, v.file_id, v.duration, m.caption_html, parse_mode='html')
            elif hasattr(m, 'video_note') and m.video_note:
                vn = m.video_note
                r = bot.send_video_note(uid, vn.file_id, vn.duration, vn.length)
            elif hasattr(m, 'contact') and m.contact:
                c = m.contact
                r = bot.send_contact(uid, c.phone_number, c.first_name, c.last_name)
            elif hasattr(m, 'location') and m.location:
                l = m.location
                r = bot.send_location(uid, l.latitude, l.longitude)
            elif hasattr(m, 'venue') and m.venue:
                v = m.venue
                r = bot.send_venue(uid, v.location.latitude, v.location.longitude, v.title, v.address, v.foursquare_id)
            elif hasattr(m, 'text') and m.text:
                txt = m.text_html
                if txt.startswith('!sign') or txt.startswith('/sign'):
                    txt = txt[5:] + f'\n\n____________\n' \
                                    f'by <a href="tg://user?id={m.from_user.id}">{escape(m.from_user.full_name)}</a>'
                r = bot.send_message(uid, txt, 'html')
        except Unauthorized:
            User.objects.filter(user_id=uid).delete()
        except TelegramError:
            pass


def setup(dispatcher):
    start_callback = partial(start, bot_instance=dispatcher.bot_instance)
    stop_callback = partial(stop, bot_instance=dispatcher.bot_instance)
    message_callback = partial(message, bot_instance=dispatcher.bot_instance)
    dispatcher.add_handler(CommandHandler('start', start_callback))
    dispatcher.add_handler(CommandHandler('stop', stop_callback))
    dispatcher.add_handler(MessageHandler(Filters.all, message_callback))
    return dispatcher
