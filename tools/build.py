#!/usr/bin/env python3
"""Builds the static Markov's site into /home/claude/markovs-site (run: python3 build.py)."""
import os, re, datetime
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://markovs.example'          # replace with the live domain (see README)
EMAIL = 'workwithmarkov@gmail.com'
DISCORD = 'https://discord.gg/mFfBt4drfa'
TODAY = '24 October 2026'

NAV = [('services.html', 'Services'), ('about.html', 'About'), ('creators.html', 'Creators'), ('contact.html', 'Contact')]
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
UPRIGHT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg>'


def head(title, desc, file, extra=''):
    url = BASE + ('/' if file == 'index.html' else '/' + file)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Markov's">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/img/og-image.png">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="img/favicon.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="css/style.css">
{extra}</head>
<body>
'''


def header(active):
    AC = ' aria-current="page"'
    links = ''.join(f'<a href="{h}"{AC if h == active else ""}>{t}</a>' for h, t in NAV)
    mlinks = ''.join(f'<a href="{h}"{AC if h == active else ""}>{t}</a>' for h, t in [('index.html', 'Home')] + NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="cur" id="cur" aria-hidden="true"></div>
<header class="nav" id="nav">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Markov's home"><img src="img/logo.webp" alt="" width="36" height="36"><span>Markov's</span></a>
    <nav class="links" aria-label="Primary">{links}</nav>
    <a class="btn sm mag" href="contact.html"><span>Start a campaign</span></a>
    <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Open menu"><i></i></button>
  </div>
</header>
<div class="mnav" id="mnav">
  {mlinks}
  <div class="mfoot"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{DISCORD}" target="_blank" rel="noopener">Join our Discord</a></div>
</div>
'''


DISCORD_BAND = f'''<section class="discord" aria-label="Community">
  <div class="wrap">
    <div class="dband">
      <div><div class="eyebrow rv">Community</div><h3 class="rv d1" style="margin-top:16px">Join the Markov's Discord.</h3><p class="rv d2">Talk with the team and with the creators and brands building alongside us.</p></div>
      <a class="btn mag" href="{DISCORD}" target="_blank" rel="noopener"><span>Join on Discord</span>{UPRIGHT}</a>
    </div>
  </div>
</section>
'''

FOOTER = f'''<footer>
  <div class="wrap">
    <div class="fcols">
      <div><a class="logo" href="index.html" aria-label="Markov's home"><img src="img/logo.webp" alt="" width="36" height="36"><span>Markov's</span></a><p class="tag">Ignite your presence.</p></div>
      <div><h4>Explore</h4><ul><li><a href="index.html">Home</a></li><li><a href="services.html">Services</a></li><li><a href="about.html">About</a></li><li><a href="creators.html">Creators</a></li></ul></div>
      <div><h4>Connect</h4><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{DISCORD}" target="_blank" rel="noopener">Discord</a></li><li><a href="contact.html">Start a campaign</a></li></ul></div>
      <div><h4>Legal</h4><ul><li><a href="privacy.html">Privacy</a></li><li><a href="terms.html">Terms</a></li></ul></div>
    </div>
    <div class="fbase"><span>© 2026 Markov's. All rights reserved.</span><span>The finest influencer marketing.</span></div>
  </div>
  <div class="big" aria-hidden="true">Markov's</div>
</footer>
'''


def scripts(*names):
    return ''.join(f'<script src="js/{n}.js" defer></script>\n' for n in ['main', *names]) + '</body>\n</html>\n'


def phero(eyebrow, h1, lede=''):
    p = f'<p class="lede">{lede}</p>' if lede else ''
    return f'''<main id="main">
<section class="phero" aria-label="{eyebrow}">
  <canvas id="web" aria-hidden="true"></canvas>
  <div class="wrap"><div class="eyebrow">{eyebrow}</div><h1>{h1}</h1>{p}</div>
</section>
'''


def cta_band(h='Ready to ignite <em>your presence?</em>', sub=''):
    return f'''<section class="contact" aria-label="Start a campaign">
  <div class="wrap">
    <div class="cbox" style="align-items:center">
      <div><div class="eyebrow rv">Start here</div><h2 class="rv d1" style="margin-top:22px">{h}</h2></div>
      <div class="rv d2"><p style="color:var(--g4);margin:0 0 22px;max-width:420px">{sub or 'Tell us about your brand and what you want to achieve. We read every message.'}</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn mag" href="contact.html"><span>Start a campaign</span>{ARROW}</a><a class="btn ghost mag" href="mailto:{EMAIL}"><span>Email us</span></a></div></div>
    </div>
  </div>
</section>
</main>
'''


def steps(items):
    s = ''.join(f'<div class="step"><span class="dot">{i+1}</span><h3>{t}</h3><p>{p}</p></div>' for i, (t, p) in enumerate(items))
    return f'<div class="steps" id="steps"><div class="rail"><i></i></div>{s}</div>'


PROCESS = [
    ('Understand the brand', 'Product, audience, goal and budget, written down as one clear brief.'),
    ('Match the creators', 'Each creator is ranked against the brief on niche, audience, engagement, price and risk.'),
    ('Agree the deals', 'Professional offers with fees and deliverables stated plainly, and every response tracked.'),
    ('Run the campaign', 'Deadlines, drafts and exceptions handled as they arise, so nothing slips.'),
    ('Verify and learn', 'Delivery is confirmed against the agreement, and the results shape the next campaign.'),
]

FORM = f'''<form class="form rv d2" id="cform" autocomplete="on">
  %%TOPIC%%
  <label for="cn">Your name<input id="cn" name="name" required placeholder="Full name" autocomplete="name"></label>
  <label for="cb">%%BRANDLABEL%%<input id="cb" name="brand" required placeholder="%%BRANDPH%%"></label>
  <label for="cg">What do you want to achieve?<textarea id="cg" name="goal" required placeholder="Launch a product, grow an audience, reach a new market"></textarea></label>
  <button class="btn mag" type="submit"><span>Send by email</span>{ARROW}</button>
  <div class="out" id="cout" role="status" aria-live="polite">This opens your email app with the message ready to send to <b>{EMAIL}</b>.</div>
</form>'''


def form(topic=False):
    t = ''
    if topic:
        t = '''<label for="ct">I am a<select id="ct" name="topic"><option data-key="brand">Brand enquiry</option><option data-key="creator">Creator application</option><option data-key="other">General question</option></select></label>'''
    return FORM.replace('%%TOPIC%%', t).replace('%%BRANDLABEL%%', 'Brand or channel').replace('%%BRANDPH%%', 'Brand, company or channel name')


pages = {}

# ---------------------------------------------------------------- HOME
home_ld = f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"Markov's","slogan":"Ignite your presence","url":"{BASE}/","logo":"{BASE}/img/icon-512.png","email":"{EMAIL}","sameAs":["{DISCORD}"]}}</script>
'''
home = head("Markov's | Ignite your presence", "Markov's is the finest influencer marketing agency for brands that mean to be seen. Finest creators, measured deals, campaigns built to carry on.", 'index.html', home_ld) + header('index.html') + f'''<main id="main">
<section class="hero" aria-label="Introduction">
  <canvas id="web" aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="eyebrow">Influencer marketing, at its finest</div>
    <h1 aria-label="Ignite your presence"><span class="ln"><span>Ignite</span></span><span class="ln"><span>your presence</span></span></h1>
    <p class="lede">Markov's is the finest influencer marketing agency for brands that mean to be seen. Every creator chosen with care. Every deal measured. Every campaign built to carry on.</p>
    <div class="cta"><a class="btn mag" href="contact.html"><span>Start a campaign</span>{ARROW}</a><a class="btn ghost mag" href="#chain"><span>See how the web works</span></a></div>
  </div>
  <div class="hint"><i></i>Move through the web. Click to ignite it.</div>
</section>

<div class="marq" aria-hidden="true"><div class="track" id="track"></div></div>

<section class="statement" aria-label="Our belief">
  <div class="wrap">
    <div class="eyebrow rv">What we believe</div>
    <p id="stmt">We do not rent attention. We build the web of voices that carries a brand from first glance to loyal customer, one finest creator at a time.</p>
  </div>
</section>

<section class="services" id="services">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow rv" style="margin-bottom:22px">Services</div><h2 class="rv d1">Four crafts.<br>One finest standard.</h2></div><p class="rv d2">Everything a brand needs to work with creators well, handled by one team that treats each campaign as its own. <a href="services.html" style="text-decoration:underline;text-underline-offset:3px;color:var(--ink);font-weight:700">See all services</a></p></div>
    <div class="rows">
      <article class="row rv"><span class="idx">I</span><h3>Creator discovery and vetting</h3><p>The finest creators, found through data and confirmed by people. Audience, engagement and risk are checked before a name reaches your shortlist.</p>
        <svg class="ico" viewBox="0 0 64 64" aria-hidden="true"><line x1="14" y1="16" x2="32" y2="34"/><line x1="50" y1="14" x2="32" y2="34"/><line x1="32" y1="34" x2="18" y2="52"/><line x1="32" y1="34" x2="52" y2="50"/><circle cx="14" cy="16" r="5"/><circle cx="50" cy="14" r="5"/><circle cx="18" cy="52" r="5"/><circle cx="52" cy="50" r="5"/><circle class="hub" cx="32" cy="34" r="8"/></svg></article>
      <article class="row rv"><span class="idx">II</span><h3>Campaign strategy</h3><p>A clear brief, a clear budget and a clear plan. We turn your goal into one specification that every creator can read and agree to.</p>
        <svg class="ico" viewBox="0 0 64 64" aria-hidden="true"><line x1="10" y1="32" x2="30" y2="18"/><line x1="30" y1="18" x2="54" y2="30"/><line x1="30" y1="18" x2="34" y2="48"/><line x1="10" y1="32" x2="34" y2="48"/><circle cx="10" cy="32" r="5"/><circle cx="54" cy="30" r="5"/><circle cx="34" cy="48" r="5"/><circle class="hub" cx="30" cy="18" r="8"/></svg></article>
      <article class="row rv"><span class="idx">III</span><h3>Execution and delivery</h3><p>Offers, deadlines, content and proof, followed to the day. You always know where every creator stands.</p>
        <svg class="ico" viewBox="0 0 64 64" aria-hidden="true"><line x1="10" y1="48" x2="26" y2="32"/><line x1="26" y1="32" x2="42" y2="38"/><line x1="42" y1="38" x2="54" y2="14"/><line x1="26" y1="32" x2="30" y2="12"/><circle cx="10" cy="48" r="5"/><circle cx="54" cy="14" r="5"/><circle cx="30" cy="12" r="5"/><circle class="hub" cx="26" cy="32" r="8"/></svg></article>
      <article class="row rv"><span class="idx">IV</span><h3>Performance and learning</h3><p>Every campaign teaches the next one. We report what worked, what did not, and what we will do differently.</p>
        <svg class="ico" viewBox="0 0 64 64" aria-hidden="true"><line x1="12" y1="50" x2="26" y2="36"/><line x1="26" y1="36" x2="38" y2="42"/><line x1="38" y1="42" x2="52" y2="16"/><line x1="26" y1="36" x2="22" y2="14"/><circle cx="12" cy="50" r="5"/><circle cx="52" cy="16" r="5"/><circle cx="22" cy="14" r="5"/><circle class="hub" cx="38" cy="42" r="8"/></svg></article>
    </div>
  </div>
</section>

<section class="chain" id="chain">
  <div class="wrap">
    <div class="panel">
      <div class="eyebrow rv">The web, in motion</div>
      <h2 class="rv d1" style="margin-top:22px">Every audience is a chain.<br>We tune the links.</h2>
      <p class="lead rv d2">A person moves from unaware to customer one state at a time, and each step has a probability. That is a Markov chain, and it is how we think about every campaign. Switch the view and watch the walk change.</p>
      <div class="ctrl">
        <div class="seg" role="group" aria-label="Campaign view"><button id="mA" type="button" aria-pressed="true">Unaided</button><button id="mB" type="button" aria-pressed="false">With Markov's</button></div>
        <div class="readout">Chance of reaching Customer<b id="rate">0%</b></div>
      </div>
      <svg class="chainsvg" id="chainsvg" viewBox="0 0 1000 400" role="img" aria-label="A Markov chain with five audience states. A marker walks from Unaware toward Customer, or drops to Lost, following the transition probabilities shown."></svg>
      <p class="note">Illustrative probabilities for explaining the idea. Not client results.</p>
    </div>
  </div>
</section>

<section class="prin">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow rv" style="margin-bottom:22px">Why Markov's</div><h2 class="rv d1">The finest work<br>is never crowded.</h2></div></div>
    <div class="pgrid">
      <div class="rv"><span class="tag">Selection</span><h3>Chosen, not crowded</h3><p>We would rather put five right creators in front of your audience than fifty loud ones.</p></div>
      <div class="rv d1"><span class="tag">Evidence</span><h3>Measured, not guessed</h3><p>Reach, engagement, audience and risk are weighed with data before anyone is offered a deal.</p></div>
      <div class="rv d2"><span class="tag">Delivery</span><h3>Delivered, not promised</h3><p>Content is checked against the agreement. What was agreed is what goes live.</p></div>
    </div>
  </div>
</section>

<section class="process" id="process">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow rv" style="margin-bottom:22px">Process</div><h2 class="rv d1">From first call<br>to finished campaign.</h2></div><p class="rv d2">Five steps, in this order, every time.</p></div>
    {steps(PROCESS)}
  </div>
</section>

{DISCORD_BAND}
<section class="contact" id="contact">
  <div class="wrap">
    <div class="cbox">
      <div><div class="eyebrow rv">Contact</div><h2 class="rv d1" style="margin-top:22px">Ready to ignite <em>your presence?</em></h2></div>
      {form().replace('Brand or channel','Brand')}
    </div>
  </div>
</section>
</main>
''' + FOOTER + scripts('web', 'chain', 'contact')
pages['index.html'] = home

# ---------------------------------------------------------------- SERVICES
SV = [
    ('I', 'Creator discovery and vetting', 'The finest creators, found through data and confirmed by people. We look for the right audience first and the biggest number second.',
     ['Shortlists built around your niche, audience and country', 'Audience quality, engagement and risk reviewed for every name', 'Fees and expected reach stated before you decide']),
    ('II', 'Campaign strategy', 'A campaign works when everyone reads the same plan. We turn what you want into one written specification.',
     ['One brief covering goal, budget, platforms, countries and deliverables', 'A proposed creator mix and budget split before any outreach', 'A timeline with dates everyone can see']),
    ('III', 'Execution and delivery', 'Once the deals are agreed we keep the work moving, and we keep you informed while we do.',
     ['Professional offers with terms and deliverables written down', 'Deadlines, drafts and approvals tracked in one place', 'Delivery checked against the agreement']),
    ('IV', 'Performance and learning', 'The point of a campaign is what it teaches you. We close every one with a clear account of what happened.',
     ['Reporting on what each creator delivered', 'Plain-language notes on what worked and what did not', 'Findings carried into the next campaign']),
]
sv_html = ''.join(f'''<article class="sdetail rv"><div><span class="idx">{i}</span><h2>{t}</h2></div><div><p>{d}</p><ul class="ticks">{''.join(f'<li>{x}</li>' for x in b)}</ul></div></article>''' for i, t, d, b in SV)
pages['services.html'] = head("Services | Markov's", "Creator discovery and vetting, campaign strategy, execution and delivery, and performance reporting. The finest influencer marketing services from Markov's.", 'services.html') + header('services.html') + phero('Services', 'Four crafts.<br>One finest standard.', 'Everything a brand needs to work with creators well, handled by one team that treats each campaign as its own.') + f'''
<section style="padding-block:clamp(40px,7vh,80px) clamp(60px,9vh,110px)"><div class="wrap">{sv_html}</div></section>
<section class="process" id="process"><div class="wrap">
  <div class="sec-head"><div><div class="eyebrow rv" style="margin-bottom:22px">How we work</div><h2 class="rv d1">From first call<br>to finished campaign.</h2></div><p class="rv d2">Five steps, in this order, every time.</p></div>
  {steps(PROCESS)}
</div></section>
''' + DISCORD_BAND + cta_band() + FOOTER + scripts('web')

# ---------------------------------------------------------------- ABOUT
pages['about.html'] = head("About | Markov's", "Markov's is an influencer marketing agency built on careful craft and clear data. Learn how we work and what we believe.", 'about.html') + header('about.html') + phero('About', 'Built with care.<br>Grown with proof.', "We are building an influencer marketing agency that earns its place one campaign at a time.") + f'''
<section class="statement" aria-label="Our belief"><div class="wrap"><div class="eyebrow rv">What we believe</div>
<p id="stmt">The finest agencies are not the loudest. They are the ones whose brands, creators and results keep coming back.</p></div></section>

<section><div class="wrap split">
  <h2 class="rv">Where we begin,<br>and where we are going.</h2>
  <div class="rv d1"><p>We begin close to the work. We take on campaigns we can do properly, build real relationships with creators, and learn from every result.</p>
  <p>As the relationships, the data and the operation grow, so does what we can offer. The aim is not to stay a standard agency. It is to build something much larger on a base of finest work.</p>
  <p>Our name comes from the Markov chain, a way of describing how one state leads to the next. It is how we think about audiences, and about growing a business.</p></div>
</div></section>

<section class="prin"><div class="wrap">
  <div class="sec-head"><div><div class="eyebrow rv" style="margin-bottom:22px">Principles</div><h2 class="rv d1">What we hold to.</h2></div></div>
  <div class="pgrid">
    <div class="rv"><span class="tag">Selection</span><h3>Chosen, not crowded</h3><p>A small number of right creators beats a large number of loud ones.</p></div>
    <div class="rv d1"><span class="tag">Evidence</span><h3>Measured, not guessed</h3><p>We weigh data first, then use judgement on top of it.</p></div>
    <div class="rv d2"><span class="tag">Delivery</span><h3>Delivered, not promised</h3><p>Agreed terms are the standard we hold ourselves and every creator to.</p></div>
  </div>
</div></section>
''' + DISCORD_BAND + cta_band() + FOOTER + scripts('web')

# ---------------------------------------------------------------- CREATORS
CR = [('Introduce yourself', 'Tell us about your channel, your audience and the kind of work you enjoy.'),
      ('Get matched', 'When a brand fits your niche and audience, we bring it to you with the details up front.'),
      ('Agree the terms', 'Fee, deliverables and dates are written down and agreed before any work starts.'),
      ('Create', 'Make the content in your own voice. We handle the logistics around it.'),
      ('Close out', 'Delivery is checked against what was agreed, and we talk through how it went.')]
pages['creators.html'] = head("For creators | Markov's", "Work with brands worth your audience. Markov's matches creators with campaigns on clear terms. Introduce yourself to our team.", 'creators.html') + header('creators.html') + phero('For creators', 'Brands worth<br>your audience.', 'We match creators with campaigns that fit their niche and their viewers, on terms that are clear from the first message.') + f'''
<section class="prin" style="padding-top:clamp(50px,8vh,90px)"><div class="wrap">
  <div class="pgrid">
    <div class="rv"><span class="tag">Fit</span><h3>The right brand</h3><p>We bring you campaigns that suit your niche and your audience, not every offer that exists.</p></div>
    <div class="rv d1"><span class="tag">Clarity</span><h3>Terms up front</h3><p>Fee, deliverables and timeline are stated in the first offer, so you can decide with the full picture.</p></div>
    <div class="rv d2"><span class="tag">Respect</span><h3>Your voice, kept</h3><p>You know your audience best. Briefs set the goal, and you decide how to say it.</p></div>
  </div>
</div></section>
<section class="process" id="process"><div class="wrap">
  <div class="sec-head"><div><div class="eyebrow rv" style="margin-bottom:22px">How it works</div><h2 class="rv d1">From hello<br>to a finished deal.</h2></div><p class="rv d2">Five steps, in this order.</p></div>
  {steps(CR)}
</div></section>
<section class="contact"><div class="wrap"><div class="cbox" style="align-items:center">
  <div><div class="eyebrow rv">Apply</div><h2 class="rv d1" style="margin-top:22px">Introduce <em>yourself.</em></h2></div>
  <div class="rv d2"><p style="color:var(--g4);margin:0 0 22px;max-width:420px">Send us your channel and a few lines about what you make. We read every message, and we will come back when a campaign fits.</p>
  <div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn mag" href="contact.html?topic=creator"><span>Apply to join</span>{ARROW}</a><a class="btn ghost mag" href="{DISCORD}" target="_blank" rel="noopener"><span>Join our Discord</span></a></div></div>
</div></div></section>
</main>
''' + FOOTER + scripts('web')

# ---------------------------------------------------------------- CONTACT
pages['contact.html'] = head("Contact | Markov's", "Start a campaign or apply as a creator. Email Markov's at workwithmarkov@gmail.com or join our Discord.", 'contact.html') + header('contact.html') + phero('Contact', 'Let us ignite<br>your presence.', 'Tell us about your brand or your channel. We read every message.') + f'''
<section><div class="wrap"><div class="cgrid">
  {form(True)}
  <div class="cinfo rv d1">
    <div><span class="k">Email</span><a class="big-link" href="mailto:{EMAIL}">{EMAIL}</a><p><button type="button" class="linkbtn" data-copy="{EMAIL}">Copy address</button></p></div>
    <div><span class="k">Community</span><a class="big-link" href="{DISCORD}" target="_blank" rel="noopener">Join our Discord</a><p>Talk with the team and with other creators and brands.</p></div>
    <div><span class="k">Good to include</span><p style="margin-top:0">For brands: your product, your target audience and countries, and a rough budget. For creators: your channel link, niche and typical views.</p></div>
  </div>
</div></div></section>
</main>
''' + FOOTER + scripts('web', 'contact')

# ---------------------------------------------------------------- LEGAL
def legal(file, title, desc, h1, body):
    return head(title, desc, file) + header('') + f'''<main id="main">
<section class="phero" aria-label="{h1}"><canvas id="web" aria-hidden="true" style="opacity:.5"></canvas><div class="wrap"><div class="eyebrow">Legal</div><h1 style="font-size:clamp(40px,7vw,108px)">{h1}</h1></div></section>
<div class="wrap"><div class="prose"><p class="upd">Last updated {TODAY}</p>{body}</div></div>
</main>
''' + FOOTER + scripts('web')

pages['privacy.html'] = legal('privacy.html', "Privacy | Markov's", "How Markov's handles information on this website.", 'Privacy', f'''
<p>This page explains what information Markov's ("we", "us") handles when you use this website.</p>
<h2>What this site collects</h2>
<p>This site does not run accounts, analytics or advertising trackers, and it does not store what you type into its contact form. The form opens your own email app with a message addressed to us. Nothing is sent until you send it from your email app.</p>
<h2>Information you send us</h2>
<p>If you email us, we receive the details you include, such as your name, your brand or channel and your message. We use them to reply to you and to assess whether we can work together. We do not sell them.</p>
<h2>Third-party services</h2>
<ul><li><b>Google Fonts</b> supplies the typeface used on this site. Your browser requests it from Google, which can see your IP address and browser details.</li><li><b>Discord</b> is linked from this site. If you follow the link, Discord's own terms and privacy policy apply.</li></ul>
<h2>Your choices</h2>
<p>You can ask us to correct or delete the emails you have sent us by writing to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Changes</h2>
<p>If we change how this site works, we will update this page and its date.</p>
<h2>Contact</h2>
<p>Questions about this page: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''')

pages['terms.html'] = legal('terms.html', "Terms | Markov's", "Terms of use for the Markov's website.", 'Terms', f'''
<p>By using this website you agree to these terms. If you do not agree, please do not use it.</p>
<h2>About this site</h2>
<p>This site describes the services of Markov's and lets you contact us. Information here is general and may change. It is not an offer, and any work we do together is governed by a separate written agreement.</p>
<h2>Intellectual property</h2>
<p>The Markov's name, logo, design and content on this site belong to Markov's. Please do not copy or reuse them without our written permission.</p>
<h2>Acceptable use</h2>
<p>Please do not misuse the site, attempt to disrupt it, or use it to send us unlawful or abusive material.</p>
<h2>Links to other sites</h2>
<p>This site links to services we do not control, such as Discord. We are not responsible for their content or practices.</p>
<h2>No warranty</h2>
<p>We work to keep the site accurate and available, but we provide it as it is, without promises that it will be error-free or uninterrupted. Examples and illustrative figures, including those in the Markov chain section, are for explanation only and are not results for any client.</p>
<h2>Changes</h2>
<p>We may update these terms. The date above shows the latest version.</p>
<h2>Contact</h2>
<p>Questions about these terms: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''')

# ---------------------------------------------------------------- 404
pages['404.html'] = head("Page not found | Markov's", "This page could not be found.", '404.html', '<meta name="robots" content="noindex">\n') + header('') + f'''<main id="main">
<section class="nf"><canvas id="web" aria-hidden="true"></canvas><div class="wrap" style="position:relative;z-index:2"><div class="eyebrow">Lost in the web</div><h1>404</h1><p>That page is not part of the web. Head back to the start and pick up the thread.</p><a class="btn mag" href="index.html"><span>Back to home</span>{ARROW}</a></div></section>
</main>
''' + FOOTER + scripts('web')

# ---------------------------------------------------------------- write
for f, html in pages.items():
    open(os.path.join(OUT, f), 'w').write(html)

open(os.path.join(OUT, 'site.webmanifest'), 'w').write('''{
  "name": "Markov's",
  "short_name": "Markov's",
  "description": "Ignite your presence.",
  "start_url": "/",
  "display": "browser",
  "background_color": "#ffffff",
  "theme_color": "#ffffff",
  "icons": [
    {"src": "img/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "img/icon-512.png", "sizes": "512x512", "type": "image/png"}
  ]
}
''')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
iso = datetime.date(2026, 10, 24).isoformat()
urls = ['index.html', 'services.html', 'about.html', 'creators.html', 'contact.html', 'privacy.html', 'terms.html']
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'  <url><loc>{BASE}{"/" if u=="index.html" else "/"+u}</loc><lastmod>{iso}</lastmod></url>\n' for u in urls) + '</urlset>\n'
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)
open(os.path.join(OUT, '_headers'), 'w').write('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=()

/css/*
  Cache-Control: public, max-age=3600
/js/*
  Cache-Control: public, max-age=3600
/img/*
  Cache-Control: public, max-age=604800
''')
print('built', len(pages), 'pages')
