# Workflows Directory

This directory contains the n8n workflow export for **AI-Powered LinkedIn Content Automation**.

## Files

| File | Purpose | Tracked in Git? |
| :--- | :--- | :--- |
| [`linkedin_content_automation.json`](linkedin_content_automation.json) | Sanitized, import-ready n8n workflow JSON with all personal IDs and credential IDs replaced by placeholders. | Yes |
| `original_workflow.local.json` | Unmodified local reference export (contains local instance/account IDs). | **No** (excluded via `.gitignore`) |

## Sanitization Summary

Before publishing to GitHub, the following fields were replaced with placeholders in `linkedin_content_automation.json`:

- `LinkedIn` node -> `parameters.person`: replaced personal LinkedIn ID with `YOUR_LINKEDIN_PERSON_ID`
- `LinkedIn` node -> `credentials.linkedInOAuth2Api.id`: replaced internal credential ID with `YOUR_LINKEDIN_CREDENTIAL_ID`
- `Notify on Telegram` node -> `parameters.chatId`: replaced personal Telegram chat ID with `YOUR_TELEGRAM_CHAT_ID`
- `Notify on Telegram` node -> `webhookId`: replaced with `YOUR_TELEGRAM_WEBHOOK_ID`
- `Notify on Telegram` node -> `credentials.telegramApi.id`: replaced internal credential ID with `YOUR_TELEGRAM_CREDENTIAL_ID`
- `meta.instanceId` and top-level `id`: replaced with `YOUR_N8N_INSTANCE_ID` and `YOUR_WORKFLOW_ID`

## Importing into n8n

1. Open your n8n dashboard and create a new workflow.
2. Open the top-right menu (**⋮**) -> **Import from File...**.
3. Select `workflows/linkedin_content_automation.json`.
4. Re-bind your own OpenAI, Google Gemini, LinkedIn OAuth2, and Telegram credentials in the respective nodes.
5. Replace `YOUR_LINKEDIN_PERSON_ID` and `YOUR_TELEGRAM_CHAT_ID` with your own values.
