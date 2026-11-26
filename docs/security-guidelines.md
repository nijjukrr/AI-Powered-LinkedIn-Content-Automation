# Security Guidelines

Security is a first-class requirement for automation workflows, especially when exporting n8n JSON files to public GitHub repositories.

---

## 1. Security Audit of the Original Export

When auditing the original n8n workflow export before publishing, the following sensitive/identifying fields were discovered and sanitized:

| Location in JSON | Field | Risk | Resolution in Public Workflow |
| :--- | :--- | :--- | :--- |
| `LinkedIn` node | `parameters.person` | Exposes personal LinkedIn person identifier | Replaced with `YOUR_LINKEDIN_PERSON_ID` |
| `LinkedIn` node | `credentials.linkedInOAuth2Api.id` | Exposes internal n8n credential ID | Replaced with `YOUR_LINKEDIN_CREDENTIAL_ID` |
| `Notify on Telegram` node | `parameters.chatId` | Exposes personal Telegram chat ID | Replaced with `YOUR_TELEGRAM_CHAT_ID` |
| `Notify on Telegram` node | `webhookId` | Exposes internal webhook identifier | Replaced with `YOUR_TELEGRAM_WEBHOOK_ID` |
| `Notify on Telegram` node | `credentials.telegramApi.id` | Exposes internal n8n credential ID | Replaced with `YOUR_TELEGRAM_CREDENTIAL_ID` |
| Root `meta` & `id` | `meta.instanceId`, `id` | Exposes n8n instance fingerprint and workflow ID | Replaced with `YOUR_N8N_INSTANCE_ID` and `YOUR_WORKFLOW_ID` |

The unmodified original export is retained **locally only** and excluded from Git via `.gitignore` (`workflows/*.local.json`).

---

## 2. How n8n Stores Credentials Safely

- **Never** paste API keys, Bearer tokens, OAuth Client Secrets, or Bot Tokens directly into n8n node parameter fields or HTTP Request headers inside exported JSON.
- Always use n8n's built-in **Credentials** vault, which encrypts secrets at rest using `N8N_ENCRYPTION_KEY` (self-hosted) or platform-managed encryption (n8n Cloud).
- Exported n8n workflows only reference credentials by `id` and `name`; however, you should still audit `parameters` (such as `chatId`, `person`, custom URLs, or `pinData`) before committing any export.

---

## 3. Repository `.gitignore` Policy

The repository `.gitignore` blocks accidental commits of:

- `.env` and `.env.*` (while allowing `!.env.example` if needed)
- `credentials.json`, `secrets.json`, `*.pem`, `*.key`
- `workflows/*.local.json` and `*original*.json`
- `node_modules/`, `.DS_Store`, `*.log`

---

## 4. Principle of Least Privilege

- **LinkedIn OAuth2:** Request only `w_member_social`, `openid`, and `profile`—avoid organization/admin scopes unless posting to a Company Page.
- **Telegram Bot:** Only grant the bot access to send messages to your designated `chatId`; do not add the bot to unrelated groups.
- **Testing:** Always test with `visibility: "CONNECTIONS"` or with the `LinkedIn` node disabled before enabling `PUBLIC` scheduled posting.
