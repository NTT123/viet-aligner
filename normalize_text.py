"""
Normalize text
"""

import unicodedata

translate = {
    "4": "bốn",
    "4.": "bốn.",
    "4g": "bốn gờ",
    "g7": "gờ bảy",
    "3": "ba",
    "3g": "ba gờ",
    "7": "bảy",
    "9": "chín",
    "20": "hai mươi",
    "80": "tám mươi",
    "1": "một",
    "1.": "một.",
    "2": "hai",
    "2.": "hai.",
    "5": "năm",
    "6": "sáu",
    "8": "tám",
    "8.": "tám.",
    "10": "mười",
    "10.": "mười.",
    "777": "bảy bảy bảy",
    "2-1m": "hai một,",
    "12": "mười hai",
    "13": "mười ba",
    "17": "mười bảy",
    "14": "mười bốn",
    "50": "năm mươi",
    "70": "bảy mươi",
    "600": "sáu trăm",
    "700": "bảy trăm",
}


def normalize_text(text):
    """normalize vn text"""
    text = text.lower().strip()
    text = unicodedata.normalize("NFKC", text)
    for i in "0123456789":
        if i in text:
            t = []
            for w in text.split():
                if w in translate:
                    t.append(translate[w])
                else:
                    t.append(w)
            text = " ".join(t)
            assert i not in text
    return text