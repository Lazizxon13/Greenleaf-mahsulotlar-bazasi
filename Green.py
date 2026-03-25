import telebot
from google import genai

# 1. Калитларни киритамиз
TELEGRAM_TOKEN = "8745146517:AAGu_0Zn-SE7LoT9V-nq1rMAb_lZcJK4n5I"
GEMINI_API_KEY = "AIzaSyC88GE0fnEvJhU2-Vg7vMk2jF03wOZVM48" # AIza... кодини шу ерга қўясиз

# 2. Созламалар
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

system_text = "Сен Greenleaf компаниясининг Ўзбекистондаги (Риштон) филиалининг ақлли ёрдамчисисан. Мижозларга маҳсулотлар, 50% чегирмалар ва тармоқли маркетинг (MLM) бизнес режаси ҳақида хушмуомала ва сотувга ундайдиган тарзда жавоб берасан."

# 3. Мижоз /start босганда чиқадиган биринчи хабар
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Ассалому алайкум! Мен Greenleaf 10-Асос грухининг ақлли ёрдамчисиман. Сизга қайси маҳсулот ёки ҳамкорлик бўйича маълумот керак?")

# 4. Мижозларнинг барча саволларига Gemini орқали жавоб бериш
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # Мижозга "ёзяпти..." деган статусни кўрсатиш
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Янги авлод Gemini орқали жавоб олиш
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_text
            )
        )
        
        # Мижозга жавобни юбориш
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Узр, тизимда кичик узилиш бор. Илтимос, бироздан сўнг қайта ёзинг.")

# Ботни ишга тушириш
print("Greenleaf боти ишга тушди...")
bot.infinity_polling()
