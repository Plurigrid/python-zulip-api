import os
import plurigrid_reader


class PlurigridHandler(object):
    """
    A docstring documenting this bot.
    """

    def initialize(self, bot_handler):
        self.reader = plurigrid_reader.PlurigridReader()
        config_info = bot_handler.get_config_info("plurigrid")
        os.environ["OPENAI_API_KEY"] = config_info["openai_api_key"]
        self.reader.load(config_info["data_dir"], config_info["index_path"])

    def usage(self):
        return """
        I am a conversational agent that has knowledge about
        the plurigrid protocol and ecosystem. You can tag me
        and ask questions about plurigrid or anything else. 
        """

    def handle_message(self, message, bot_handler):
        bot_handler.send_reply(message, self.reader.query(message["content"]))


handler_class = PlurigridHandler
