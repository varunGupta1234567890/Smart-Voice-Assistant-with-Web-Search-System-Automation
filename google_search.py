import requests
from urllib.parse import quote

SERPER_API_KEY = "fb58304413a22c3b9e56163605edeaf66deec083"

cache = {}
def google_answer(query):
    query = query.strip.lower()
    if query in cache:
        return cache[query]

    try:
        wiki_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + quote(query)
        wiki_res = requests.get(wiki_url, timeout=4)

        if wiki_res.status_code == 200:
            wiki_data = wiki_res.json()

            extract = wiki_data.get("extract", "")
            if extract and len(extract) > 80:
                result = extract[:500]  # limit size
                cache[query] = result
                return result

        serper_url = "https://google.serper.dev/search"
        payload = {"q": query}

        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        res = requests.post(serper_url, json=payload, headers=headers, timeout=5)

        if res.status_code != 200:
            return None

        data = res.json()

        final_text = ""

        if "answerBox" in data:
            ans = data["answerBox"].get("answer") or data["answerBox"].get("snippet")
            if ans:
                final_text += ans + " "

        if "organic" in data:
            for item in data["organic"][:2]:
                snippet = item.get("snippet")
                if snippet:
                    final_text += snippet + " "

        if len(final_text) > 50:
            result = final_text.strip()[:600]
            cache[query]=result
            return result

        ddg_url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json"}

        res = requests.get(ddg_url, params=params, timeout=5)
        data = res.json()

        if data.get("AbstractText"):
            return data["AbstractText"]

        if data.get("RelatedTopics"):
            for topic in data["RelatedTopics"]:
                if isinstance(topic, dict) and topic.get("Text"):
                    result = topic["Text"][:500]
                    cache[query]=result
                    return result

        return None

    except Exception as e:
        print("Error:", e)
        return None