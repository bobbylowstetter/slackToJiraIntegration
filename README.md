# Slack to Jira Integration


## URLs
https://us-east1-bobolopocus.cloudfunctions.net/triage

## Google Cloud Initialization
Use `gcloud init` to login to GCP. For this current setup, we are using the `bobolopocus` project.

## Deploying
Each function has its own deploy. First navigate to the `triage` folder. Then run the following command to deploy changes:
```gcloud functions deploy triage --runtime python310 --trigger-http --allow-unauthenticated --entry-point=triage --gen2 --region us-east1 --set-secrets "JIRA_AUTH=JIRA_AUTH:latest","SLACK_BOT_TOKEN=SLACK_BOT_TOKEN:latest","SLACK_SIGNING_SECRET=SLACK_SIGNING_SECRET:latest","JHNOWDEV_AUTH=JHNOWDEV_AUTH:latest"```

## Deleting
```gcloud functions delete --region us-east1 {{def}}```
Example:
```gcloud functions delete --region us-east1 triage```

## Testing the URL
```curl https://us-east1-bobolopocus.cloudfunctions.net/triage```

## Secrets
The following Secrets must be created at https://console.cloud.google.com/security/secret-manager
- JIRA_AUTH : Authentication token used for authenticating with Jira. Found https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
- SLACK_BOT_TOKEN : Token used for the slack bot found at https://api.slack.com/
- SLACK_SIGNING_SECRET : Signing secret found at https://api.slack.com/
- JHNOWDEV_AUTH : Authentication token used for authenticating with Servicenow. Found in Postman code for our Python HTTP.CLIENT code.

## Bot creation details:
You will need to adjust the following things at https://api.slack.com for your app:
- Event Subscriptions (Subscribe to Bot Events)
  - app_mention (app_mentions:read)
  - reaction_added (reactions:read)
  - reaction_removed (reactions:read)

Anytime you make a change, go ahead and reinstall the app to the workspace!