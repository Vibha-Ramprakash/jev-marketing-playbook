"""Builds index.html from the use-case list below. Edit here, then run: python3 build.py"""
import html

STARTER = """I'm not technical, so please do everything for me and explain each step in plain English.

Use Jev, TypeSafe's decision model (model id: typesafe/jev-1.13), through OpenRouter's Decisions API:
POST https://openrouter.ai/api/alpha/decisions
Header: Authorization: Bearer <my OpenRouter key>
Body: {"model": "typesafe/jev-1.13", "state": "<the context as plain text>", "questions": {"<name>": {"type": "choice", "instructions": "...", "criteria": {"option_a": "what it means", "option_b": "..."}}, "<name2>": {"type": "noul", "instructions": "<a yes/no question>"}}}
Jev returns answers with probabilities and a confidence score. It never writes text, so use Claude for any writing.

Ask me for my OpenRouter key when you need it and never save it in a file I might share. Run requests in parallel (about 40 at a time) and retry if one fails. Test on 10 items first and show me the results before running everything. Tell me the total Jev cost at the end."""

STARTER114 = """I'm not technical, so please do everything for me and explain each step in plain English.

Use Jev 1.14, TypeSafe's decision model (model id: typesafe/jev-1.14), through OpenRouter's Decisions API:
POST https://openrouter.ai/api/alpha/decisions
Header: Authorization: Bearer <my OpenRouter key>
Body: {"model": "typesafe/jev-1.14", "state": "<the context as plain text>", "questions": {"<name>": {"type": "noul", "instructions": "<a yes/no question>"}, "<name2>": {"type": "choice", "instructions": "...", "criteria": {"option_a": "what it means", "option_b": "..."}}}}
Question types: noul (yes/no), choice (pick one), score (a number, with criteria saying what the low and high ends mean) and box (new in 1.14).
Jev returns answers with probabilities and a confidence score. It never writes text, so use Claude for any writing and any maths.

IMAGES: "state" can also be a list of parts that mixes text and images (PNG or JPEG, sent as base64 data URLs, 256 to 1568 pixels per side, 16 MB max each, stills only, no video). Read the exact format in OpenRouter's Decisions API docs (openrouter.ai/docs/api/reference) before writing any code, and resize big images first.
BOX: finds ONE target in an image and returns top, bottom, left and right as fractions from 0 to 1 (0,0 is the top-left corner), plus a confidence. It takes no criteria. It has no "not found" answer, so always pair it with a noul about the same target and ignore the box when the noul is low.
EARLY FEATURES: TypeSafe says image input, Box and long context are not production-ready, and image answers are less accurate than text answers. Long inputs are slower and less accurate too, so keep each request as short as you can. Nothing here should be treated as final without my review.

Ask me for my OpenRouter key when you need it and never save it in a file I might share. Run requests in parallel (about 20 at a time for images) and retry if one fails. Test on 10 items first and show me the results before running everything. Tell me the total Jev cost at the end."""

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

 dict(id="ad-gatekeeper", tag="new", tagtxt="New in 1.14 · images", title="Ad creative gatekeeper", divider=True, starter="starter114",
  who="Paid media, performance marketers, agencies",
  what="Looks at every ad image before it goes live and flags the ones with unreadable text, a missing logo or no product, so you fix them before you spend a rupee or a dollar on them.",
  proof=[],
  steps=["Put your ad images in one folder (PNG or JPEG).",
         "Write 3 rules in plain words, like: text is readable on a phone, the logo is visible, the product is shown.",
         "Paste the prompt. Claude builds a checker page and Jev answers every rule for every image.",
         "Fix the flagged ones, and look at the low-confidence ones yourself."],
  prompt="""Check my ad images with Jev 1.14 before they go live.
1. Ask me for the folder of ad images (PNG or JPEG) and my 3 rules, for example: the text is readable on a phone, the logo is visible, the product is shown.
2. For each image, ask Jev (noul) one question per rule, such as: "Is every piece of text in this image large enough to read on a phone screen?" Resize large images before sending them.
3. Also ask Jev (score, 1 to 10, with criteria saying what 1 and 10 mean): "How clear is the main message at a glance?"
4. Build me a simple page: a grid of the images with a pass or fail badge per rule, the confidence next to each, and the lowest scores first.
5. For every image that fails, have Claude write a one-line fix. Don't change my images.""",
  honest="Jev checks clarity, not performance. A clear ad can still lose. Image answers are less accurate than text answers, so look at everything it flags and everything it's unsure about."),

 dict(id="ugc-check", tag="new", tagtxt="New in 1.14 · images", title="Creator & UGC brand check", starter="starter114",
  who="Influencer, affiliate and community managers",
  what="Screens creator and affiliate submissions for your logo, competitor logos and other apps' watermarks, then sorts each one into approve, fix or reject, with how sure it is.",
  proof=[],
  steps=["Collect the submissions as images. For a video, export one frame (Claude can do that for you). Jev only reads still images.",
         "Write your rules: which logo must show, which competitors must not.",
         "Paste the prompt. Jev checks every image and sorts them.",
         "Read the fix pile and the low-confidence pile, then send the feedback yourself."],
  prompt="""Screen my creator submissions with Jev 1.14.
1. Ask me for the folder of submissions (PNG or JPEG, one frame per video is fine), my brand name, and the competitors that must not appear.
2. For each image, ask Jev (noul): "Is [my brand] clearly visible?", "Is a competitor's logo visible? [names]" and "Is there a watermark from another app?"
3. Ask Jev (choice): approve, needs a fix, or reject. Use the answers above as the criteria.
4. Put anything Jev is unsure about in a separate "human look" pile.
5. For the "needs a fix" ones only, have Claude draft a friendly feedback message to the creator in my tone. Don't send anything.""",
  honest="Jev sees what's in a picture, not whether the content is good or on-brand in tone. Never reject anyone automatically. A person makes the final call."),

 dict(id="safe-zone", tag="new", tagtxt="New in 1.14 · Box", title="Safe-zone & CTA checker", starter="starter114",
  who="Creative teams, designers, carousel and ad makers",
  what="Finds exactly where your logo, headline and button sit on every creative, then flags the ones that break your layout rules, like a button hidden under the caption.",
  proof=[],
  steps=["Put your creatives in one folder (PNG or JPEG) and note the format (square, 4:5, 9:16).",
         "Write your layout rules, like: nothing important in the bottom 20%, headline in the top half.",
         "Paste the prompt. Jev finds the positions, a small script checks them against your rules.",
         "Open the preview with the boxes drawn on it and confirm the flags by eye."],
  prompt="""Check the layout of my creatives with Jev 1.14's Box question.
1. Ask me for the folder of creatives (PNG or JPEG), the format, and my rules, for example: no logo or button in the bottom 20% (the caption covers it), headline in the top half, button fully inside the frame. For a carousel, also check that the headline sits in the same place on every slide.
2. For each creative, ask Jev (box) one question per item: "Where is the logo?", "Where is the main headline?", "Where is the call-to-action button?" Each answer is top, bottom, left and right as fractions from 0 to 1, plus a confidence.
3. Box always returns a box, even when the thing isn't there. So for each item also ask Jev (noul): "Is there a [logo / headline / button] in this image?" and ignore the box when the noul is low.
4. Write a short script that checks the numbers against my rules (for example, a bottom edge above 0.8 means the item sits in the bottom 20%). Don't ask Jev to do the maths.
5. Show me a table of every creative and which rules it breaks, plus a preview with the boxes drawn on it so I can see what Jev saw.""",
  honest="Box is the newest and least tested part of 1.14 and it can be off. That's why step 5 draws the boxes on your image. Eyeball them before you trust any flag."),

 dict(id="swipe-file", tag="new", tagtxt="New in 1.14 · images", title="Swipe-file sorter", starter="starter114",
  who="Marketers, agencies, founders doing competitor research",
  what="Sorts a pile of saved screenshots into ads, landing pages and posts, then has Claude analyse only the ones with a clear offer, so you read 40 instead of 300.",
  proof=[],
  steps=["Put your saved competitor screenshots in one folder.",
         "List the competitors they come from.",
         "Paste the prompt. Jev filters, then Claude reads only what passed.",
         "Skim a sample of the rejected pile to make sure nothing good got dropped."],
  prompt="""Sort my competitor swipe file with Jev 1.14, then have Claude analyse the best ones.
1. Ask me for the folder of screenshots (PNG or JPEG) and the competitors they come from.
2. For each screenshot, ask Jev (choice): ad, landing page, social post, pricing page or other.
3. Ask Jev (noul): "Is a price or an offer clearly visible?" and "Is there a clear call to action?"
4. Keep only the ones where both are yes, and tell me how many passed and how many were rejected.
5. For the ones that passed, have Claude (not Jev) read each one and write the hook, the angle, the offer and what I could do differently. Group by competitor and finish with the 3 patterns that repeat.""",
  honest="Jev is the cheap filter, Claude is the expensive reader. The filter will miss some good ones, so skim 20 from the rejected pile before you trust it."),

 dict(id="account-risk", tag="new", tagtxt="New in 1.14 · long context", title="Account risk read", starter="starter114",
  who="Sales, account managers, customer success",
  what="Reads one account's whole history (emails, call notes, tickets) in a single request and tells you who may be about to leave, why, and how urgent it is.",
  proof=[],
  steps=["For your most important accounts, put each account's history in one text file, oldest first.",
         "Check your company's privacy rules before sending customer data to any outside service.",
         "Paste the prompt. Jev scores every account.",
         "Call the top of the list this week. Read the middle ones before deciding."],
  prompt="""Find which of my accounts are at risk with Jev 1.14.
1. Ask me for one text file per account with all the emails, call notes and tickets, oldest first. Start with my 20 most important accounts. Trim anything old or irrelevant, because shorter is better for Jev.
2. For each account, ask Jev (noul): "Is this customer at risk of leaving or not renewing?"
3. Ask Jev (choice) for the main reason: price, support problems, low usage, a competitor, a change on their side, or no sign of risk.
4. Ask Jev (score, 1 to 10, with criteria): "How urgent is it to talk to this customer this week?"
5. Sort into "call this week", "look closer" and "fine for now" using Jev's probability (I'll tell you the cut-offs after we see the spread). For the "call this week" ones, have Claude draft a short check-in email for me to approve. Send nothing.""",
  honest="Long context is an early feature: slower and less accurate, and TypeSafe still recommends short inputs. Use it on your top accounts and check every flag before you act."),

 dict(id="multilingual-inbox", tag="new", tagtxt="New in 1.14 · multilingual", title="Multilingual inbox triage", starter="starter114",
  who="Sales, social media managers, brands with a global audience",
  what="Sorts comments, DMs, lead replies and reviews written in any language into buyers, questions, complaints, praise and spam, with urgency, so the hot ones get answered first.",
  proof=[],
  steps=["Export or paste your comments, DMs, replies or reviews into a list.",
         "Try it first on a language you read, with 20 messages you already know the answer to.",
         "Paste the prompt. Jev sorts the original text, no translating first.",
         "Read the drafted replies and approve them yourself, or ask someone who speaks the language."],
  prompt="""Triage my multi-language inbox with Jev 1.14.
1. Help me get my comments, DMs, lead replies or reviews into a list (a CSV or a paste is fine). Send Jev the original text, don't translate it first.
2. For each message, ask Jev (noul): "Is this person showing a buying signal?"
3. Ask Jev (choice): question, complaint, praise, collab or brand deal, or spam.
4. Ask Jev (score, 1 to 10, with criteria): "How urgent is it to reply today?"
5. For the buying signals and questions only, have Claude draft a reply in the same language as the message, for me to approve. Don't send anything. Give me the sorted list, hottest first.""",
  honest="TypeSafe expects multilingual to be the biggest improvement in 1.14, but no benchmark has been published. Test it on a language you read before trusting it, and have a native speaker check any reply you can't read."),
]

NEW114 = """
<section class="block" id="new114">
  <div class="kick">New · Jev 1.14 · released 14 Oct 2026 · preview</div>
  <h2>What changed in Jev 1.14</h2>
  <p class="lede">With 1.14, TypeSafe opened up image input and added a way to find things in a picture. These 6 builds use that. They're early: I haven't tested them the way I tested the first 2, and TypeSafe says the new features aren't production-ready.</p>
  <div class="four">
    <div class="box"><b>📷 Images (early, opt-in)</b><p>Jev can look at a picture and answer yes or no, pick a category or give a score. Ads, creator content and screenshots can be sorted like leads. PNG or JPEG stills only. Documented with this release; per TypeSafe it also works on 1.13.</p></div>
    <div class="box"><b>📍 Box (new, 1.14 only)</b><p>A new question type: it points to where one thing is in an image (a logo, a button) as four edges plus how sure it is. Layout checks become maths.</p></div>
    <div class="box"><b>📚 4x the memory (early, opt-in)</b><p>Up to 262K tokens in one request, up from 64K, so a whole account history fits in one go. It's slower and less accurate, so keep inputs short when you can.</p></div>
    <div class="box"><b>🌍 Better multilingual</b><p>TypeSafe says this is the biggest expected improvement in 1.14. No benchmark has been published yet, so test it on a language you read.</p></div>
  </div>
  <p class="honest"><b>Honest bit:</b> same price as before ($0.042 per million input tokens, output free), but images count as input and every reuse of an image is billed again. The default version (jev-latest) was due to move to 1.14 around 21 Oct. These prompts pin <span class="mono">typesafe/jev-1.14</span> so they keep working either way.</p>
  <div class="promptbox" style="margin-top:18px">
    <div class="pb-head"><span>Setup text for the 6 new builds (included in their copy buttons)</span><button class="copy" data-for="starter114" data-raw="1">Copy</button></div>
    <pre id="starter114">{{STARTER114}}</pre>
  </div>
</section>
"""

TAGCLS = {"built": "t-built", "community": "t-comm", "idea": "t-idea", "new": "t-new"}

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
      <div class="pb-head"><span>Prompt · paste into Claude or Codex</span><button class="copy" data-for="p-{c["id"]}" data-starter="{c.get("starter", "starter")}">Copy prompt</button></div>
      <pre id="p-{c["id"]}">{esc(c["prompt"])}</pre>
    </div>
  </div>
</section>'''

nav = "".join(
    (f'<a href="#new114">New in 1.14</a>' if c.get("divider") else "") + f'<a href="#{c["id"]}">{i:02d} {esc(c["title"])}</a>'
    for i, c in enumerate(CASES, 1))
cards = "".join(
    (NEW114.replace("{{STARTER114}}", esc(STARTER114)) if c.get("divider") else "") + card(i, c)
    for i, c in enumerate(CASES, 1))

page = open("template.html").read().replace("{{NAV}}", nav).replace("{{CARDS}}", cards).replace("{{STARTER}}", esc(STARTER))
open("index.html", "w").write(page)
print("built index.html with", len(CASES), "use cases")
