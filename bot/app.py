#!/usr/bin/env python

import logging
import os

from beepboop import resourcer
from beepboop import bot_manager

from slack_bot import SlackBot
from slack_bot import spawn_bot

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=log_level)

    slack_token = os.getenv("SLACK_TOKEN", "")
    logging.info("token: {}".format(slack_token))
    pipedrive_api_key = os.getenv("PIPEDRIVE_API_KEY", None)
    if not pipedrive_api_key:
        raise ValueError("Pipedrive API key needs to be specified")
    logging.info("pipedrive api key: {}".format(pipedrive_api_key))
    db_api_url = os.getenv("DB_API_URL", "")
    if not db_api_url:
        raise ValueError("Pipedrive API key needs to be specified")
    logging.info("db api url: {}".format(db_api_url))
    if slack_token == "":
        logging.info("SLACK_TOKEN env var not set, expecting token to be provided by Resourcer events")
        slack_token = None
        botManager = bot_manager.BotManager(spawn_bot)
        res = resourcer.Resourcer(botManager)
        res.start()
    else:
        # only want to run a single instance of the bot in dev mode
        bot = SlackBot(pipedrive_api_key, db_api_url, slack_token)
        bot.start({})
