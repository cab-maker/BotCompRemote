# BotCompRemote

BotCompRemote is a simple Python Discord bot that allows you to control your computer remotely. You can access the computer’s IP, open or close applications, take screenshots, find and manage browser tabs, control the webcam, and more using Discord commands. This bot can also be helpful if your computer is stolen and you want to locate its IP address.

## Features
- Retrieve public and local IP addresses.
- Shut down the computer remotely.
- View and control open browser tabs.
- Perform Google searches from Discord.
- Take screenshots and send them via Discord.
- Start and stop the webcam feed.
- Remotely run or view applications.
- Create and edit notes via Notepad.

## Prerequisites

1. Python 3.8 or higher installed on your machine.
2. A Discord Bot Token (obtainable from the Discord Developer Portal).
3. Git (for cloning the repo).

## Installation Steps

### 1. Clone the Repository
To get started, clone the repository from GitHub by running:

- `git clone https://github.com/cab-maker/BotCompRemote/`
- `cd BotCompRemote`

### 2. Install Dependencies
Use pip to install all the required packages. You can find them in the `requirements.txt` file:

- `pip install -r requirements.txt`

The dependencies include:

- discord.py
- requests
- pprint
- opencv-python (cv2)
- pygetwindow
- pyautogui
- BeautifulSoup4 (bs4)

### 3. Configure the Bot Token
Edit the Python file and replace `'YOUR TOKEN HERE'` with your Discord bot token:

`bot.run('YOUR TOKEN HERE')`

### 4. Run the Bot
Once everything is set up, run the bot by using the command:

- `python main.py`

## Commands
- `!getip`: Retrieves both public and local IP addresses.
- `!shutdown`: Shuts down the computer remotely.
- `!find_tabs [browser_name]`: Lists open tabs of a specified browser (Chrome, Firefox, etc.).
- `!close_tab [browser_name] [tab_title]`: Closes a specific tab in a specified browser.
- `!google [query]`: Performs a Google search and returns the top 5 results.
- `!runapp [app_name]`: Runs a specified application (e.g., Notepad, Chrome).
- `!createnote [content]`: Creates and opens a new Notepad file with the given content.
- `!screenshot`: Takes and sends a screenshot.
- `!viewtab`: Lists open windows, allowing you to select one to view.
- `!start_cam`: Starts the webcam and streams images to Discord.
- `!stop_cam`: Stops the webcam feed.

## Usage Examples
- To find the IP address, use the command:

`!getip`

The bot will reply with your public and local IP address.

- To shut down the computer, use the command:

`!shutdown`

The bot will initiate a system shutdown.
