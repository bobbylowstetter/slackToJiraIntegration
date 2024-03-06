import os
import logging
from slack_bolt import App

# Flask adapter
from slack_bolt.adapter.google_cloud_functions import SlackRequestHandler
from flask import Request

logging.basicConfig(level=logging.DEBUG)

# process_before_response must be True when running on FaaS
app = App(process_before_response=True)

handler = SlackRequestHandler(app)

# This is the slash command. We are not really using it, but it will notify them on how to use the bot.
@app.command("/triage")
def hello_command(ack, logger):
  logger.info("I see a slash command!")
  ack("Hi from The Jira and Slack Integration bot! Use reactions to have me create (:eyes) or complete (:white_check_mark) a ticket.")

# This is the event we want to use to create a ticket
@app.event("reaction_added")
def handle_reaction_added(body, say, logger):
  logger.info("I see a reaction_added event!")
  logger.info(body)

  # Get the info we will need for Jira
  assignee = body["event"]["user"]
  reaction = body["event"]["reaction"]
  channel = body["event"]["item"]["channel"]
  ts = body["event"]["item"]["ts"]
  reporter = app.client.conversations_replies(
    channel=channel,
    ts=ts
  )["messages"][0]["user"]
  description = app.client.conversations_replies(
    channel=channel,
    ts=ts
  )["messages"][0]["text"]
  
  # TODO: Don't allow this to be run from within a thread

  # TODO: Check if the user is a team member in a separate JSON file
  
  # Create a ticket if the reaction is :eyes:
  if reaction == "eyes":
    jira_authorization=os.environ.get("JIRA_AUTH")
    say(f"Hey there <@{assignee}>! I will create a ticket for <@{reporter}> with a description of {description}!", thread_ts=body["event"]["item"]["ts"])

  # Complete the ticket if the reaction is :white_check_mark:
  elif reaction =="white_check_mark":
    say(f"Hey there <@{assignee}>! I will mark this ticket as done!", thread_ts=body["event"]["item"]["ts"])

# This will now become a help message as we are using reactions now
@app.event("app_mention")
def event_test(say, logger):
  logger.info("I see a mention!")
  say("Hi there! I am The Jira and Slack Integration bot! Use reactions to have me create (:eyes) or complete (:white_check_mark) a ticket.")

def triage(req: Request):
  app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
  )
  return handler.handle(req)

# Step1: Create a new Slack App: https://api.slack.com/apps
# Bot Token Scopes: app_mentions:read,chat:write,commands

# Step2: Set env variables
# vi .env.yaml

# Step3: Create a new Google Cloud project (if needed)
# gcloud projects create YOUR_PROJECT_NAME
# gcloud config set project YOUR_PROJECT_NAME

# Step4: Deploy a function in the project (see README for more details)
# gcloud functions describe hello_bolt_app

# Step5: Set Request URL
# Set URL in README to the following:
#  * slash command: /triage
#  * Events Subscriptions & add `app_mention` event