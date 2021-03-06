import discord
import aiohttp
import random
import asyncio
import io
import re
from aiotrivia import TriviaClient, AiotriviaException
from discord.ext import commands
from secrets import *
from random import randint, choice, sample

ZALGO_DEFAULT_AMT = 3
ZALGO_MAX_AMT = 7

ZALGO_PARAMS = {
    'above': (5, 10),
    'below': (5, 10),
    'overlay': (0, 2)
}

ZALGO_CHARS = {
    'above': ['\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305', '\u0306', '\u0307', '\u0308', '\u0309',
              '\u030A', '\u030B', '\u030C', '\u030D', '\u030E', '\u030F', '\u0310', '\u0311', '\u0312', '\u0313',
              '\u0314', '\u0315', '\u031A', '\u031B', '\u033D', '\u033E', '\u033F', '\u0340', '\u0341', '\u0342',
              '\u0343', '\u0344', '\u0346', '\u034A', '\u034B', '\u034C', '\u0350', '\u0351', '\u0352', '\u0357',
              '\u0358', '\u035B', '\u035D', '\u035E', '\u0360', '\u0361'],
    'below': ['\u0316', '\u0317', '\u0318', '\u0319', '\u031C', '\u031D', '\u031E', '\u031F', '\u0320', '\u0321',
              '\u0322', '\u0323', '\u0324', '\u0325', '\u0326', '\u0327', '\u0328', '\u0329', '\u032A', '\u032B',
              '\u032C', '\u032D', '\u032E', '\u032F', '\u0330', '\u0331', '\u0332', '\u0333', '\u0339', '\u033A',
              '\u033B', '\u033C', '\u0345', '\u0347', '\u0348', '\u0349', '\u034D', '\u034E', '\u0353', '\u0354',
              '\u0355', '\u0356', '\u0359', '\u035A', '\u035C', '\u035F', '\u0362'],
    'overlay': ['\u0334', '\u0335', '\u0336', '\u0337', '\u0338']
}

dank_links = [
    "https://cdn.discordapp.com/attachments/669003285625045027/771049182080532490/cumflushed-20201028-0001.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/786099129855246376/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/786098839421321226/video2.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/786098838934257724/video1.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/786098838539730944/video0.mp4",
    "https://cdn.discordapp.com/attachments/296056831514509312/785956008022769664/c.mp4",
    "https://cdn.discordapp.com/attachments/296056831514509312/785895491384246302/video0-111.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/785778976647544872/video0_79_1.mp4",
    "https://cdn.discordapp.com/attachments/666504348636938240/785541556404092968/9acf2f17233e2f3d79e26dc4202ed70a.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/785135513908543488/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/785093364697137233/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/785008173495877643/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/785007753008513024/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/784660759895998494/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/784623705270517770/video0_24.mov",
    "https://cdn.discordapp.com/attachments/738969720983912498/779579680172146739/videoplayback_14.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/784221811629490226/video0.mov",
    "https://cdn.discordapp.com/attachments/717069546464477184/784150651759362048/video0.mov",
    "https://cdn.discordapp.com/attachments/717069546464477184/784150592129073252/video0.mp4",
    "https://cdn.discordapp.com/attachments/738969720983912498/783754806765944842/video0-1-1.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/783570434150498354/unintelligable_japanese_th"
    "en_bonk.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/783566850118254622/RUFFLES.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/783546455994269756/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/783546215454343178/video0.mp4",
    "https://cdn.discordapp.com/attachments/479240786119098388/781970687543345183/video0.mov",
    "https://cdn.discordapp.com/attachments/717069546464477184/782739440102932510/redditsave.com-shes_right-mza35vao"
    "96261-480.mp4",
    "https://cdn.discordapp.com/attachments/479240786119098388/781970687543345183/video0.mov",
    "https://cdn.discordapp.com/attachments/604701560580341771/782022180459511858/Another_Death_In_Collective.mp4",
    "https://cdn.discordapp.com/attachments/722706822737428510/749803513013338112/Water_melon.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/782303565523714118/insertgoodtitle.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/782303564580126734/video0-1.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/782303564142870558/redditsave.com-damn-lke9wha1zft"
    "51.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/781867816437547008/VID-20201127-WA0009.mp4",
    "https://cdn.discordapp.com/attachments/735690974340317216/740981642293674104/video1.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/780656041045786634/video0_10_1.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/780630899955859506/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/780624857884655626/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/779545142536830986/video0-227.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/779545142250962964/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/779542048512147476/video0.mov",
    "https://cdn.discordapp.com/attachments/717069546464477184/779192844283412499/video0.mp4",
    "https://cdn.discordapp.com/attachments/551121914987282443/778925222895681536/-498811818.mp4",
    "https://cdn.discordapp.com/attachments/644582600366882817/778449470437326868/video0.mov",
    "https://cdn.discordapp.com/attachments/717069546464477184/778227206518210560/video0-2.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/778227158785982484/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/778227157507768340/Cut_away.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/777891720758165554/video0.mp4",
    "https://cdn.discordapp.com/attachments/669003285625045027/776038894285750342/hall-of-the-iced-tea.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/777341419538743346/video0_36.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/777326893619740682/Joker_Donald_Trump_The_world_"
    "is_an_angry_place._HD_from_The_Daily_Show.mp4",
    "https://cdn.discordapp.com/attachments/439519668819066880/776986323620986910/y2mate.com_-_Numa_Numa_480p.mp4",
    "https://cdn.discordapp.com/attachments/526517763863216148/776941268440842260/video0_2-3.mp4",
    "https://cdn.discordapp.com/attachments/439519668819066880/776978720229425172/ca42b2d7e6ac98db8bf1b7123395a1ad.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776525245002547210/26f7aa5e641743079fd06040fd137287.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776478936896634880/YJBEgJ6T9hkfnzeS.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776478936540250112/hwLRr-Hja-t6sUXS.mp4",
    "https://cdn.discordapp.com/attachments/644582600366882817/776217505869070336/video0-259.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776179149811220480/zk32h4rf1gqOmQPn.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776179149411975198/76EYcJI5U0wBCuML.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776179149043400734/1q45zzh4k1_s3PbD.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776179148074123274/redditsave.com-amongst_ourselves-"
    "kxxhyk2t6vt51.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776179147529257010/y2mate.com_-_Dont_be_a_dinophob"
    "e_luigi_480p.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776179147214553138/redditsave.com-im_gonna_do_this-ieato"
    "p2ldzw51.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776179144177352754/Bpa38DWrOeBT0pb.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776146694155796490/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776118577144266783/video0-2.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776118558244732928/video0-3.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776118537164423188/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776118484102545428/redditsave.com-you_can_build_anyt"
    "hing-lvcwblipx3r51.mp4",
    "https://cdn.discordapp.com/attachments/754488572786114610/775638737223942144/baboio.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776115685364596756/gum.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776114702639431691/1604834350862.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776113915942928404/video0_10.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/776113697608695809/video0-27.mp4",
    "https://cdn.discordapp.com/attachments/754203239557234739/775247069031956520/like_ya_cut_g-1.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/775413650751619113/imma_head_out.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/775413650214354944/discord.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/775413649627545640/video0-32-1.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/775413648708599858/s.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/775413295221178418/fridge.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/775413290884792330/video0-3.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/775413290360373258/yes.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/775413289735159808/video0-5.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/775357653782102046/VID-20191106-WA0002.mp4",
    "https://cdn.discordapp.com/attachments/344324740292411394/771595635446906920/Prank.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/770855163552071700/beanosofficial-20201027-0001.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/770439177011593216/video0.mp4",
    "https://cdn.discordapp.com/attachments/703648926863065102/786171587065282570/video0.mp4",
    "https://cdn.discordapp.com/attachments/546763235051700314/786418329903824916/Le_Fishe_1.mp4",
    "https://cdn.discordapp.com/attachments/764954302481170432/785534987214258246/waffle.webm",
    "https://cdn.discordapp.com/attachments/700660206329135196/783792312785567754/video0.mp4",
    "https://cdn.discordapp.com/attachments/669003285625045027/783946564082073610/video0-4.mp4",
    "https://cdn.discordapp.com/attachments/669003285625045027/780525591081779230/memerzone-20201108-0001.mp4",
    "https://cdn.discordapp.com/attachments/669003285625045027/779503628049448990/twitter_20201120_132847.mp4",
    "https://cdn.discordapp.com/attachments/669003285625045027/779180044005670983/twitter_20201119_114156.mp4",
    "https://cdn.discordapp.com/attachments/669003285625045027/775506582141927444/twitter_20201108_110152.mp4",
    "https://cdn.discordapp.com/attachments/748563164362440856/775340600395431946/mario_and_luigi_jam.mp4",
    "https://cdn.discordapp.com/attachments/669003285625045027/775358206079533056/video0_2.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/788307395259400202/lorax.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/788244139728568340/video0.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/787960372598145024/video07.mov",
    "https://cdn.discordapp.com/attachments/717069546464477184/788429059490971688/Santa.mp4",
    "https://cdn.discordapp.com/attachments/524938738258935828/605814230691610645/68422251_120564069234715_"
    "3090335658794515478_n.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/789218689584857188/uranus.mp4",
    "https://cdn.discordapp.com/attachments/717069546464477184/789184521521463296/st.mp4"]



class Fun(commands.Cog):
    """Use NOVA to have a little fun on your server"""

    def __init__(self, client):
        self.client = client
        self.trivia = TriviaClient()

    @commands.command(aliases=['pupper', 'doggo'])
    async def dog(self, ctx):
        # all credit to R.Danny for this command
        """Get a nice dog to brighten your day"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No dog found')

                filename = await resp.text()
                url = f'https://random.dog/{filename}'
                filesize = ctx.guild.filesize_limit if ctx.guild else 8388608
                if filename.endswith(('.mp4', '.webm')):
                    async with ctx.typing():
                        async with cs.get(url) as other:
                            if other.status != 200:
                                return await ctx.send('Could not download dog video :/')

                            if int(other.headers['Content-Length']) >= filesize:
                                return await ctx.send(f'Video was too big to upload... See it here: {url} instead.')

                            fp = io.BytesIO(await other.read())
                            await ctx.send(file=discord.File(fp, filename=filename))
                else:
                    await ctx.send(embed=discord.Embed(color=0x5643fd,
                                                       description=f"<:github:734999696845832252> "
                                                                   f"[Source Code]"
                                                                   f"(https://github.com/Rapptz/RoboDanny/blob/rewrite/"
                                                                   f"cogs/funhouse.py#L44-L66)").set_image(url=url)
                                   .set_footer(text='https://random.dog/woof'))

    @commands.command(aliases=['catto', 'kitty'])
    async def cat(self, ctx):
        """Waste time with some cat images"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.thecatapi.com/v1/images/search") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No cat found')
                js = await resp.json()
                await ctx.send(embed=discord.Embed(color=0x5643fd,
                                                   description=f"<:github:734999696845832252> "
                                                               f"[Source Code]"
                                                               f"(https://github.com/DevilJamJar"
                                                               f"/DevilBot/blob/master/cogs/fun."
                                                               f"py)").set_image(
                    url=js[0]['url']).set_footer(text='https://api.thecatapi.com/v1/images/search'))

    @commands.command()
    async def panda(self, ctx):
        """Cute panda images."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/panda") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No panda found.')
                js = await resp.json()
                embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
                embed.set_image(url=js['link'])
                await ctx.send(embed=embed)

    @commands.command(aliases=['birb'])
    async def bird(self, ctx):
        """Cute birb images."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/birb") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No birb found.')
                js = await resp.json()
                embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
                embed.set_image(url=js['link'])
                await ctx.send(embed=embed)

    @commands.command()
    async def fox(self, ctx):
        """Cute fox images."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/fox") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No fox found.')
                js = await resp.json()
                embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
                embed.set_image(url=js['link'])
                await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, aliases=['astronomy'])
    async def apod(self, ctx):
        # APOD command group
        """Astronomy Picture of the Day"""
        p = ctx.prefix
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(f"https://api.nasa.gov/planetary/apod?api_key={nasa_key}") \
                    as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No image could be found')
                else:
                    js = await resp.json()
                    embed = discord.Embed(color=0x5643fd, title=js['title'],
                                          timestamp=ctx.message.created_at)
                    embed.set_image(url=js['url'])
                    embed.add_field(name='Date', value=js['date'], inline=True)
                    embed.add_field(name='Sub Commands',
                                    value=f"``{p}apod hd``\n``{p}apod description``\n``{p}apod date``",
                                    inline=True)
                    await ctx.send(embed=embed)

    @apod.command()
    async def date(self, ctx, date):
        """Show the astronomy picture of the day for a given date (YYYY-MM-DD)"""
        link = f"https://api.nasa.gov/planetary/apod?date={date}&api_key={nasa_key}"
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(link) as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No image could be found')
                else:
                    js = await resp.json()
                    embed = discord.Embed(color=0x5643fd, title=js['title'],
                                          timestamp=ctx.message.created_at)
                    embed.set_image(url=js['url'])
                    embed.add_field(name='Date', value=js['date'], inline=True)
                    embed.add_field(name='HD Version', value=f"<:asset:734531316741046283> [Link]({js['hdurl']})",
                                    inline=True)
                    await ctx.send(embed=embed)

    @apod.command()
    async def hd(self, ctx):
        """HD version for the astronomy picture of the day"""
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(f"https://api.nasa.gov/planetary/apod?api_key={nasa_key}") \
                    as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No image could be found')
                else:
                    js = await resp.json()
                    embed = discord.Embed(color=0x5643fd, title=f"{js['title']} (HD)",
                                          timestamp=ctx.message.created_at)
                    embed.set_image(url=js['hdurl'])
                    await ctx.send(embed=embed)

    @apod.command()
    async def description(self, ctx):
        """Explanation for the astronomy picture of the day"""
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(f"https://api.nasa.gov/planetary/apod?api_key={nasa_key}") \
                    as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No description could be found')
                else:
                    js = await resp.json()
                    embed = discord.Embed(color=0x5643fd, title=js['title'], description=js['explanation'],
                                          timestamp=ctx.message.created_at)
                    await ctx.send(embed=embed)

    @commands.command()
    async def inspiro(self, ctx):
        """Look at beautiful auto-generated quotes"""
        url = 'https://inspirobot.me/api?generate=true'
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(url) as r:
                data = await r.text()
        embed = discord.Embed(color=0x5643fd,
                              description="<:github:734999696845832252> [Source Code](https://github.com/DevilJamJar/"
                                          "DevilBot/blob/master/cogs/fun.py)", timestamp=ctx.message.created_at)
        embed.set_image(url=data)
        embed.set_footer(text='Copyright 2020 Deviljamjar')
        await ctx.send(embed=embed)

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        """Allow the mystical NOVA to answer all of life's important questions"""
        responses = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it',
                     'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
                     'Reply hazy, try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now',
                     'Concentrate and ask again', 'Do not count on it', 'My reply is no', 'My sources say no',
                     'The outlook is not so good', 'Very doubtful']
        embed = discord.Embed(title='Magic 8ball says', color=0x5643fd, timestamp=ctx.message.created_at)
        embed.add_field(name='Question:', value=question, inline=False)
        embed.add_field(name='Answer:', value=random.choice(responses), inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/726475732569555014/747266621512614009/8-Ball-'
                                'Pool-Transparent-PNG.png')
        await ctx.send(embed=embed)

    @commands.command()
    async def motivation(self, ctx):
        """Need motivation? NOVA has you covered."""
        responses = ['https://youtu.be/kGOQfLFzJj8', 'https://youtu.be/kYfM5uKBKKg', 'https://youtu.be/VV_zfO3HmTQ',
                     'https://youtu.be/fLeJJPxua3E', 'https://youtu.be/5aPntFAyRts', 'https://youtu.be/M2NDQOgGycg',
                     'https://youtu.be/FDDLCeVwhx0', 'https://youtu.be/P10hDp6mUG0', 'https://youtu.be/K8S8OvPhMDg',
                     'https://youtu.be/zzfREEPbUsA', 'https://youtu.be/mgmVOuLgFB0', 'https://youtu.be/t8ApMdi24LI',
                     'https://youtu.be/JXQN7W9y_Tw', 'https://youtu.be/fKtmM_45Dno', 'https://youtu.be/k9zTr2MAFRg',
                     'https://youtu.be/bm-cCn0uRXQ', 'https://youtu.be/9bXWNeqKpjk', 'https://youtu.be/ChF3_Zbuems',
                     'https://youtu.be/BmIM8Hx6yh8', 'https://youtu.be/oNYKDM4_ZC4', 'https://youtu.be/vdMOmeljTvA',
                     'https://youtu.be/YPTuw5R7NKk', 'https://youtu.be/jnT29dd7LWM', 'https://youtu.be/7XzxDIJKXlk']
        await ctx.send(random.choice(responses))

    @commands.command()
    async def hex(self, ctx, code):
        """Explore hex colors"""
        color = discord.Colour(int(code, 16))
        thumbnail = f'https://some-random-api.ml/canvas/colorviewer?hex={code}'
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(f"https://www.thecolorapi.com/id?hex={code}") \
                    as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No hex code could be found.')
                else:
                    js = await resp.json()
                    name = js['name']
                    image = js['image']
                    rgb = js['rgb']
                    hsl = js['hsl']
                    hsv = js['hsv']
                    cmyk = js['cmyk']
                    xyz = js['XYZ']
                    try:
                        embed = discord.Embed(title=f"Showing hex code ``#{code}``", color=color,
                                              timestamp=ctx.message.created_at)
                        embed.set_thumbnail(url=thumbnail)
                        embed.add_field(name='Name', value=f"{name['value']}")
                        embed.add_field(name='Exact name?', value=f"``{name['exact_match_name']}``")
                        embed.add_field(name='Closest named hex', value=f"``{name['closest_named_hex']}``")
                        embed.add_field(name='🔗 Image Links',
                                        value=f"<:asset:734531316741046283> [Bare]({image['bare']})\n"
                                              f"<:asset:734531316741046283> [Labeled]({image['named']})",
                                        inline=False)
                        embed.add_field(name='Other Codes',
                                        value=f"**rgb**({rgb['r']}, {rgb['g']}, {rgb['b']})\n"
                                              f"**hsl**({hsl['h']}, {hsl['s']}, {hsl['l']})\n"
                                              f"**hsv**({hsv['h']}, {hsv['s']}, {hsv['v']})\n"
                                              f"**cmyk**({cmyk['c']}, {cmyk['m']}, {cmyk['y']}, {cmyk['k']})\n"
                                              f"**XYZ**({xyz['X']}, {xyz['Y']}, {xyz['Z']})", inline=False)
                        await ctx.send(embed=embed)
                    except ValueError:
                        await ctx.send("<:redx:732660210132451369> "
                                       "That is not a valid hex code, please try again with a different value.")
                    except BaseException:
                        await ctx.send("<:redx:732660210132451369> "
                                       "Could not process that hex code, please try again with a different value.")

    @commands.command()
    @commands.cooldown(1, 59, commands.BucketType.member)
    async def poke(self, ctx, member: discord.Member, *, message):
        """This command shows up in the dictionary under the definition of annoying."""
        member = member or ctx.message.author
        await ctx.send(f'<a:a_check:742966013930373151> Message successfully sent to ``{member}``')
        embed = discord.Embed(title=f'Message from {ctx.message.author}:', color=0x5643fd, description=message,
                              timestamp=ctx.message.created_at)
        await member.send(embed=embed)

    @commands.command()
    async def news(self, ctx, result: int = 0):
        """Show the top headlines in the U.S. for today. Enter a number (0-15) to show a certain result. """
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={news_key}'
        # I could get a lot more results than 15 articles but it updates everyday and the results are always different
        # I had to put a reasonable limit on the index so the index was always in range to avoid errors.
        sort = range(-1, 16)
        if result not in sort:
            return await ctx.send('<:redx:732660210132451369> This is not a valid search index. Please choose a number '
                                  'between 0 and 15.')
        if result in sort:
            async with aiohttp.ClientSession() as cs, ctx.typing():
                async with cs.get(url) as resp:
                    if resp.status == 500:
                        return await ctx.send("<:redx:732660210132451369> The API's server is currently down. "
                                              "Check back later. This is not a problem on my end.")
                    if resp.status == 429:
                        return await ctx.send('<:redx:732660210132451369> This command is on a timeout. '
                                              'Check back tomorrow when we have more API requests available.')
                    if resp.status == 400:
                        return await ctx.send('<:redx:732660210132451369> Something went wrong with the request. '
                                              'Try again with different parameters.')
                    if resp.status == 200:
                        js = await resp.json()
                        # result is the index
                        a = js['articles'][result]
                        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at, title=a['title'],
                                              url=a['url'])
                        embed.add_field(name='Content', inline=False, value=a['content'])
                        embed.add_field(name='Publish Date', inline=False, value=a['publishedAt'])
                        embed.add_field(name='Source', inline=False, value=a['source']['name'])
                        embed.set_author(name=a['author'])
                        embed.set_image(url=a['urlToImage'])
                        return await ctx.send(embed=embed)

    @commands.command()
    async def chat(self, ctx, *, words):
        """Chat with an AI."""
        url = f'https://some-random-api.ml/chatbot?message={words}'
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send("<:redx:732660210132451369> Looks like there was an error and you won't be "
                                          "able to chat today.")
                js = await resp.json()
                await ctx.send(js['response'])

    @commands.command()
    async def lyrics(self, ctx, *, song):
        """Find song lyrics."""
        url = f'https://some-random-api.ml/lyrics?title={song}'
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send("<:redx:732660210132451369> Could not find any lyrics for that song.")
                js = await resp.json()
                thumbnail = js['thumbnail']
                links = js['links']
                embed = discord.Embed(title=js['title'], color=0x5643fd, timestamp=ctx.message.created_at,
                                      description=f"*[Find the full lyrics on genius.com"
                                                  f"]({links['genius']})*\n\n{js['lyrics'][:1000]}")
                embed.set_thumbnail(url=thumbnail['genius'])
                embed.set_author(name=f"By: {js['author']}")

                await ctx.send(embed=embed)

    @commands.command(aliases=['thispersondoesnotexist'])
    async def person(self, ctx):
        """This person does not exist."""
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get('https://fakeface.rest/face/json') as resp:
                if resp.status != 200:
                    return await ctx.send("<:redx:732660210132451369> Could not find you a person.")
                js = await resp.json()
                gender = js['gender'].capitalize()
                embed = discord.Embed(title='This person does not exist', timestamp=ctx.message.created_at,
                                      color=0x5643fd)
                embed.set_image(url=js['image_url'])
                embed.add_field(name='Age:', value=js['age'], inline=True)
                embed.add_field(name='Gender:', value=gender, inline=True)
                embed.set_footer(text=f"Source: {js['source']}")
                await ctx.send(embed=embed)

    @commands.command()
    async def weather(self, ctx, *, city):
        """Gather weather data for a given city."""
        url = f'http://api.weatherapi.com/v1/current.json?key=c1319477d52b4806a66154914200211&q={city}'
        direction_list = {
            "N": "North",
            "S": "South",
            "E": "East",
            "W": "West",
            "NW": "Northwest",
            "NE": "Northeast",
            "SE": "Southeast",
            "SW": "Southwest",
            "NNW": "North-Northwest",
            "NNE": "North-Northeast",
            "WNW": "West-Northwest",
            "ENE": "East-Northeast",
            "WSW": "West-Southwest",
            "ESE": "East-Southeast",
            "SSW": "South-Southwest",
            "SSE": "South-Southeast"}
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send(f"<:redx:732660210132451369> Could not find any weather data for ``{city}``.")
                js = await resp.json()
                embed = discord.Embed(color=0x5643fd, title=js['location']['name'], timestamp=ctx.message.created_at,
                                      description=f"**Region:** {js['location']['region']}\n"
                                                  f"**Country:** {js['location']['country']}\n"
                                                  f"**Coordinates:** {js['location']['lat']}, {js['location']['lon']}\n"
                                                  f"**Timezone:** {js['location']['tz_id']}\n"
                                                  f"**Local Time:** {js['location']['localtime']}")
                embed.set_thumbnail(url=f"https:{js['current']['condition']['icon']}")
                embed.add_field(name='**__Weather Data:__** <:temperature:742933558221340723>☀', inline=False,
                                value=
                                f"**Overview:** {js['current']['condition']['text']}\n"
                                f"**Temperature:** {js['current']['temp_c']} Celsius | "
                                f"{js['current']['temp_f']} Fahrenheit\n"
                                f"**Feels like:** {js['current']['feelslike_c']} Celsius | "
                                f"{js['current']['feelslike_f']} Fahrenheit\n"
                                f"**Wind Speed:** {js['current']['wind_kph']} kph | {js['current']['wind_mph']} mph\n"
                                f"**Wind Direction:** {direction_list[js['current']['wind_dir']]}\n"
                                f"**Humidity:** {js['current']['humidity']}\n"
                                f"**Cloud Coverage:** {js['current']['cloud']}%")
                await ctx.send(embed=embed)

    @commands.command(aliases=["bigemote"])
    async def bigmote(self, ctx, *emoji: discord.Emoji):
        """Emotes, but B I G (only works from the bot's cache)"""
        a = []
        y = ""
        for item in emoji:
            a.append(self.client.get_emoji(item.id))
        emote = a[0]
        x = emote.id
        if emote.animated is True:
            y += 'gif'
        else:
            y += 'png'
        await ctx.send(f"https://cdn.discordapp.com/emojis/{x}.{y}")

    @commands.command(aliases=['dankvid', 'video'])
    async def dankvideo(self, ctx):
        """Randomly generate a funny video."""
        m = random.choice(dank_links)
        await ctx.send(m)

    # credit some random github page https://github.com/calebj/calebj-cogs/blob/master/zalgo/zalgo.py
    @commands.command()
    async def zalgo(self, ctx, *, text: str):
        """Make your text look like it came from the scary side of town."""
        fw = text.split()[0]
        try:
            amount = min(int(fw), ZALGO_MAX_AMT)
            text = text[len(fw):].strip()
        except ValueError:
            amount = ZALGO_DEFAULT_AMT
        text = self.zalgoify(text.upper(), amount)
        await ctx.send(text)

    def zalgoify(self, text, amount=3):
        zalgo_text = ''
        for c in text:
            zalgo_text += c
            if c != ' ':
                for t, range in ZALGO_PARAMS.items():
                    range = (round(x * amount / 5) for x in range)
                    n = min(randint(*range), len(ZALGO_CHARS[t]))
                    zalgo_text += ''.join(sample(ZALGO_CHARS[t], n))
        return zalgo_text


def setup(client):
    client.add_cog(Fun(client))
