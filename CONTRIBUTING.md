# Contributing

Contributions, bug reports, and documentation improvements are welcome!

## Guidelines

1. **Never commit credentials or personal IDs:** Audit any exported n8n JSON file before committing (`person`, `chatId`, `credential.id`, `webhookId`, `instanceId`).
2. **Validate JSON:** Ensure any modified workflow JSON parses cleanly before opening a pull request:
   ```bash
   python -m json.tool workflows/linkedin_content_automation.json > /dev/null
   ```
3. **Preserve existing node contracts:** If you add a new node or enhancement (such as an `Error Trigger` or Telegram approval gate), document the changes in `docs/workflow-explanation.md` and `docs/system-architecture.md`.
4. **Branching:** Create a feature branch from `main` (e.g., `feat/human-approval-gate` or `docs/update-setup`) and use clear, descriptive commit messages.
