# API Integrations

This document details every external API integrated into the 15-node workflow, authentication methods, parameter mappings, and model availability notes.

---

## 1. OpenAI Chat API (via LangChain Nodes)

- **n8n Node Type:** `@n8n/n8n-nodes-langchain.lmChatOpenAi` (`v1.3`)
- **Credential Type:** `openAiApi` (configured with `__aiGatewayManaged: true` in the original export)
- **Instances in Workflow:**
  1. `OpenAI Chat Model` -> Model: `gpt-5.6-luna` (backs `Content topic generator2`)
  2. `OpenAI Chat Model1` -> Model: `gpt-5.6-luna` (backs `Content creator`)
  3. `OpenAI Chat Model2` -> Model: `gpt-5.4` (backs `Hashtag generator /SEO`)
- **Role:** Powers topic ideation, LinkedIn copywriting, and SEO hashtag generation. Each model is paired with a `Structured Output Parser` (`v1.2`) so responses conform strictly to JSON schemas.
- **Model Identifier vs. Standard API Note:** The original workflow export uses n8n AI Gateway model identifiers (`gpt-5.6-luna`, `gpt-5.4`). These are gateway-managed routing labels. When self-hosting n8n or using standard direct OpenAI API keys, select your available chat model (such as `gpt-4o` or `gpt-4o-mini`) from the model dropdown.

---

## 2. Google Gemini API (Image Generation)

- **n8n Node Type:** `@n8n/n8n-nodes-langchain.googleGemini` (`v1.2`)
- **Credential Type:** `googlePalmApi` (Google AI Studio API key)
- **Configuration:**
  - `resource`: `"image"`
  - `modelId`: `"models/gemini-3.1-flash-image"` (`Nano Banana 2`)
  - `prompt`: `=Generate an image for a linkedin post this is the description: {{ $json.output['image description'] }} .The images should be realistic for linkedin.`
  - `retryOnFail`: `true` (`maxTries: 2`, `waitBetweenTries: 3000`)
- **Role:** Converts the `image description` produced by `Content creator` into a binary image attached to the n8n execution item under `binary.data`.

---

## 3. LinkedIn API (OAuth 2.0)

- **n8n Node Type:** `n8n-nodes-base.linkedIn` (`v1`)
- **Credential Type:** `linkedInOAuth2Api`
- **Configuration:**
  - `person`: `YOUR_LINKEDIN_PERSON_ID` (personal profile URN/ID)
  - `shareMediaCategory`: `"IMAGE"`
  - `binaryPropertyName`: `"data"`
  - `additionalFields.visibility`: `"CONNECTIONS"` (safe initial testing default; switch to `PUBLIC` only after verification)
  - `additionalFields.title`: `={{ $json.formattedTitle }}`
  - `text`: `={{ $json.formattedText }}` (received directly from the `Validate & Format Post` Code node)
  - `retryOnFail`: `false` (explicitly prevents duplicate posts if a network request times out after post creation)
- **Required LinkedIn App Products / Scopes:**
  - **Share on LinkedIn** (`w_member_social`)
  - **Sign In with LinkedIn using OpenID Connect** (`openid`, `profile`)
- **Output:** Returns the created post metadata, including `$json.urn` (used by Telegram to build the live post URL).

---

## 4. Telegram Bot API

- **n8n Node Type:** `n8n-nodes-base.telegram` (`v1.2`)
- **Credential Type:** `telegramApi`
- **Configuration:**
  - `chatId`: `YOUR_TELEGRAM_CHAT_ID`
  - `additionalFields.parse_mode`: `"HTML"`
  - `additionalFields.appendAttribution`: `false`
  - `text`: Conditionally checks `$json.urn`. If present, delivers an HTML-escaped post title, live URL (`https://www.linkedin.com/feed/update/<urn>`), and IST timestamp. If missing, sends an explicit warning to inspect LinkedIn profile and n8n execution logs before retrying.
- **Role:** Provides real-time mobile/desktop delivery confirmation and failure alerts after each LinkedIn publishing attempt.
