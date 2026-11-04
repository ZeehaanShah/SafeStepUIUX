"""'Ask Before You Click' — looks for common scam warning signs in English, Hindi and Marathi messages."""
import html
import re

RULES = [
    dict(k="urgent", w=2, re=re.compile(r"urgent|immediately|today|right now|\bnow\b|within \d+|blocked|block|suspend|expire|last chance|tonight|जल्दी|तुरंत|अभी|आज|बंद|तातडीने|लगेच|आत्ताच|बंद होईल|मुदत", re.I),
         t=["Creates urgency", "जल्दबाज़ी पैदा करता है", "घाई निर्माण करतो"],
         d=["It pushes you to act before you have time to think.", "यह आपको सोचने का समय दिए बिना कदम उठाने पर मजबूर करता है।", "विचार करायला वेळ मिळण्याआधीच तो तुम्हाला काहीतरी करायला भाग पाडतो."]),
    dict(k="link", w=2, re=re.compile(r"https?://\S+|www\.\S+|bit\.ly\S*|tinyurl\S*|\.(in|com|co|xyz|top|link|info)\b/?|\[link\]|click here|लिंक|क्लिक", re.I),
         t=["Asks you to click a link", "लिंक पर क्लिक करने को कहता है", "लिंकवर क्लिक करायला सांगतो"],
         d=["Links in unexpected messages often lead to fake pages. Open the official app instead.", "अनचाहे संदेशों के लिंक अक्सर नकली पेज पर ले जाते हैं। इसकी जगह आधिकारिक ऐप खोलें।", "अनपेक्षित संदेशांतील लिंक अनेकदा बनावट पानांवर नेतात. त्याऐवजी अधिकृत ॲप उघडा."]),
    dict(k="code", w=3, re=re.compile(r"\botp\b|\bpin\b|password|cvv|card number|ओटीपी|पिन|पासवर्ड", re.I),
         t=["Asks for a code or PIN", "कोड या पिन मांगता है", "कोड किंवा पिन मागतो"],
         d=["No bank, courier or government office ever needs your OTP or PIN.", "कोई भी बैंक, कूरियर या सरकारी दफ्तर कभी आपका OTP या पिन नहीं मांगता।", "कोणतीही बँक, कुरिअर किंवा सरकारी कार्यालय कधीही तुमचा OTP किंवा पिन मागत नाही."]),
    dict(k="money", w=1, re=re.compile(r"₹|\brs\.?\s?\d|rupees|prize|won|winner|lottery|refund|cashback|fee|pay |payment|invest|double|इनाम|रिफंड|फ़ीस|फीस|भुगतान|पैसे|जीत|बक्षीस|शुल्क|जिंकल|पेमेंट", re.I),
         t=["Talks about money or prizes", "पैसे या इनाम की बात करता है", "पैसे किंवा बक्षिसाबद्दल बोलतो"],
         d=["Unexpected prizes, refunds or small fees are common bait.", "अचानक इनाम, रिफंड या छोटी फ़ीस आम चारा हैं।", "अचानक बक्षीस, रिफंड किंवा छोटे शुल्क हे नेहमीचे आमिष असते."]),
    dict(k="generic", w=1, re=re.compile(r"dear (customer|user|sir|madam)|valued customer|प्रिय ग्राहक", re.I),
         t=["Doesn’t use your name", "आपका नाम इस्तेमाल नहीं करता", "तुमचे नाव वापरत नाही"],
         d=["Real messages from your bank usually address you by name.", "आपके बैंक के असली संदेश आमतौर पर आपका नाम लेते हैं।", "तुमच्या बँकेचे खरे संदेश सहसा तुमच्या नावाने असतात."]),
    dict(k="threat", w=2, re=re.compile(r"arrest|police|court|legal action|warrant|customs|cbi|गिरफ्तार|पुलिस|अदालत|कानूनी|अटक|पोलीस|न्यायालय|कायदेशीर|गुन्हा", re.I),
         t=["Uses fear or threats", "डर या धमकी का इस्तेमाल करता है", "भीती किंवा धमकी वापरतो"],
         d=["Threats of arrest or legal trouble are used to scare you into paying.", "गिरफ्तारी या कानूनी मुसीबत की धमकी आपको डराकर पैसे दिलवाने के लिए होती है।", "अटक किंवा कायदेशीर अडचणीची धमकी तुम्हाला घाबरवून पैसे काढण्यासाठी दिली जाते."]),
    dict(k="kyc", w=1, re=re.compile(r"kyc|verify|verification|update your|सत्यापित|अपडेट|पडताळणी", re.I),
         t=["Asks you to “verify” or “update”", "“सत्यापित” या “अपडेट” करने को कहता है", "“पडताळणी” किंवा “अपडेट” करायला सांगतो"],
         d=["Fake KYC updates are one of the most common message scams.", "नकली KYC अपडेट सबसे आम संदेश ठगी में से एक है।", "बनावट KYC अपडेट ही सर्वात सामान्य संदेश फसवणुकींपैकी एक आहे."]),
    dict(k="remote", w=3, re=re.compile(r"anydesk|teamviewer|quicksupport|screen ?share|remote access", re.I),
         t=["Asks you to install a screen-sharing app", "स्क्रीन-शेयरिंग ऐप इंस्टॉल करवाता है", "स्क्रीन-शेअरिंग ॲप इन्स्टॉल करायला सांगतो"],
         d=["Screen-sharing apps give strangers control of your phone and bank apps.", "स्क्रीन-शेयरिंग ऐप अजनबियों को आपके फोन और बैंक ऐप का नियंत्रण दे देते हैं।", "स्क्रीन-शेअरिंग ॲप अनोळखी लोकांना तुमच्या फोनचा आणि बँक ॲप्सचा ताबा देतात."]),
]


def analyze(text: str) -> dict:
    flags = [r for r in RULES if r["re"].search(text or "")]
    score = sum(r["w"] for r in flags)
    level = "high" if score >= 4 else "mid" if score >= 2 else "low"
    return {"flags": flags, "score": score, "level": level, "pos": min(0.95, max(0.08, score / 8)), "text": text}


def highlight(text: str, flags) -> str:
    """Escape the message and wrap every risky phrase in <mark> (animated one after another)."""
    spans = sorted((m.start(), m.end()) for r in flags for m in r["re"].finditer(text) if m.end() > m.start())
    merged = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    out, pos = [], 0
    for i, (s, e) in enumerate(merged):
        out.append(html.escape(text[pos:s]))
        out.append(f'<mark style="--i:{i}">{html.escape(text[s:e])}</mark>')
        pos = e
    out.append(html.escape(text[pos:]))
    return "".join(out).replace("\n", "<br>")
