"""Builds index.html from the use-case list below. Edit here, then run: python3 build.py"""
import html

STARTER = """I'm not technical, so please do everything for me and explain each step in plain English.

Use Jev, TypeSafe's decision model (model id: typesafe/jev-1.13), through OpenRouter's Decisions API:
POST https://openrouter.ai/api/alpha/decisions
Header: Authorization: Bearer <my OpenRouter key>
Body: {"model": "typesafe/jev-1.13", "state": "<the context as plain text>", "questions": {"<name>": {"type": "choice", "instructions": "...", "criteria": {"option_a": "what it means", "option_b": "..."}}, "<name2>": {"type": "noul", "instructions": "<a yes/no question>"}}}
Jev returns answers with probabilities and a confidence score. It never writes text, so use Claude for any writing.

Ask me for my OpenRouter key when you need it and never save it in a file I might share. Run requests in parallel (about 40 at a time) and retry if one fails. Test on 10 items first and show me the results before running everything. Tell me the total Jev cost at the end."""

CASES = [
 dict(id="lead-scoring", tag="built", tagtxt="I built this", title="Lead scoring",
  who="Sales, BD, founders",
  what="Reads every lead against your ideal customer and tells you who to call today, who to nurture and who to skip, with how sure it is.",
  proof=[("700 leads","my run"),("8.9 sec",""),("$0.0159","")],
  tool=("tools/lead-scorer/","Open the Lead X-Ray tool"),
  steps=["Write 3 lines on your ideal customer: role, company type, size, and what a buying signal looks like.",
         "Export your leads as a CSV from your CRM, LinkedIn Sales Navigator or a spreadsheet.",
         "Use the ready-made tool above, or paste the prompt into Claude to build your own version.",
         "Download the scored list and call the HOT ones first."],
  prompt="""Score my leads with Jev.
1. Ask me to describe my ideal customer and to upload my lead CSV.
2. For each lead, ask Jev (choice): hot, warm or cold. Hot = strong fit AND a recent buying signal. Warm = good fit, no signal yet. Cold = wrong role, company or size.
3. Also ask Jev (noul): "Is there a recent buying signal?"
4. Build me a simple page that shows the leads being scored live, with a timer and the total cost.
5. Let me download the scored list, sorted best first.""",
  honest="Garbage in, garbage out. If your CSV only has names and emails, Jev has nothing to judge. Add a job title, company and any notes you have."),
 dict(id="link-audit", tag="built", tagtxt="I built this", title="Internal link audit (SEO)",
  who="SEO, content, website owners",
  what="Reads every page on your site, finds the related pages that should link to each other, picks the anchor text and fixes orphan pages. You get a CSV link plan.",
  proof=[("1,208 pages","my run"),("6,718 decisions",""),("3,013 links",""),("3 min 49 sec",""),("$0.22 vs ~$26.71 on Claude Opus","")],
  tool=("tools/link-audit/","Open the Link Audit tool"),
  steps=["Get your OpenRouter key ready.",
         "Download this playbook and ask Claude to start the link audit tool for you (instructions on the tool page).",
         "Paste your website and hit Run. It reads your sitemap, then Jev decides every link.",
         "Download the CSV and hand it to whoever edits your site. Start with the orphan pages."],
  prompt="""Audit my website's internal links with Jev.
1. Read every page in my sitemap: title, H1, main text and the links already on it.
2. For each page, find the 6 most related pages it doesn't link to yet.
3. For each pair, ask Jev (noul): "Following hub-and-spoke SEO rules, should this page link to that page?" Articles link up to their service pages, service pages link down to their articles, and no forced links between unrelated topics.
4. Ask Jev (choice) which of 2 or 3 anchor text options is the most descriptive.
5. Flag orphan pages (nothing links to them) and give me a CSV: source page, target page, anchor text, confidence.""",
  honest="Jev picks the links, a human still places them. Skim the CSV before anything goes live, especially links to your money pages."),
 dict(id="focus-group", tag="community", tagtxt="From the community", title="AI focus group",
  who="Marketers, media buyers, founders",
  what="Creates 30 buyer personas and has each one decide 'stop or scroll' on every ad, so you know which ads stop your buyer before you spend on them.",
  proof=[("723 ads","@TheMattBerman"),("30 personas",""),("21,690 decisions",""),("22¢","")],
  steps=["Describe your product and who buys it.",
         "Collect competitor ads (Meta Ad Library, screenshots or ad text are fine).",
         "Paste the prompt. Claude writes the personas, Jev makes every stop-or-scroll call.",
         "Use the winners to brief your next ads."],
  prompt="""Build me an AI focus group with Jev.
1. Ask me about my product and who buys it. Then write 30 realistic, varied buyer personas (Claude writes these).
2. Help me collect ads from the Meta Ad Library for the competitors I name (ad text, headline, image description).
3. For every persona and ad, ask Jev (noul): "Would this person stop scrolling for this ad?"
4. And ask Jev (choice) what stopped them: offer, hook, visual, social proof or nothing.
5. Show me a grid of personas vs ads, the top 5 ads by stop rate, and which persona each ad wins.""",
  honest="Personas are a simulation, not real people. Use it to pick what to test, not to skip testing."),
 dict(id="competitor-ads", tag="community", tagtxt="From the community", title="Competitor ad sorter",
  who="Marketers, agencies, founders",
  what="Sorts every live competitor ad by funnel stage, angle and offer, so you can see their whole strategy on one page, and the angles nobody is using.",
  proof=[("1,891 ads","@OriSilver"),("19 sec",""),("$0.12","")],
  steps=["List 3 to 10 competitors.",
         "Pull their live ads from the Meta Ad Library (Claude can help, or use a scraper like Apify).",
         "Paste the prompt. Jev tags every ad.",
         "Read the gaps table. That's your next campaign."],
  prompt="""Sort my competitors' ads with Jev.
1. Help me collect all active ads for these competitors from the Meta Ad Library: [competitor names]. Get the ad text, headline, call to action and landing page. Ask me before spending money on any scraping tool.
2. For every ad, ask Jev (choice) the funnel stage: unaware, problem aware, solution aware, product aware or most aware.
3. Ask Jev (choice) the main angle: price, pain, outcome, social proof, urgency or authority.
4. Ask Jev (choice) the offer type: free trial, discount, lead magnet, demo, straight purchase or none.
5. Give me a table per brand, plus a gaps table showing the angles and stages nobody is using.""",
  honest="The Ad Library shows what's running, not what's working. Ads that have been running for a long time are your best clue."),
 dict(id="comment-triage", tag="idea", tagtxt="My pick", title="Instagram comment & DM triage",
  who="Creators, brands, social media managers",
  what="Sorts hundreds of comments and DMs into buyers, questions, fans, brand deals and spam, so you reply to the people who want to buy first.",
  proof=[],
  steps=["Export or copy your comments and DMs (Claude can help you get them).",
         "Paste the prompt.",
         "Jev sorts everything. Claude drafts replies for buyers and questions only.",
         "You read, tweak and send. Nothing goes out on its own."],
  prompt="""Triage my Instagram comments and DMs with Jev.
1. Help me get my recent comments and DMs into a list (a CSV or a paste is fine).
2. For each one, ask Jev (choice): buyer intent, a question I should answer, fan, collab or brand deal, or spam.
3. Ask Jev (noul): "Does this need a reply from me today?"
4. For the buyer and question ones only, have Claude draft a reply in my voice for me to approve. Don't send anything.
5. Give me the sorted list, buyers first.""",
  honest="It drafts, you approve. Never let it reply to people on its own."),
 dict(id="keyword-intent", tag="idea", tagtxt="My pick", title="Keyword intent sorter",
  who="SEO, content, paid search",
  what="Sorts your whole keyword list by search intent and whether the searcher could actually buy from you, so you build pages for the keywords that pay.",
  proof=[],
  steps=["Export your keywords from Google Search Console, Google Ads or any SEO tool.",
         "Write one line on what you sell.",
         "Paste the prompt.",
         "Build pages for the top 20 first."],
  prompt="""Sort my keyword list with Jev.
1. Ask me for my keyword CSV and one line on what I sell.
2. For every keyword, ask Jev (choice) the intent: informational, commercial, transactional, navigational or local.
3. Ask Jev (noul): "Could someone searching this realistically buy what I sell?"
4. Group the keywords into topic clusters (Claude can do the grouping).
5. Tell me the 20 keywords to build pages for first, and which existing page each one belongs to.""",
  honest="Jev judges intent from the words alone. For your biggest keywords, still look at what Google actually shows."),
 dict(id="visitor-followup", tag="idea", tagtxt="Idea via @angus.sewell", title="Website visitor → best follow-up",
  who="Sales, marketing ops, founders",
  what="When someone visits your site, Jev combines what they looked at, where they came from and your CRM, and picks which of your follow-up emails fits them best.",
  proof=[],
  steps=["Write 3 to 6 follow-up email templates (Claude can help).",
         "Export recent visitors or leads from your analytics or CRM.",
         "Paste the prompt. Jev picks a template for each person.",
         "Review and send. Once you trust the picks, have it prepare drafts in your CRM."],
  prompt="""Match my website visitors to the best follow-up email with Jev.
1. Ask me which analytics and CRM tools I use. Start with a CSV export if that's easier.
2. For each visitor or lead, combine the pages they viewed, where they came from, their company, and whether they're already in my CRM.
3. Ask Jev (choice) which of my follow-up templates fits best: [paste your template names and one line on each].
4. Ask Jev (noul): "Is this person ready for a sales call?"
5. Put the pick next to each person so I can review and send. Don't send anything automatically.""",
  honest="Only follow up with people who gave you their details. Check your privacy rules before you enrich anyone."),
 dict(id="hook-analyser", tag="community", tagtxt="From the community", title="Viral hook analyser",
  who="Content creators, social media managers",
  what="Reads hundreds of posts in your niche, tags every hook by type, and shows you which kinds of hooks actually get views. Then Claude writes you 10 in that style.",
  proof=[("100,000 posts","@0xMovez"),("20 sec",""),("$0.67","")],
  steps=["Pick 5 to 10 accounts in your niche.",
         "Collect their recent posts with view counts (a scraper like Apify works).",
         "Paste the prompt. Jev tags every hook.",
         "Use the winning hook types for your next week of content."],
  prompt="""Analyse the hooks in my niche with Jev.
1. Help me collect the last 200 posts from these accounts, with views and the first line: [handles]. Ask me before spending money on a scraper.
2. For each post, ask Jev (choice) the hook type: number, contrarian, how-to, story, question, before and after, or news.
3. Ask Jev (noul): "Does the first line promise a specific payoff?"
4. Show me which hook types get the most views on average.
5. Then have Claude write me 10 hooks for my topic in the top 3 styles.""",
  honest="Views depend on more than the hook. Treat this as a direction, not a formula."),
]

TAGCLS = {"built": "t-built", "community": "t-comm", "idea": "t-idea"}

def esc(s): return html.escape(s, quote=True)

def card(i, c):
    proof = "".join(f'<span class="chip">{esc(a)}{f" <em>{esc(b)}</em>" if b else ""}</span>' for a, b in c["proof"])
    tool = f'<a class="tool" href="{c["tool"][0]}">{esc(c["tool"][1])} →</a>' if c.get("tool") else ""
    steps = "".join(f"<li>{esc(s)}</li>" for s in c["steps"])
    return f'''
<section class="case" id="{c["id"]}">
  <div class="case-head">
    <span class="num">{i:02d}</span>
    <div>
      <span class="tag {TAGCLS[c["tag"]]}">{esc(c["tagtxt"])}</span>
      <h2>{esc(c["title"])}</h2>
      <p class="who">For: {esc(c["who"])}</p>
    </div>
  </div>
  <p class="what">{esc(c["what"])}</p>
  {f'<div class="chips">{proof}</div>' if proof else ""}
  {tool}
  <div class="cols">
    <div>
      <h3>Step by step</h3>
      <ol>{steps}</ol>
      <p class="honest"><b>Honest bit:</b> {esc(c["honest"])}</p>
    </div>
    <div class="promptbox">
      <div class="pb-head"><span>Prompt · paste into Claude or Codex</span><button class="copy" data-for="p-{c["id"]}">Copy prompt</button></div>
      <pre id="p-{c["id"]}">{esc(c["prompt"])}</pre>
    </div>
  </div>
</section>'''

nav = "".join(f'<a href="#{c["id"]}">{i:02d} {esc(c["title"])}</a>' for i, c in enumerate(CASES, 1))
cards = "".join(card(i, c) for i, c in enumerate(CASES, 1))

page = open("template.html").read().replace("{{NAV}}", nav).replace("{{CARDS}}", cards).replace("{{STARTER}}", esc(STARTER))
open("index.html", "w").write(page)
print("built index.html with", len(CASES), "use cases")
