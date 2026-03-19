import json
import os
from flask import current_app

translations_cache = {}


def load_translations(lang):
    if lang in translations_cache:
        return translations_cache[lang]

    trans_dir = os.path.join(os.path.dirname(__file__), "translations")
    trans_file = os.path.join(trans_dir, f"{lang}.json")

    if os.path.exists(trans_file):
        with open(trans_file, "r", encoding="utf-8") as f:
            translations_cache[lang] = json.load(f)
            return translations_cache[lang]

    return {}


def get_translation(key, lang="en"):
    trans = load_translations(lang)
    return trans.get(key, key)


def inject_translations():
    from flask import session, request, g

    if "lang" in session:
        lang = session["lang"]
    elif hasattr(g, "lang"):
        lang = g.lang
    else:
        lang = request.accept_languages.best_match(["en", "es"]) or "en"

    return {"t": lambda key: get_translation(key, lang), "current_lang": lang}
