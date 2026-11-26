# Beginner-Friendly User Guide

This guide helps a new user set up and operate **AI-Powered LinkedIn Content Automation**. No coding is required for normal use, but you must connect your own accounts and credentials.

> **Security:** This repository does not provide the maintainer's private API keys, OAuth tokens, LinkedIn profile ID or Telegram chat ID. Use your own accounts. Never publish API keys or bot tokens in GitHub.

## 1. What the project does

The 15-node n8n workflow:
1. Runs on its configured schedule (every 8 hours in the template).
2. Generates a student/early-career LinkedIn topic.
3. Writes a post and image description.
4. Generates an image using Google Gemini.
5. Generates relevant hashtags.
6. Merges the image and hashtag data and validates/formats the post.
7. Publishes an image post to LinkedIn.
8. Sends a Telegram notification after the LinkedIn publishing step.

For technical details, see [Workflow Explanation](workflow-explanation.md).

## 2. What you need

- n8n Cloud or a self-hosted n8n instance.
- An AI model connection for the three OpenAI chat-model nodes, or supported n8n Gateway credits where available.
- Google Gemini image-generation access, or supported Gateway credits for that operation.
- A LinkedIn account and LinkedIn Developer app with member-posting access.
- A Telegram account and a bot created through @BotFather.

Some services charge for usage. Check current provider pricing and free-tier conditions before running regularly.

## 3. Start n8n

### Option A — n8n Cloud (simplest)

1. Visit [n8n](https://n8n.io/) and create an account.
2. Start the available Cloud trial or choose a plan.
3. Open your workspace.
4. Check whether Gateway credits are available and enabled. Do not assume they are unlimited or recurring.

### Option B — Self-hosted n8n

You can run n8n on your own computer/server using Docker or npm. Follow the official [n8n hosting documentation](https://docs.n8n.io/hosting/).

**Important:** Self-hosting does not automatically include n8n Cloud Gateway credits. You normally connect your own AI provider credentials.

## 4. Download and import the workflow

1. Open this repository on GitHub.
2. Open [linkedin_content_automation.json](../workflows/linkedin_content_automation.json).
3. Download the JSON file to your computer.
4. In n8n, create a new workflow.
5. Open the workflow menu (three dots) and choose **Import from File**.
6. Select the downloaded JSON file and save the workflow.

**Use this file for a new setup:** workflows/linkedin_content_automation.json.

It is the sanitized template, inactive by default, with LinkedIn visibility set to CONNECTIONS. Do not use live-production-export-redacted.json as your starting point: it is a redacted live export and its active/public settings may not suit your account.

## 5. Configure the AI model nodes

There are three OpenAI Chat Model nodes:
- **OpenAI Chat Model** — topic generation.
- **OpenAI Chat Model1** — post writing.
- **OpenAI Chat Model2** — hashtag generation.

Open each node and configure a credential and model available to your account.

### Option A — Use n8n Gateway credits if available

Gateway credits can be a convenient way to try supported models without creating separate provider accounts or managing separate API keys.

1. Current n8n documentation lists Gateway credits for eligible **n8n Cloud Starter and Pro** workspaces on n8n 2.36.0 or later. It is not currently available for self-hosted n8n or Enterprise.
2. Open a supported AI model node.
3. In the credential selector, look for **Use Gateway credits**.
4. If available, select it and check the displayed balance.
5. Choose a model listed as supported in that node.
6. Repeat for other AI nodes only where Gateway credits are offered.
7. Run a small test and monitor your balance.

**Are the credits free?** n8n documents a small one-time Gateway credit allowance for eligible new Cloud accounts and credits in Cloud free trials. This is limited trial usage, not unlimited free AI and not a guaranteed monthly allowance. When the balance reaches zero, Gateway-credit requests stop until eligible credits are added. Trial users may not be able to top up. Check your own n8n console and the official [Gateway credits guide](https://docs.n8n.io/).

Gateway credits are separate from n8n Assistant credits. Assistant credits do not pay for AI nodes in your workflow.

### Option B — Use your own OpenAI API key

If Gateway credits are unavailable or exhausted:

1. Create/sign in to an OpenAI API account.
2. Review current API pricing and billing requirements.
3. Create an API key in the provider dashboard.
4. In n8n Credentials, create an OpenAI API credential and store the key there.
5. Select that credential in all three OpenAI Chat Model nodes.
6. Choose a model your account can access.

A ChatGPT subscription does not automatically include API usage credits. API billing is separate.

## 6. Configure Gemini image generation

The Gemini Image Generator node creates the visual attached to the post.

**Gateway credits option:** If the node credential selector offers Use Gateway credits and the exact image model/operation is listed as supported, you can select it and check the balance. Support is node- and operation-specific; do not assume every Gemini image operation is covered.

**Own API key option:**
1. Open [Google AI Studio](https://aistudio.google.com/).
2. Review Gemini API availability, model access and pricing.
3. Create an API key if available to you.
4. In n8n Credentials, create the Google Gemini/Google PaLM API credential type offered by your n8n version.
5. Select it in the Gemini Image Generator node.
6. Confirm the configured image model is available to your key. If not, select an image model supported by your account and n8n node version.

Never put your API key in workflow JSON or a public GitHub issue.

## 7. Configure LinkedIn publishing

1. Open the [LinkedIn Developer Portal](https://www.linkedin.com/developers/) and create an app.
2. Follow LinkedIn's current product and access requirements for member posting.
3. In n8n Credentials, create a LinkedIn OAuth2 API credential.
4. Copy the OAuth redirect/callback URL shown by n8n and add it to the LinkedIn app's authorized redirect URLs.
5. Complete OAuth using the LinkedIn account you want to publish from.
6. In the LinkedIn node, select your credential/profile and confirm it refers to your own profile.
7. Keep visibility set to **CONNECTIONS** for the first test. Change to **PUBLIC** only when you intentionally want public posts and have verified the output.

LinkedIn controls API access and permissions; approval and available scopes can vary. See [LinkedIn API documentation](https://learn.microsoft.com/en-us/linkedin/).

## 8. Configure Telegram notifications

1. In Telegram, open **@BotFather**.
2. Send /start, then /newbot, and follow the prompts.
3. Copy the bot token and store it in an n8n Telegram API credential.
4. Start a chat with your new bot and send /start.
5. Obtain your own numeric chat ID using the Telegram Bot API getUpdates after messaging the bot, or a reputable chat-ID helper.
6. Open the Notify on Telegram node, select your Telegram credential and replace YOUR_TELEGRAM_CHAT_ID with your own numeric ID.
7. Save the workflow.

Treat the bot token like a password. Never commit it to GitHub or share it.

## 9. Review settings before the first run

Check that:
- All three OpenAI Chat Model nodes have working credentials and accessible models.
- Gemini Image Generator has a working credential and supported image model.
- LinkedIn OAuth is connected to the intended profile.
- Telegram credential and chat ID are yours and correct.
- LinkedIn visibility is CONNECTIONS for the first test.
- The workflow is saved and remains inactive until you choose to activate it.

Replace placeholders in your own n8n workspace. Never commit real secrets to the public repository.

## 10. Run a controlled manual test

1. Keep the workflow inactive.
2. Click **Execute Workflow** in the n8n editor.
3. Open the execution view and inspect the nodes in order.
4. Confirm the topic generator returns a topic.
5. Confirm the content creator returns a title, post body and image description.
6. Confirm Gemini returns image binary data.
7. Confirm the hashtag generator returns a hashtag array.
8. Confirm Merge and Validate & Format Post complete successfully.
9. Confirm LinkedIn publishes to the intended audience.
10. Confirm the Telegram notification arrives with the expected details.

If a node fails, inspect its error details before changing settings or rerunning. Do not repeatedly retry LinkedIn publishing if you are unsure whether the post was already created.

## 11. Activate scheduled posting

Only after the manual test succeeds:

1. Review the generated post and LinkedIn visibility.
2. Confirm the Schedule Trigger interval. The template is configured for every 8 hours.
3. Activate the workflow using n8n's **Active** toggle.
4. Monitor the first scheduled execution in n8n Executions.
5. Check LinkedIn and Telegram to confirm the result.

To stop scheduled posts, deactivate the workflow in n8n. This does not delete posts already published.

## 12. Troubleshooting

| Problem | What to check |
|---|---|
| Model not found | Select a model available to your credential/Gateway balance and n8n node version. |
| Gateway credits option missing | Check Cloud plan eligibility, n8n version, instance settings and support for that node/operation. Self-hosted n8n does not get Cloud Gateway credits. |
| Gateway credits exhausted | Check the balance. Use your own provider credential or add credits if your plan permits. |
| Gemini image generation fails | Check API access, model availability, credential and usage limits. |
| LinkedIn 401/403 | Reconnect OAuth and check the app's current member-posting access. |
| LinkedIn post has no image | Inspect Gemini binary output and confirm Merge receives the image on input 0. |
| Telegram says chat not found | Start the bot conversation and verify the numeric chat ID and credential. |
| Workflow does not run on schedule | Confirm the workflow is Active, schedule/timezone are correct and n8n is running. |

## 13. Cost and free-use guidance

- Start with Gateway credits only if n8n shows a balance in your eligible Cloud account. Treat this as limited trial credit, not a permanent free tier.
- If Gateway credits are unavailable, compare provider free tiers and API pricing before creating keys or running the schedule.
- Reduce costs by testing manually first, limiting unnecessary executions and avoiding repeated image-generation tests.
- Gateway credits do not pay for every external service or guarantee free LinkedIn publishing or Telegram usage.
- Self-hosting n8n may avoid a Cloud subscription, but it does not make third-party AI API calls free. You still need a provider credential or another service with a genuine free allowance.

## 14. More help

- [Repository README](../README.md)
- [Installation & Setup Guide](installation-guide.md)
- [Workflow Explanation](workflow-explanation.md)
- [API Integrations](api-integrations.md)
- [Security Guidelines](security-guidelines.md)
- [n8n documentation](https://docs.n8n.io/)
- [n8n Gateway credits documentation](https://docs.n8n.io/)

When reporting an issue, never include credentials, tokens, private IDs or personal data.
