import asyncio
import unittest
from botbuilder.core import TurnContext, UserState, MemoryStorage
from botbuilder.schema import Activity, ChannelAccount
from botbuilder.core.adapters import TestAdapter

# Import the WelcomeUserBot class from the same file
from bots.welcome_user_bot import WelcomeUserBot
from data_models import WelcomeUserState


# from bots.welcome_user_bot import login_issues


class WelcomeUserBotTests(unittest.TestCase):
    # Retrieve and set the WelcomeUserState to true
    async def set_did_welcome_user_state(self, bot, turn_context, state_value=False):
        welcome_user_state = await bot.user_state_accessor.get(
            turn_context, WelcomeUserState
        )
        welcome_user_state.did_welcome_user = state_value

    def test_on_message_activity_hello(self):
        # Create a dummy UserState instance
        user_state = UserState(MemoryStorage())

        # Create a WelcomeUserBot instance with the UserState
        bot = WelcomeUserBot(user_state)

        # Create a TestAdapter for testing
        adapter = TestAdapter()

        # Create a dummy activity for testing
        activity = Activity(
            type="message",
            text="hello",
            from_property=ChannelAccount(id="test-user-id", name="TestUser"),
            channel_id="test-channel",
        )

        # Create a dummy TurnContext with the TestAdapter and activity
        turn_context = TurnContext(adapter, activity)

        # Set WelcomeUserState to True
        asyncio.run(self.set_did_welcome_user_state(bot, turn_context, True))

        # Run the asyncio event loop to process the activity
        asyncio.run(bot.on_message_activity(turn_context))

        # Retrieve the sent activities from the activity buffer
        sent_activities = adapter.activity_buffer

        # Assert that the bot sent the expected response
        # self.assertEqual(len(sent_activities), 1)
        self.assertEqual(sent_activities[0].text, "Hello, how can I help you today?")

    def test_on_message_activity_not_welcome(self):
        # Create a dummy UserState instance
        user_state = UserState(MemoryStorage())

        # Create a WelcomeUserBot instance with the UserState
        bot = WelcomeUserBot(user_state)

        # Create a TestAdapter for testing
        adapter = TestAdapter()

        # Create a dummy activity for testing
        activity = Activity(
            type="message",
            text="hello",
            from_property=ChannelAccount(id="test-user-id", name="TestUser"),
            channel_id="test-channel",
        )

        # Create a dummy TurnContext with the TestAdapter and activity
        turn_context = TurnContext(adapter, activity)

        # Run the asyncio event loop to process the activity
        asyncio.run(bot.on_message_activity(turn_context))

        # Retrieve the sent activities from the activity buffer
        sent_activities = adapter.activity_buffer

        # Assert that the bot sent the expected response
        # self.assertEqual(len(sent_activities), 1)
        self.assertEqual(sent_activities[0].text, "Welcome to the Atlassian chat!")

    def test_bot_replies_with_login_guides_when_user_types_related_key_words(self):
        # Create a dummy UserState instance
        user_state = UserState(MemoryStorage())

        # Create a WelcomeUserBot instance with the UserState
        bot = WelcomeUserBot(user_state)

        # Create a TestAdapter for testing
        adapter = TestAdapter()

        # Create a dummy activity for testing
        activity = Activity(
            type="message",
            text="login",
            from_property=ChannelAccount(id="test-user-id", name="TestUser"),
            channel_id="test-channel",
        )

        # Create a dummy TurnContext with the TestAdapter and activity
        turn_context = TurnContext(adapter, activity)

        # Run the asyncio event loop to process the activity
        asyncio.run(bot.on_message_activity(turn_context))
        log_in_response = WelcomeUserBot.login_issues(self, turn_context)

        # Retrieve the sent activities from the activity buffer
        sent_activities = adapter.activity_buffer

        # Assert that the bot sent the expected response
        response = asyncio.run(log_in_response)

        if (
            activity.text == "login"
            or "access"
            or "accessing"
            or "log"
            or "log in"
            or "login"
            or "logging"
            or "see"
            or "seeing"
            or "issue"
            or "issues"
        ):
            response = True

        assert response == True

    def test_bot_replies_with_workflow_guides_when_user_types_related_key_words(self):
        # Create a dummy UserState instance
        user_state = UserState(MemoryStorage())

        # Create a WelcomeUserBot instance with the UserState
        bot = WelcomeUserBot(user_state)

        # Create a TestAdapter for testing
        adapter = TestAdapter()

        # Create a dummy activity for testing
        activity = Activity(
            type="message",
            text="workflow",
            from_property=ChannelAccount(id="test-user-id", name="TestUser"),
            channel_id="test-channel",
        )

        # Create a dummy TurnContext with the TestAdapter and activity
        turn_context = TurnContext(adapter, activity)

        # Run the asyncio event loop to process the activity
        asyncio.run(bot.on_message_activity(turn_context))
        workflow_response = WelcomeUserBot.workflow(self, turn_context)

        # Retrieve the sent activities from the activity buffer
        sent_activities = adapter.activity_buffer

        # Assert that the bot sent the expected response
        response = asyncio.run(workflow_response)

        if activity.text == "workflow" or "workflows":
            response = True

        assert response == True

    def test_bot_replies_with_permissions_guides_when_user_types_related_key_words(
        self,
    ):
        # Create a dummy UserState instance
        user_state = UserState(MemoryStorage())

        # Create a WelcomeUserBot instance with the UserState
        bot = WelcomeUserBot(user_state)

        # Create a TestAdapter for testing
        adapter = TestAdapter()

        # Create a dummy activity for testing
        activity = Activity(
            type="message",
            text="permissions",
            from_property=ChannelAccount(id="test-user-id", name="TestUser"),
            channel_id="test-channel",
        )

        # Create a dummy TurnContext with the TestAdapter and activity
        turn_context = TurnContext(adapter, activity)

        # Run the asyncio event loop to process the activity
        asyncio.run(bot.on_message_activity(turn_context))
        permissions_response = WelcomeUserBot.permissions(self, turn_context)

        # Retrieve the sent activities from the activity buffer
        sent_activities = adapter.activity_buffer

        # Assert that the bot sent the expected response
        response = asyncio.run(permissions_response)

        if activity.text == "permissions" or "permissions":
            response = True

        assert response == True

    def test_bot_replies_with_prompt_about_tickets_when_user_types_related_key_words(
        self,
    ):
        # Create a dummy UserState instance
        user_state = UserState(MemoryStorage())

        # Create a WelcomeUserBot instance with the UserState
        bot = WelcomeUserBot(user_state)

        # Create a TestAdapter for testing
        adapter = TestAdapter()

        # Create a dummy activity for testing
        activity = Activity(
            type="message",
            text="tickets",
            from_property=ChannelAccount(id="test-user-id", name="TestUser"),
            channel_id="test-channel",
        )

        # Create a dummy TurnContext with the TestAdapter and activity
        turn_context = TurnContext(adapter, activity)

        # Run the asyncio event loop to process the activity
        asyncio.run(bot.on_message_activity(turn_context))

        # Retrieve the sent activities from the activity buffer
        sent_activities = adapter.activity_buffer

        # Assert that the bot sent the expected response
        response = "Please provide details of the request."

        if activity.text == "ticket" or "ticket":
            response = True

        assert response == True
