#! python3
'''This is a discord bot to assist with FFXIV'''

import urllib.request
import discord
from discord.ext import commands
from bs4 import BeautifulSoup

Client = discord.Client()
bot_prefix = "?"
client = commands.Bot(command_prefix=bot_prefix)
baseSearchContext = 'https://ffxiv.consolegameswiki.com/mediawiki/index.php?title=Special%3ASearch&profile=default&fulltext=Search&search='
baseResultContext = 'https://ffxiv.consolegameswiki.com/wiki/'

@client.event
async def on_ready():
    '''local echo for notification that bot is online'''
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    await client.change_presence(game=discord.Game(name='FFXIV4U'))

@client.command(pass_context=True)
async def ping(ctx):
    '''basic response functionality'''
    await client.say("Pong!")

@client.command(pass_context=True)
async def wiki(ctx):
    '''returns a link from ffxiv.consolegameswiki.com for the
    context provided. It just uses the search function and returns
    the first page title match.'''

    # Set the default message to be returned
    #TODO: Replace this with alternative suggestions
    #TODO: account for spelling mistakes?
    returnMessage = "Sorry, but I couldn't find that."
    # Set the User-Agent for later
    #TODO: Check license. Is this allowed?
    userAgent = ""

    # grab the whole message that triggered the bot
    terms = ctx.message.content
    # remove the trigger and whitespace
    terms = terms.replace("?wiki ", "")
    # replace the whitespace with the + character to
    terms = terms.replace(" ", "+")
    # append the search terms to the base search URL
    url = baseSearchContext + terms
    # make url request using the user agent identified above
    req = urllib.request.Request(url, headers={'User-Agent' : userAgent})
    # open a port and scrape the page into the file
    with urllib.request.urlopen(req) as response:
        data = response.read()
    # now that we have the data, parse it into a BeautifulSoup object
    #TODO: Modify this to only read until the important part of the file.
    soup = BeautifulSoup(data, 'html.parser')
    # use a feature of BeautifulSoup to find the mw-search-exists class
    #TODO: Is there a better way?
    searchResult = soup.select(".mw-search-exists")
    # if the result exists, grab the substring that represents the page and format it into a link
    # this is pretty ham-fisty, it seems like there is probably a better way to do this with Beautiful Soup.
    if searchResult != []:
        resultURL = soup.p.a.contents[0]
        resultURL = resultURL.replace("'", "%27")
        resultURL = resultURL.replace(" ", "_")
        # adding the angle brackets disables discord's preview of the page
        returnMessage = "<" + baseResultContext + resultURL + ">"

    await client.say(returnMessage)

# Your own token goes here
client.run("")
