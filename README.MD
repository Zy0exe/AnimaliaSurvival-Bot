# Animalia Bot

## Overview
A discord bot that allows Staff to manage their server via commands, and players to have fun such has play roulette, buy/inject animals and win coins for staying in voice chats!

**YOU HAVE TO HOST THIS BOT YOURSELF**

## Motivation
So basically i used to play the game and like many people wanted to make my own server, at the time it required a lot of my time and my staff time in order to be able to get things solved, getting Growths etc. So i decided to make my own bot that would handle all of that and even more giving me some sort of way to compete with the big servers. So hopefully his will open doors for new servers!

## FAQ
**Q: Why Python?**

A: I had not used python in a while and given that python is pretty much forgotten by discord i wanted to make it more interesting / challanging for me.

**Q: Does the bot have any malicious code?**

A: No, the bot is fully open-source none of its code is obfuscted or encrypted.

**Q: How is the bot performance wise?**

A: I dont have a good computer by todays standards by any means and i have always been able to keep it running and do literally anything i wanted on my computer.

**Q: How long did it take you to make this?**

A: Well initially when i made it just for my server i coded it in about a week, now im just trying to make it a public thing and release it for people to use.

**Q: Would you be willing to give support?**

A: Yes, you can contact me at any time via discord, with anything even if you want me to setup the bot for you. My discord is: _zeroxzero

**Q: Will you update the bot?**

A: Yes, i still have some features in mind that i can code, but that would require the devs to help me out a little.

## Prerequisites

This is basically the "base setup" so pay attention as it is not hard at all.

To start of you will want to create a discord application, so.

1 - Get [Python](https://www.python.org/) installed on your machine.

2 - Go to [Discord Dev Portal](https://discord.com/developers/applications) and make a new application (Leave this tab open).

3 - Go to [Steam API Key](https://steamcommunity.com/dev/apikey) and make a key if you dont have one already (Leave this tab open).

4 - Get a program to manage databases, i recommend [HeidiSql](https://www.heidisql.com/).

5 - Get [XAMPP](https://www.apachefriends.org/) this allows you to actually create databases.

6 - Get a program so you can change any code you want there's tons out there some people like using notepad++,
 I recommend using [Visual Studio Code](https://code.visualstudio.com/)



## Setup
For the advanced people looking into this, just go ahead and clone the repository using
```bash
git clone https://github.com/Zy0exe/AnimaliaSurvial-Bot.git
```
If you have all of the Prerequisites all you need to do after this is run this command

```bash
pip install -r requirements.txt
```
(Im sorry about the requirements.txt having some stuff that might not be needed for the actual funcionality of the bot but its just stuff that i have and use regularly).

---
# HeidiSql / XAMPP
For this part it might look complicated but it isnt!

After downloading both programs you will want to open up XAMPP first this is what it will look like, you want to press "Start" where the Arrow Points. Thats it for XAMPP yes you need to keep this app open.
![Alt text](https://cdn.discordapp.com/attachments/878741391323312129/1186599712963448832/image.png?ex=6593d619&is=65816119&hm=8d4a5e8ad41afb24b82558e0c3c3e3a50047546aa57610796a64103c59a6e3fb&)

For HeidiSql now, this is whats gonna look like when u open it, you wont have the "server" that i have but do not panic. Just click the green buttom at the bottom left "New" and you can name it whatever u want and click open.
![Alt text](https://cdn.discordapp.com/attachments/878741391323312129/1186600211674578944/image.png?ex=6593d690&is=65816190&hm=c886b913ecd6136fdb90d20c56ded653ad09a77ab817f8e5dea8cf123d93cafb&)

After this yours should looks like this:
![Alt text](https://cdn.discordapp.com/attachments/878741391323312129/1186601408364036126/image.png?ex=6593d7ad&is=658162ad&hm=93407c9ade8d5201110c8e0976ccfee24abad2921012a105fdf0748e6c04b8d7&)

Right Click New->Database and you can name it anything you want, After doing that you will want to open the file called db.sql that comes with the bot on the HeidiSql just click on the folder icon.
![Alt text](https://cdn.discordapp.com/attachments/878741391323312129/1186603297654714418/image.png?ex=6593d970&is=65816470&hm=bc21696ea09c6bd2782b3f5ca6293101dc86b462ef8e94a06a1f07bdce7f4811&)

After that just select the database you created (Left Click it) and then press the blue triangle next to the folder!


---
For the not so advanced people! I will be telling you how to do this based on all of the Prerequisites i mentioned above, so make sure you have Python | HeidiSql | Visual Studio Code installed.

You are going to press the green button that says "<>Code"
- Click "Download Zip"-
I personally had this in my server folder, but you can extract it anywhere u want.

Open up Visual Studio Code and do this:

1- Click "File" on the top

2- Click "Open Folder" and select the bot folder.

After this it should open up the folder and look something like this:
![Alt text](https://cdn.discordapp.com/attachments/878741391323312129/1186580742025789460/image.png?ex=6593c46e&is=65814f6e&hm=94cf80075a5a8be6eb28376aac6cbc09a464934a4ddf6d6a42565f61718e633d&)
If you dont see the "Terminal" tab at the bottom go to "Terminal" at the top and click "New Terminal"-

---

## Configuration
So the config file is the ".env" file and by **Default** it looks like this:
```bash
#Bot
TOKEN=
STEAM_API_KEY=""

#!Server
SERVER_NAME=Animalia 
SERVER_MAX_PLAYERS=100

#Paths
SERVER_FOLDER_PATH=
ANIMAL_TEMPLATES_PATH=
ADMINLIST_PATH=
BANLIST_PATH=

#Role Stuff
SUPER_USER_ID=
ADMIN_ROLE_ID=
MOD_ROLE_ID=

# Roulette Stuff
ROULETTE_CHANNEL_ID=
RED_BLACK_PAY=2
GREEN_PAYOUT=10

#Webhooks
PAY_WEBHOOK=
```
Well hoping that you didnt close the Discord |  Steam tabs previously in the 
```TOKEN=``` you will need to add your bot token in there so on the Discord Dev Portal select your application and go to the Bot section, copy the token and put it in there. (DO NOT SHARE THIS TOKEN!)

And in the ```STEAM_API_KEY``` just paste the key that you got on the steam website.

The Server part is pretty straigh forward it works with [topgameservers](https://topgameservers.net/) so you will need to register your server in there.

Now the Paths this is the important part so do not mess this up!

```SERVER_FOLDER_PATH``` will be the path to the PlayerData folder example:
```SERVER_FOLDER_PATH=C:/server/AnimaliaServer/AnimaliaSurvival/Saved/SaveGames/PlayerData/testLevel```

```ANIMAL_TEMPLATES_PATH``` will be the path for the folder that comes with the bot example:
```ANIMAL_TEMPLATES_PATH=C:/server/AnimaliaServer/AnimaliaSurvival/AnimaliaBot/AnimalTemplates/```

```ADMINLIST_PATH``` will be the path to your admin list example:  
```ADMINLIST_PATH=C:/servidores/animalia/AnimaliaSurvival/AdminList.txt```

```BANLIST_PATH``` will be the path to your ban list example:  
```BANLIST_PATH=C:/servidores/animalia/AnimaliaSurvival/banlist.txt```

---

For the roles it makes it so you set the amount of perms each person has, how do you get role ids? easy.
After making a discord role right click it and click "copy role id".

SuperUser has access to everything.

Admin has perms to ban, give animals to players but not manage the server like remove admins etc.

Mod has perms to Warn players and to "look" at their "game profile".

---

## I did all of this but the bot isnt on my discord?
Invite it to the server!

![Alt text](https://cdn.discordapp.com/attachments/878741391323312129/1186606210699513907/image.png?ex=6593dc26&is=65816726&hm=f4311e8840510fc716c770e3f96f6c207020c5c47cb3c4a2e2b6193112625471&)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)
