from utils import build_duration_string
from scarletio import ReuAsyncIO
from random import choice
from hata import (
    Client,
    Guild,
    AuditLogEvent,
    wait_for_interruption,
    Embed,
    DiscordException,
    ERROR_CODES,
    COLORS,
)
from hata.ext.slash import P, abort
from datetime import timedelta as TimeDelta, datetime
from dotenv import load_dotenv
from os import environ
from hata.ext.plugin_loader import register_and_load_plugin
from helper import files_

load_dotenv()
BOT_TOKEN = environ["PEANUTS_BOT"]
# SPY_TESTING_GUILD_ID = 1092844476390711326
SPY_TESTING_GUILD_ID = 1043895269021991052
TEST_GUILD = Guild.precreate(SPY_TESTING_GUILD_ID)

Peanuts = Client(BOT_TOKEN, extensions="slash")

MAX_TIMEOUT_DURATION = TimeDelta(28)

register_and_load_plugin('plugins')


async def try_notify(client, user, message, guild_channel=None):
    private_channel = await client.channel_private_create(user)

    try:
        await client.message_create(private_channel, message)
    except DiscordException as err:
        if err.code != ERROR_CODES.cannot_message_user:
            raise
    else:
        if guild_channel is not None:
            await client.message_create(guild_channel, message)


def check_basic_permission(event, client, user):
    guild = event.guild

    if guild is None:
        abort("Use this command in a guild!")

    if not event.user_permissions.can_moderate_users:
        abort("You must have moderator permissions!")

    if not guild.cached_permissions_for(client).can_moderate_users:
        abort("Client must have moderator permissions!")

    if not event.user.has_higher_role_than_at(user, guild):
        abort(f"You must have higher role than {user.name}!")

    if not client.has_higher_role_than_at(user, guild):
        abort(f"Client must have higher role than {user.name}")


def get_duration(days, hours, minutes, seconds):
    if not (days or hours or minutes or seconds):
        return abort("Mute duration must be positive.")

    duration = TimeDelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    if duration > MAX_TIMEOUT_DURATION:
        duration = MAX_TIMEOUT_DURATION

    return duration


@Peanuts.interactions(guild=TEST_GUILD)
async def dm_me(client, event):
    channel = await event.client.channel_private_create(event.user)
    await client.message_create(channel, "I dmed you")


@Peanuts.interactions(guild=TEST_GUILD)
async def peanut(event, user: ("user", "To who?")):
    """Gifts a peanut!"""
    return Embed(description=f"{event.user:f} just gifted a peanut to {user:f} !")


@Peanuts.interactions(guild=TEST_GUILD)
async def badinginator(event, user: ("str", "who?")):
    """tells if a person is bading or not"""
    return Embed(
        description=f"{user} is {'very' if choice((True, False)) else 'not'} bading"
    )


@Peanuts.events
async def ready(client):
    print(f"{client:f} logged in.")


# -------------------------------------------------------------------------------------

@Peanuts.interactions(guild=TEST_GUILD)
async def show_photos(
    client,
    event,
):
    paths = files_["photos"]

    for path in paths:
        for pat in path:
            with (await ReuAsyncIO(pat)) as io:
                message = await client.message_create(event.channel, file=io)


@Peanuts.interactions(guild=TEST_GUILD)
async def mute(
    client,
    event,
    user: ("user", "Who to mute? >:D"),
    days: P("int", "days", min_value=0, max_value=28) = 0,
    hours: P("int", "hours", min_value=0, max_value=24) = 0,
    minutes: P("int", "minutes", min_value=0, max_value=60) = 0,
    seconds: P("int", "seconds", min_value=0, max_value=60) = 0,
    reason: ("str", "Why though?") = None,
    notify: ("bool", "Should I notify the user?") = False,
):
    """Though shaall be in timeout"""
    check_basic_permission(event, client, user)

    total_timeout_duraton = get_duration(days, hours, minutes, seconds)
    total_duration = build_duration_string(total_timeout_duraton)

    await event.client.user_guild_profile_edit(
        event.guild, user, timeout_duration=total_timeout_duraton, reason=reason
    )

    if notify:
        message = (
            Embed("You have been muted!", reason, COLORS.red)
            .add_field("Mute duration:", total_duration)
            .add_field("Reason", reason)
        )

        await try_notify(client, user, message, event.channel)

    embed = (
        Embed(
            title="User Muted",
            description=f"{user.name} has been muted for {total_duration}.",
            color=COLORS.red,
        )
        .add_field("Reason", reason)
        .add_field("Notified", "Yes" if notify else "No")
        .add_field("Muted by", event.user.name)
        .add_field("Mute Time", total_duration)
    )

    return embed


@Peanuts.interactions(guild=TEST_GUILD)
async def unmute(
    client,
    event,
    user: ("user", "Who to unmute? >:D"),
    reason: ("str", "Why though?") = None,
    notify: ("bool", "Should I notify the user?") = False,
):
    """Thou shall speak"""
    check_basic_permission(event, client, user)

    await event.client.user_guild_profile_edit(
        event.guild, user, timeout_duration=None, reason=reason
    )

    if notify:
        message = Embed("You have been unmuted!", reason, COLORS.green).add_field(
            "Reason", reason
        )

        await try_notify(client, user, message, event.channel)

    embed = (
        Embed(
            title="User Unmuted",
            description=f"{user.name} has been unmuted",
            color=COLORS.green,
        )
        .add_field("Reason", reason)
        .add_field("Notified", "Yes" if notify else "No")
        .add_field("Unmuted by", event.user.name)
    )

    return embed


@Peanuts.interactions(guild=TEST_GUILD)
async def kick(
    client,
    event,
    user: ("user", "Who to kick? >:D"),
    reason: ("str", "Why though?") = None,
    notify: ("bool", "Should I notify the user?") = False,
):
    """Thou shall be kicked"""
    check_basic_permission(event, client, user)

    await client.guild_user_delete(event.guild, user, reason)

    if notify:
        message = Embed("You have been kicked LMAO!", COLORS.red).add_field(
            "Reason", reason
        )

        await try_notify(client, user, message)

    embed = (
        Embed(
            title="User Kicked LMAO",
            description=f"{user.name} has been kicked",
            color=COLORS.red,
        )
        .add_field("Reason", reason)
        .add_field("Notified", "Yes" if notify else "No")
        .add_field("Kicked by", event.user.name)
    )

    return embed


# duration
@Peanuts.interactions(guild=TEST_GUILD)
async def ban(
    client,
    event,
    user: ("user", "Who to ban? >:D"),
    reason: ("str", "Why though?") = None,
    notify: ("bool", "Should I notify the user?") = False,
):
    """Thou shall be kicked"""
    check_basic_permission(event, client, user)

    await client.guild_ban_add(event.guild, user, reason=reason)

    if notify:
        message = Embed("You have been banned LMAO!", COLORS.red).add_field(
            "Reason", reason
        )

        await try_notify(client, user, message)

    embed = (
        Embed(
            title="User banned LMAO",
            description=f"{user.name} has been banned",
            color=COLORS.red,
        )
        .add_field("Reason", reason)
        .add_field("Notified", "Yes" if notify else "No")
        .add_field("Banned by", event.user.name)
    )

    return embed


# duration
@Peanuts.interactions(guild=TEST_GUILD)
async def unban(
    client,
    event,
    user: ("user", "Who to unban? >:D"),
    reason: ("str", "Why though?") = None,
    notify: ("bool", "Should I notify the user?") = False,
):
    """Thou shall be unbanned"""
    check_basic_permission(event, client, user)

    await client.guild_ban_delete(event.guild, user, reason)

    if notify:
        message = Embed("You have been unbanned", COLORS.red).add_field(
            "Reason", reason
        )

        await try_notify(client, user, message)

    embed = (
        Embed(
            title="User unbanned",
            description=f"{user.name} has been unbanned",
            color=COLORS.red,
        )
        .add_field("Reason", reason)
        .add_field("Notified", "Yes" if notify else "No")
        .add_field("Unbanned by", event.user.name)
    )

    return embed


# -------------------------------------------------------------------------------------

"""
WRITE MOD TOP LIST COMMAND

when a user bans / kicks / mutes an other (unique) user, then they get 1 mod score
this should count the actions done by the mod and the actions done through the bot too
the actions should be requested from audit logs
options for filtering: page, action type, months

SHOULD count a user's manual ban & bot ban

page: int
action type: (require) kick, mute, ban
months: int

------------- ------------- ------------- -------------
    
"""


LOG_MAX_DAYS = 45

FLAG_BAN = 1 << 0
FLAG_KICK = 1 << 1
FLAG_MUTE = 1 << 2
FLAG_ALL = FLAG_BAN | FLAG_KICK | FLAG_MUTE

ACTION_TYPES = {
    "all": FLAG_ALL,
    "mute": FLAG_MUTE,
    "kick": FLAG_KICK,
    "ban": FLAG_BAN,
}


def is_actually_mute(audit_log_entry):
    changes = audit_log_entry.changes

    if changes is not None:
        for change in changes:
            if change.attribute_name == "timed_out_until":
                if change.after is not None:
                    return True
                break

    return False


async def process_audit_log(
    client, guild, days, action_type, event_type, users_action_count
):
    async for audit_log_entry in await client.audit_log_iterator(
        guild, event=event_type
    ):
        if audit_log_entry.created_at < days:
            break

        if event_type == "mute" and not is_actually_mute(audit_log_entry):
            continue

        user_id = audit_log_entry.user_id
        users_action_count = users_action_count.setdefault(
            user_id, {event_type: 0, "all": 0})

        users_action_count[event_type] += 1
        users_action_count["all"] += 1

    return users_action_count


@Peanuts.interactions(guild=TEST_GUILD)
async def mod_top_list(
    client,
    event,
    action_type: (ACTION_TYPES, "What action do you want to filter") = FLAG_ALL,
    days: P("int", "days", min_value=1, max_value=LOG_MAX_DAYS) = LOG_MAX_DAYS,
):
    guild = event.guild
    days_ago = datetime.utcnow() - TimeDelta(days=days)

    users_action_count = {}

    if action_type & FLAG_MUTE:
        users_action_count = await process_audit_log(
            client,
            guild,
            days_ago,
            "mute",
            AuditLogEvent.member_update,
            users_action_count,
        )

    if action_type & FLAG_KICK:
        users_action_count = await process_audit_log(
            client,
            guild,
            days_ago,
            "kick",
            AuditLogEvent.member_kick,
            users_action_count,
        )

    if action_type & FLAG_BAN:
        users_action_count = await process_audit_log(
            client,
            guild,
            days_ago,
            "ban",
            AuditLogEvent.member_ban_add,
            users_action_count,
        )

    sorted_users = sorted(
        users_action_count.items(),
        key=lambda x: sum(x[1].values()),
        reverse=True,
    )

    description = ["```py"]

    for n, (user_id, action_counts) in enumerate(sorted_users, 1):
        name = (await client.user_get(user_id)).full_name
        values = [str(x) for x in action_counts.values()]
        description.append("".join([str(n), ".: ", " ".join(values), " ", name]))

    description.append("```")
    description = "\n".join(description)

    embed = Embed(
        "Mod Top-List",
        description,
        COLORS.gold,
        timestamp=datetime.utcnow(),
    )

    return embed


Peanuts.start()
wait_for_interruption()
