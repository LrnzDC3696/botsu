# Importing `Client` and `wait_for_interruption` from hata
from utils import build_duration_string
from hata import Client, Guild, wait_for_interruption, Embed, Color, DiscordException, ERROR_CODES, COLORS
from hata.ext.slash import P, abort
from datetime import timedelta as TimeDelta
from dotenv import load_dotenv
from os import environ

load_dotenv()
BOT_TOKEN = environ["PEANUTS_BOT"]
SPY_TESTING_GUILD_ID = 1092844476390711326
TEST_GUILD = Guild.precreate(SPY_TESTING_GUILD_ID)

Peanuts = Client(BOT_TOKEN, extensions="slash")

MAX_TIMEOUT_DURATION = TimeDelta(28)


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
async def peanut(event, user: ("user", "To who?")):
    """Gifts a peanut!"""
    return Embed(description=f"{event.user:f} just gifted a peanut to {user:f} !")


@Peanuts.events
async def ready(client):
    print(f"{client:f} logged in.")


# -------------------------------------------------------------------------------------


@Peanuts.interactions(guild=TEST_GUILD)
async def dm_me(client, event):
    channel = await event.client.channel_private_create(event.user)
    await client.message_create(channel, "I dmed you")


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

    total_timeout_duraton = get_duration(
        days, hours, minutes, seconds
    )
    total_duration = build_duration_string(total_timeout_duraton)

    await event.client.user_guild_profile_edit(
        event.guild, user, timeout_duration=total_timeout_duraton, reason=reason
    )

    if notify:
        message = Embed(
            "You have been muted!",
            reason,
            COLORS.red
        ).add_field("Mute duration:", total_duration
        ).add_field("Reason", reason)

        await try_notify(client, user, message, event.channel)

    embed = Embed(
        title="User Muted",
        description=f"{user.name} has been muted for {total_duration}.",
        color=COLORS.red
    ).add_field("Reason", reason
    ).add_field("Notified", "Yes" if notify else "No"
    ).add_field("Muted by", event.user.name
    ).add_field("Mute Time", total_duration)

    return embed

@Peanuts.interactions(guild=TEST_GUILD)
async def unmute(event, user: ("user", "Who to unmute? >:D")):
    """thou shall speak"""
    return "pong"


@Peanuts.interactions(guild=TEST_GUILD)
async def kick(event, user: ("user", "Who to kick? >:D")):
    """cyaio"""
    "https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client#guild_user_delete"
    return "pong"


@Peanuts.interactions(guild=TEST_GUILD)
async def ban(event, user: ("user", "Who to ban? >:D")):
    """YEEEEEEEEEEEEEEEEEEEEEEEEEEEETTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT!"""
    "https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client#guild_ban_add"
    return "pong"


@Peanuts.interactions(guild=TEST_GUILD)
async def unban(event, user: ("user", "Who to unban? >:D")):
    """unyeet."""
    event.client.guild_user_delete(event.guild.id, user)
    return "pong"


# -------------------------------------------------------------------------------------

ACTION_TYPE = ["All", "Mute", "Kick", "Ban"]


@Peanuts.interactions(guild=TEST_GUILD)
async def mod_top_list(
    event,
    action_type: (ACTION_TYPE, "What action do you want to filter") = "All",
):
    pass


Peanuts.start()
wait_for_interruption()
