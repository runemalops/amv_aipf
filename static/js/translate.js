async function translateToSpanish(text, endpoint) {
    const response = await fetch(endpoint, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        credentials: 'include',
        body: JSON.stringify({text: text, target_lang: 'es'})
    });
    const data = await response.json();
    return data.translated;
}

async function handleTranslate(btn, translateFn) {
    btn.disabled = true;
    btn.textContent = 'Translating...';
    try {
        await translateFn();
    } catch (e) {
        alert('Translation failed. Please try again.');
    }
    btn.disabled = false;
    btn.textContent = 'Auto-Translate from English';
}
