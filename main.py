import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Charger les variables d'environnement
load_dotenv()

# Obtenir les tokens de l'environnement
token = os.getenv('TOKEN')
deepl_api_key = os.getenv('DEEPL_TOKEN')

# Fonction de démarrage
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenue sur notre bot de traduction ! Utilisez la commande /translate pour traduire un mot ou une phrase."
    )

# Fonction de traduction
async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_to_translate = ' '.join(context.args)
    if not text_to_translate:
        await update.message.reply_text("Veuillez fournir le texte à traduire après la commande /translate.")
        return

    translated_text = translate_text(text_to_translate)
    await update.message.reply_text(translated_text)

# Fonction pour appeler l'API Deepl
def translate_text(text):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        'auth_key': deepl_api_key,
        'text': text,
        'target_lang': get_target_language(text)  # Obtenir la langue cible appropriée
    }
    response = requests.post(url, data=params)
    result = response.json()
    return result['translations'][0]['text']

# Fonction pour déterminer la langue cible en fonction de la langue source
def get_target_language(text):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        'auth_key': deepl_api_key,
        'text': text,
        'target_lang': 'EN'  # Utiliser 'EN' temporairement pour obtenir la langue source
    }
    response = requests.post(url, data=params)
    result = response.json()
    detected_source_lang = result['translations'][0]['detected_source_language']

    if detected_source_lang == 'FR':
        return 'AR'  # Traduire du français vers l'arabe
    elif detected_source_lang == 'EN':
        return 'FR'  # Traduire de l'anglais vers le français
    elif detected_source_lang == 'AR':
        return 'FR'  # Traduire de l'arabe vers le français
    else:
        return 'FR'  # Par défaut, traduire vers le français

if __name__ == '__main__':
    # Créer l'application de bot Telegram
    app = Application.builder().token(token).build()
    
    # Ajouter les gestionnaires de commande
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('translate', translate))

    # Démarrer le bot
    app.run_polling(poll_interval=2)
