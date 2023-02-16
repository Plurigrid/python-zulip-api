import os
import agent
import asyncio


class PlurigridHandler(object):
    # def initialize(self, bot_handler):

    def usage(self):
        return """
        I am a conversational agent. You can tag me
        and tell me to add you to my DAO, or to curate your lamp configuration. 
        """

    def handle_message(self, message, bot_handler):
        loop = asyncio.get_event_loop()
        coroutine = agent.test(message["content"])
        reply = loop.run_until_complete(coroutine)
        bot_handler.send_reply(message, reply)


handler_class = PlurigridHandler
