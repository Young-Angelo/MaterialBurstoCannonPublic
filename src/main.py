#from discord import colour
from jikanpy import Jikan
from discord.ext import tasks
import discord
import random
# from discord import member
from os import getenv
from discord.ext import commands
from rss_anime import *
from utils import *
from rss import *
from jikantest import *
import asyncio
from rss_anime1 import *
from UserDB import *
from AniScheduleScrape import *
from MALUser import *

client = commands.Bot(command_prefix=">")

last_modified = ""
last_anime = ""
blacklisted_ids = [40746]
channels = [727907805352427672,815163188789379092,815139546312343553,810492636326264862]
# server_preferences_location = "../server_preferences.json"
# server_preferences = dict(read_json(server_preferences_location))

@tasks.loop(seconds=5)
async def slow_count():
    print(GetAnimeSchedule())

async def periodic():
    global last_modified
    global last_anime
    # global client
    while True:
        now_modified = await get_rss_live_from_anischedule_modified()
        if now_modified == None:
            continue
        if last_modified != now_modified:
            last_anime,link,status = await get_rss_live_from_anischedule(last_anime)
            #gets the status of the feed, whether it was updated or not
            last_anime_firebase = await animeTrack.lastAnime()
            last_modified = now_modified
            # we need to update the modified anyway regardless of status
            if status and(last_anime not in last_anime_firebase):
                #if it was updated and there is a new anime
                send_stuff = str(last_anime) + '\n' + str(link)
                for channel_id in channels:
                    channel = client.get_channel(channel_id)
                    if channel == None:
                        continue
                    #get the channel to send the update
                    await channel.send(send_stuff)
                await animeTrack.updateAnime(last_anime)
                    #send the title of the feed entry
                    # await channel.send(link)
                #send the link of the feed entry
        await asyncio.sleep(10)

# # def stop():
    # # task.cancel()
# loop.call_later(5, stop)

jikan = Jikan()
# storage_recommendation = "recommendation_data.json"
# storage_recommended = "recommended_data.json"
# recommendation = dict(read_json(storage_recommendation))
# recommended = dict(read_json(storage_recommended))
user_db = UserDatabase()
user_rec = UserRecDatabase()
animeTrack = AnimeStoreRss()
userMAL = UserMAL()
TOKEN = getenv("DISCORD_BOT_TOKEN")
emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','❌']
chika_dance = None
@client.event
async def on_ready():
    print("Bot is ready, {0.user}".format(client))
    await client.change_presence(status=discord.Status.online, activity=discord.Game('>help'))
    loop = asyncio.get_event_loop()
    task = loop.create_task(periodic())
    global chika_dance
    chika_dance = str(client.get_emoji(818744163213770752))
    # slow_count.next_iteration()
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        embed1 = discord.Embed(title = "Not Enough Permissions", description="The bot doesn't have enough permissions")
        message = await ctx.send(embed=embed1)
        await asyncio.sleep(5)
        await message.delete()
    elif isinstance(error,commands.CommandNotFound):
        embed1 = discord.Embed(title = "No such command", description="No such command is defined",color=discord.Color.red())
        message = await ctx.send(embed=embed1)
        await asyncio.sleep(5)
        await message.delete()
    elif isinstance(error,commands.MissingRequiredArgument):
        embed1 = discord.Embed(title = "No argument given", description="Please provide an argument",color=discord.Color.red())
        message =await ctx.send(embed=embed1)
        await asyncio.sleep(5)
        await message.delete()
    elif isinstance(error,commands.MemberNotFound):
        embed1 = discord.Embed(title = "No such member exists", description="Please provide a member name",color=discord.Color.red())
        message =await ctx.send(embed=embed1)
        await asyncio.sleep(5)
        await message.delete()
    # elif isinstance(error,commands.CommandInvokeError):
        # embed1 = discord.Embed(title = "No Permissions", description="No permissions",color=discord.Color.red())
        # message =await ctx.send(embed=embed1)
        # await asyncio.sleep(5)
        # await message.delete()
    else:
        raise error

@client.command()
async def hello(ctx):
    await ctx.send("Hi")

@client.command()
async def quote(ctx):
    await ctx.send(get_quote())

@client.command()
async def store(ctx,*,arg1):
    # print(chika_dance)
    author_id = str(ctx.author.id)
    # recommendation = dict(read_json(storage_recommendation))
    # if author_id not in recommendation:
        # recommendation[author_id] = [arg1]
    # else:
        # temp_arr = [x.lower() for x in recommendation[author_id]]
        # if arg1.lower() in temp_arr:
            # await ctx.send("Duplicates not allowed")
            # return
        # else:
            # recommendation[author_id].append(arg1)
    # write_json(recommendation,storage_recommendation)
    results = await searchAnime(arg1)
    hyperlinks = []
    des = ""
    for i in range(0,len(results)):
        if results[i][2] == "Rx" or results[i][3] in blacklisted_ids: #or search_tag[i] == "R+":
            results[i][0] = "Redacted PG"
            results[i][1] = "Redacted"
            results[i][2] = 'Rx'
        k = i + 1
        hyperlinks.append('[{a}]({link})'.format(a=results[i][0], link=results[i][1] ))
        des += str(k) + "." + hyperlinks[i] + '\n'
    show_embed = discord.Embed(title = "Add To Favourites",description=des,color = discord.Color.purple())
    message = await ctx.send(embed=show_embed)
    for i in emojis:
        await message.add_reaction(i)
    def checkEmo(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emojis
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=checkEmo)
    except asyncio.TimeoutError:
            await message.clear_reactions()
            timeEmbed = discord.Embed(title = 'Time out',description='Timed out',color=discord.Color.red())
            await message.edit(embed = timeEmbed)
    else:
        # print(reaction.id)
        reaction1 = str(reaction)
        if reaction1 == emojis[0] :
            selection = 0
            print(selection)
        elif reaction1 == emojis[1] :
            selection = 1
            print(selection)
        elif reaction1 == emojis[2] :
            selection = 2
            print(selection)
        elif reaction1 == emojis[3] :
            selection = 3
            print(selection)
        elif reaction1 == emojis[4] :
            selection = 4
            print(selection)
        else:
            selection = 0
            show1 = discord.Embed(title="Cancelled",description="This has been cancelled",color=discord.Color.red())
            await message.clear_reactions()
            await message.edit(embed=show1)
            return
        if results[selection][2] == 'Rx':
            await message.clear_reactions()
            noEmbed = discord.Embed(title = 'PG Restriction',description="You can't do that",color = discord.Color.red())
            await message.edit(embed =noEmbed)
            return
            # await ctx.send('You Can\'t Do That')
        else:
            await message.clear_reactions()
            # await ctx.send('Done')
            result = await user_db.UpdateData(author_id,[results[selection][0],results[selection][1],results[selection][3]])
            if result == -1:
                await message.edit(content = 'You cannot add more than 10',embed = None)
                return
            elif result == -2:
                await message.edit(content = "You already have that in your list",embed = None)
                return
            else:
                yesEmbed = discord.Embed(title = 'Done',description='Added '+results[selection][0]+' to your list',color=discord.Color.green())
                await message.edit(embed = yesEmbed)
                return
        # emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣']
@client.command()
async def recommend(ctx,user_to: discord.Member,*,arg1):
        #msg = await client.wait_for("message",check=check(ctx.author))
    results = await searchAnime(arg1)
    hyperlinks = []
    des = ""
    for i in range(0,len(results)):
        if results[i][2] == "Rx" or results[i][3] in blacklisted_ids: #or search_tag[i] == "R+":
            results[i][0] = "Redacted PG"
            results[i][1] = "Redacted"
            results[i][2] = 'Rx'
        k = i + 1
        hyperlinks.append('[{a}]({link})'.format(a=results[i][0], link=results[i][1] ))
        des += str(k) + "." + hyperlinks[i] + '\n'
    show_embed = discord.Embed(title = "Add To Favourites",description=des,color = discord.Color.purple())
    message = await ctx.send(embed=show_embed)
    for i in emojis:
        await message.add_reaction(i)
    def checkEmo(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emojis
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=checkEmo)
    except asyncio.TimeoutError:
            await message.clear_reactions()
            timeEmbed = discord.Embed(title = 'Time out',description='Timed out',color=discord.Color.red())
            await message.edit(embed = timeEmbed)
    else:
        # print(reaction.id)
        reaction1 = str(reaction)
        if reaction1 == emojis[0] :
            selection = 0
            print(selection)
        elif reaction1 == emojis[1] :
            selection = 1
            print(selection)
        elif reaction1 == emojis[2] :
            selection = 2
            print(selection)
        elif reaction1 == emojis[3] :
            selection = 3
            print(selection)
        elif reaction1 == emojis[4] :
            selection = 4
            print(selection)
        else:
            selection = 0
            show1 = discord.Embed(title="Cancelled",description="This has been cancelled",color=discord.Color.red())
            await message.clear_reactions()
            await message.edit(embed=show1)
            return
        if results[selection][2] == 'Rx':
            await message.clear_reactions()
            noEmbed = discord.Embed(title = 'PG Restriction',description="You can't do that",color = discord.Color.red())
            await message.edit(embed =noEmbed)
            return
            # await ctx.send('You Can\'t Do That')
        else:
            await message.clear_reactions()
            # await ctx.send('Done')
            # result = await user_rec.UpdateData(str(user_to.id),arg1)
            result = await user_rec.UpdateData(str(user_to.id),[results[selection][0],results[selection][1],results[selection][3],str(ctx.author)])
            if result == -1:
                await message.edit(content = 'You cannot add more than 10 to the list',embed = None)
                return
            elif result == -2:
                await message.edit(content = "User already has that in his list",embed = None)
                return
            else:
                yesEmbed = discord.Embed(title = 'Done',description='Added '+results[selection][0]+' to the user\'s list',color=discord.Color.green())
                await message.edit(embed = yesEmbed)
                return
        # recommended = dict(read_json(storage_recommended))
        # if str(user.id) not in recommended:
            # recommended[str(user.id)] = [arg1]
        # else:
            # recommended[str(user.id)].append(arg1)
        # print(type(recommended[str(user.id)]))
        # write_json(recommended,storage_recommended)

@client.command()
async def show_r(ctx,user:discord.Member=None):
    if user is None:
        user_id = ctx.author.id
        user_name = ctx.message.author.display_name
    else:
        user_id = user.id
        user_name = user.name
    # try:
        # tempo1 = dict(read_json(storage_recommendation))
        # tempo = tempo1[str(user_id)]
    # except KeyError:
        # await ctx.send(user_name + " doesn't have anything in his/her list")
        # return
    tempo = await user_rec.GetData(user_id)
    if tempo == None:
        await ctx.send(user_name+" doesn't have anything in list")
        return
    numbers = [str(x) for x in range(1,len(tempo)+1)]
    # names = []
    # urls = []
    hyperlinks = []
    description = ""
    for i in range(0,len(tempo)):
        # names.append(numbers[i] + "." + tempo[i][0])
        # urls.append(numbers[i] + "." + tempo[i][1])
        hyperlinks.append('[{a}]({link})'.format(a=tempo[i][0] + " (by " + tempo[i][3] + ")", link = tempo[i][1]))
        description+= numbers[i] + ". " + hyperlinks[i] + "\n"
    show = discord.Embed(title = chika_dance +  " Recommendation list of " + user_name + " " + chika_dance,description = description,color = discord.Color.teal())
    await ctx.send(embed=show)

@client.command()
async def remove_r(ctx,arg1):
    # try:
        # recommended = dict(read_json(storage_recommended))
        # tempo = recommended[str(ctx.author.id)].pop(int(arg1)-1)
        # write_json(tempo,storage_recommended)
    # except:
        # await ctx.send("You don't have such item in your list")
        # return
    author_id = str(ctx.author.id)
    status = ""
    arg1 = int(arg1)
    # try:
        # recommendation = dict(read_json(storage_recommendation))
        # temp_arr = [x.lower() for x in recommendation[author_id]]
        # index = temp_arr.index(arg1.lower())
        # recommendation[author_id].pop(index)
        # status = "Done, removed " + arg1 + " from your list"
        # write_json(recommendation,storage_recommendation)
    # except:
        # status = "You don't have such a item in your list"
    arg1 -= 1
    result = await user_rec.RemoveData(author_id,arg1)
    if result == -1 or result == -2:
        status = 'Out Of Bound'
       # await ctx.send(status)
    else:
        status = "Done removed it from your list"
    await ctx.send(status)
    # await ctx.send("The item was sucessfully removed")

@client.command()
async def remove(ctx,*,arg1):
    author_id = str(ctx.author.id)
    status = ""
    arg1 = int(arg1)
    # try:
        # recommendation = dict(read_json(storage_recommendation))
        # temp_arr = [x.lower() for x in recommendation[author_id]]
        # index = temp_arr.index(arg1.lower())
        # recommendation[author_id].pop(index)
        # status = "Done, removed " + arg1 + " from your list"
        # write_json(recommendation,storage_recommendation)
    # except:
        # status = "You don't have such a item in your list"
    arg1 -= 1
    result = await user_db.RemoveData(author_id,arg1)
    if result == -1 or result == -2:
        status = 'Out Of Bound'
       # await ctx.send(status)
    else:
        status = "Done removed it from your list"
    await ctx.send(status)

@client.command()
async def show(ctx,user : discord.Member=None):
    if user is None:
        user_id = ctx.author.id
        user_name = ctx.message.author.display_name
    else:
        user_id = user.id
        user_name = user.name
    # try:
        # tempo1 = dict(read_json(storage_recommendation))
        # tempo = tempo1[str(user_id)]
    # except KeyError:
        # await ctx.send(user_name + " doesn't have anything in his/her list")
        # return
    tempo = await user_db.GetData(user_id)
    if tempo == None:
        await ctx.send(user_name+" doesn't have anything in list")
        return
    numbers = [str(x) for x in range(1,len(tempo)+1)]
    # names = []
    # urls = []
    hyperlinks = []
    description = ""
    for i in range(0,len(tempo)):
        # names.append(numbers[i] + "." + tempo[i][0])
        # urls.append(numbers[i] + "." + tempo[i][1])
        hyperlinks.append('[{a}]({link})'.format(a=tempo[i][0], link = tempo[i][1]))
        description+= numbers[i] + ". " + hyperlinks[i] + "\n"
    show = discord.Embed(title = chika_dance +  " Favourites of " + user_name + " " + chika_dance,description = description,color = discord.Color.teal())
    await ctx.send(embed=show)

@client.command()
async def search(ctx,*,arg1):
    search_result = jikan.search('anime',arg1,page=1)
    search_url = [search_result['results'][x]['url'] for x in range(5)]
    search_title = [search_result['results'][y]['title'] for y in range(5)]
    search_tag = [search_result['results'][z]['rated'] for z in range(5)]
    #search_image = [search_result['results'][l]['image_url'] for l in range(5)]
   #for x in range(5):
    #    search_url.append(search_result['results'][x]['url'])
    show = discord.Embed(title = "Search Results",color = 0xFF5733)
    #titles = '\n'.join(search_title)
    #links = '\n'.join(search_url)
    #show.description = "[{title}]({link})".format(title = titles,link=links)
    description=""
    hyperlinks = []
    for i in range(0,len(search_title)):
        if search_tag[i] == "Rx": #or search_tag[i] == "R+":
            search_title[i] = "Redacted PG"
            search_url[i] = "Redacted"
            search_result['results'][i]['synopsis'] = "Redacted"
            search_result['results'][i]['image_url'] = "https://assets.stickpng.com/images/58864e1fd27829db9cf6da57.png"
        k = i + 1
        hyperlinks.append('[{a}]({link})'.format(a=search_title[i], link = search_url[i]))
        description += str(k) + '.' + hyperlinks[i]+ '\n'

    show.description = description
    message = await ctx.send(embed=show)
    # msg = await client.wait_for("message",check=check(ctx.author))
    for i in emojis:
        await message.add_reaction(i)
    # if msg.content == 'cancel':
        # await ctx.send("Cancelled")
        # return
    def checkEmo(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emojis
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=checkEmo)
    except asyncio.TimeoutError:
            await message.clear_reactions()
            timeEmbed = discord.Embed(title = 'Time out',description='Timed out',color=discord.Color.red())
            await message.edit(embed = timeEmbed)
    else:
        reaction1 = str(reaction)
        if reaction1 == emojis[0] :
            selection = 0
            print(selection)
        elif reaction1 == emojis[1] :
            selection = 1
            print(selection)
        elif reaction1 == emojis[2] :
            selection = 2
            print(selection)
        elif reaction1 == emojis[3] :
            selection = 3
            print(selection)
        elif reaction1 == emojis[4] :
            selection = 4
            print(selection)
        else:
            selection = 0
            show1 = discord.Embed(title="Cancelled",description="This has been cancelled",color=discord.Color.red())
            await message.clear_reactions()
            await message.edit(embed=show1)
            return
    # try:
        # selection = int(msg.content)
    # except ValueError:
        # await ctx.send("Please select a valid value ")
        # return
    # if selection > 5 or selection < 0:
        # await ctx.send("Out Of Bound")
    # else:
        show_des = search_result['results'][selection]['synopsis']
        show_img = search_result['results'][selection]['image_url']
        show1 = discord.Embed(description = show_des,color = discord.Color.magenta())
        show1.title=search_title[selection]
        #show1.set_footer(text = search_url[selection])
        show1.add_field(name = "MAL",value = hyperlinks[selection])
        show1.set_thumbnail(url=show_img)
        await message.clear_reactions()
        await message.edit(embed = show1)
@client.command()
async def feed(ctx):
    results,results2,result3 = get_rss()
    #results = get_rss()
    result = []
    for i in range(len(results)):
        hyperlink = "[{a}]({link})".format(a= results[i],link = result3[i])
        result.append(hyperlink + "\n -" + results2[i])
    final = '\n\n'.join(result)
    final = final.replace("<cite>","")
    final = final.replace("</cite>","")
    show = discord.Embed(title = "News Feed ", description = final,color = 0xFF00FF)
    await ctx.send(embed=show)

#@client.command()
#async def kaenisass(ctx):
#    for i in range(100):
#        await ctx.send("KAEN IS ASS, HIS MOM IS FAT")

@client.command()
async def manga(ctx,*,arg1):
    search_result = jikan.search('manga',arg1,page=1)
    search_url = [search_result['results'][x]['url'] for x in range(5)]
    search_title = [search_result['results'][y]['title'] for y in range(5)]
    #search_tag = [search_result['results'][z]['rated'] for z in range(5)]
    #search_image = [search_result['results'][l]['image_url'] for l in range(5)]
   #for x in range(5):
    #    search_url.append(search_result['results'][x]['url'])
    show = discord.Embed(title = "Search Results",color = 0xFF5733)
    #titles = '\n'.join(search_title)
    #links = '\n'.join(search_url)
    #show.description = "[{title}]({link})".format(title = titles,link=links)
    description=""
    hyperlinks = []
    for i in range(0,len(search_title)):
     #   if search_tag[i] == "Rx": #or search_tag[i] == "R+":
      #      continue;
        k = i + 1
        hyperlinks.append('[{a}]({link})'.format(a=search_title[i], link = search_url[i]))
        description += str(k) + '.' + hyperlinks[i]+ '\n'
    show.description = description
    message = await ctx.send(embed=show)
    for i in emojis:
        await message.add_reaction(i)
    # if msg.content == 'cancel':
        # await ctx.send("Cancelled")
        # return
    def checkEmo(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emojis
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=checkEmo)
    except asyncio.TimeoutError:
            await message.clear_reactions()
            timeEmbed = discord.Embed(title = 'Time out',description='Timed out',color=discord.Color.red())
            await message.edit(embed = timeEmbed)
    else:
        reaction1 = str(reaction)
        if reaction1 == emojis[0] :
            selection = 0
            print(selection)
        elif reaction1 == emojis[1] :
            selection = 1
            print(selection)
        elif reaction1 == emojis[2] :
            selection = 2
            print(selection)
        elif reaction1 == emojis[3] :
            selection = 3
            print(selection)
        elif reaction1 == emojis[4] :
            selection = 4
            print(selection)
        else:
            selection = 0
            show1 = discord.Embed(title="Cancelled",description="This has been cancelled",color=discord.Color.red())
            await message.clear_reactions()
            await message.edit(embed=show1)
            return
        show_des = search_result['results'][selection]['synopsis']
        show_img = search_result['results'][selection]['image_url']
        show1 = discord.Embed(description = show_des,color = discord.Color.green())
        show1.title=search_title[selection]
        #show1.set_footer(text = search_url[selection-1])
        show1.add_field(name = "MAL",value = hyperlinks[selection])
        show1.set_thumbnail(url=show_img)
        await message.clear_reactions()
        await message.edit(embed = show1)

@client.command()
async def eps(ctx):
    results = get_rss_live()
    show = discord.Embed(title = "Expected Episodes", description = '\n'.join(results), color = 0xFF00FF)
    await ctx.send(embed=show)

####USER PHASE###########
@client.command()
async def cw(ctx,user: discord.Member=None):
    if user is None:
        user_id_discord = ctx.author
    else:
        user_id_discord = user
    user_name_temp = await userMAL.GetData(str(user_id_discord.id))
    if user_name_temp is None:
        await ctx.send("The user hasn't setup an account yet")
        return
    try:
        cw_anime,status = await currently(user_name_temp)
        if len(cw_anime) == 0:
            await ctx.send(user_id_discord.display_name+" ain't watching anything right now")
            return
    except:
        await ctx.send("No such user")
        return
    Embed = discord.Embed(title = user_name_temp,description ='\n'.join(cw_anime),color = discord.Color.blue())
    await ctx.send(embed=Embed)

####COMPLETED ANIME PHASE####

@client.command()
async def completed(ctx,user: discord.Member=None):
    if user is None:
        user_id_discord = ctx.author
    else:
        user_id_discord = user
    user_name_temp = await userMAL.GetData(str(user_id_discord.id))
    if user_name_temp is None:
        await ctx.send("The user hasn't setup an account yet")
        return
    try:
        completed_ani = await completed_anime(user_name_temp)
        if len(completed_ani) == 0:
            await ctx.send(user_id_discord.display_name + " hasn't completed a show yet")
            return
    except:
        await ctx.send("No such user")
        return
    if len(completed_ani) < 50:
        Embed = discord.Embed(title = user_name_temp, description = '\n'.join(completed_ani),color = discord.Colour.gold())
        await ctx.send(embed=Embed)
    else:
        Embed1 = discord.Embed(title=user_id_discord.display_name,description = '\n'.join(completed_ani[0:50]),color = discord.Color.gold())
        Embed2 = discord.Embed(title=user_id_discord.display_name,description = '\n'.join(completed_ani[50:]),color = discord.Color.gold())
        await ctx.send(embed=Embed1)
        await ctx.send(embed=Embed2)
# @client.command()
# async def set_channel(ctx,channel_set : discord.TextChannel):
    # server_id = ctx.message.guild.id
    # try:
        # server_preferences[str(server_id)] = str(channel_set.id)
        # write_json(server_preferences,server_preferences_location)
    # except:
        # await ctx.send("No such channel exists")

@client.command()
async def ptw(ctx,user: discord.Member=None):
    if user is None:
        user_id_discord = ctx.author
    else:
        user_id_discord = user
    user_name_temp = await userMAL.GetData(str(user_id_discord.id))
    if user_name_temp is None:
        await ctx.send("The user hasn't setup an account yet")
        return
    try:
        plan_to_watch_mal = await plantowatch(user_name_temp)
        if len(plan_to_watch_mal) == 0:
            await ctx.send(user_id_discord.display_name + " hasn't completed a show yet")
            return
    except:
        await ctx.send("No such user")
        return
    if len(plan_to_watch_mal) < 50:
        Embed = discord.Embed(title = user_name_temp, description = '\n'.join(plan_to_watch_mal),color = discord.Colour.gold())
        await ctx.send(embed=Embed)
    else:
        Embed1 = discord.Embed(title=user_id_discord.display_name,description = '\n'.join(plan_to_watch_mal[0:50]),color = discord.Color.gold())
        Embed2 = discord.Embed(title=user_id_discord.display_name,description = '\n'.join(plan_to_watch_mal[50:]),color = discord.Color.gold())
        await ctx.send(embed=Embed1)
        await ctx.send(embed=Embed2)

@client.command()
async def set_profile(ctx,user_name):
    user_id = str(ctx.author.id)
    check_mal = await userMAL.CheckUser(user_id)
    if check_mal == -1:
        await ctx.send("You already have set an account")
        return
    authentication =  await MalAuthUser(user_name)
    if authentication == -1:
        await ctx.send("Not a valid username")
        return
    random_number = random.randint(0,1000)
    show1 = discord.Embed(title="Update your MAL Location for Authentication",description="Please go to [this link](https://myanimelist.net/editprofile.php) and change your location to the number " + str(random_number) + " within 120 seconds",color = discord.Colour.dark_red())
    message_sent = await ctx.send(embed=show1)
    await asyncio.sleep(120)
    authentication = await MalAuthUser(user_name)
    if str(random_number) not in authentication:
        await message_sent.edit(content="You didn't update your location, your account has not been set ",embed=None)
        return
    else:
        await userMAL.SetProfile(user_id,user_name)
        await message_sent.edit(content="Successfully Updated",embed=None)
        return
client.run(TOKEN)
