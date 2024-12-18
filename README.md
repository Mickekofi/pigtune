
=<p align="center">
  <a href="https://github.com/Mickekofi/pigtune/tree/master">
    <img src="https://github.com/Mickekofi/pigtune/tree/master/logo" alt="Logo" width="130">
  </a>
  <a href = "https://github.com/Mickekofi/pigtune">
  <h1 align="center"><strong>PigTune</strong></h1>
  </a>
</p>

---


### Image Processing Bot

<ol>
    <li><strong> Perform Major Image Enhancement Tasks like;</strong>
        <ul>
            <li>✓ [ 🟥 Red Background ]</li>
            <li>✓ [ 🟨 Yellow Background ]</li>
            <li>✓ [ 🟩 Green Background ]</li>
            <li>✓ [ ⬛️ Black Background ]</li>
            <li>✓ [ ⬜️ White Background ] [& more]</li>
            <br>
            <li>✓ [ ✏️ 2D Anime Sketch]</li>
            <li>✓ [ 🐦 3d Egyptian Art ]</li>
            <li>✓ [ 🩻 Grayscale Artistic]</li>
            <li>✓ [ ✂️ Resize ]</li>
            <li>✓ [ 🛠 Extract Text from Image ]</li>
            <li>✓ [ ✨ Retouch Enhance]</li>
        </ul>
    </li>


#### Tutorial

![Preview](https://github.com/Mickekofi/EyeTubeBot/blob/master/Documentation_For_End_User/tutorials4.gif)


PigTune is a Telegram bot that provides various image processing functionalities, including background removal, image enhancement, and artistic effects. The bot also supports update checking and automatic updates.

## Features

- Background removal with customizable background colors
- Image enhancement (sharpness, brightness, contrast, saturation, etc.)
- Artistic effects (grayscale, 2D anime sketch, 3D Egyptian art, etc.)
- Text extraction from images
- Update checking and automatic updates

## Requirements

- Python 3.7+
- Telegram Bot API token
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository:

```sh
git clone https://github.com/Mickekofi/pigtune.git
cd pigtune
```

2. Create a virtual environment and activate it:

```sh
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```sh
pip install -r requirements.txt
```

4. Set up your Telegram Bot API token:

```python
TOKEN = input("Please enter your Telegram API token: ")
bot = telebot.TeleBot(TOKEN)
```

**How to Set up your token**

- Get your **Telegram Bot API Token** from [BotFather](https://t.me/BotFather).

- Complete the process to get your token
 

## Usage

1. Run the bot:

    ```sh
    python pigtune.py
    ```

2. Interact with the bot on Telegram using the provided commands:

    - `/start` - Start the bot and display the welcome message
    - `/Help` - Display help information
    - `/About` - Display information about the bot
    - `/check_update` - Check for updates
    - `/update` - Update the bot
    - `/rm_bg` - Remove the background of an image


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
