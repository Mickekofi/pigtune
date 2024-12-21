import asyncio
import logging
import time
import re
from collections import Counter
from collections import defaultdict
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
import logging
from rembg import remove
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import io
import pytesseract
import subprocess
import support
from update_checker import UpdateChecker
logging.basicConfig(level=logging.INFO)

print("\n\n\033[93mLets start PigTune Version(1.0.0) ...\n\033[0m")
support.check_support()
admin = input("\n\n\033[92mPlease enter any Prefered Admin Name 👉 : \033[0m")
TOKEN = input("\n\033[92mPlease enter your Telegram API token 👉 : \033[0m")

if not TOKEN:
    print("\033[91m❓You provided No API token.\n\n Shuting down/Exiting...\033[0m")
    exit(1)

try:
    bot = telebot.TeleBot(TOKEN)
    print("\033[92mBot initialized successfully!\033[0m")
    
    bot_info = bot.get_me()
    print(f"\033[92mBot Username: {bot_info.username}\033[0m")
    print("\033[92mReady to receive commands.\033[0m")
    
except Exception as e:
    print(f"\033[91mError: Failed to initialize bot. {e}\033[0m")

#==============================================================================
# Retry Error Handling
def retry_on_failure(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error: {e}. Retrying in 5 seconds...")
                time.sleep(20)
    return wrapper

# UPDATE METHODS
#==============================================================================
update_checker = UpdateChecker("https://raw.githubusercontent.com/Mickekofi/pigtune")

@bot.message_handler(commands=['check_update'])
def check_updates(message):
    """Check for updates and notify the user."""
    chat_id = message.chat.id

    try:
        latest_version = update_checker.get_latest_version()
        local_version = update_checker.get_local_version()

        if latest_version is None:
            bot.send_message(chat_id, "Failed to fetch the latest version. Please try again later.")
        elif local_version != latest_version:
            bot.send_message(chat_id, f"📌 A new version ({latest_version}) is available!")
            bot.send_message(chat_id, "⬆️ Please update your bot by typing /update.")
        else:
            bot.send_message(chat_id, "✅ Your bot is up to date.")
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred while checking for updates: {e}")


@bot.message_handler(commands=['update'])
def update_bot(message):
    """Handle the bot update process."""
    chat_id = message.chat.id
    bot.send_message(chat_id, "𝙎𝙩𝙖𝙧𝙩𝙞𝙣𝙜 𝙩𝙝𝙚 𝙪𝙥𝙙𝙖𝙩𝙚 𝙥𝙧𝙤𝙘𝙚𝙨𝙨...")

    try:
        subprocess.run(["git", "pull", "origin", "master"], check=True)
        
        latest_version = update_checker.get_latest_version()
        
        if latest_version:
            update_checker.update_local_version(latest_version)
            
            markup = InlineKeyboardMarkup()
            update_button = InlineKeyboardButton("🎁 Check What is Newly Packed for you", url="https://github.com/Mickekofi/pigtune/blob/master/update.md")
            markup.add(update_button)
            
            bot.send_message(chat_id, f"✅ 𝗕𝗼𝘁 𝘂𝗽𝗱𝗮𝘁𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆! 𝗩𝗲𝗿𝘀𝗶𝗼𝗻: {latest_version}", reply_markup=markup)
        else:
            bot.send_message(chat_id, "Update completed, but failed to fetch the latest version. Please check manually.")
    except subprocess.CalledProcessError as e:
        bot.send_message(chat_id, f"Failed to update the bot: {e}")
    except Exception as e:
        bot.send_message(chat_id, f"An unexpected error occurred: {e}")



# WELCOME START
#==============================================================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    # Creating buttons
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('/Help')
    itembtn2 = telebot.types.KeyboardButton('/Engineer')
    itembtn3 = telebot.types.KeyboardButton('/check_update')
    itembtn4 = telebot.types.KeyboardButton('/update')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    bot.reply_to(message, f"🕹 {bot_info.username} is Operated by {admin}.\n\n𝙎𝙚𝙣𝙙 me 𝙖𝙣 𝙄𝙢𝙖𝙜𝙚 🫗 for Magic", reply_markup=markup)

#============================================================================================
#About
@bot.message_handler(commands=['Help'])
def open_about_command(message):
    # Create an inline keyboard
    keyboard = types.InlineKeyboardMarkup()

    # Create 4 buttons with different links
    button1 = types.InlineKeyboardButton(text="𝐏𝐢𝐠𝐓𝐮𝐧𝐞 𝐏𝐚𝐠𝐞", url="https://raw.githubusercontent.com/Mickekofi/pigtune")
    button4 = types.InlineKeyboardButton(text="👥 𝐖𝐡𝐨 𝐚𝐫𝐞 𝐖𝐞", url="https://github.com/Mickekofi/pigtune/tree/master/who_are_we.md")
    button5 = types.InlineKeyboardButton(text="𝐖𝐡𝐚𝐭 𝐢𝐬 𝐢𝐧 𝐟𝐨𝐫 𝐭𝐡𝐢𝐬 𝐔𝐩𝐝𝐚𝐭𝐞", url="https://raw.githubusercontent.com/Mickekofi/pigtune/update.md")
    
    keyboard.add(button1)
    keyboard.add(button4)  # Adding the other two buttons side by side
    keyboard.add(button5)
    # Send the message with the inline keyboard
    bot.send_message(message.chat.id, "About Info", reply_markup=keyboard)
    
    bot.send_message(message.chat.id,'''❓𝐒𝐮𝐠𝐠𝐞𝐬𝐭 𝐚𝐧 𝐈𝐬𝐬𝐮𝐞 𝐚 𝐁𝐮𝐠 𝐨𝐫 𝐚 𝐅𝐞𝐚𝐭𝐮𝐫𝐞 𝐑𝐞𝐪𝐮𝐞𝐬𝐭?📬𝐬;
    𝐜𝐨𝐩𝐲 𝐚𝐧𝐝 𝐩𝐚𝐬𝐭𝐞 below 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐛𝐫𝐨𝐰𝐬𝐞𝐫 
                     👇''')
    bot.send_message(message.chat.id, f'''mailto:eyetubebot@gmail.com?subject=📬ID_{message.from_user.id}%20[Issue]%20Report%20&body=(🖇Please_Attach_your_Issue_screenshot)%0A%0A-[Country]:%0A%0A%0A%0A-%5BPlease%20describe%20your%20Issue%20here%5D%20:
                     ''')
    

    
@bot.message_handler(commands=['Engineer'])
def send_engineer(message):
    # Send photo of the developer
    bot.send_photo(message.chat.id, open('Michael.jpg', 'rb'), caption="💬 \"🅰🅽🆈🅱🅾🅳🆈 🅲🅰🅽 🅲🅾🅾🅺\" - 𝗠𝗶𝗰𝗵𝗮𝗲𝗹 𝗔𝗽𝗽𝗶𝗮𝗵")

    # Provide contact details and a brief bio
    bot.reply_to(message, """
    
𝐘𝐞𝐥𝐥𝐨 , 𝐈'𝐦 𝐌𝐢𝐜𝐡𝐚𝐞𝐥 𝐀𝐩𝐩𝐢𝐚𝐡, 𝐚𝐧 𝐚𝐬𝐩𝐢𝐫𝐢𝐧𝐠 𝐀𝐫𝐭𝐢𝐟𝐢𝐜𝐢𝐚𝐥 𝐈𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞 𝐄𝐧𝐠𝐢𝐧𝐞𝐞𝐫 𝐚𝐧𝐝 𝐭𝐡𝐞 𝐥𝐞𝐚𝐝𝐞𝐫 𝐨𝐟 𝐏𝐨𝐬𝐬𝐢𝐛𝐢𝐥𝐢𝐭𝐲 𝐀𝐢 𝐚𝐧𝐝 𝐂𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲 𝐚 𝐒𝐭𝐮𝐝𝐞𝐧𝐭 𝐨𝐟 𝐭𝐡𝐞 𝐔𝐧𝐢𝐯𝐞𝐫𝐬𝐢𝐭𝐲 𝐨𝐟 𝐄𝐝𝐮𝐜𝐚𝐭𝐢𝐨𝐧, 𝐖𝐢𝐧𝐧𝐞𝐛𝐚.
    
    𝐈 𝐬𝐩𝐞𝐜𝐢𝐚𝐥𝐢𝐳𝐞 𝐢𝐧 𝐁𝐮𝐢𝐥𝐝𝐢𝐧𝐠 𝐀𝐢 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐞𝐝 𝐂𝐡𝐚𝐭𝐁𝐨𝐭𝐬, 𝐒𝐲𝐬𝐭𝐞𝐦𝐬 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐨𝐧 𝐚𝐧𝐝 𝐒𝐨𝐟𝐭𝐰𝐚𝐫𝐞 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭 𝐮𝐬𝐢𝐧𝐠 𝐏𝐲𝐭𝐡𝐨𝐧 𝐚𝐧𝐝 𝐂++.

    𝐂𝐨𝐧𝐧𝐞𝐜𝐭 𝐰𝐢𝐭𝐡 𝐦𝐞:  
               
    • 𝙇𝙞𝙣𝙠𝙚𝙙𝙄𝙣: [𝙈𝙞𝙘𝙝𝙖𝙚𝙡 𝘼𝙥𝙥𝙞𝙖𝙝](https://www.linkedin.com/in/michael-appiah-9b6919255) 💼
    
    • 𝙓(𝙏𝙬𝙞𝙩𝙩𝙚𝙧) : ( https://x.com/mickekofi )             
   
    • 𝙂𝙞𝙩𝙃𝙪𝙗: [𝙈𝙞𝙘𝙠𝙚𝙠𝙤𝙛𝙞] (https://github.com/Mickekofi) 🧑‍💻
    
    
                 
            ©️ Possibility AI `24
                                  
    """)


# Image Processing Zone
#==============================================================================
from PIL import Image, ImageEnhance, ImageOps

#------------------------------Tuning Functions--------------------------------------

# Sharpness adjustment (-100 to 100)
def apply_sharpness(img, sharpness_percentage):
    
    sharpener = ImageEnhance.Sharpness(img)
    sharpness_factor = 1 + (sharpness_percentage / 100) if sharpness_percentage >= 0 else 1 / (1 - (sharpness_percentage / 100))
    return sharpener.enhance(sharpness_factor)

# Brightness adjustment (-100 to 100)
def apply_brightness(img, brightness_percentage):
    
    enhancer_bright = ImageEnhance.Brightness(img)
    brightness_factor = 1 + (brightness_percentage / 100) if brightness_percentage >= 0 else 1 / (1 - (brightness_percentage / 100))
    return enhancer_bright.enhance(brightness_factor)

# Contrast adjustment (-100 to 100)
def apply_contrast(img, contrast_percentage):
    
    enhancer_contrast = ImageEnhance.Contrast(img)
    contrast_factor = 1 + (contrast_percentage / 100) if contrast_percentage >= 0 else 1 / (1 - (contrast_percentage / 100))
    return enhancer_contrast.enhance(contrast_factor)

# Saturation adjustment (-100 to 100)
def apply_saturation(img, saturation_percentage):
    
    enhancer_color = ImageEnhance.Color(img)
    saturation_factor = 1 + (saturation_percentage / 100) if saturation_percentage >= 0 else 1 / (1 - (saturation_percentage / 100))
    return enhancer_color.enhance(saturation_factor)

# Ambiance (brightness approximation) (-100 to 100)
def apply_ambiance(img, ambiance_percentage):
    
    return apply_brightness(img, ambiance_percentage)

# Shadow adjustment (approximated with brightness) (-100 to 100)
def apply_shadow(img, shadow_percentage):
    
    return apply_brightness(img, shadow_percentage)

# Warmth adjustment (color approximation) (-100 to 100)
def apply_warmth(img, warmth_percentage):
    
    return apply_saturation(img, warmth_percentage)

# Structure adjustment (combines contrast and sharpness) (-100 to 100)
def apply_structure(img, structure_percentage):
    
    img = apply_contrast(img, structure_percentage)
    img = apply_sharpness(img, structure_percentage / 2)
    return img

# Highlight adjustment (only positive values)
def apply_highlights(img, highlights_percentage):
    
    grayscale_img = img.convert("L")
    threshold = 200
    highlights_mask = grayscale_img.point(lambda p: 255 if p > threshold else 0)

    if img.mode in ("RGBA", "LA"):
        img = img.convert("RGBA")
        highlights_mask = highlights_mask.convert("1")
        enhancer_bright = ImageEnhance.Brightness(img)
        highlights_factor = 1 + (highlights_percentage / 100)
        brightened_img = enhancer_bright.enhance(highlights_factor)
        img = Image.composite(brightened_img, img, highlights_mask)
    else:
        img = ImageEnhance.Brightness(img).enhance(1 + (highlights_percentage / 100))

    return img

# Vignette effect (0 to 100)
def apply_vignette(img, vignette_percentage):
    
    width, height = img.size
    vignette = Image.new("L", (width, height), 0)
    
    for x in range(width):
        for y in range(height):
            distance = ((x - width / 2) ** 2 + (y - height / 2) ** 2) ** 0.5
            vignette.putpixel((x, y), int(min(255, max(0, vignette_percentage * (distance / max(width, height))))))

    vignette_img = ImageOps.colorize(vignette, "black", "white")
    img = Image.blend(img, vignette_img, vignette_percentage / 100)
    
    return img

# Clarity adjustment (-100 to 100)
def apply_clarity(img, clarity_percentage):
    
    return apply_contrast(img, clarity_percentage)

# Exposure adjustment (-100 to 100)
def apply_exposure(img, exposure_percentage):
    
    return apply_brightness(img, exposure_percentage)

# Blue Tone Adjustment
def apply_blue_tone(img, blue_percentage):
    
    r, g, b = img.split()  # Split into red, green, blue channels
    b = ImageEnhance.Brightness(b).enhance(1 + (blue_percentage / 100))  # Modify the blue channel
    img = Image.merge('RGB', (r, g, b))  # Merge channels back
    return img

# Red Tone Adjustment
def apply_red_tone(img, red_percentage):
    
    r, g, b = img.split()  # Split into red, green, blue channels
    r = ImageEnhance.Brightness(r).enhance(1 + (red_percentage / 100))  # Modify the red channel
    img = Image.merge('RGB', (r, g, b))  # Merge channels back
    return img

# White Tone Adjustment (Approximated by increasing brightness on all channels)
def apply_white_tone(img, white_percentage):
    
    r, g, b = img.split()  # Split into red, green, blue channels
    r = ImageEnhance.Brightness(r).enhance(1 + (white_percentage / 100))  # Modify the red channel
    g = ImageEnhance.Brightness(g).enhance(1 + (white_percentage / 100))  # Modify the green channel
    b = ImageEnhance.Brightness(b).enhance(1 + (white_percentage / 100))  # Modify the blue channel
    img = Image.merge('RGB', (r, g, b))  # Merge channels back
    return img

# Black and White tone adjustment (-100 to 100)
def apply_black_and_white(img, bw_percentage):
    
    grayscale_img = img.convert("L").convert("RGB")
    bw_percentage = max(-100, min(100, bw_percentage))  # Clamping between -100 and 100
    factor = abs(bw_percentage) / 100
    
    if bw_percentage >= 0:
        return Image.blend(img, grayscale_img, factor)
    else:
        # If bw_percentage is negative, blend in the opposite direction (keep color)
        return Image.blend(grayscale_img, img, factor)

# Yellow tone adjustment (-100 to 100)
def apply_yellow_tone(img, yellow_percentage):
    
    yellow_layer = Image.new("RGB", img.size, (255, 255, 0))  # Create a yellow layer
    yellow_percentage = max(-100, min(100, yellow_percentage))  # Clamping between -100 and 100
    factor = abs(yellow_percentage) / 100
    
    if yellow_percentage >= 0:
        return Image.blend(img, yellow_layer, factor)
    else:
        # If yellow_percentage is negative, blend to remove yellow tint (back to original colors)
        return Image.blend(yellow_layer, img, factor)



# Directory to store temporary images
TEMP_FOLDER = 'temp_images'
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

# Maximum image size (in bytes) for input and output (20MB)
MAX_IMAGE_SIZE = 20 * 1024 * 1024

# Maximum allowed dimensions for images to save memory
#MAX_WIDTH = 3000  # Max width in pixels
#MAX_HEIGHT = 3000  # Max height in pixels


# Step 1: Handle /rm_bg command
# Store file_id temporarily in a dictionary
user_data = {}


# Step 1: Handle the /rm_bg command
@bot.message_handler(commands=['rm_bg'])
def rm_bg_command(message):
    bot.reply_to(message, "🌆 Please send an image (up to 20MB) for background removal or resizing.")


# Step 2: Handle Image
# Store file_id temporarily in a dictionary
user_data = {}



# Step 2: Handle Image
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    user_id = message.chat.id

    # Check if user is allowed to send a photo
    
    # Check if the user has already uploaded an image that has not been processed
    if user_id in user_data:
        bot.reply_to(message, "⚠️ Warning...You didnt finnish processing your Previous Image. Please choose an option for the previous image before Uploading a new one.")
        return  # Alert the user and do not process the new image

    
    # Get the new image info
    try:
        # logging.info(f"Received image from user {message.chat.id}")
        file_info = bot.get_file(message.photo[-1].file_id)
        file_size = message.photo[-1].file_size

        if file_size > MAX_IMAGE_SIZE:
            bot.reply_to(message, "The image is larger than 20MB. Please upload a smaller image.")
            logging.warning(f"Image too large ({file_size} bytes) for user {message.chat.id}")
            return

        # Download the image
        downloaded_file = bot.download_file(file_info.file_path)
        image_path = os.path.join(TEMP_FOLDER, f"{message.photo[-1].file_id}.png")

        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            logging.info(f"Image saved to {image_path} for user {message.chat.id}")

        # Resize image to reduce memory usage if necessary
        """
        img = Image.open(image_path)
        img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
        img.save(image_path)  # Overwrite the original file with the resized version
        logging.info(f"Image resized to fit within {MAX_WIDTH}x{MAX_HEIGHT} for user {message.chat.id}")
        """

        # Store the image path and file ID for later use
        user_data[message.chat.id] = {
            'file_id': message.photo[-1].file_id,
            'image_path': image_path
        }

        # Ask the user for background color, sketch, resize, text extraction, or retouch enhancement options
        markup = telebot.types.InlineKeyboardMarkup()
        options = [
            'Background 🟥_Red', 'Background 🟨_Yellow', 'Background ⬜️_White', 
            'Background ⬛️_Black', 'Background 🟩_Green', '✏️_2D Anime Sketch','🐦_3d Egyptian Art', 
            '🩻_Grayscale Artistic', '✂️_Resize', '🛠_Extract Text from Image', '✨_Retouch Enhance'
        ]
        for option in options:
            markup.add(telebot.types.InlineKeyboardButton(option, callback_data=f"{option.lower()}"))

        bot.reply_to(message, "🎨 *Choose an Image Processing Option*:", reply_markup=markup, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, "❌ Error processing the image.")
        logging.error(f"Error processing image for user {user_id}: {str(e)}")

    except Exception as e:
        bot.reply_to(message, "❌ Error processing the image.")
        logging.error(f"Error processing image for user {user_id}: {str(e)}")
 
   
@bot.callback_query_handler(func=lambda call: '_' in call.data)
def handle_color_choice(call):
    
    if call.message.chat.id not in user_data:
        bot.reply_to(call.message, "⚠️ Image not found. Please upload an image first.")
        return
    
    chosen_option = call.data.split('_')[1]
    image_info = user_data.get(call.message.chat.id)
    image_path = image_info['image_path']

    if not os.path.exists(image_path):
        bot.reply_to(call.message, "⚠️ Image processing failed. Please try again.")
        return

    
    if chosen_option == 'grayscale artistic':
        bot.reply_to(call.message, "🌊 _Applying Grayscale Artistic effect..._", parse_mode="Markdown")
        apply_grayscale_artistic(call)


    elif chosen_option == 'resize':
        bot.send_message(call.message.chat.id, "✂️ Please enter the new dimensions in the format WIDTHxHEIGHT (e.g., 800x600):")
        bot.register_next_step_handler(call.message, resize_image)
    
    elif chosen_option == 'extract text from image':
        bot.reply_to(call.message, "🔍 _Extracting text from image..._", parse_mode="Markdown")
        extract_text(call)

    elif chosen_option == '3d egyptian art':
        bot.reply_to(call.message,"Moulding Image in Ceramics")
        apply_ceramic_art(call)

    elif chosen_option == 'retouch enhance':
        bot.reply_to(call.message, "✨ _Applying Retouch Enhancement_ ✨", parse_mode="Markdown")
        asyncio.run(retouch_enhance(call))
    else:
        bot.reply_to(call.message, f"🫗 _Processing the image with {chosen_option} effect..._", parse_mode="Markdown")
        process_image(call, chosen_option)



# Step 4: Apply Grayscale Artistic effect
def apply_grayscale_artistic(call):
    try:
        image_info = user_data.get(call.message.chat.id)
        image_path = image_info['image_path']

        img = Image.open(image_path)
        img = img.filter(ImageFilter.SMOOTH_MORE)  # Apply a smoothing filter
        

        #Tuning
        img = apply_brightness(img,-15)
        img = apply_red_tone(img,70)
        img = apply_black_and_white(img,70)
        img = apply_highlights(img,-5)
        img = apply_sharpness(img,90)




        processed_image_path = os.path.join(TEMP_FOLDER, f"grayscale_artistic_{image_info['file_id']}.png")
        img.save(processed_image_path)

        with open(processed_image_path, 'rb') as processed_file:
            bot.send_photo(call.message.chat.id, processed_file)

        os.remove(image_path)
        os.remove(processed_image_path)

        del user_data[call.message.chat.id]

    except Exception as e:
        bot.reply_to(call.message, f"An error occurred: {str(e)}")
        logging.error(f"Error applying grayscale artistic effect for user {call.message.chat.id}: {str(e)}")



def resize_image(message):
    try:
        new_size = message.text.split('x')
        new_width = int(new_size[0])
        new_height = int(new_size[1])

        if message.chat.id not in user_data:
            bot.reply_to(message, "⚠️ Image not found. Please upload an image first.")
            logging.error(f"No image found for user {message.chat.id}")
            return

        image_info = user_data.get(message.chat.id)
        image_path = image_info['image_path']

        # Open the original image and resize it
        img = Image.open(image_path)
        img = ImageOps.fit(img, (new_width, new_height), Image.Resampling.LANCZOS)

        resized_image_path = os.path.join(TEMP_FOLDER, f"resized_{image_info['file_id']}.png")
        img.save(resized_image_path)

        bot.reply_to(message, "✂️ Image resized and sent successfully ✂️")

        # Send the resized image
        with open(resized_image_path, 'rb') as resized_file:
            bot.send_photo(message.chat.id, resized_file)

        # Clean up both resized and original images
        os.remove(resized_image_path)
        os.remove(image_path)  # Delete the original image

        # Clear the user data to avoid future issues
        del user_data[message.chat.id]

    except Exception as e:
        bot.reply_to(message, "Invalid input. Please enter the dimensions in the format WIDTHxHEIGHT.")
        logging.error(f"Error resizing image for user {message.chat.id}: {str(e)}")

# Step 5: Extract text from the image
from textblob import TextBlob

def extract_text(call):
    try:
        # Retrieve the image info from user data
        image_info = user_data.get(call.message.chat.id)
        if not image_info:
            bot.send_message(call.message.chat.id, "⚠️ No image found. Please upload an image first.")
            return
        
        image_path = image_info['image_path']
        
        # Open the image
        img = Image.open(image_path)
        
        # Optionally, preprocess the image for better accuracy (e.g., convert to grayscale)
        img = img.convert('L')  # Convert to grayscale
        
        # Extract text from the image using pytesseract
        extracted_text = pytesseract.image_to_string(img)
        
        # Check if text was extracted successfully
        if extracted_text.strip():
            # Optionally, correct spelling using TextBlob
            corrected_text = str(TextBlob(extracted_text).correct())
            
            # Send the extracted (and corrected) text to the user
            bot.send_message(call.message.chat.id, f"🔍 Extracted text:\n{corrected_text}")
        else:
            bot.send_message(call.message.chat.id, "⁉️ I couldn't find any text in your image. Please make sure the image is clear.")

        # Clean up by deleting the image
        if os.path.exists(image_path):
            os.remove(image_path)

        # Remove user data entry for this image
        del user_data[call.message.chat.id]

    except Exception as e:
        bot.reply_to(call.message, f"An error occurred while extracting text: {str(e)}. Please try again with a clearer image.")
        logging.error(f"Error extracting text for user {call.message.chat.id}: {str(e)}")





# High-Quality Retouch Enhancement (Asynchronous version)
 # Main function to apply all enhancements
async def retouch_enhance(call):
    user_id = call.message.chat.id

    image_info = user_data.get(user_id)
    if not image_info:
        bot.reply_to(call.message, "No image found. Please upload an image first.")
        return

    image_path = image_info['image_path']

    bot.reply_to(call.message, "🔧 Enhancing image quality, please wait...")
    
    try:
        img = Image.open(image_path)

        # Apply individual enhancements
        """
        img = apply_sharpness(img, 80)       # Example: 15% sharpness
        img = apply_contrast(img,30)
        img = apply_brightness(img,30)
        img = apply_saturation(img,15)
        img = apply_highlights(img,-40)
           """

        img = apply_saturation(img,30)
        img = apply_ambiance(img,5)
        img = apply_highlights(img,1)
        img = apply_brightness(img,-25)
        img = apply_shadow(img,20)
        img = apply_blue_tone(img,50)
        img = apply_sharpness(img,80)
        img = apply_structure(img,-7)
        img = img.filter(ImageFilter.SMOOTH_MORE)
        # Save the enhanced image
        enhanced_image_path = image_path.replace(".png", "_enhanced.png")
        img.save(enhanced_image_path, dpi=(300, 300))  # Save with high DPI
        
        # Send enhanced image back to user
        with open(enhanced_image_path, 'rb') as enhanced_file:
            bot.send_photo(call.message.chat.id, enhanced_file)

        # Clean up temporary files
        os.remove(enhanced_image_path)
        # Clean up by deleting the original image
        if os.path.exists(image_path):
            os.remove(image_path)

        # Remove user data entry for this image
        del user_data[user_id]

    except Exception as e:
        bot.reply_to(call.message, f"An error occurred: {str(e)}")
        logging.error(f"Error enhancing image for user {call.message.chat.id}: {str(e)}")




# Step 7: Process the image with the chosen effect (background color or sketch)
def process_image(call, chosen_option):
    try:

        user_id = call.message.chat.id

    # Check if the user has uploaded an image
        if user_id not in user_data or 'image_path' not in user_data[user_id]:
            bot.reply_to(call.message, "⚠️ No image found. Please upload an image first.")
            return

    # Mark the image as processed
        user_data[user_id]['processed'] = True

        image_path = user_data[user_id]['image_path']

        image_info = user_data.get(call.message.chat.id)
        image_path = image_info['image_path']

        if chosen_option == '2d anime sketch':
            img = Image.open(image_path).convert("L")  # Convert to grayscale
            img = img.filter(ImageFilter.CONTOUR)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)

            processed_image_path = os.path.join(TEMP_FOLDER, f"sketch_{image_info['file_id']}.png")
        else:
            with open(image_path, 'rb') as input_file:
                img_data = input_file.read()
                output_img_data = remove(img_data)

            img = Image.open(io.BytesIO(output_img_data)).convert("RGBA")

            if chosen_option != 'transparent':
                bg_color_map = {
                    'red': (255, 0, 0, 255),
                    'yellow': (255, 255, 0, 255),
                    'white': (255, 255, 255, 255),
                    'black': (0, 0, 0, 255),
                    'green': (0, 255, 0, 255),
                    }
                bg_color = bg_color_map.get(chosen_option, (255, 255, 255, 255))

                bg = Image.new("RGBA", img.size, bg_color)
                img = Image.alpha_composite(bg, img)

            processed_image_path = os.path.join(TEMP_FOLDER, f"processed_{image_info['file_id']}.png")
        
        img.save(processed_image_path)
        logging.info(f"Processed image saved to {processed_image_path} for user {call.message.chat.id}")

        with open(processed_image_path, 'rb') as processed_file:
            bot.send_photo(call.message.chat.id, processed_file)

        os.remove(image_path)
        os.remove(processed_image_path)

        del user_data[call.message.chat.id]

    except Exception as e:
        bot.reply_to(call.message, f"An error occurred: {str(e)}")
        logging.error(f"Error processing image for user {call.message.chat.id}: {str(e)}")



def apply_ceramic_art(call):
    try:
        # Retrieve image path from user data
        image_info = user_data.get(call.message.chat.id)
        image_path = image_info['image_path']

        # Step 1: Open the image
        img = Image.open(image_path)

        # Step 2: Apply a smoothing filter
        img = img.filter(ImageFilter.SMOOTH_MORE)

        # Step 3: Convert to grayscale for the base effect
        img = img.convert("L")

        # Step 4: Apply edge detection to simulate drawing strokes
        edges = img.filter(ImageFilter.FIND_EDGES)

        # Step 5: Emboss the image to give it a 3D-like appearance
        embossed_img = img.filter(ImageFilter.EMBOSS)

        # Step 6: Enhance contrast to make the 3D effect more powerful
        contrast_enhancer = ImageEnhance.Contrast(embossed_img)
        contrast_img = contrast_enhancer.enhance(2.0)

        # Step 7: Smoothen the image to simulate artistic strokes
        smoothed_img = contrast_img.filter(ImageFilter.SMOOTH)

        # Step 8: Blend edges with the embossed and smoothed image for the final artistic touch
        artistic_drawing = Image.blend(smoothed_img.convert("RGB"), edges.convert("RGB"), alpha=0.3)

        # Step 9: Enhance the overall contrast and brightness for a dramatic effect
        final_image = ImageEnhance.Contrast(artistic_drawing).enhance(1.5)
        final_image = ImageEnhance.Brightness(final_image).enhance(1.2)

        # Step 10: Save the processed image
        processed_image_path = os.path.join(TEMP_FOLDER, f"ceramic_art_{image_info['file_id']}.png")
        final_image.save(processed_image_path)

        # Send the processed image back to the user
        with open(processed_image_path, 'rb') as processed_file:
            bot.send_photo(call.message.chat.id, processed_file)

        # Clean up temporary files
        os.remove(image_path)
        os.remove(processed_image_path)

        # Remove user data after processing
        del user_data[call.message.chat.id]

    except Exception as e:
        bot.reply_to(call.message, f"An error occurred: {str(e)}")
        logging.error(f"Error applying ceramic art effect for user {call.message.chat.id}: {str(e)}")


#==============================================================================
@retry_on_failure
def bot_polling():
    bot.polling(none_stop=True, timeout=60)

bot_polling()
