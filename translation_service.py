import urllib.request
import json

def translate_text(text, target_lang='es'):
    if not text or not text.strip():
        return text
    
    try:
        import urllib.parse
        lang_pair = f"en|{target_lang}"
        query = urllib.parse.quote(text)
        url = f"https://api.mymemory.translated.net/get?q={query}&langpair={lang_pair}"
        
        response = urllib.request.urlopen(url, timeout=10)
        data = json.loads(response.read().decode())
        
        if data.get('responseStatus') == 200:
            return data.get('responseData', {}).get('translatedText', text)
        
        return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def translate_html(html_content, target_lang='es'):
    return translate_text(html_content, target_lang)
