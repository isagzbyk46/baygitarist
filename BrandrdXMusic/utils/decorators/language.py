from strings import get_string  # Dil dosyasından çeviri alıyor
from BrandrdXMusic.misc import SUDOERS
from BrandrdXMusic.utils.database import get_lang, is_maintenance

# Eğer app ve SUPPORT_CHAT tanımlı değilse import edilmeli
from BrandrdXMusic import app  

SUPPORT_CHAT = "https://t.me/your_support_chat"  # Buraya destek grubunun linkini ekle


def language(mystic):
    async def wrapper(_, message, **kwargs):
        if not await is_maintenance():
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} bakımda, detaylar için <a href={SUPPORT_CHAT}>destek sohbetini</a> ziyaret edin.",
                    disable_web_page_preview=True,
                )
        try:
            await message.delete()
        except Exception:
            pass

        try:
            lang_code = await get_lang(message.chat.id)  # Kullanıcının dilini al
            language = get_string(lang_code)  # Doğru dil dosyasını çek
        except Exception:
            language = get_string("en")  # Varsayılan olarak İngilizce

        return await mystic(_, message, language)

    return wrapper


def languageCB(mystic):
    async def wrapper(_, CallbackQuery, **kwargs):
        if not await is_maintenance():
            if CallbackQuery.from_user.id not in SUDOERS:
                return await CallbackQuery.answer(
                    f"{app.mention} bakımda, detaylar için destek sohbetini ziyaret edin.",
                    show_alert=True,
                )

        try:
            lang_code = await get_lang(CallbackQuery.message.chat.id)
            language = get_string(lang_code)
        except Exception:
            language = get_string("en")

        return await mystic(_, CallbackQuery, language)

    return wrapper


def LanguageStart(mystic):
    async def wrapper(_, message, **kwargs):
        try:
            lang_code = await get_lang(message.chat.id)
            language = get_string(lang_code)
        except Exception:
            language = get_string("en")

        return await mystic(_, message, language)

    return wrapper
