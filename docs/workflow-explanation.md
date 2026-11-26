# Workflow Explanation & Node-by-Node Deep Dive

This document provides an engineering-level breakdown of all **15 nodes** in [`workflows/linkedin_content_automation.json`](../workflows/linkedin_content_automation.json), including internal data flow, structured output contracts, parallel execution, validation, and expression logic.

---

## Workflow Settings & Metadata

- **Execution Order:** `v1` (modern n8n branch execution order)
- **Binary Mode:** `separate` (binary attachments such as the Gemini-generated image are stored separately from JSON metadata)
- **Node Groups:**
  1. **Plan post topic:** `Content topic generator2`, `OpenAI Chat Model`, `Structured Output Parser`
  2. **Create post assets:** `Content creator`, `OpenAI Chat Model1`, `Structured Output Parser1`, `Gemini Image Generator`, `Hashtag generator /SEO`, `OpenAI Chat Model2`, `Structured Output Parser2`, `Merge`
  3. **Publish and alert me:** `LinkedIn`, `Notify on Telegram`

---

## Node-by-Node Specification

### 1. `Schedule Trigger`
- **Type:** `n8n-nodes-base.scheduleTrigger` (`v1.2`)
- **Purpose:** Initiates the automation on a fixed cadence.
- **Input Data:** None (trigger node).
- **Processing:** Configured with `rule.interval[0]` set to `field: "hours"`, `hoursInterval: 8`.
- **Output Data:** Emits an item containing execution timestamp metadata.
- **Next Node:** `Content topic generator2` (`main` index 0).

---

### 2. `Content topic generator2`
- **Type:** `@n8n/n8n-nodes-langchain.agent` (`v3.1`)
- **Purpose:** Acts as a Content Researcher for college students and fresh graduates.
- **Input Data:** Trigger item from `Schedule Trigger`.
- **Processing:**
  - Evaluates `{{ $now.toFormat("yyyy-MM-dd HH:mm") }}` for current date context.
  - Evaluates a JavaScript array of 10 career/student themes using `Math.floor(Math.random() * 10)` to inject `TODAY'S FOCUS THEME`.
  - Applies a system prompt instructing the agent to act like a relatable senior/mentor and ensure the **first** topic matches `TODAY'S FOCUS THEME`.
  - Delegates LLM inference to `OpenAI Chat Model` and schema enforcement to `Structured Output Parser`.
- **Output Data:** JSON object with `output` array: `[{ title, rationale, hook }]`.
- **Next Node:** `Content creator` (`main` index 0).

---

### 3. `OpenAI Chat Model`
- **Type:** `@n8n/n8n-nodes-langchain.lmChatOpenAi` (`v1.3`)
- **Purpose:** Provides LLM inference for `Content topic generator2`.
- **Configuration:** Model `gpt-5.6-luna` (AI Gateway managed in the original export).
- **Connection:** `ai_languageModel` -> `Content topic generator2`.

---

### 4. `Structured Output Parser`
- **Type:** `@n8n/n8n-nodes-langchain.outputParserStructured` (`v1.2`)
- **Purpose:** Constrains `Content topic generator2` to return valid JSON matching an array of `{ title, rationale, hook }` objects.
- **Connection:** `ai_outputParser` -> `Content topic generator2`.

---

### 5. `Content creator`
- **Type:** `@n8n/n8n-nodes-langchain.chainLlm` (`v1.7`)
- **Purpose:** Expands the top-ranked topic into a full LinkedIn post and an image description.
- **Input Data:** `$json.output[0].title`, `$json.output[0].rationale`, and `$json.output[0].hook` from `Content topic generator2`.
- **Processing:**
  - Uses a `chainLlm` (lighter than an `agent` since no external tools are needed—pure text transformation).
  - Explicitly instructs: *"Do NOT include any hashtags in the post content; hashtags are added separately. Also describe a suitable image for the post."*
- **Output Data:** JSON object under `output`:
  ```json
  {
    "post title": "...",
    "post content": "...",
    "image description": "..."
  }
  ```
- **Next Nodes (Parallel Fan-Out):**
  - `Gemini Image Generator` (`main` index 0)
  - `Hashtag generator /SEO` (`main` index 0)

---

### 6. `OpenAI Chat Model1`
- **Type:** `@n8n/n8n-nodes-langchain.lmChatOpenAi` (`v1.3`)
- **Purpose:** Provides LLM inference (`gpt-5.6-luna`) for `Content creator`.
- **Connection:** `ai_languageModel` -> `Content creator`.

---

### 7. `Structured Output Parser1`
- **Type:** `@n8n/n8n-nodes-langchain.outputParserStructured` (`v1.2`)
- **Purpose:** Enforces `{ "post title", "post content", "image description" }` schema on `Content creator`.
- **Connection:** `ai_outputParser` -> `Content creator`.

---

### 8. `Gemini Image Generator`
- **Type:** `@n8n/n8n-nodes-langchain.googleGemini` (`v1.2`)
- **Purpose:** Generates a realistic visual asset for the LinkedIn post.
- **Input Data:** `$json.output['image description']` from `Content creator`.
- **Processing:** Calls `models/gemini-3.1-flash-image` (`Nano Banana 2`) with `resource: "image"` and prompt:
  `Generate an image for a linkedin post this is the description: {{ $json.output['image description'] }} .The images should be realistic for linkedin.`
- **Output Data:** Item containing binary image data (stored in n8n's `binary` property).
- **Next Node:** `Merge` (`main` input `index 0`).

---

### 9. `Hashtag generator /SEO`
- **Type:** `@n8n/n8n-nodes-langchain.agent` (`v3.1`)
- **Purpose:** Acts as a LinkedIn SEO Specialist to generate relevant hashtags.
- **Input Data:** `$json.output['post title']` and `$json.output['post content']` from `Content creator`.
- **Processing:** Requests 3–5 broad hashtags, 3–5 niche hashtags, and 1–2 trending hashtags.
- **Output Data:** JSON object under `output` including `"Hashtags": ["#...", "#..."]`.
- **Next Node:** `Merge` (`main` input `index 1`).

---

### 10. `OpenAI Chat Model2`
- **Type:** `@n8n/n8n-nodes-langchain.lmChatOpenAi` (`v1.3`)
- **Purpose:** Provides LLM inference (`gpt-5.4`) for `Hashtag generator /SEO`.
- **Connection:** `ai_languageModel` -> `Hashtag generator /SEO`.

---

### 11. `Structured Output Parser2`
- **Type:** `@n8n/n8n-nodes-langchain.outputParserStructured` (`v1.2`)
- **Purpose:** Enforces `{ "Hashtags": ["#...", "#..."] }` JSON structure without unrelated post fields.
- **Connection:** `ai_outputParser` -> `Hashtag generator /SEO`.

---

### 12. `Merge`
- **Type:** `n8n-nodes-base.merge` (`v3.2`)
- **Purpose:** Synchronizes the parallel image and hashtag branches before validation.
- **Input Data:**
  - Input `0`: Image binary item from `Gemini Image Generator` (`binary.data`).
  - Input `1`: Hashtags JSON item from `Hashtag generator /SEO`.
- **Processing:** Configured with `mode: "combine"` and `combineBy: "combineByPosition"`. n8n waits until both branches complete, then merges item 0 from Input 0 with item 0 from Input 1.
- **Output Data:** Single combined item containing both `binary.data` and `json.output.Hashtags`.
- **Next Node:** `Validate & Format Post` (`main` index 0).

---

### 13. `Validate & Format Post`
- **Type:** `n8n-nodes-base.code` (`v2`)
- **Purpose:** Acts as a deterministic pre-publish quality and binary-integrity gate.
- **Input Data:** Merged item from `Merge` + cross-node reference to `$('Content creator').item.json.output`.
- **Processing:**
  - Verifies `post title` and `post content` are non-empty strings (throws an explicit error if missing).
  - Verifies `$binary && $binary.data` exists from `Gemini Image Generator` (prevents calling `LinkedIn` without an image).
  - Strips any accidental `#` lines from `post content`.
  - Normalizes `Hashtags`: strips invalid characters, ensures `#` prefix, removes empty tokens, and deduplicates case-insensitively.
- **Output Data:** `{ formattedTitle, formattedText, normalizedHashtags }` + preserved `binary`.
- **Next Node:** `LinkedIn` (`main` index 0).

---

### 14. `LinkedIn`
- **Type:** `n8n-nodes-base.linkedIn` (`v1`)
- **Purpose:** Publishes the validated post and image to a personal LinkedIn profile.
- **Input Data:** Validated item from `Validate & Format Post`.
- **Processing:**
  - Uses `={{ $json.formattedText }}` and `={{ $json.formattedTitle }}`.
  - **Media:** `shareMediaCategory: "IMAGE"` with `binaryPropertyName: "data"`.
  - **Visibility:** Defaults to `CONNECTIONS` for safe initial testing (switch to `PUBLIC` only after manual verification).
  - **Retry Policy:** `retryOnFail: false` to prevent duplicate posts on ambiguous network timeouts.
- **Output Data:** LinkedIn API response including `urn` (the published post URN).
- **Next Node:** `Notify on Telegram` (`main` index 0).

---

### 15. `Notify on Telegram`
- **Type:** `n8n-nodes-base.telegram` (`v1.2`)
- **Purpose:** Sends an immediate confirmation alert (or missing-URN warning) to the workflow owner.
- **Input Data:** LinkedIn response (`$json.urn`) + `$('Validate & Format Post').item.json.formattedTitle`.
- **Processing:**
  - Checks `$json.urn`: only reports a published post and `https://www.linkedin.com/feed/update/<urn>` when `urn` is present; otherwise sends a warning to check LinkedIn/logs before retrying.
  - Escapes `&`, `<`, `>` in `formattedTitle` for safe `HTML` parsing.
  - Formats `$now.setZone('Asia/Calcutta').toFormat('dd MMM yyyy, HH:mm')` IST.
- **Output Data:** Telegram `sendMessage` API response.

---

## Why Structured Output Parsers Matter Here

Without `Structured Output Parser` nodes, LLMs frequently wrap JSON in markdown fences (` ```json ... ``` `) or add conversational preambles, which breaks downstream expressions like `$json.output[0].title` or `$json.output.Hashtags`. By attaching `outputParserStructured` to each LangChain node, n8n injects schema instructions and parses the response into a guaranteed JSON object under `$json.output`.
