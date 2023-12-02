from botbuilder.core import (
    ActivityHandler,
    CardFactory,
    MessageFactory,
    TurnContext,
    UserState,
)
from botbuilder.schema import (
    ActionTypes,
    CardAction,
    CardImage,
    ChannelAccount,
    HeroCard,
)
from flask import Flask

from data_models import WelcomeUserState

app = Flask(__name__)
import sys
import logging

logger = logging.getLogger("azure")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


class WelcomeUserBot(ActivityHandler):
    def __init__(self, user_state: UserState):
        if user_state is None:
            raise TypeError(
                "[WelcomeUserBot]: Missing parameter. user_state is required but None was given"
            )

        self._user_state = user_state

        self.user_state_accessor = self._user_state.create_property("WelcomeUserState")

        self.WELCOME_MESSAGE = """This is a simple Welcome Bot sample. This bot will introduce you
                        to welcoming and greeting users. You can say 'intro' to see the
                        introduction card. If you are running this bot in the Bot Framework
                        Emulator, press the 'Restart Conversation' button to simulate user joining
                        a bot or a channel"""

        self.INFO_MESSAGE = """You are seeing this message because the bot received at least one
                        'ConversationUpdate' event, indicating you (and possibly others)
                        joined the conversation. If you are using the emulator, pressing
                        the 'Start Over' button to trigger this event again. The specifics
                        of the 'ConversationUpdate' event depends on the channel. You can
                        read more information at: https://aka.ms/about-botframework-welcome-user"""

        self.LOCALE_MESSAGE = """"You can use the 'activity.locale' property to welcome the
                        user using the locale received from the channel. If you are using the 
                        Emulator, you can set this value in Settings."""

        self.PATTERN_MESSAGE = """It is a good pattern to use this event to send general greeting
                        to user, explaining what your bot can do. In this example, the bot
                        handles 'hello', 'hi', 'help' and 'intro'. Try it now, type 'hi'"""

        logger.info("Bot initiated")

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # save changes to WelcomeUserState after each turn
        await self._user_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"Hi there { member.name }. " + self.WELCOME_MESSAGE
                )

                await turn_context.send_activity(self.INFO_MESSAGE)

                await turn_context.send_activity(
                    f"{ self.LOCALE_MESSAGE } Current locale is { turn_context.activity.locale }."
                )

                await turn_context.send_activity(self.PATTERN_MESSAGE)

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Respond to messages sent from the user.
        """
        # Get the state properties from the turn context.
        welcome_user_state = await self.user_state_accessor.get(
            turn_context, WelcomeUserState
        )

        if not welcome_user_state.did_welcome_user:
            welcome_user_state.did_welcome_user = True

            await turn_context.send_activity("Welcome to the Atlassian chat!")

            name = turn_context.activity.from_property.name
            await turn_context.send_activity(f"Hello {name}, how can I help you?")
            logger.info(f"{name} is typing ...")
        else:
            text = turn_context.activity.text.lower()
            logger.info(f"{text} was typed")
            if text in ("hello", "hi"):
                await turn_context.send_activity(f"Hello, how can I help you today?")
            elif text in (
                "help",
                "access",
                "accessing",
                "log",
                "log in",
                "login",
                "logging",
                "see",
                "seeing",
                "issue",
                "issues",
            ):
                await self.login_issues(turn_context)
            elif text in ("workflow", "workflows"):
                await self.workflow(turn_context)
            elif text in ("permissions", "permission"):
                await self.permissions(turn_context)
            elif text in ("ticket", "incident"):
                await turn_context.send_activity(
                    "Please provide details of the request."
                )
            else:
                await turn_context.send_activity(self.WELCOME_MESSAGE)
                await turn_context.send_activity(
                    "Sorry, I didn't get this. Please try again."
                )

    async def login_issues(self, turn_context: TurnContext):
        card = HeroCard(
            title="If you're having issues accessing our Atlassian site, please refer to these guides.",
            text="👇👇👇",
            # images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Issues logging in to our Atlassian site",
                    text="Issues logging in to our Atlassian site",
                    display_text="Issues logging in to our Atlassian site",
                    value="https://kpmgengineering.atlassian.net/wiki/spaces/FRONTLINE/pages/41751653/Troubleshooting",
                ),
                CardAction(
                    type=ActionTypes.open_url,
                    title="Log in for the 1st time to our Atlassian site",
                    text="Log in for the 1st time to our Atlassian site",
                    display_text="Log in for the 1st time to our Atlassian site",
                    value="https://kpmgengineering.atlassian.net/wiki/spaces/ATL/pages/13402464/Login+for+First+Time",
                ),
                CardAction(
                    type=ActionTypes.open_url,
                    title="Request site access",
                    text="Request site access",
                    display_text="Request site access",
                    value="https://kpmgengineering.atlassian.net/wiki/spaces/ATL/pages/13402358/Request+site+access",
                ),
            ],
        )

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(card))
        )

    async def workflow(self, turn_context: TurnContext):
        card = HeroCard(
            title="If you want more information on how to modify your project workflow, please refer to this guide.",
            text="👇👇👇",
            # images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Modify workflow",
                    text="Modify workflow",
                    display_text="Modify workflow",
                    value="https://kpmgengineering.atlassian.net/wiki/spaces/FRONTLINE/pages/216564050/How+to+Create+Edit+Project+Workflows",
                ),
            ],
        )

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(card))
        )

    async def permissions(self, turn_context: TurnContext):
        card = HeroCard(
            title="If you want more information on how to edit permissions for your project, please refer to this guide.",
            text="👇👇👇",
            # images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Modify project permissions",
                    text="Modify project permissions",
                    display_text="Modify project permissions",
                    value="https://kpmgengineering.atlassian.net/wiki/spaces/FRONTLINE/pages/41749670/Manage+Project+Permissions",
                ),
            ],
        )

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(card))
        )
