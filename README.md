# Telegram Bot - ReadMe

This repository contains a Telegram bot built using Python and the Telethon library. The bot is designed to fetch messages from source channels, filter and translate them, and then post them to designated target channels. This README provides instructions on how to set up, configure, and run the bot.

## Features
- Fetch messages from multiple Telegram channels.
- Filter out specific words, URLs, and usernames.
- Translate messages to a specified language using Google Translate.
- Post the translated messages to target Telegram channels.
- Track and display statistics on the number of messages processed.

## Prerequisites
Before running the bot, you need to have the following:

- **Python 3.7 or higher**
- **Telethon library**: Used to interact with Telegram's API.
- **Googletrans library**: For message translation.
- **Telegram API credentials**: `api_id`, `api_hash`, and `phone_number`.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `config.py` file** with your Telegram credentials:
   ```python
   # config.py
   api_id = 'YOUR_API_ID'
   api_hash = 'YOUR_API_HASH'
   phone_number = 'YOUR_PHONE_NUMBER'
   ```

4. **Create the following files** (if needed):
   - **`filtered_words.txt`**: A text file containing words to be filtered out from the messages. Each word should be on a separate line.
   - **`target_language.txt`**: A text file containing the target language code (e.g., `en` for English, `es` for Spanish). If not specified, the default is English.

## Usage

1. **Run the bot**:
   ```bash
   python bot.py
   ```

   When the bot starts, it will listen to the configured source channels and will handle new messages accordingly.

## Configuration

### Source and Target Channels
- **Source Channels**: The channels from which messages are fetched are defined in the `channel_groups` dictionary. Each group is represented as a key (e.g., `group1`) and the list of source channels for that group.
  ```python
  channel_groups = {
      'group1': ['testpublish1', 'source_channel_2'],
      'group2': ['source_channel_3', 'source_channel_4'],
      'group3': ['source_channel_5', 'source_channel_6']
  }
  ```
- **Target Channels**: The target channels to which messages are posted are defined in the `target_channels` dictionary.
  ```python
  target_channels = {
      'group1': 'testpublish1',
      'group2': 'target_channel_2',
      'group3': 'target_channel_3'
  }
  ```

### Filtered Words
- The bot can remove specific words from messages before posting them. These words are loaded from the `filtered_words.txt` file.

### Translation
- The bot uses Google Translate (via the `googletrans` library) to translate messages to a target language. By default, this language is set to English (`en`). You can change it by modifying the `target_language.txt` file.

## Logging
- **Error Logging**: Errors and other log information are logged to a file located in the `log` directory (`log/error_log.txt`).
- **Console Output**: Logs are also printed to the console for easier debugging.

## Handling Messages
- The bot listens for new messages from the configured source channels.
- When a message is received, it goes through the following steps:
  1. **Filtering**: URLs, usernames, and filtered words are removed.
  2. **Translation**: If translation is enabled, the message is translated to the target language.
  3. **Posting**: The cleaned and translated message is posted to the corresponding target channel.
- **Media Handling**: The bot also supports forwarding media (photos, videos, documents) with the translated caption.

## Statistics
- The bot keeps track of the number of messages processed from each channel group.
- **Statistics** are displayed in the terminal every 5 minutes, showing the number of messages processed for each group.

## Error Handling and Retries
- If an error occurs while processing a message, the bot will retry up to 3 times.
- If the retries fail, an error message is logged to both the log file and the console.

## Running the Bot
- **Main Function**: The bot starts by calling the `main()` function, which initializes the Telegram client, starts the event handlers, and runs until the bot is disconnected.
- To run the bot:
  ```bash
  python bot.py
  ```

## Notes
- The bot requires a Telegram session to be saved. Make sure to use the correct phone number when prompted.
- Ensure that your Telegram account is authorized to access the channels specified in the configuration.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.

## Contact
For any questions or issues, please open an issue on GitHub or contact me at [your_email@example.com].

