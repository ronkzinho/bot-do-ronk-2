import discord
from discord.ext import commands
from .functions.searchMember import SearchMember

class Adm(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=["banir", "b"])
    @commands.has_guild_permissions(administrator=True, ban_members=True)
    @commands.bot_has_guild_permissions(administrator=True, ban_members=True)
    async def ban(self, ctx, member: SearchMember=None, *, reason=None):
        if not member: return await ctx.send("Coloque um membro válido!")
        if member.id == ctx.author.id: return await ctx.send("Se banir?")
        if member.top_role.position >= ctx.author.top_role.position: raise commands.MissingPermissions("No")
        if member.top_role.position >= ctx.guild.get_member(self.client.user.id).top_role.position: raise commands.BotMissingPermissions("No")

        msg = await ctx.send(f"Você tem certeza que deseja banir o(a) {member.display_name}?")
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=lambda reaction, user: user.id == ctx.author.id and reaction.emoji in ["✅", "❌"] and reaction.message.id == msg.id)
        if(reaction.emoji == "✅"):
            await member.send("Você foi banido por <@{}>, {}".format(user.id, "pelo motivo: " + reason if reason else "sem motivo aparente!"))
            await member.ban(reason=reason)
            await msg.delete()
            await ctx.send(f"<@{member.id}> banido com sucesso!")
        else:
            return msg.edit("ok")

    @commands.command(aliases=["kickar", "k"])
    @commands.has_guild_permissions(administrator=True, kick_members=True)
    @commands.bot_has_guild_permissions(administrator=True, kick_members=True)
    async def kick(self, ctx, member: SearchMember=None, *, reason=None):
        if not member: return await ctx.send("Coloque um membro válido!")
        if member.id == ctx.author.id: return await ctx.send("Se kickar?")
        if member.top_role.position >= ctx.author.top_role.position: raise commands.MissingPermissions("No")
        if member.top_role.position >= ctx.guild.get_member(self.client.user.id).top_role.position: raise commands.BotMissingPermissions("No")

        msg = await ctx.send(f"Você tem certeza que deseja kickar o(a) {member.display_name}?")
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=lambda reaction, user: user.id == ctx.author.id and reaction.emoji in ["✅", "❌"] and reaction.message.id == msg.id)
        if(reaction.emoji == "✅"):
            await member.send("Você foi kickado por <@{}>, {}".format(user.id, "pelo motivo: " + reason if reason else "sem motivo aparente!"))
            await member.kick(reason=reason)
            await msg.delete()
            await ctx.send(f"<@{member.id}> kickado com sucesso!")
        else:
            return msg.edit("ok")

    async def cog_command_error(self, ctx, error):
        await ctx.message.add_reaction("❌")
        if isinstance(error, commands.MissingPermissions):
            await self.client.wait_for('reaction_add', timeout=30.0, check=lambda reaction, user: user.id == ctx.author.id and reaction.emoji == '❌' and reaction.message.id == ctx.message.id)
            return await ctx.send(f"Você não tem permissão para {ctx.command.aliases[0]} esse membro!")
        if isinstance(error, commands.BotMissingPermissions):
            await self.client.wait_for('reaction_add', timeout=30.0, check=lambda reaction, user: user.id == ctx.author.id and reaction.emoji == '❌' and reaction.message.id == ctx.message.id)
            return await ctx.send(f"Bot não pode {ctx.command.aliases[0]} esse membro!")
        else:
            raise error

def setup(client):
    client.add_cog(Adm(client))