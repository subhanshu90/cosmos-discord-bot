import discord
import typing

from .base import RoleShopBase

from discord.ext.commands import has_permissions


class RoleShopSettings(RoleShopBase):
    """A plugin to manage and setup Role Shop in server."""

    @RoleShopBase.role_shop.command(name="create")
    @has_permissions(manage_roles=True)
    async def create_role(self, ctx, points: int, *, role: typing.Union[discord.Role, str]):
        """Create a new or use specified role for the Role Shop."""
        if len(ctx.guild_profile.roleshop.roles) >= self.plugin.data.roleshop.max_roles:
            res = f"❌    Sorry but role shop can't have more than {self.plugin.data.roleshop.max_roles} roles."
            return await ctx.send_line(res)

        if isinstance(role, str):
            role = await ctx.guild.create_role(name=role, reason=f"Role created for role shop. [{ctx.author}]")
        await ctx.guild_profile.roleshop.create_role(role.id, points)
        await ctx.send_line(f"✅    Added {role.name} to role shop with {points} points.")

    @RoleShopBase.role_shop.command(name="remove", aliases=["delete"])
    @has_permissions(manage_roles=True)
    async def delete_role(self, ctx, *, role: discord.Role = None):
        """Remove specified role from the Role Shop.
        It displays an interactive reaction based menu to choose your desired role if it's not specified.

        """
        description = "```css\nDisplaying Role Shop roles. React with respective emote to remove that role.```"
        role = await self._get_role(ctx, role, ctx.guild_profile.roleshop.roles, "Delete Menu - Role Shop", description)

        if await ctx.confirm(f"⚠    Are you sure to remove {role.name} from role shop?"):
            # await role.delete(reason=f"Role deleted from role shop. [{ctx.author}]")
            await ctx.guild_profile.roleshop.remove_role(role.id)

            await ctx.send_line(f"✅    {role.name} has been removed from role shop.")

    @RoleShopBase.role_shop.group(name="modify", aliases=["edit"])
    @has_permissions(manage_roles=True)
    async def modify_role(self, ctx):
        """Make changes to existing Role Shop role."""
        pass

    @modify_role.command(name="points", aliases=["point"])
    async def modify_points(self, ctx, new_points: int, *, role: discord.Role = None):
        """Modify points required to redeem or purchase role.
        It displays an interactive reaction based menu to choose your desired role if it's not specified.

        """
        description = "```css\nDisplaying Role Shop roles. React with respective emote to modify that role.```"
        role = await self._get_role(ctx, role, ctx.guild_profile.roleshop.roles, "Modify Menu - Role Shop", description)

        if await ctx.confirm(f"⚠    Are you sure to change points of {role.name} to {new_points}?"):
            await ctx.guild_profile.roleshop.set_points(role.id, new_points)

            await ctx.send_line(f"✅    {role.name} points has been changed to {new_points}.")