import discord
from discord.ext import commands

#-----------------------------------------------------------

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
            
    @commands.command(aliases=["info"])
    async def serverinfo(self, ctx):
        guild = ctx.guild

        embed = discord.Embed(
            title=guild.name,
            description=f"_{guild.description}_",
            color=discord.Color(0x90d5ff)
        )
        embed.set_footer(text=f"Server ID: {guild.id}")
        embed.set_thumbnail(url=guild.icon)
        embed.set_author(name="Server Info")

        embed.add_field(name="Server Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Creation Time", value=guild.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)

        embed.add_field(name="Categories", value=len(guild.categories), inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Emojis", value=len(guild.emojis), inline=True)

        embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Stickers", value=len(guild.stickers), inline=True)

        online = [m for m in guild.members if m.status != discord.Status.offline]

        embed.add_field(name="Humans", value=sum(1 for m in guild.members if not m.bot), inline=True)
        embed.add_field(name="Bots", value=sum(1 for m in guild.members if m.bot), inline=True)
        embed.add_field(name="Active", value=len(online), inline=True)

        await ctx.send(embed=embed)

    #-----------------------------------------------------------

    @commands.command(aliases=["me"])
    async def aboutme(self, ctx):

        embed = discord.Embed(
            title="Veronika",
            description="Hello, my name is Veronika and I am a bot whose task is to serve my Master however he needs! Only <@1359316905969586338> and <@726790716210020374> are my Masters, but I can also help you with what you need, as long as you don't overstep your boundaries.",
            color=discord.Color(0x90d5ff)
        )
        embed.set_footer(text="Use =help to view all of my commands!")
        embed.set_author(name="About Me")

        embed.add_field(name=":light_blue_heart: Information", value="Information about this server or its members.", inline=True)
        embed.add_field(name=":heart: Moderation", value="Moderation tools for those with mod perms.", inline=True)
        embed.add_field(name=":white_heart: Minigames", value="I can provide you with minigames! Some of them come with risks, hehe...", inline=True)
        embed.add_field(name=":black_heart: Miscellaneous", value="Random commands that don't really do much but are somewhat fun.", inline=True)
        embed.add_field(name=":orange_heart: Game Profile", value="Your character profile! You need a profile to play games.", inline=True)
        embed.add_field(name=":pink_heart: Sirius Program", value="Apparently, there exists a civilization somewhere in the Sirius star system... or so I heard from Master!", inline=True)
        embed.add_field(name=":purple_heart: Japanese", value="Master's Japanese study tools. Can only be used by Master.", inline=True)
        embed.add_field(name=":green_heart: Master Only", value="Master-only tools and settings.", inline=True)
        embed.add_field(name=":sparkles: Reactions", value="I have various reactions for when Master mentions me! However, only Master has the right to do so.", inline=True)
        
        await ctx.send(embed=embed)

    #-----------------------------------------------------------

    @commands.command(aliases=["user"])
    async def aboutuser(self, ctx, *, arg=None):
        try:
            if arg is None:
                target = ctx.author
                
            elif arg.isdigit():
                member = ctx.guild.get_member(int(arg))
                target = member if member else await ctx.bot.fetch_user(int(arg))

            else:
                # Try to resolve as a member mention or name
                target = await commands.MemberConverter().convert(ctx, arg)

        except Exception:
            await ctx.send("Sorry, user not found.")
            return

        embed = discord.Embed(
            title=target.name,
            description=f"Server name: `{target.display_name}`" if isinstance(target, discord.Member) else None,
            color=discord.Color(0x90d5ff)
        )
        embed.set_footer(text=f"User ID: {target.id}")
        embed.set_thumbnail(url=target.avatar.url)
        embed.set_author(name="User Info")

        #-----------------------------------------------------------

        # MEMBER ONLY: Status, Activity
        if isinstance(target, discord.Member):

            # Status
            embed.add_field(name="Status", value=target.status, inline=True)

            # Activity
            standard_activities = [
                discord.ActivityType.playing,
                discord.ActivityType.streaming,
                discord.ActivityType.listening,
                discord.ActivityType.watching,
            ]
            
            activities = [a for a in target.activities if a.type in standard_activities and not isinstance(a, discord.CustomActivity)]

            if activities:
                activity_lines = [f"{a.name or 'Unknown'}" for a in activities]
                activity_name = ",\n".join(activity_lines)
            else:
                activity_name = "None"

            embed.add_field(name=f"Activity", value=activity_name, inline=True)

        # User Type
        user = "Bot" if target.bot else "Human"
        embed.add_field(name="Type", value=user, inline=True)
        
        # MEMBER ONLY: Custom Status
        if isinstance(target, discord.Member):
            custom = next((a for a in target.activities if isinstance(a, discord.CustomActivity)), None)
            if custom and custom.name:
                embed.add_field(name="Custom Status", value=custom.name, inline=True)

        # Account Creation
        embed.add_field(name="Account Created", value=target.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)
            
        # MEMBER ONLY: Server Joined, Roles
        if isinstance(target, discord.Member):
            roles = [role.mention for role in target.roles if role.name != "@everyone"]
            role_list = ", ".join(roles) if roles else "None"

            # Server Joined
            embed.add_field(name="Server Joined", value=target.joined_at.strftime("%d/%m/%Y %H:%M"), inline=True)

            # Roles
            embed.add_field(name="Roles", value=role_list, inline=False)

        await ctx.send(embed=embed)
        

    #-----------------------------------------------------------

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, *, arg=None):
        if arg is None:
            target = ctx.author
        elif arg.isdigit():
            target = await ctx.bot.fetch_user(int(arg))
        else:
            target = await commands.MemberConverter().convert(ctx, arg)

        embed = discord.Embed(
            title=f"{target.name}'s Avatar",
            color=discord.Color(0x90d5ff)
        )
        embed.set_author(name="Avatar check")
        embed.set_image(url=target.display_avatar.url)
        
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
