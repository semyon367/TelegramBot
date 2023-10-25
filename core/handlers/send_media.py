from aiogram.types import Message, FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram import Bot
from aiogram.utils.chat_action import ChatActionSender


async def get_audio(message: Message, bot: Bot):
    audio = FSInputFile(path=r"C:\Users\Семён\Downloads\X2Download.app - Luis Fonsi, Demi Lovato - Échame La Culpa (320 kbps).mp3",
                        filename='Audio.mp3')
    await bot.send_audio(message.chat.id, audio=audio)


async def get_document(message: Message, bot: Bot):
    document = FSInputFile(path=r"C:\Users\Семён\Downloads\myb_Chernykh_21-08-2023.pdf")
    await bot.send_document(message.chat.id, document=document, caption='Its document')


async def get_media_group(message: Message, bot: Bot):
    photo1_mg = InputMediaPhoto(type='photo', media=FSInputFile(r"C:\Users\Семён\Pictures\3294.jpg"),
                                caption='Its media group')
    photo2_mg = InputMediaPhoto(type='photo', media=FSInputFile(r"C:\Users\Семён\Pictures\1482071447167197362.jpg"))
    video_mg = InputMediaVideo(type='video', media=FSInputFile(r"C:\Users\Семён\Downloads\videoplayback.mp4"))
    media = [photo1_mg, photo2_mg, video_mg]
    await bot.send_media_group(message.chat.id, media)


async def get_photo(message: Message, bot: Bot):
    photo = FSInputFile(r"C:\Users\Семён\Pictures\2021-Mercedes-AMG-E63-S-007-2160.jpg")
    await bot.send_photo(message.chat.id, photo, caption='Its photo')


async def get_sticker(message: Message, bot: Bot):
    sticker = FSInputFile(r"C:\Users\Семён\Pictures\persik.png")
    await bot.send_sticker(message.chat.id, sticker)


async def get_video(message: Message, bot: Bot):
    video = FSInputFile(r"C:\Users\Семён\Downloads\Luis Fonsi, Demi Lovato - Échame La Culpa.mp4")
    await bot.send_video(message.chat.id, video)


async def get_video_note(message: Message, bot: Bot):
    video_note = FSInputFile(r"C:\Users\Семён\Downloads\video.mp4")
    await bot.send_video_note(message.chat.id, video_note)


async def get_voice(message: Message, bot: Bot):
    voice = FSInputFile(r"C:\Users\Семён\Downloads\audio_2023-09-16_12-53-08.ogg")
    await bot.send_voice(message.chat.id, voice)