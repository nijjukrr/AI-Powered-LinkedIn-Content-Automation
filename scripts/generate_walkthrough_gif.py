"""Generates an animated walkthrough GIF demonstrating how the 15-node workflow executes.
Saves to assets/demo/workflow-walkthrough.gif for embedding in GitHub README.
"""

import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 960
HEIGHT = 540

# Color palette (Modern Developer Dark Theme)
BG_COLOR = (15, 23, 42)          # slate-900
SURFACE_COLOR = (30, 41, 59)     # slate-800
BORDER_COLOR = (51, 65, 85)      # slate-700
ACCENT_BLUE = (59, 130, 246)     # blue-500
ACCENT_GREEN = (34, 197, 94)     # green-500
ACCENT_PURPLE = (168, 85, 247)   # purple-500
ACCENT_CYAN = (6, 182, 212)      # cyan-500
ACCENT_YELLOW = (234, 179, 8)    # yellow-500
TEXT_MAIN = (248, 250, 252)      # slate-50
TEXT_MUTED = (148, 163, 184)     # slate-400
TEXT_CODE = (226, 232, 240)      # slate-200

# Fonts
WIN_FONTS = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
try:
    FONT_TITLE = ImageFont.truetype(os.path.join(WIN_FONTS, "segoeui.ttf"), 18)
    FONT_BOLD = ImageFont.truetype(os.path.join(WIN_FONTS, "segoeuib.ttf"), 15)
    FONT_SUBTITLE = ImageFont.truetype(os.path.join(WIN_FONTS, "segoeui.ttf"), 13)
    FONT_SMALL = ImageFont.truetype(os.path.join(WIN_FONTS, "segoeui.ttf"), 11)
    FONT_CODE = ImageFont.truetype(os.path.join(WIN_FONTS, "consola.ttf"), 12)
    FONT_CODE_BOLD = ImageFont.truetype(os.path.join(WIN_FONTS, "consolab.ttf"), 13)
except Exception:
    FONT_TITLE = FONT_BOLD = FONT_SUBTITLE = FONT_SMALL = FONT_CODE = FONT_CODE_BOLD = ImageFont.load_default()


def create_base_canvas(active_step_idx=0):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Top window bar
    draw.rectangle([(0, 0), (WIDTH, 42)], fill=(10, 15, 30))
    draw.line([(0, 42), (WIDTH, 42)], fill=BORDER_COLOR, width=1)

    # Window dots
    draw.ellipse([(16, 16), (26, 26)], fill=(239, 68, 68))
    draw.ellipse([(34, 16), (44, 26)], fill=(245, 158, 11))
    draw.ellipse([(52, 16), (62, 26)], fill=(34, 197, 94))

    # Window title
    draw.text((76, 12), "AI-Powered LinkedIn Content Automation — Execution Walkthrough", font=FONT_TITLE, fill=TEXT_MAIN)

    # Status Pill
    draw.rounded_rectangle([(WIDTH - 150, 10), (WIDTH - 16, 32)], radius=11, fill=(22, 101, 52))
    draw.text((WIDTH - 138, 14), "● 15 NODES ACTIVE", font=FONT_SMALL, fill=(187, 247, 208))

    # Stepper bar
    steps = [
        "1. Trigger",
        "2. Topic AI",
        "3. Copywriter",
        "4. Parallel Assets",
        "5. Validation",
        "6. LinkedIn",
        "7. Telegram"
    ]
    step_w = (WIDTH - 32) / len(steps)
    for i, step in enumerate(steps):
        x1 = 16 + i * step_w
        x2 = x1 + step_w - 6
        is_active = (i == active_step_idx)
        is_done = (i < active_step_idx)

        bg = (30, 58, 138) if is_active else ((20, 83, 45) if is_done else (30, 41, 59))
        border = ACCENT_BLUE if is_active else (ACCENT_GREEN if is_done else BORDER_COLOR)
        text_col = TEXT_MAIN if (is_active or is_done) else TEXT_MUTED

        draw.rounded_rectangle([(x1, 52), (x2, 80)], radius=6, fill=bg, outline=border, width=1)
        prefix = "✔ " if is_done else ("▶ " if is_active else "○ ")
        draw.text((x1 + 8, 58), prefix + step, font=FONT_SUBTITLE, fill=text_col)

    return img, draw


def render_scene_1():
    """Scene 1: Trigger & Content Topic Generator."""
    img, draw = create_base_canvas(active_step_idx=0)

    # Main Card
    draw.rounded_rectangle([(16, 96), (WIDTH - 16, HEIGHT - 16)], radius=10, fill=SURFACE_COLOR, outline=BORDER_COLOR)

    # Header badge
    draw.rounded_rectangle([(32, 112), (340, 142)], radius=6, fill=(59, 130, 246, 40), outline=ACCENT_BLUE)
    draw.text((42, 118), "STAGE 1 & 2: SCHEDULE TRIGGER & TOPIC AI", font=FONT_BOLD, fill=ACCENT_BLUE)

    # Trigger Info
    draw.rounded_rectangle([(32, 156), (300, 240)], radius=8, fill=(15, 23, 42), outline=BORDER_COLOR)
    draw.text((46, 170), "Schedule Trigger (v1.2)", font=FONT_BOLD, fill=ACCENT_GREEN)
    draw.text((46, 192), "• Interval: Every 8 Hours", font=FONT_SUBTITLE, fill=TEXT_MUTED)
    draw.text((46, 212), "• Cadence: 00:00, 08:00, 16:00 IST", font=FONT_SUBTITLE, fill=TEXT_MUTED)

    # Arrow
    draw.text((320, 190), "──────▶", font=FONT_BOLD, fill=ACCENT_BLUE)

    # Agent Card
    draw.rounded_rectangle([(400, 156), (WIDTH - 32, 240)], radius=8, fill=(15, 23, 42), outline=ACCENT_BLUE)
    draw.text((414, 168), "Content topic generator2 (@n8n/n8n-nodes-langchain.agent v3.1)", font=FONT_BOLD, fill=TEXT_MAIN)
    draw.text((414, 190), "• LLM: OpenAI Chat Model (gpt-5.6-luna)", font=FONT_SUBTITLE, fill=ACCENT_CYAN)
    draw.text((414, 212), "• Parser: Structured Output Parser (Topic Array Schema)", font=FONT_SUBTITLE, fill=ACCENT_PURPLE)

    # JSON Preview Card
    draw.rounded_rectangle([(32, 256), (WIDTH - 32, HEIGHT - 32)], radius=8, fill=(10, 15, 30), outline=BORDER_COLOR)
    draw.text((46, 268), "Structured Output: $json.output[0] (Schema Enforced)", font=FONT_CODE_BOLD, fill=ACCENT_YELLOW)

    code_lines = [
        '{',
        '  "title": "Why Building One Real Project Beats Five Tutorial Clones",',
        '  "theme": "Landing internships as a student (strategies most students miss)",',
        '  "rationale": "Recruiters see hundreds of identical to-do lists. Showing one deployed,',
        '               well-documented project demonstrates ownership and engineering judgment.",',
        '  "hook": "Stop adding tutorial clones to your GitHub. One messy project you actually debugged',
        '          will outscore ten polished copy-paste repos in an internship interview."',
        '}'
    ]
    y = 296
    for line in code_lines:
        draw.text((46, y), line, font=FONT_CODE, fill=TEXT_CODE)
        y += 20

    return img


def render_scene_2():
    """Scene 2: Content Creator (Drafting Copy & Image Prompt)."""
    img, draw = create_base_canvas(active_step_idx=2)

    draw.rounded_rectangle([(16, 96), (WIDTH - 16, HEIGHT - 16)], radius=10, fill=SURFACE_COLOR, outline=BORDER_COLOR)

    # Header badge
    draw.rounded_rectangle([(32, 112), (320, 142)], radius=6, fill=(168, 85, 247, 40), outline=ACCENT_PURPLE)
    draw.text((42, 118), "STAGE 3: CONTENT CREATOR (LLM CHAIN)", font=FONT_BOLD, fill=ACCENT_PURPLE)

    draw.text((340, 120), "Node: Content creator (chainLlm v1.7) | Model: gpt-5.6-luna", font=FONT_SUBTITLE, fill=TEXT_MUTED)

    # Post copy box
    draw.rounded_rectangle([(32, 156), (560, HEIGHT - 32)], radius=8, fill=(10, 15, 30), outline=BORDER_COLOR)
    draw.text((46, 168), "Drafted LinkedIn Post Copy ($json.output['post content'])", font=FONT_CODE_BOLD, fill=ACCENT_CYAN)

    post_lines = [
        "Stop adding tutorial clones to your GitHub.",
        "",
        "When recruiters scan student portfolios, they recognize standard",
        "tutorial projects in seconds.",
        "",
        "What actually stands out in an internship interview?",
        " 1. A problem you picked yourself",
        " 2. Trade-offs you had to make (cost, latency, error handling)",
        " 3. Clear documentation explaining how it works and what's next",
        "",
        "You don't need 15 repos. You need 2 or 3 you can explain deeply.",
        "",
        "What is the one project on your resume you are most proud of?"
    ]
    y = 196
    for line in post_lines:
        draw.text((46, y), line, font=FONT_CODE, fill=TEXT_CODE)
        y += 19

    # Image prompt box
    draw.rounded_rectangle([(580, 156), (WIDTH - 32, HEIGHT - 32)], radius=8, fill=(10, 15, 30), outline=BORDER_COLOR)
    draw.text((594, 168), "Image Prompt ($json.output['image description'])", font=FONT_CODE_BOLD, fill=ACCENT_YELLOW)

    prompt_lines = [
        "\"A realistic modern desk workspace with",
        "a laptop displaying an architecture diagram",
        "and clean code editor, warm ambient lighting,",
        "notebook and pen beside keyboard, minimal tech",
        "aesthetic suitable for a professional LinkedIn",
        "software engineering post.\"",
        "",
        "Strict Rule Enforced:",
        "✔ No hashtags in post body",
        "✔ Structured Output Parser1 validated",
        "✔ Dispatched to parallel branches"
    ]
    y = 200
    for line in prompt_lines:
        col = ACCENT_GREEN if line.startswith("✔") else (ACCENT_PURPLE if line.startswith("Strict") else TEXT_MUTED)
        draw.text((594, y), line, font=FONT_CODE, fill=col)
        y += 22

    return img


def render_scene_3():
    """Scene 3: Parallel Asset Generation (Gemini Image + SEO Hashtags)."""
    img, draw = create_base_canvas(active_step_idx=3)

    draw.rounded_rectangle([(16, 96), (WIDTH - 16, HEIGHT - 16)], radius=10, fill=SURFACE_COLOR, outline=BORDER_COLOR)

    # Header badge
    draw.rounded_rectangle([(32, 112), (360, 142)], radius=6, fill=(6, 182, 212, 40), outline=ACCENT_CYAN)
    draw.text((42, 118), "STAGE 4: PARALLEL ASSET GENERATION", font=FONT_BOLD, fill=ACCENT_CYAN)

    draw.text((380, 120), "Branch Fan-Out: Concurrent image generation & SEO optimization", font=FONT_SUBTITLE, fill=TEXT_MUTED)

    # Left: Gemini Image Generator
    draw.rounded_rectangle([(32, 156), (465, HEIGHT - 32)], radius=8, fill=(10, 15, 30), outline=ACCENT_BLUE)
    draw.text((46, 168), "BRANCH A: Gemini Image Generator", font=FONT_BOLD, fill=ACCENT_BLUE)
    draw.text((46, 190), "• Node: @n8n/n8n-nodes-langchain.googleGemini (v1.2)", font=FONT_SMALL, fill=TEXT_MUTED)
    draw.text((46, 208), "• Model: models/gemini-3.1-flash-image (Nano Banana 2)", font=FONT_SMALL, fill=ACCENT_CYAN)
    draw.text((46, 226), "• Retry Policy: retryOnFail=true (maxTries: 2, wait: 3s)", font=FONT_SMALL, fill=ACCENT_GREEN)

    # Simulated visual card
    draw.rounded_rectangle([(46, 256), (450, HEIGHT - 46)], radius=6, fill=(20, 30, 50), outline=BORDER_COLOR)
    draw.rectangle([(56, 266), (440, 440)], fill=(30, 41, 59))
    draw.text((120, 330), "💻 [ Realistic Developer Workspace ]", font=FONT_BOLD, fill=ACCENT_CYAN)
    draw.text((100, 360), "Architecture Flowchart • VS Code Editor", font=FONT_SUBTITLE, fill=TEXT_MUTED)
    draw.text((140, 455), "Output: $binary.data (image/png)", font=FONT_CODE_BOLD, fill=ACCENT_GREEN)

    # Right: Hashtag Generator / SEO
    draw.rounded_rectangle([(495, 156), (WIDTH - 32, HEIGHT - 32)], radius=8, fill=(10, 15, 30), outline=ACCENT_PURPLE)
    draw.text((509, 168), "BRANCH B: Hashtag generator /SEO", font=FONT_BOLD, fill=ACCENT_PURPLE)
    draw.text((509, 190), "• Node: @n8n/n8n-nodes-langchain.agent (v3.1)", font=FONT_SMALL, fill=TEXT_MUTED)
    draw.text((509, 208), "• Model: OpenAI Chat Model (gpt-5.4)", font=FONT_SMALL, fill=ACCENT_CYAN)
    draw.text((509, 226), "• Schema: Structured Output Parser2 ({ Hashtags: [...] })", font=FONT_SMALL, fill=ACCENT_YELLOW)

    # Hashtags list
    draw.rounded_rectangle([(509, 256), (WIDTH - 46, HEIGHT - 46)], radius=6, fill=(20, 30, 50), outline=BORDER_COLOR)
    draw.text((525, 274), "Generated SEO Hashtags Array:", font=FONT_CODE_BOLD, fill=TEXT_MAIN)

    tags = [
        "#SoftwareEngineering",
        "#TechCareers",
        "#Internships",
        "#StudentPortfolio",
        "#GitHubProjects",
        "#EarlyCareer"
    ]
    ty = 310
    for tag in tags:
        draw.rounded_rectangle([(525, ty), (720, ty + 26)], radius=13, fill=(30, 58, 138), outline=ACCENT_BLUE)
        draw.text((538, ty + 5), tag, font=FONT_CODE_BOLD, fill=TEXT_MAIN)
        ty += 32

    return img


def render_scene_4():
    """Scene 4: Merge & Validation Gate (Code node v2)."""
    img, draw = create_base_canvas(active_step_idx=4)

    draw.rounded_rectangle([(16, 96), (WIDTH - 16, HEIGHT - 16)], radius=10, fill=SURFACE_COLOR, outline=BORDER_COLOR)

    # Header badge
    draw.rounded_rectangle([(32, 112), (400, 142)], radius=6, fill=(34, 197, 94, 40), outline=ACCENT_GREEN)
    draw.text((42, 118), "STAGE 5: MERGE & CODE VALIDATION GATE", font=FONT_BOLD, fill=ACCENT_GREEN)

    draw.text((420, 120), "Deterministic Gate: Rejoining streams & guarding data integrity", font=FONT_SUBTITLE, fill=TEXT_MUTED)

    # Merge Node Card
    draw.rounded_rectangle([(32, 156), (360, 260)], radius=8, fill=(10, 15, 30), outline=BORDER_COLOR)
    draw.text((46, 168), "Merge (v3.2)", font=FONT_BOLD, fill=ACCENT_CYAN)
    draw.text((46, 192), "• Mode: combine", font=FONT_SUBTITLE, fill=TEXT_MUTED)
    draw.text((46, 212), "• CombineBy: combineByPosition", font=FONT_SUBTITLE, fill=TEXT_MUTED)
    draw.text((46, 232), "• Synchronizes Branch A & Branch B", font=FONT_SUBTITLE, fill=TEXT_MUTED)

    draw.text((380, 200), "──────▶", font=FONT_BOLD, fill=ACCENT_GREEN)

    # Code Node Card
    draw.rounded_rectangle([(440, 156), (WIDTH - 32, 260)], radius=8, fill=(10, 15, 30), outline=ACCENT_GREEN)
    draw.text((454, 168), "Validate & Format Post (n8n-nodes-base.code v2)", font=FONT_BOLD, fill=ACCENT_GREEN)
    draw.text((454, 192), "• Script: scripts/validate_format_post.js", font=FONT_SUBTITLE, fill=TEXT_CODE)
    draw.text((454, 212), "• Validates non-empty title/body & binary.data", font=FONT_SUBTITLE, fill=TEXT_MUTED)
    draw.text((454, 232), "• Case-insensitive hashtag deduplication & stripping", font=FONT_SUBTITLE, fill=TEXT_MUTED)

    # Checklist Card
    draw.rounded_rectangle([(32, 276), (WIDTH - 32, HEIGHT - 32)], radius=8, fill=(10, 15, 30), outline=BORDER_COLOR)
    draw.text((46, 290), "Runtime Validation Checklist (Passed in 8ms):", font=FONT_CODE_BOLD, fill=ACCENT_YELLOW)

    checks = [
        "✔ Input Items Check: Exactly 1 merged item received from parallel branches",
        "✔ Post Title Check: 'One Real Project Beats Five Tutorial Clones' (Non-empty, trimmed)",
        "✔ Post Body Check: Clean body text verified; stray inline '#' lines stripped",
        "✔ Binary Image Check: $binary.data verified and normalized for LinkedIn node",
        "✔ Hashtag Deduplication: 6 raw tokens normalized to 5 unique hashtags: #SoftwareEngineering #TechCareers #Internships...",
        "✔ Ready for Safe Publishing: Emitted { formattedTitle, formattedText, binary: { data } }"
    ]
    cy = 320
    for c in checks:
        draw.text((46, cy), c, font=FONT_CODE, fill=ACCENT_GREEN)
        cy += 24

    return img


def render_scene_5():
    """Scene 5: LinkedIn Publishing & Telegram Notification Alert."""
    img, draw = create_base_canvas(active_step_idx=5)

    draw.rounded_rectangle([(16, 96), (WIDTH - 16, HEIGHT - 16)], radius=10, fill=SURFACE_COLOR, outline=BORDER_COLOR)

    # Header badge
    draw.rounded_rectangle([(32, 112), (420, 142)], radius=6, fill=(10, 102, 194, 40), outline=(10, 102, 194))
    draw.text((42, 118), "STAGE 6 & 7: LINKEDIN PUBLISHING & TELEGRAM ALERT", font=FONT_BOLD, fill=(14, 165, 233))

    # Left: LinkedIn Post Card
    draw.rounded_rectangle([(32, 156), (510, HEIGHT - 32)], radius=8, fill=(10, 15, 30), outline=(10, 102, 194))
    draw.text((46, 168), "LinkedIn (v1) — OAuth2 Image Share", font=FONT_BOLD, fill=(14, 165, 233))
    draw.text((46, 190), "• Visibility: CONNECTIONS (Safe testing default)", font=FONT_SMALL, fill=ACCENT_GREEN)
    draw.text((46, 208), "• Media Category: IMAGE | binaryPropertyName: data", font=FONT_SMALL, fill=TEXT_MUTED)
    draw.text((46, 226), "• API Status: 201 Created | URN: urn:li:share:714295821", font=FONT_SMALL, fill=ACCENT_YELLOW)

    # Simulated post UI
    draw.rounded_rectangle([(46, 246), (496, HEIGHT - 46)], radius=6, fill=(20, 30, 50), outline=BORDER_COLOR)
    draw.ellipse([(60, 258), (90, 288)], fill=ACCENT_BLUE)
    draw.text((68, 266), "NK", font=FONT_BOLD, fill=TEXT_MAIN)
    draw.text((102, 258), "nijjukrr • LinkedIn Creator", font=FONT_BOLD, fill=TEXT_MAIN)
    draw.text((102, 276), "Just now • 🌐 Connections", font=FONT_SMALL, fill=TEXT_MUTED)

    draw.text((60, 302), "One Real Project Beats Five Tutorial Clones", font=FONT_BOLD, fill=TEXT_MAIN)
    draw.text((60, 324), "Stop adding tutorial clones to your GitHub...", font=FONT_SUBTITLE, fill=TEXT_MUTED)
    draw.text((60, 344), "What actually stands out in an internship interview?", font=FONT_SUBTITLE, fill=TEXT_MUTED)
    draw.text((60, 368), "#SoftwareEngineering #TechCareers #Internships", font=FONT_CODE, fill=ACCENT_BLUE)

    draw.rectangle([(60, 392), (482, 470)], fill=(30, 41, 59))
    draw.text((150, 425), "[ Attached Gemini 3.1 Visual ]", font=FONT_SUBTITLE, fill=ACCENT_CYAN)

    # Right: Telegram Notification Card
    draw.rounded_rectangle([(530, 156), (WIDTH - 32, HEIGHT - 32)], radius=8, fill=(10, 15, 30), outline=ACCENT_CYAN)
    draw.text((544, 168), "Notify on Telegram (v1.2)", font=FONT_BOLD, fill=ACCENT_CYAN)
    draw.text((544, 190), "• Instant mobile push alert via Bot API", font=FONT_SMALL, fill=TEXT_MUTED)
    draw.text((544, 208), "• HTML parse mode with sanitized entity escaping", font=FONT_SMALL, fill=TEXT_MUTED)

    # Telegram Bubble
    draw.rounded_rectangle([(544, 236), (WIDTH - 46, HEIGHT - 46)], radius=8, fill=(15, 23, 42), outline=ACCENT_GREEN)
    tg_lines = [
        "🔔 Telegram Notification",
        "────────────────────────────────────────",
        "✅ New LinkedIn post published",
        "",
        "One Real Project Beats Five Tutorial Clones",
        "",
        "🔗 https://www.linkedin.com/feed/update/",
        "   urn:li:share:714295821",
        "",
        "🕒 Posted at 26 Nov 2026, 08:00 IST",
        "",
        "Status: Delivered to chatId"
    ]
    ty = 250
    for line in tg_lines:
        col = ACCENT_GREEN if "✅" in line or "Delivered" in line else (ACCENT_CYAN if "🔗" in line else TEXT_MAIN)
        draw.text((558, ty), line, font=FONT_CODE, fill=col)
        ty += 18

    return img


def render_scene_6():
    """Scene 6: Final Execution Summary & Health Metrics."""
    img, draw = create_base_canvas(active_step_idx=6)

    draw.rounded_rectangle([(16, 96), (WIDTH - 16, HEIGHT - 16)], radius=10, fill=SURFACE_COLOR, outline=ACCENT_GREEN, width=2)

    # Header badge
    draw.rounded_rectangle([(32, 112), (460, 142)], radius=6, fill=(34, 197, 94, 40), outline=ACCENT_GREEN)
    draw.text((42, 118), "WORKFLOW EXECUTION COMPLETE — 15/15 NODES PASSED", font=FONT_BOLD, fill=ACCENT_GREEN)

    # Metric Cards
    metrics = [
        ("EXECUTION STATUS", "SUCCESS (200 OK)", ACCENT_GREEN),
        ("TOTAL DURATION", "4.12 SECONDS", ACCENT_CYAN),
        ("PARALLEL ASSETS", "2/2 SYNCHRONIZED", ACCENT_PURPLE),
        ("NEXT SCHEDULED", "IN 8 HOURS", ACCENT_YELLOW)
    ]
    card_w = (WIDTH - 64 - 36) / 4
    for i, (title, val, col) in enumerate(metrics):
        cx1 = 32 + i * (card_w + 12)
        cx2 = cx1 + card_w
        draw.rounded_rectangle([(cx1, 160), (cx2, 230)], radius=8, fill=(10, 15, 30), outline=BORDER_COLOR)
        draw.text((cx1 + 12, 172), title, font=FONT_SMALL, fill=TEXT_MUTED)
        draw.text((cx1 + 12, 194), val, font=FONT_BOLD, fill=col)

    # Summary table
    draw.rounded_rectangle([(32, 250), (WIDTH - 32, HEIGHT - 32)], radius=8, fill=(10, 15, 30), outline=BORDER_COLOR)
    draw.text((46, 264), "Engineering Integrity Summary:", font=FONT_CODE_BOLD, fill=TEXT_MAIN)

    summary_items = [
        ("Structured Contracts", "Strict JSON schemas enforced via 3 Structured Output Parsers"),
        ("Concurrency", "Google Gemini Image Generator & OpenAI SEO Agent executed in parallel"),
        ("Deterministic Gate", "Validate & Format Post Code node verified binary buffer & cleaned hashtags"),
        ("Safe Defaults", "Public export inactive by default; LinkedIn visibility initialized to CONNECTIONS"),
        ("Automated Tests", "14 Python test cases + 7 direct Node.js unit tests passing in CI (0.57s)"),
        ("Observability", "Instant Telegram push alert with clickable LinkedIn post URN link")
    ]
    sy = 296
    for k, v in summary_items:
        draw.text((46, sy), f"• {k}:", font=FONT_CODE_BOLD, fill=ACCENT_CYAN)
        draw.text((250, sy), v, font=FONT_CODE, fill=TEXT_MUTED)
        sy += 28

    return img


def main():
    print("Generating animated walkthrough GIF frames...")
    scenes = [
        (render_scene_1(), 2800),  # Trigger & Topic
        (render_scene_2(), 2800),  # Copywriter
        (render_scene_3(), 3200),  # Parallel Assets
        (render_scene_4(), 3000),  # Validation Gate
        (render_scene_5(), 3500),  # LinkedIn & Telegram
        (render_scene_6(), 3500),  # Summary
    ]

    frames = []
    durations = []
    for img, duration in scenes:
        # Quantize each frame with adaptive palette
        paletted = img.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
        frames.append(paletted)
        durations.append(duration)

    out_path = os.path.join("assets", "demo", "workflow-walkthrough.gif")
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True
    )

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"Generated {out_path} ({size_mb:.2f} MB, {len(frames)} scenes)")


if __name__ == "__main__":
    main()
