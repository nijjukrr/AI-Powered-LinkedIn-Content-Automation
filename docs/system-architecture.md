# System Architecture

This document describes the technical architecture of **AI-Powered LinkedIn Content Automation** as implemented in [`workflows/linkedin_content_automation.json`](../workflows/linkedin_content_automation.json), and clearly separates **implemented components** from **proposed enhancements**.

---

## High-Level Architecture Diagram

```mermaid
flowchart TB
    subgraph Input["1. Input & Trigger Layer"]
        ST["Schedule Trigger<br/>(n8n-nodes-base.scheduleTrigger v1.2)<br/>Interval: Every 8 hours"]
    end

    subgraph Ideation["2. AI Ideation Layer"]
        CTG["Content topic generator2<br/>(@n8n/n8n-nodes-langchain.agent v3.1)<br/>10-Theme Randomizer"]
        OAI0["OpenAI Chat Model<br/>(gpt-5.6-luna)"] -.->|"ai_languageModel"| CTG
        SOP0["Structured Output Parser<br/>([{title, rationale, hook}])"] -.->|"ai_outputParser"| CTG
    end

    subgraph Copywriting["3. AI Content Generation Layer"]
        CC["Content creator<br/>(@n8n/n8n-nodes-langchain.chainLlm v1.7)<br/>Reads $json.output[0]"]
        OAI1["OpenAI Chat Model1<br/>(gpt-5.6-luna)"] -.->|"ai_languageModel"| CC
        SOP1["Structured Output Parser1<br/>({post title, post content, image description})"] -.->|"ai_outputParser"| CC
    end

    subgraph ParallelAssets["4. Parallel Asset Generation"]
        subgraph ImageLayer["4a. Image Generation Layer"]
            GIG["Gemini Image Generator<br/>(googleGemini v1.2)<br/>models/gemini-3.1-flash-image<br/>(retryOnFail: 2 tries)"]
        end
        subgraph SEOLayer["4b. SEO Optimization Layer"]
            HG["Hashtag generator /SEO<br/>(@n8n/n8n-nodes-langchain.agent v3.1)"]
            OAI2["OpenAI Chat Model2<br/>(gpt-5.4)"] -.->|"ai_languageModel"| HG
            SOP2["Structured Output Parser2<br/>({Hashtags: [...]})"] -.->|"ai_outputParser"| HG
        end
    end

    subgraph Merging["5. Data Merging & Validation Layer"]
        MRG["Merge<br/>(n8n-nodes-base.merge v3.2)<br/>Mode: combine / combineByPosition"]
        VAL["Validate &amp; Format Post<br/>(n8n-nodes-base.code v2)<br/>Body, Binary &amp; Hashtag Guard"]
    end

    subgraph Publishing["6. Publishing & Alerting Layer"]
        LI["LinkedIn<br/>(n8n-nodes-base.linkedIn v1)<br/>shareMediaCategory: IMAGE, CONNECTIONS<br/>(retryOnFail: false)"]
        TG["Notify on Telegram<br/>(n8n-nodes-base.telegram v1.2)<br/>HTML Alert + IST Timestamp"]
    end

    ST --> CTG
    CTG --> CC
    CC --> GIG
    CC --> HG
    GIG -->|"index 0"| MRG
    HG -->|"index 1"| MRG
    MRG --> VAL
    VAL --> LI
    LI --> TG
```

---

## Architectural Layers (Implemented)

### 1. Input Layer
- **Component:** `Schedule Trigger` (`n8n-nodes-base.scheduleTrigger` v1.2).
- **Behavior:** Configured to fire every 8 hours (`hoursInterval: 8`) when activated. Default workflow export is inactive (`active: false`) for safe credential setup and verification.
- **Note:** Currently, dynamic context comes from `$now` and an inline 10-theme array evaluated at runtime.

### 2. Processing & Ideation Layer
- **Component:** `Content topic generator2` (`@n8n/n8n-nodes-langchain.agent` v3.1) + `OpenAI Chat Model` (`gpt-5.6-luna`) + `Structured Output Parser`.
- **Behavior:** Selects one of 10 student/fresher career themes and instructs the agent to return a structured JSON array (`[{ title, rationale, hook }]`) where the first topic corresponds to the chosen theme.

### 3. AI Content Generation Layer
- **Component:** `Content creator` (`@n8n/n8n-nodes-langchain.chainLlm` v1.7) + `OpenAI Chat Model1` (`gpt-5.6-luna`) + `Structured Output Parser1`.
- **Behavior:** Consumes `$json.output[0]` from the topic generator and generates a full LinkedIn post with strong opening hook, actionable insights, and readable formatting. Explicitly forbids inline hashtags in `post content` and outputs an `image description`.

### 4. Image Generation Layer (Parallel Branch A)
- **Component:** `Gemini Image Generator` (`@n8n/n8n-nodes-langchain.googleGemini` v1.2).
- **Behavior:** Receives `image description` and calls `models/gemini-3.1-flash-image` (`Nano Banana 2`) with `resource: "image"`. Configured with `retryOnFail: true` (`maxTries: 2`, `waitBetweenTries: 3000`) for resilience against transient rate-limit or network errors. Stores generated image in the item's binary data (`settings.binaryMode: "separate"`).

### 5. SEO Optimization Layer (Parallel Branch B)
- **Component:** `Hashtag generator /SEO` (`@n8n/n8n-nodes-langchain.agent` v3.1) + `OpenAI Chat Model2` (`gpt-5.4`) + `Structured Output Parser2`.
- **Behavior:** Generates 3–5 broad industry hashtags, 3–5 niche hashtags, and 1–2 topical hashtags based on the post title and body to maximize discoverability (without claiming real-time trend retrieval). Output is enforced to `{ "Hashtags": [...] }`.

### 6. Data Merging & Validation Layer
- **Components:** `Merge` (`n8n-nodes-base.merge` v3.2) -> `Validate & Format Post` (`n8n-nodes-base.code` v2).
- **Behavior:**
  - `Merge` combines Branch A (image binary on index 0) and Branch B (hashtags JSON on index 1) by position (`combineByPosition`).
  - `Validate & Format Post` enforces that exactly 1 merged item exists, verifies non-empty `post title` and `post content`, verifies binary image integrity, strips stray `#` lines from body copy, normalizes hashtags, and guarantees `binary.data` is provided to downstream nodes.

### 7. Publishing & Notification Layer
- **Components:** `LinkedIn` (`n8n-nodes-base.linkedIn` v1) -> `Notify on Telegram` (`n8n-nodes-base.telegram` v1.2).
- **Behavior:**
  - `LinkedIn` publishes the validated `formattedText` and `formattedTitle` along with the attached image (`binaryPropertyName: "data"`). Defaults to `visibility: "CONNECTIONS"` for safe testing. `retryOnFail: false` prevents accidental duplicate posts on ambiguous timeouts.
  - `Notify on Telegram` formats an HTML alert. If a valid LinkedIn `urn` is returned, it provides a direct clickable link (`https://www.linkedin.com/feed/update/<urn>`); if no URN is returned, it sends an explicit warning to check profile and logs before retrying.

---

## Implemented vs. Proposed Enhancements

| Capability | Current Status | Notes |
| :--- | :--- | :--- |
| Scheduled execution (8h) | **Implemented** | `Schedule Trigger` (defaults to `active: false`) |
| 10-theme student/career ideation | **Implemented** | `Content topic generator2` |
| Structured JSON parsing (3 stages) | **Implemented** | `Structured Output Parser` 0, 1, 2 |
| Parallel Gemini image + SEO hashtags | **Implemented** | `Gemini Image Generator` & `Hashtag generator /SEO` |
| Pre-publish validation & binary check | **Implemented** | `Validate & Format Post` (Code node v2) |
| Bounded retries on image generation | **Implemented** | `Gemini Image Generator` (`retryOnFail: true`, 2 tries) |
| Idempotent publishing policy | **Implemented** | `LinkedIn` (`retryOnFail: false`, `CONNECTIONS` default) |
| Telegram post-publish alert | **Implemented** | `Notify on Telegram` (URN-checked HTML alert) |
| Human-in-the-loop approval gate | **Proposed** | See [`future-enhancements.md`](future-enhancements.md) |
| Duplicate-topic memory / DB | **Proposed** | Not yet implemented |
| Centralized Error Trigger workflow | **Proposed** | Not yet implemented |
| Post analytics & multi-platform publishing | **Proposed** | Not yet implemented |
