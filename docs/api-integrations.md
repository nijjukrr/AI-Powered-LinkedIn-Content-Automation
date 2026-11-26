# API Integrations

This document details every external API integrated into the workflow, how n8n authenticates with each service, and the exact parameters used.

---

## 1. OpenAI Chat API (via LangChain Nodes)

- **n8n Node Type:** `@n8n/n8n-nodes-langchain.lmChatOpenAi` (`v1.3`)
- **Credential Type:** `openAiApi` (configured with `__aiGatewayManaged: true` in the original export)
- **Instances in Workflow:**
  1. `OpenAI Chat Model` -> Model: `gpt-5.6-luna` (backs `Content topic generator2`)
  2. `OpenAI Chat Model1` -> Model: `gpt-5.6-luna` (backs `Content creator`)
  3. `OpenAI Chat Model2` -> Model: `gpt-5.4` (backs `Hashtag generator /SEO`)
- **Role:** Powers topic ideation, LinkedIn copywriting, and SEO hashtag generation. Each model is paired with a `Structured Output Parser` (`v1.2`) so responses conform to JSON schemas.
- **Portability Note:** If you import this workflow into a self-hosted n8n instance without n8n AI Gateway credits, attach a standard OpenAI API key and update the model selector to your available models.

---

## 2. Google Gemini API (Image Generation)

- **n8n Node Type:** `@n8n/n8n-nodes-langchain.googleGemini` (`v1.2`)
- **Credential Type:** `googlePalmApi` (configured with `"name": "Gateway credits"`, `__aiGatewayManaged: true` in the original export)
- **Configuration:**
  - `resource`: `"image"`
  - `modelId`: `"models/gemini-3.1-flash-image"` (`Nano Banana 2`)
  - `prompt`: `=Generate an image for a linkedin post this is the description: {{ $json.output['image description'] }} .The images should be realistic for linkedin.`
- **Role:** Converts the `image description` produced by `Content creator` into a binary image file attached to the n8n item.

---

## 3. LinkedIn API (OAuth 2.0)

- **n8n Node Type:** `n8n-nodes-base.linkedIn` (`v1`)
- **Credential Type:** `linkedInOAuth2Api`
- **Configuration:**
  - `person`: `YOUR_LINKEDIN_PERSON_ID` (personal profile URN/ID)
  - `shareMediaCategory`: `"IMAGE"`
  - `additionalFields.visibility`: `"PUBLIC"`
  - `additionalFields.title`: `={{ $('Content creator').item.json.output['post title'] }}`
  - `text`: Expression that strips any `#` lines from `post content` and appends deduplicated hashtags from `$json.output.Hashtags`.
- **Required LinkedIn App Products / Scopes:**
  - **Share on LinkedIn** (`w_member_social`)
  - **Sign In with LinkedIn using OpenID Connect** (`openid`, `profile`)
- **Output:** Returns the created post metadata, including `$json.urn` (used by Telegram to build the direct post URL).

---

## 4. Telegram Bot API

- **n8n Node Type:** `n8n-nodes-base.telegram` (`v1.2`)
- **Credential Type:** `telegramApi`
- **Configuration:**
  - `chatId`: `YOUR_TELEGRAM_CHAT_ID`
  - `additionalFields.parse_mode`: `"HTML"`
  - `additionalFields.appendAttribution`: `false`
  - `text`: HTML-escaped post title, `https://www.linkedin.com/feed/update/<urn>`, and `Asia/Calcutta` (IST) timestamp.
- **Role:** Provides real-time mobile/desktop delivery confirmation after each scheduled LinkedIn post.
