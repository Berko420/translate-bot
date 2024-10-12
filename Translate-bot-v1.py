import logging
import os
from telethon import TelegramClient, events
from googletrans import Translator
from datetime import datetime, timezone, timedelta
import asyncio
from config import api_id, api_hash, phone_number
import time

# Create 'log' directory if it doesn't exist
if not os.path.exists('log'):
    os.makedirs('log')

# Set up logging to log both to a file and print to the console
log_file = os.path.join('log', 'error_log.txt')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # Log info and errors to a file with timestamp
logging.getLogger().addHandler(logging.StreamHandler())  # Print errors to terminal

# Create a Telegram bot object
client = TelegramClient('bot_session', api_id, api_hash)

# Create a translation object to use Google Translate API
translator = Translator()

# Load filtered words from external txt file (words to be removed from messages)
filtered_words = []
if os.path.exists('filtered_words.txt'):
    with open('filtered_words.txt', 'r') as file:
        filtered_words = [line.strip() for line in file.readlines()]

# Source channels from which messages are fetched, categorized by groups
channel_groups = {
    'group1': ['source_channel_1', 'source_channel_2'],
    'group2': ['source_channel_3', 'source_channel_4'],
    'group3': ['source_channel_5', 'source_channel_6']
}

# Target channels to which translated messages are posted
target_channels = {
    'group1': 'target_channel_1',
    'group2': 'target_channel_2',
    'group3': 'target_channel_3'
}

# Load the target language from an external txt file (default is English)
if os.path.exists('target_language.txt'):
    with open('target_language.txt', 'r') as file:
        target_language = file.read().strip()
else:
    target_language = 'en'  # Default to English if not specified

# Labels for translated messages
labels = {
    'published_in_channel': {
        'en': 'Published in channel'
    }
}

# Statistics dictionary to track the number of messages processed from each channel group
statistics = {key: 0 for key in channel_groups.keys()}

# Function to handle incoming messages, translate, and post to target channel
async def handle_event(event, target_channel, translate=True, target_lang=None):
    retries = 3  # Number of retries in case of failure
    for attempt in range(retries):
        try:
            message = event.message.message
            channel_name = event.chat.title if event.chat else "Unknown channel"
            channel_username = f"@{event.chat.username}" if event.chat.username else "Unknown"

            # Clean message by removing URLs, @usernames, and filtered words
            if message:
                message = '\n'.join([line for line in message.splitlines() if not line.startswith(('filetword', 'filterword2'))])
                for word in filtered_words:
                    message = message.replace(word, '')

            # Translate the message and channel name to the target language if translation is enabled
            translated_message = message
            translated_channel_name = channel_name

            if translate and (message or channel_name):
                try:
                    if message:
                        translation_result = translator.translate(message, dest=target_lang or target_language)
                        translated_message = translation_result.text if translation_result and translation_result.text else None

                    channel_translation_result = translator.translate(channel_name, dest=target_lang or target_language)
                    translated_channel_name = channel_translation_result.text if channel_translation_result and channel_translation_result.text else channel_name

                except Exception as e:
                    translated_message = f"⚠️ Error in translation: {str(e)}"
                    logging.error(f"Error in translation: {str(e)}")

            # Update statistics for the current channel group
            for key, channels in channel_groups.items():
                if event.chat.username in channels or event.chat.title in channels:
                    statistics[key] += 1
                    break

            # Determine the correct label for "published in channel"
            label_published_in_channel = labels['published_in_channel'].get(target_lang or target_language, labels['published_in_channel']['en'])

            # Prepare the message with channel info if there's text to send
            if translated_message and translated_channel_name:
                final_message = (f"\U0001F4E2 {label_published_in_channel}: {translated_channel_name} ({channel_username})\n\n"
                                 f"{translated_message}")

                # Send the message to the target channel
                await client.send_message(target_channel, final_message)
                logging.debug(f"Message sent to {target_channel} from {channel_name} ({channel_username})")

            # Handle media (photos, videos, documents, web pages)
            if event.message.media:
                caption = f"\U0001F4E2 {label_published_in_channel}: {translated_channel_name} ({channel_username})"
                if translated_message:
                    caption += f"\n\n{translated_message}"
                await client.send_file(target_channel, event.message.media, caption=caption)
                logging.debug(f"Media sent to {target_channel} from {channel_name} ({channel_username})")

            break  # Break the loop if successful

        except Exception as e:
            logging.error(f"Error handling event (attempt {attempt + 1}): {str(e)}")
            if attempt < retries - 1:
                logging.warning(f"Retrying ({attempt + 1}/{retries})...")
                await asyncio.sleep(2)  # Wait before retrying
            else:
                logging.error(f"Failed to handle event after {retries} attempts")

# Generic event handler for channels
async def channel_handler(event, channel_key):
    try:
        await handle_event(event, target_channels[channel_key], translate=True, target_lang=target_language)
    except Exception as e:
        logging.error(f"Error in {channel_key} handler: {e}")

# Register handlers for each group of channels
for channel_key, channels in channel_groups.items():
    @client.on(events.NewMessage(chats=channels))
    async def handler(event, key=channel_key):
        await channel_handler(event, key)

# Function to display statistics in the terminal every 5 minutes
async def send_statistics():
    while True:
        try:
            # Get the current time in Israel (UTC+3)
            now = datetime.now(timezone.utc) + timedelta(hours=3)
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

            # Format the statistics message
            stats_message = (
                f"\n--- Updated Statistics ({formatted_time}) ---\n" +
                "\n".join([f"{key.capitalize()}: {statistics[key]} messages" for key in statistics]) +
                "\n-------------------------------\n"
            )

            # Print the statistics to the terminal
            print(stats_message)
            logging.info(stats_message)

            # Wait for 5 minutes before the next update
            await asyncio.sleep(300)  # 300 seconds = 5 minutes

        except Exception as e:
            logging.error(f"Error in statistics update: {str(e)}")

# Main function to start the bot
async def main():
    await client.start(phone_number)
    print("Bot is listening to channels...")

    # Start the statistics display loop
    asyncio.ensure_future(send_statistics())

    # Run the client until disconnected
    await client.run_until_disconnected()

# Run the bot if this script is executed directly
if __name__ == "__main__":
    client.loop.run_until_complete(main())