"""Automated validation and unit tests for AI-Powered LinkedIn Content Automation.

Runs offline without external API credentials.
Usage:
    python -m unittest discover -s tests -v
"""

import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOW_PATH = ROOT / "workflows" / "linkedin_content_automation.json"


def normalize_hashtags(raw_hashtags):
    """Mirror the hashtag normalization and deduplication logic in Validate & Format Post."""
    if not isinstance(raw_hashtags, list):
        return []
    seen = set()
    result = []
    for entry in raw_hashtags:
        for token in re.split(r"[,\s]+", str(entry or "")):
            cleaned = re.sub(r"[^a-zA-Z0-9_]", "", token.strip().lstrip("#"))
            if not cleaned:
                continue
            formatted = f"#{cleaned}"
            lower = formatted.lower()
            if lower not in seen:
                seen.add(lower)
                result.append(formatted)
    return result


def escape_telegram_html(text):
    """Mirror the HTML escaping used in Notify on Telegram."""
    return (
        str(text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_linkedin_url(urn):
    """Mirror the LinkedIn post URL construction with missing-URN fallback."""
    if urn:
        return f"https://www.linkedin.com/feed/update/{urn}"
    return "Check your LinkedIn profile for the post."


class TestWorkflowStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
            cls.wf = json.load(f)
        cls.nodes_by_name = {n["name"]: n for n in cls.wf["nodes"]}

    def test_01_workflow_json_valid_and_inactive(self):
        self.assertIsInstance(self.wf, dict)
        self.assertFalse(self.wf.get("active"), "Public workflow must be inactive by default")
        self.assertEqual(self.wf.get("settings", {}).get("binaryMode"), "separate")

    def test_02_required_nodes_exist_and_unique(self):
        expected_nodes = {
            "Schedule Trigger",
            "Content topic generator2",
            "OpenAI Chat Model",
            "Structured Output Parser",
            "Content creator",
            "OpenAI Chat Model1",
            "Structured Output Parser1",
            "Gemini Image Generator",
            "Hashtag generator /SEO",
            "OpenAI Chat Model2",
            "Structured Output Parser2",
            "Merge",
            "Validate & Format Post",
            "LinkedIn",
            "Notify on Telegram",
        }
        actual_names = [n["name"] for n in self.wf["nodes"]]
        self.assertEqual(len(actual_names), len(set(actual_names)), "Node names must be unique")
        self.assertTrue(expected_nodes.issubset(set(actual_names)))

    def test_03_connections_are_valid(self):
        connections = self.wf.get("connections", {})
        for src_name, conn_types in connections.items():
            self.assertIn(src_name, self.nodes_by_name, f"Unknown source node: {src_name}")
            for _, branches in conn_types.items():
                for branch in branches:
                    for edge in branch:
                        self.assertIn(
                            edge["node"],
                            self.nodes_by_name,
                            f"Unknown target node: {edge['node']}",
                        )

        # Verify Merge -> Validate & Format Post -> LinkedIn -> Notify on Telegram
        self.assertEqual(
            connections["Merge"]["main"][0][0]["node"], "Validate & Format Post"
        )
        self.assertEqual(
            connections["Validate & Format Post"]["main"][0][0]["node"], "LinkedIn"
        )
        self.assertEqual(
            connections["LinkedIn"]["main"][0][0]["node"], "Notify on Telegram"
        )

    def test_04_schedule_configuration(self):
        sched = self.nodes_by_name["Schedule Trigger"]["parameters"]["rule"]["interval"][0]
        self.assertEqual(sched["field"], "hours")
        self.assertEqual(sched["hoursInterval"], 8)

    def test_05_credential_placeholders_and_safe_defaults(self):
        li = self.nodes_by_name["LinkedIn"]
        tg = self.nodes_by_name["Notify on Telegram"]
        self.assertEqual(li["parameters"]["person"], "YOUR_LINKEDIN_PERSON_ID")
        self.assertEqual(
            li["credentials"]["linkedInOAuth2Api"]["id"], "YOUR_LINKEDIN_CREDENTIAL_ID"
        )
        self.assertEqual(li["parameters"]["additionalFields"]["visibility"], "CONNECTIONS")
        self.assertEqual(li["parameters"].get("binaryPropertyName"), "data")
        self.assertFalse(li.get("retryOnFail", False))

        self.assertEqual(tg["parameters"]["chatId"], "YOUR_TELEGRAM_CHAT_ID")
        self.assertEqual(tg["webhookId"], "YOUR_TELEGRAM_WEBHOOK_ID")
        self.assertEqual(
            tg["credentials"]["telegramApi"]["id"], "YOUR_TELEGRAM_CREDENTIAL_ID"
        )
        self.assertEqual(self.wf["meta"]["instanceId"], "YOUR_N8N_INSTANCE_ID")
        self.assertEqual(self.wf["id"], "YOUR_WORKFLOW_ID")

    def test_06_structured_output_parser2_schema_clean(self):
        parser2 = self.nodes_by_name["Structured Output Parser2"]
        schema = json.loads(parser2["parameters"]["jsonSchemaExample"])
        self.assertEqual(list(schema.keys()), ["Hashtags"])
        self.assertIsInstance(schema["Hashtags"], list)

    def test_07_binary_validation_in_code_node(self):
        code_node = self.nodes_by_name["Validate & Format Post"]
        js = code_node["parameters"]["jsCode"]
        self.assertIn("$binary.data", js)
        self.assertIn("binary: $binary", js)


class TestExamplesAndHelpers(unittest.TestCase):
    def test_08_example_outputs_match_schemas(self):
        with open(ROOT / "examples" / "sample-topic-output.json", encoding="utf-8") as f:
            topic = json.load(f)
        self.assertIsInstance(topic["output"], list)
        self.assertTrue({"title", "rationale", "hook"}.issubset(topic["output"][0].keys()))

        with open(ROOT / "examples" / "sample-post-output.json", encoding="utf-8") as f:
            post = json.load(f)
        self.assertTrue(
            {"post title", "post content", "image description"}.issubset(post["output"].keys())
        )

        with open(ROOT / "examples" / "sample-hashtag-output.json", encoding="utf-8") as f:
            tags = json.load(f)
        self.assertEqual(list(tags["output"].keys()), ["Hashtags"])
        self.assertIsInstance(tags["output"]["Hashtags"], list)

    def test_09_hashtag_normalization_and_deduplication(self):
        raw = ["#AI, ai", "  #LinkedIn! ", "", "###Tech_2026", "#tech_2026", "Software"]
        self.assertEqual(
            normalize_hashtags(raw),
            ["#AI", "#LinkedIn", "#Tech_2026", "#Software"],
        )
        self.assertEqual(normalize_hashtags(None), [])

    def test_10_html_escaping_and_url_construction(self):
        self.assertEqual(
            escape_telegram_html("AI & ML <2026>"),
            "AI &amp; ML &lt;2026&gt;",
        )
        self.assertEqual(
            build_linkedin_url("urn:li:share:12345"),
            "https://www.linkedin.com/feed/update/urn:li:share:12345",
        )
        self.assertEqual(
            build_linkedin_url(""),
            "Check your LinkedIn profile for the post.",
        )

    def test_11_documentation_links_and_secret_scan(self):
        link_re = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
        for md in ROOT.rglob("*.md"):
            text = md.read_text(encoding="utf-8")
            for match in link_re.finditer(text):
                target = match.group(1)
                if target.startswith(("http://", "https://")):
                    continue
                resolved = (md.parent / target).resolve()
                self.assertTrue(resolved.exists(), f"Broken link in {md}: {target}")

        secret_patterns = [
            re.compile(r"sk-[A-Za-z0-9]{20,}"),
            re.compile(r"ghp_[A-Za-z0-9]{20,}"),
            re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
            re.compile(r"bot[0-9]{8,}:[A-Za-z0-9_-]{30,}"),
        ]
        for p in ROOT.rglob("*"):
            if p.is_file() and ".git" not in p.parts and not p.name.endswith(".local.json"):
                content = p.read_text(encoding="utf-8", errors="ignore")
                for pattern in secret_patterns:
                    self.assertIsNone(
                        pattern.search(content),
                        f"Potential secret pattern matched in {p}",
                    )


if __name__ == "__main__":
    unittest.main()
