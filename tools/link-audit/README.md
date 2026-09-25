# Jev internal link audit

Reads every page on a website, then asks Jev (typesafe/jev-1.13 on OpenRouter) which internal links each page is missing, and which anchor text to use. Uses hub-and-spoke SEO rules. At the end you can download a CSV link plan.

## Run it (no coding)
1. Open this playbook folder in Claude (desktop app, Code tab).
2. Say: `Start the Jev link audit tool in tools/link-audit and open it for me`
3. Paste your website and your OpenRouter key (openrouter.ai/settings/keys), then hit **Run audit**.

## Run it yourself
```
python3 server.py
```
Then open http://localhost:8765 in your browser.

The helper (`server.py`) only fetches pages so your browser can read them. Your key never touches it. Jev calls go straight from your browser to OpenRouter.
