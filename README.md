<h1>DiscordMadnessboard</h1>
A local soundboard for your discord server, no strings attached!<br>
A video installation guide will be up shortly!
<h2>First Things First</h2>
Download the <a href="https://github.com/Rasmusb94/DiscordMadnessboard/releases">latest release of DiscordMadnessboard</a> and extract the folder to your preferred location.
<h2>Creating Your Bot</h2>
Go to <a href="https://discord.com/developers/applications">the Discord Developer Portal</a>.
<ul>
  <li>Click New Application</li>
  <li>Set a name for your bot and accept the T&C</li>
  <li>Set an avatar for your bot if you like</li>
  <li>Go to the "Bot" tab</li>
  <li>Scroll down to "Privileged Gateway Intents" and enable all three options</li>
  <li>Scroll back up and select "Reset Token" to show your bot token, you will need this for the bot data file</li>
  <li>Invite your bot by going to - www.discordapp.com/oauth2/authorize?client_id={CLIENT_ID}&scope=bot&permissions=35184408799232
Replace the {CLIENT_ID} including the brackets with the "Application ID" found under the "General Information" tab in your Application settings.</li>
  <li>Select which server you want to add the bot to.</li>
</ul>
<h2>Bot Data Information</h2>
Open the botdata.json file using your text editor of choice. Any notepad should work just fine.
Note: Make sure NOT TO add OR remove any " or , characters in the file.
<ul>
  <li>Update the discord_token field using the token you just got from the developer Portal</li>
  <li>Update the soundfiles_path field with the path to your sounds folder. To easily get the path, right click the folder, go properties, and copy the location. Remember to change all \ to /</li>
  <li>Enabling developer mode to get the server ID.
If you cannot find the ID of your server, you must go to user settings, scroll to "Advanced" under "App Settings" and enable Developer mode.
After doing this, simply right click your server and select "Copy Server ID"</li>
  <li>Update the discord_server_id field with the ID of your server</li>
  <li>(Optional) Feel free to edit the other fields but make sure to keep the format as is</li>
</ul>
<h2>Dependencies</h2>
<h3>FFMpeg</h3>
<ul>
  <li>Go to www.github.com/BtbN/FFmpeg-Builds/releases and download the latest gpl build for your system</li>
  <li>Open the Zipped folder and extract the "bin" folder to your preferred location, for example in the DiscordMadnessboard directory</li>
  <li>Open Windows System Properties and click the "Advanced" tab, and go to "Environment Variables"</li>
  <li>Click the "Path" System variable, "Edit", and "New". Here you will need to add the path to your /bin folder, which can quickly be found by right clicking the folder and going to properties</li>
  <li>Click OK and exit System Properties, FFMpeg is now ready to be used</li>
</ul>
<h3>Python</h3>
Should work with Python 3.10 + but only tested with 3.11
<ul>
  <li>Go to <a href="https://python.org/downloads/">the Python website</a> and download the latest version of Python 3.11</li>
  <li>When installing, make sure to tick the "Add python.exe to PATH" box, or otherwise do the same as you did for FFMpeg by manually adding Python to path</li>
</ul>
<h3>Python Libraries</h3>
<ul>
  <li>Open Windows PowerShell as an Administrator</li>
  <li>Type "pip install discord"</li>
  <li>Type "pip install mutagen"</li>
  <li>Type "pip install PyNaCl"</li>
</ul>
This should install the required libraries to Python, if it does not work please check your Python installation completed correctly, or use another method such as choco to install the libraries.

<h2>Running the Bot</h2>
That's it!<br>
You can now run the soundboard by opening the bot.py file with Python. For troubleshooting you can run the file in debug mode using your developing environment of choice, such as VS Code.
<h3>Commands</h3>
The currently available commands are as follows:
<ul>
  <li>random - Plays a random soundfile</li>
  <li>spam - Plays a number of clips with a set delay - ?spam 5 0.5</li>
  <li>chaos - Plays a random number of clips with a random delay</li>
  <li>fullchaos - Plays a random number of clips without interruptions</li>
  <li>dr - Plays 2 random soundfiles - ?dr 0.5</li>
  <li>combo - Plays clips including the given word - ?combo ramsey 5 0.5</li>
  <li>list - Sends a list of all available soundfiles to the user</li>
  <li>help</li>
  <li>stop</li>
  <li>join</li>
  <li>leave</li>
</ul>
<h3>Updating the Soundfiles</h3>
I've added some sample clips but I encourage you to add your own for the best experience.<br>
Make sure to cut the clips quite close to where the audio starts and naming the clips smartly for the "combo" command.
