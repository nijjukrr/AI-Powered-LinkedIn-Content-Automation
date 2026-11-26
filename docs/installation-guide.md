# Installation & Setup Guide

This guide walks a developer from cloning the repository to importing, configuring, testing, and activating the n8n workflow.

---

## Prerequisites

- **n8n** (v1.x+ with `@n8n/n8n-nodes-langchain` support — included in modern n8n Cloud and official Docker images)
- **OpenAI API account** (or n8n AI Gateway credits)
- **Google Gemini API key** (Google AI Studio / `googlePalmApi` credential in n8n)
- **LinkedIn Developer App** with OAuth 2.0 credentials
- **Telegram Bot** created via `@BotFather` + your personal Telegram `chatId`

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/nijjukrr/AI-Powered-LinkedIn-Content-Automation.git
cd AI-Powered-LinkedIn-Content-Automation
```

---

## Step 2: Start n8n (If Self-Hosting)

### Option A: Docker (Recommended for Local Reproducibility)

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

### Option B: Node.js / npx

```bash
npx n8n
```

Open your browser to `http://localhost:5678`.

---

## Step 3: Import the Workflow

1. In n8n, click **+ Add workflow**.
2. Click the **⋮** menu (top right) -> **Import from File...**.
3. Choose [`workflows/linkedin_content_automation.json`](../workflows/linkedin_content_automation.json).
4. Save the workflow immediately.

---

## Step 4: Configure Credentials & Placeholders

1. **OpenAI Chat Models (`OpenAI Chat Model`, `OpenAI Chat Model1`, `OpenAI Chat Model2`):**
   - Create an **OpenAI API** credential in n8n and attach it to all three OpenAI Chat Model nodes.
   - If your account does not have access to `gpt-5.6-luna` or `gpt-5.4` (used in the original AI Gateway export), select an available chat model such as `gpt-4o` or `gpt-4o-mini`.
2. **Google Gemini (`Gemini Image Generator`):**
   - Create a **Google Gemini (PaLM) API** (`googlePalmApi`) credential with your Google AI Studio API key.
   - Verify `models/gemini-3.1-flash-image` is available for your key, or select an available Gemini image generation model.
3. **LinkedIn (`LinkedIn`):**
   - Create a **LinkedIn OAuth2 API** credential (`linkedInOAuth2Api`) and complete the OAuth consent flow.
   - In the `LinkedIn` node, replace `YOUR_LINKEDIN_PERSON_ID` with your LinkedIn profile selection.
4. **Telegram (`Notify on Telegram`):**
   - Create a **Telegram API** credential (`telegramApi`) using your `@BotFather` bot token.
   - Replace `YOUR_TELEGRAM_CHAT_ID` with your numeric Telegram chat ID (obtainable via `@userinfobot` or `getUpdates`).

---

## Step 5: Testing Checklist (Safe Dry Run)

The imported workflow is **inactive (`active: false`)** and sets LinkedIn visibility to **`CONNECTIONS`** by default so you never publish test posts publicly by accident.

1. **Run Offline Automated Tests Locally:**
   ```bash
   python -m unittest discover -s tests -v
   ```
2. **Disable `LinkedIn` Temporarily** (optional for initial dry runs) and click **Execute Workflow** manually in n8n.
3. Inspect each node's output in the n8n execution panel:
   - `Content topic generator2`: Verify `output` is an array of objects with `title`, `rationale`, `hook`.
   - `Content creator`: Verify `output` has `post title`, `post content` (no `#hashtags`), and `image description`.
   - `Gemini Image Generator`: Verify a binary image file is produced.
   - `Hashtag generator /SEO`: Verify `output.Hashtags` is a non-empty array of `#` tags.
   - `Merge`: Verify 1 item containing both binary image data and JSON `output.Hashtags`.
4. Reconnect `LinkedIn`, run one controlled test, and verify both the LinkedIn post and the `Notify on Telegram` message.
5. Toggle the workflow **Active** only after verifying end-to-end execution.

---

## Common Troubleshooting

| Symptom | Likely Cause | Fix |
| :--- | :--- | :--- |
| `Model not found` on OpenAI nodes | `gpt-5.6-luna` / `gpt-5.4` requires n8n AI Gateway or specific tier | Switch the model dropdown to an available model on your OpenAI key |
| `LinkedIn` fails with 401/403 | Expired OAuth token or missing `w_member_social` scope | Re-authorize the LinkedIn OAuth2 credential in n8n |
| `LinkedIn` posts text without image | Binary data missing from `Gemini Image Generator` | Check `Merge` inputs (`index 0` must be Gemini, `index 1` must be Hashtags) |
| `Telegram` fails with `chat not found` | Incorrect `chatId` or user hasn't started the bot | Send `/start` to your bot in Telegram and verify the numeric `chatId` |
