from googletrans import LANGUAGES

code_to_lang = LANGUAGES
lang_to_code = {lang: code for code, lang in LANGUAGES.items()}
languages = list(lang_to_code.keys())