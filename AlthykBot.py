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
altResultContext = 'https://duckduckgo.com/?q=ffxiv.consolegameswiki.com+'
userAgent = ''
clientToken = ''

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

    returnMessage = 'If you see this, something bad happened with the search...'
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
    # When a search term has its own page, ffxivwiki results include a
    # specific class (.mw-search-exists). Use a feature of BeautifulSoup
    # to find the mw-search-exists class
    #TODO: Is there a better way? There is BeautifulSoup documentation for
    # grabbing only part of the page into the object. If there is a hit,
    # the target class will be close to the top of the page.
    searchResult = soup.select(".mw-search-exists")
    # now that we've looked at the page for the class, the ffxivwiki site is useless
    # if the term wasn't found or was misspelled, etc. In this case, the bot should return
    # a link to a duckduckgo search for the terms.
    if searchResult == []:
        returnMessage = "<" + altResultContext + terms + ">"
    # if the result exists, grab the substring that represents the page and format it into a link
    # this is pretty ham-fisted, it seems like there is probably a better way to do the parsing with Beautiful Soup.
    if searchResult != []:
        # this is a direct drilldown to the link portion of the tag
        resultURL = soup.p.a.contents[0]
        # quick manipulation to end up with a string that will work as a url
        resultURL = resultURL.replace("'", "%27")
        resultURL = resultURL.replace(" ", "_")
        # adding the angle brackets disables discord's preview of the page
        returnMessage = "<" + baseResultContext + resultURL + ">"

    # post the link to the channel
    await client.say(returnMessage)

# The token goes here
client.run(clientToken)
