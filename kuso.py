import telebot
import requests
from bs4 import BeautifulSoup
from telegraph import Telegraph
from telebot import types

TOKEN_BOT = '1835554210:AAFerCa7Yko4mH6pDUNCZ8zq_ax7_x_c6Kk'
bot = telebot.TeleBot(TOKEN_BOT)

TELEGRAPH_TOKEN = 'cf70c520d1d0057bb5b5f86a32f47edeb2b50e978a5453ca748ac50051b4'
telegraph = Telegraph(TELEGRAPH_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Gunakan perintah ini dengan format /kuso [URL anime]\n\nContoh: /kuso https://kusonime.com/jigokuraku-batch-subtitle-indonesia/")

@bot.message_handler(commands=['kuso'])
def anime_info_command(message):
    if len(message.text.split()) != 2:
        bot.reply_to(message, "Gunakan perintah ini dengan format /kuso [URL anime]\n\nContoh: /kuso https://kusonime.com/jigokuraku-batch-subtitle-indonesia/")
        return

    url = message.text.split()[1]
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        anime = {}

        anime['title'] = soup.select_one('.jdlz').get_text().strip()
        anime['thumbnail'] = soup.select_one('.post-thumb img')['src']
        for el in soup.select('.info p'):
            key = el.find('b').get_text().lower().strip().replace(' ', '_')
            el.find('b').decompose()
            value = el.get_text().split(':')[-1].strip()
            anime[key] = None if value == '' else value
        sinopsis_element = soup.select_one('.lexot > p')
        anime['sinopsis'] = sinopsis_element.get_text().strip() if sinopsis_element else 'Sinopsis not found'
        
       
        
        anime['list_download'] = []
        for el in soup.select('.smokeddlrh'):
            download_link = []
            title = el.select_one('.smokettlrh').get_text().strip()

            for ele in el.select('.smokeurlrh'):
                type_ = ele.select_one('strong').get_text().strip()

                links = []
                for elem in ele.select('a'):
                    name = elem.get_text().strip()
                    url = elem['href']
                    links.append({'name': name, 'url': url})

                download_link.append({'type': type_, 'links': links})

            for ele in el.select('.smokeurl'):
                type_ = ele.select_one('strong').get_text().strip()

                links = []
                for elem in ele.select('a'):
                    name = elem.get_text().strip()
                    url = elem['href']
                    links.append({'name': name, 'url': url})

                download_link.append({'type': type_, 'links': links})

            anime['list_download'].append({'title': title, 'download_link': download_link})

        # Membuat halaman di Telegraph
        content = f"<img src='{anime['thumbnail']}'/><br>"
        content += f"<b>{anime['title']}</b><br>"
        content += f"Genre: {anime.get('genre', 'N/A')}<br>"
        content += f"Status: {anime.get('status', 'N/A')}<br>"
        content += f"Seasons: {anime.get('seasons', 'N/A')}<br>"
        content += f"Producers: {anime.get('producers', 'N/A')}<br>"
        content += f"Type: {anime.get('type', 'N/A')}<br>"
        content += f"Total Episodes: {anime.get('total_episode', 'N/A')}<br>"
        content += f"Score: {anime.get('score', 'N/A')}<br>"
        content += f"Duration: {anime.get('duration', 'N/A')}<br>"
        content += f"Released on: {anime.get('released_on', 'N/A')}<br>"
        content += f"Sinopsis: {anime['sinopsis']}<br>"

        list_download = anime.get('list_download', None)
        if list_download:
            content += "<b>List Download:</b><br>"
            for download in list_download:
                content += f"{download['title']}<br>"
                for link in download['download_link']:
                    content += f"{link['type']}:\n<br>"
                    for l in link['links']:
                        content += f"- <a href='{l['url']}'>{l['name']}</a><br>"

        content += "<br><i>Bot by @ilham_maulana1</i><br>"
        content += "<i>Jika Bot ini membantu, dukung bot ini dengan cara donasi ke 6282137021145 dana :)</i>"

        response = telegraph.create_page(
            f"Anime: {anime['title']}",
            html_content=content
        )
        telegraph_url = 'https://telegra.ph/{}'.format(response['path'])

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Link Download", url=telegraph_url))

        # Kirim gambar thumbnail bersama pesan teks
        photo_url = anime['thumbnail']
        caption = ( 
            f"Title: {anime['title']}\n"
            f"Score: {anime.get('score', 'N/A')}\n"
            f"Episodes: {anime.get('total_episode', 'N/A')}\n"
            f"Genre: {anime.get('genre', 'N/A')}\n"
            f"Duration: {anime.get('duration', 'N/A')}\n"
            f"Status: {anime.get('status', 'N/A')}\n"
            f"Seasons: {anime.get('seasons', 'N/A')}\n"
            f"Producers: {anime.get('producers', 'N/A')}\n"
            f"Released on: {anime.get('released_on', 'N/A')}\n"
           
        )
        bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup)
    except Exception as error:
        bot.reply_to(message, f"Terjadi kesalahan: report @ilham_maulana1")

bot.polling()
