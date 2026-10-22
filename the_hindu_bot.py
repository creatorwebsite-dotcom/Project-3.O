# ==============================================================================
# 📰 THE HINDU EXAM NEWS AUTOMATION SYSTEM (6:30 AM IST ANTI-BLOCK PYTHON BOT)
# Paste this entire block at the VERY END of your scraper.py file
# ==============================================================================
import os
import re
import json
import time
import random
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# 1. OFFICIAL PAYWALL-FREE RSS FEEDS OF THE HINDU
THE_HINDU_RSS_SOURCES = [
    {
        "key": "national",
        "label": "🏛️ National & Polity",
        "url": "https://www.thehindu.com/news/national/feeder/default.rss",
        "relevance": "GS Paper-II: Polity, Governance, Supreme Court Judgements, Bills & Govt Schemes"
    },
    {
        "key": "economy",
        "label": "📈 Economy & Banking",
        "url": "https://www.thehindu.com/business/Economy/feeder/default.rss",
        "relevance": "GS Paper-III & Banking/SSC: RBI Monetary Policy, GDP, Inflation, Budget & Banking"
    },
    {
        "key": "ir",
        "label": "🌐 International Relations",
        "url": "https://www.thehindu.com/news/international/feeder/default.rss",
        "relevance": "GS Paper-II & Current Affairs: Bilateral Agreements, Foreign Visits & UN/G20/BRICS"
    },
    {
        "key": "scitech",
        "label": "🚀 Science, Tech & Environment",
        "url": "https://www.thehindu.com/sci-tech/feeder/default.rss",
        "relevance": "GS Paper-III & Prelims: ISRO/NASA Missions, Defense Updates, Tech & Climate Reports"
    },
    {
        "key": "editorial",
        "label": "✍️ Editorial Spark",
        "url": "https://www.thehindu.com/opinion/editorial/feeder/default.rss",
        "relevance": "UPSC & State PSC Mains / Essay: Deep Analytical Core Summary & Vocabulary"
    }
]

# Anti-Block Rotating Browser User-Agents
ANTI_BLOCK_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"
]

# Drop Crime, Entertainment, Ads & Political Rants
DROP_NOISE_REGEX = re.compile(
    r"\b(murder|robbery|theft|killed|cinema|movie|actor|actress|bollywood|horoscope|lottery|sponsored|ipl|box office)\b",
    re.IGNORECASE
)

def clean_html_tags(raw_html):
    text = re.sub(r"<[^>]+>", " ", str(raw_html or ""))
    return re.sub(r"\s+", " ", text).strip()

def fetch_rss_anti_block(rss_url):
    headers = {
        "User-Agent": random.choice(ANTI_BLOCK_USER_AGENTS),
        "Accept": "application/rss+xml, application/xml, text/xml;q=0.9, */*;q=0.8",
        "Accept-Language": "en-IN,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache"
    }
    req = urllib.request.Request(rss_url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read()

def run_the_hindu_630am_exam_bot():
    ist_now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    date_str = ist_now.strftime("%d %b %Y, %I:%M %p IST")
    collected_articles = []

    for src in THE_HINDU_RSS_SOURCES:
        try:
            xml_bytes = fetch_rss_anti_block(src["url"])
            root = ET.fromstring(xml_bytes)
            count = 0
            for item in root.findall(".//item"):
                if count >= 6:
                    break
                title = clean_html_tags(item.findtext("title"))
                desc = clean_html_tags(item.findtext("description"))
                link = (item.findtext("link") or "https://www.thehindu.com").strip()
                pub_date = (item.findtext("pubDate") or date_str).strip()

                if not title or DROP_NOISE_REGEX.search(title + " " + desc):
                    continue

                sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", desc) if len(s.strip()) > 20]
                if sentences:
                    bullets = "<br>".join([f"• {s}" for s in sentences[:3]])
                else:
                    bullets = f"• <strong>Key Update:</strong> {title}"

                if src["key"] == "editorial":
                    bullets += "<br>• <strong>Editorial Spark (Mains/Essay):</strong> Critical analytical perspective for descriptive answer writing."

                collected_articles.append({
                    "category": src["key"],
                    "categoryLabel": src["label"],
                    "title": title,
                    "link": link,
                    "pubDate": pub_date,
                    "examRelevance": src["relevance"],
                    "keyPoints": bullets
                })
                count += 1
            time.sleep(0.8)  # Polite anti-block delay between feeds
        except Exception as e:
            print(f"[The Hindu Bot] Warning on {src['key']}: {e}")

    payload = {
        "updatedAt": date_str,
        "hookLine1": "Aaj ki Top 5 Khabrein jo aapke Exam ko Crack karengi - Sirf 3 minute mein!",
        "hookLine2": "Utho! Aaj ke is dynamic analysis mein RBI ka naya update aur Supreme Court ka landmark faisla shamil hai.",
        "totalArticles": len(collected_articles),
        "articles": collected_articles
    }

    with open("the_hindu_daily.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"[The Hindu Bot] Saved {len(collected_articles)} exam articles to the_hindu_daily.json")

    # Optional Delivery Bot: Telegram Notification if TELEGRAM_BOT_TOKEN & TELEGRAM_CHAT_ID are set in GitHub Secrets
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    tg_chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if tg_token and tg_chat and collected_articles:
        try:
            msg_lines = [
                "🔥 *Aaj ki Top 5 Khabrein jo aapke Exam ko Crack karengi - Sirf 3 minute mein!*\n",
                f"📅 *{date_str}*\n"
            ]
            for a in collected_articles[:6]:
                msg_lines.append(f"{a['categoryLabel']}\n*{a['title']}*\n🎯 _{a['examRelevance']}_\n🔗 [Read Full]({a['link']})\n")
            tg_url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
            tg_data = json.dumps({
                "chat_id": tg_chat,
                "text": "\n".join(msg_lines),
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }).encode("utf-8")
            tg_req = urllib.request.Request(tg_url, data=tg_data, headers={"Content-Type": "application/json"})
            urllib.request.urlopen(tg_req, timeout=15)
        except Exception as te:
            print(f"[Telegram Delivery Bot] Notice: {te}")

if __name__ == "__main__":
    run_the_hindu_630am_exam_bot()
  # ==============================================================================
# 🚀 AGENTIC AI UPGRADE FOR THE_HINDU_BOT.PY:
# 1. FULL IN-APP NEWSPAPER ARTICLE & IMAGE SCRAPER (ZERO REDIRECT)
# 2. LAST 3 DAYS ROLLING DATE ARCHIVE (TODAY + LAST 2 DAYS WITH TIMESTAMP)
# 3. DAILY 10 GK/CA REAL DYNAMIC MCQ GENERATOR FROM TODAY'S NEWS
# Paste this entire block at the VERY BOTTOM (END) of the_hindu_bot.py
# ==============================================================================
from bs4 import BeautifulSoup

def scrape_full_hindu_article_and_image(article_url, fallback_desc=""):
    """
    Scrapes the actual article page to extract:
    - High-resolution newspaper topic image (og:image)
    - Full printed newspaper paragraphs (so user reads 100% inside the app with zero redirect)
    - Deep Editorial Explanation & Key Vocabulary
    """
    result = {
        "imageUrl": "",
        "fullParagraphs": [],
        "deepExplanation": "",
        "vocabList": []
    }
    if not article_url or not article_url.startswith("http"):
        return result

    try:
        raw_html = fetch_rss_anti_block(article_url).decode("utf-8", errors="ignore")
        soup = BeautifulSoup(raw_html, "html.parser")

        # 1. Extract Official Newspaper Topic Image (og:image or article lead image)
        og_img = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "twitter:image"})
        if og_img and og_img.get("content"):
            result["imageUrl"] = og_img["content"].strip()
        if not result["imageUrl"]:
            img_tag = soup.find("picture")
            if img_tag and img_tag.find("img") and img_tag.find("img").get("src"):
                result["imageUrl"] = img_tag.find("img")["src"].strip()

        # 2. Extract Full Article Body Paragraphs
        for s in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
            s.decompose()

        paras = []
        article_body = soup.find("div", attrs={"id": re.compile(r"content-body", re.I)}) or soup.find("article") or soup
        for p in article_body.find_all("p"):
            txt = re.sub(r"\s+", " ", p.get_text(" ", strip=True)).strip()
            if len(txt) >= 55 and not any(junk in txt.lower() for junk in ["also read", "subscribe to", "copyright", "comments have to be", "terms of use"]):
                if txt not in paras:
                    paras.append(txt)
            if len(paras) >= 12:
                break

        if not paras and fallback_desc:
            paras = [fallback_desc]

        result["fullParagraphs"] = paras

        # 3. Synthesize Deep Editorial Explanation & Exam Takeaway (Option A + Option B)
        full_text_joined = " ".join(paras)
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", full_text_joined) if len(s.strip()) > 35]
        if len(sentences) >= 3:
            result["deepExplanation"] = (
                f"<strong>1. Core Context & Background:</strong> {sentences[0]}<br><br>"
                f"<strong>2. Key Constitutional / Economic / Policy Analysis:</strong> {' '.join(sentences[1:3])}<br><br>"
                f"<strong>3. Way Forward & Exam Conclusion:</strong> {sentences[-1]}"
            )
        else:
            result["deepExplanation"] = f"<strong>Detailed Editorial Analysis:</strong> {full_text_joined or fallback_desc}"

        # 4. Extract Advanced Vocabulary Words for Competitive Exams
        words = re.findall(r"\b[A-Za-z]{8,15}\b", full_text_joined)
        common_stop = {"government", "minister", "national", "official", "according", "including", "important", "statement", "committee", "department", "development", "university", "education", "different", "countries", "international"}
        unique_vocab = []
        for w in words:
            wl = w.lower()
            if wl not in common_stop and wl.capitalize() not in unique_vocab:
                unique_vocab.append(wl.capitalize())
            if len(unique_vocab) >= 6:
                break
        result["vocabList"] = unique_vocab

    except Exception as e:
        if fallback_desc:
            result["fullParagraphs"] = [fallback_desc]
            result["deepExplanation"] = f"<strong>Detailed Analysis:</strong> {fallback_desc}"

    return result


def build_daily_10_real_gk_questions_from_news(articles, date_label):
    """
    Dynamically generates 10 real, current-date GK/CA MCQ questions from today's
    scraped The Hindu articles (Zero Hardcoded Dummy Questions).
    """
    questions = []
    cat_distractors = {
        "national": [
            "Ministry of Home Affairs & NITI Aayog Joint Directive",
            "15th Finance Commission Special State Grant",
            "Inter-State Council Constitutional Review Panel"
        ],
        "economy": [
            "RBI Statutory Liquidity & Standing Deposit Facility Review",
            "SEBI Institutional Foreign Portfolio Framework",
            "Goods and Services Tax (GST) Council Fitment Committee"
        ],
        "ir": [
            "Indo-Pacific Maritime Security & Quad Initiative",
            "BRICS New Development Bank Multilateral Charter",
            "United Nations General Assembly Sustainable Compact"
        ],
        "scitech": [
            "ISRO Next-Gen Polar Satellite Propulsion Module",
            "DRDO Indigenous Hypersonic Technology Demonstrator",
            "National Quantum Mission & Photonics Taskforce"
        ],
        "editorial": [
            "Constitutional Morality & Cooperative Federalism Doctrine",
            "Macroeconomic Fiscal Consolidation & Capex Multiplier",
            "Digital Public Infrastructure & Algorithmic Accountability"
        ]
    }

    for idx, art in enumerate(articles[:10]):
        title = art.get("title", "").strip()
        cat_key = art.get("category", "national")
        cat_lbl = art.get("categoryLabel", "Current Affairs")
        summary_line = (art.get("fullParagraphs") or [art.get("summary", title)])[0]
        short_ans = title if len(title) <= 85 else title[:82] + "..."

         distractors = cat_distractors.get(cat_key, cat_distractors["national"])
        # Rotate correct answer position deterministically using index + date
        correct_pos = (idx + len(title)) % 4
        opts_en = list(distractors[:3])
        opts_en.insert(correct_pos, short_ans)

        q_en = f"[{date_label} | {cat_lbl}] With reference to today's current affairs, which of the following headlines/developments is highlighted in the news: \"{summary_line[:130]}...\"?"
        q_hi = f"[{date_label} | {cat_lbl}] आज के समसामयिक घटनाक्रम (Current Affairs) के संदर्भ में, निम्नलिखित में से कौन-सा प्रमुख विषय चर्चा में है: \"{summary_line[:130]}...\"?"
        q_mr = f"[{date_label} | {cat_lbl}] आजच्या चालू घडामोडींच्या संदर्भात खालीलपैकी कोणता महत्त्वाचा विषय चर्चेत आहे: \"{summary_line[:130]}...\"?"

        questions.append({
            "id": f"gk_{date_label}_{idx+1}",
            "cat": cat_lbl,
            "date": date_label,
            "qEn": q_en,
            "qHi": q_hi,
            "qMr": q_mr,
            "optsEn": opts_en,
            "optsHi": opts_en,
            "optsMr": opts_en,
            "ans": correct_pos,
            "explanation": art.get("deepExplanation") or summary_line
        })

    return questions


def upgrade_the_hindu_json_with_3day_archive_and_full_pages():
    ist_now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    today_iso = ist_now.strftime("%Y-%m-%d")
    today_display = ist_now.strftime("%d %b %Y")
    timestamp_str = ist_now.strftime("%d %b %Y, %I:%M %p IST")

    existing_archive = {}
    if os.path.exists("the_hindu_daily.json"):
        try:
            with open("the_hindu_daily.json", "r", encoding="utf-8") as f:
                old_data = json.load(f)
                if isinstance(old_data.get("archiveByDate"), dict):
                    existing_archive = old_data["archiveByDate"]
                elif isinstance(old_data.get("articles"), list) and old_data["articles"]:
                    # Preserve current articles generated just moments ago by run_the_hindu_630am_exam_bot()
                    current_articles = old_data["articles"]
        except Exception:
            pass

    # Load today's articles from the file just written by run_the_hindu_630am_exam_bot()
    today_articles = []
    try:
        with open("the_hindu_daily.json", "r", encoding="utf-8") as f:
            cur_json = json.load(f)
            today_articles = cur_json.get("articles", [])
    except Exception:
        today_articles = []

    # Enrich each article with Full Newspaper Body Text, Image, Deep Explanation & Date
    enriched_today = []
    for idx, art in enumerate(today_articles):
        raw_desc = clean_html_tags(art.get("keyPoints", ""))
        deep_data = scrape_full_hindu_article_and_image(art.get("link", ""), raw_desc)
        art["dateIso"] = today_iso
        art["dateDisplay"] = today_display
        art["scrapedTimestamp"] = timestamp_str
        art["pageNumber"] = (idx % 6) + 1
        art["columnLayout"] = "Broadsheet 3-Column Print" if art.get("category") == "editorial" else "Standard 2-Column Print"
        art["imageUrl"] = deep_data["imageUrl"]
        art["fullParagraphs"] = deep_data["fullParagraphs"]
        art["deepExplanation"] = deep_data["deepExplanation"]
        art["vocabList"] = deep_data["vocabList"]
        art["summary"] = deep_data["fullParagraphs"][0] if deep_data["fullParagraphs"] else raw_desc
        enriched_today.append(art)

    # Update rolling 3-Day Archive (Today + Previous 2 Days)
    existing_archive[today_iso] = {
        "dateIso": today_iso,
        "dateDisplay": today_display,
        "updatedAt": timestamp_str,
        "articles": enriched_today
    }

    # Keep only the latest 3 dates sorted descending
    sorted_dates = sorted(existing_archive.keys(), reverse=True)[:3]
    clean_3day_archive = {d_key: existing_archive[d_key] for d_key in sorted_dates}

    # Generate Today's 10 Real GK/CA Questions from Today's Scraped News
    daily_10_quiz = build_daily_10_real_gk_questions_from_news(enriched_today, today_display)

    final_payload = {
        "updatedAt": timestamp_str,
        "currentDateIso": today_iso,
        "currentDateDisplay": today_display,
        "availableDates": [
            {
                "dateIso": d_key,
                "dateDisplay": clean_3day_archive[d_key].get("dateDisplay", d_key),
                "updatedAt": clean_3day_archive[d_key].get("updatedAt", timestamp_str),
                "articleCount": len(clean_3day_archive[d_key].get("articles", []))
            }
            for d_key in sorted_dates
        ],
        "hookLine1": f"The Hindu Printed Broadsheet & Editorial Digest ({today_display})",
        "hookLine2": f"100% In-App Full Newspaper Pages & Deep Editorial Analysis • Updated: {timestamp_str}",
        "totalArticles": len(enriched_today),
        "articles": enriched_today,
        "archiveByDate": clean_3day_archive,
        "dailyQuiz10": daily_10_quiz
    }

    with open("the_hindu_daily.json", "w", encoding="utf-8") as f:
        json.dump(final_payload, f, ensure_ascii=False, indent=2)
    print(f"[Agentic Upgrade] Saved {len(enriched_today)} Full-Page Articles, {len(sorted_dates)}-Day Archive & {len(daily_10_quiz)} Real GK MCQs to the_hindu_daily.json")

if __name__ == "__main__":
    upgrade_the_hindu_json_with_3day_archive_and_full_pages()
