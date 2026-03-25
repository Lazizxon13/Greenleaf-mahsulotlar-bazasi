import telebot
import google.generativeai as genai

# 1. Калитларни киритамиз
TELEGRAM_TOKEN = "8745146517:AAGu_0Zn-SE7LoT9V-nq1rMAb_lZcJK4n5I"
GEMINI_API_KEY = "ШУ_ЕРГА_GEMINI_КАЛИТНИ_ҚЎЯСИЗ" # AIza... кодини шу ерга қўясиз

# 2. Созламалар
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# Gemini моделини Greenleaf бўйича мутахассис қилиб созлаймиз
system_instruction = "Сен Greenleaf компаниясининг Ўзбекистондаги (Риштон) филиалининг ақлли ёрдамчисисан. Мижозларга маҳсулотлар, 50% чегирмалар ва тармоқли маркетинг (MLM) бизнес режаси ҳақида хушмуомала ва сотувга ундайдиган тарзда жавоб берасан."
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

# 3. Мижоз /start босганда чиқадиган биринчи хабар
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Ассалому алайкум! Мен Greenleaf компаниясининг ақлли ёрдамчисиман. Сизга қайси маҳсулот ёки ҳамкорлик бўйича маълумот керак?")

# 4. Мижозларнинг барча саволларига Gemini орқали жавоб бериш
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # Мижозга "ёзяпти..." деган статусни кўрсатиш
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Gemini'дан жавоб олиш
        response = model.generate_content(message.text)
        
        # Мижозга жавобни юбориш
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Узр, тизимда кичик узилиш бор. Илтимос, бироздан сўнг қайта ёзинг.")

# Ботни ишга тушириш
print("Greenleaf боти ишга тушди...")
bot.infinity_polling()