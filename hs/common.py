import re

def get_keywords(text):
    keywords = ""
    pattern = re.compile(r'<b>([^</b>]*)</b>')
    results = pattern.findall(text)
    if results:
        keys = set() 
        for r in results:
            r = r.replace("：", "").split("，")
            for key in r:
                keys.add(key)
        keywords = ",".join(keys)
    return keywords