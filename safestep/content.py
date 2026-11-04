"""SafeStep content: scam words, quizzes, scenarios, facts and tips — each text is [English, हिंदी, मराठी]."""
import json
from pathlib import Path

_DATA = json.loads((Path(__file__).resolve().parent.parent / "data" / "content.json").read_text(encoding="utf-8"))
TERMS = _DATA["terms"]          # 8 "Learn a Word" cards, 5 quiz questions each
SCEN = _DATA["scenarios"]       # 7 practice scenarios; "c" is the safer choice
TERM = {x["key"]: x for x in TERMS}

SCEN_TERM = {"The Bank Call": "OTP Fraud", "The Grandson Emergency": "Deepfake", "The Delivery Message": "Smishing",
             "The Shop QR Code": "QR Code Scam", "The Free Computer Help": "Vishing", "The Investment Group": "Phishing",
             "The Police Video Call": "Digital Arrest Scam"}

ALL_BADGES = ["Calm Caller", "Family Checker", "Link Spotter", "QR Guard", "Screen Shield", "Smart Saver", "Steady Mind",
              "Caller ID Champion", "Word Wise"]

FACTS = {
    "Phishing": ["A real bank email will never ask you to log in through a link. Type the bank’s address yourself or open its app.",
                 "असली बैंक का ईमेल कभी लिंक से लॉग इन करने को नहीं कहता। बैंक का पता खुद टाइप करें या उसका ऐप खोलें।",
                 "खरी बँक ईमेल कधीही लिंकवरून लॉग इन करायला सांगत नाही. बँकेचा पत्ता स्वतः टाइप करा किंवा तिचे ॲप उघडा."],
    "Smishing": ["Couriers show delivery problems inside their own app. A text asking for a small fee through a link is a common trick.",
                 "कूरियर डिलीवरी की दिक्कत अपने ऐप में दिखाते हैं। लिंक से छोटी फ़ीस मांगने वाला टेक्स्ट एक आम चाल है।",
                 "कुरिअर डिलिव्हरीतील अडचणी त्यांच्या स्वतःच्या ॲपमध्ये दाखवतात. लिंकवरून छोटे शुल्क मागणारा SMS ही नेहमीची युक्ती आहे."],
    "Vishing": ["Caller ID can be faked. A call that shows your bank’s name can still be a scammer.",
                "कॉलर ID नकली बनाई जा सकती है। बैंक के नाम से आई कॉल भी ठग की हो सकती है।",
                "कॉलर ID बनावट असू शकतो. तुमच्या बँकेचे नाव दाखवणारा कॉलही फसवणूक करणाऱ्याचा असू शकतो."],
    "Deepfake": ["Agree on a family code word. If a “relative” asking for money can’t say it, hang up and call back.",
                 "परिवार में एक कोड शब्द तय करें। पैसे मांगने वाला “रिश्तेदार” वह न बता पाए, तो फोन काटकर वापस कॉल करें।",
                 "कुटुंबात एक सांकेतिक शब्द ठरवा. पैसे मागणाऱ्या “नातेवाईकाला” तो सांगता आला नाही, तर फोन ठेवा आणि परत कॉल करा."],
    "OTP Fraud": ["An OTP message says what it is for. If it says “payment” and you didn’t start one, someone else did.",
                  "OTP संदेश बताता है कि वह किस काम के लिए है। अगर उसमें “भुगतान” लिखा है और आपने शुरू नहीं किया, तो किसी और ने किया है।",
                  "OTP संदेशात तो कशासाठी आहे ते लिहिलेले असते. त्यात “पेमेंट” लिहिले असेल आणि तुम्ही ते सुरू केले नसेल, तर दुसऱ्या कोणीतरी केले आहे."],
    "Digital Arrest Scam": ["Police and courts never arrest anyone or collect fines over a video call.",
                            "पुलिस और अदालतें कभी भी वीडियो कॉल पर गिरफ्तारी या जुर्माना नहीं करतीं।",
                            "पोलीस आणि न्यायालये कधीही व्हिडिओ कॉलवर अटक करत नाहीत किंवा दंड वसूल करत नाहीत."],
    "QR Code Scam": ["Receiving money on UPI never needs your PIN. If an app asks for your PIN after you scan, money is leaving your account.",
                     "UPI पर पैसा पाने के लिए कभी पिन नहीं लगता। अगर स्कैन के बाद ऐप पिन मांगे, तो पैसा आपके खाते से जा रहा है।",
                     "UPI वर पैसे मिळवण्यासाठी कधीच पिन लागत नाही. स्कॅन केल्यानंतर ॲप पिन मागत असेल, तर पैसे तुमच्या खात्यातून जात आहेत."],
    "ATM Card Skimming": ["Hidden cameras can sit on the ATM itself, so cover the keypad every time — not just when someone is behind you.",
                          "छिपे कैमरे ATM पर ही लगे हो सकते हैं, इसलिए हर बार कीपैड ढकें — सिर्फ तब नहीं जब कोई पीछे हो।",
                          "लपवलेले कॅमेरे ATM वरच असू शकतात, म्हणून प्रत्येक वेळी कीपॅड झाका — फक्त मागे कोणी असेल तेव्हाच नाही."],
}
FALLBACK_FACT = ["Your bank will never ask for your OTP, PIN or password — not on a call, SMS or email.",
                 "आपका बैंक कभी भी आपका OTP, पिन या पासवर्ड नहीं मांगता — न कॉल पर, न SMS या ईमेल पर।",
                 "तुमची बँक कधीही तुमचा OTP, पिन किंवा पासवर्ड मागत नाही — ना कॉलवर, ना SMS किंवा ईमेलवर."]
TIPS = [["Your bank will never ask for your OTP.", "आपका बैंक कभी भी आपका OTP नहीं मांगेगा।", "तुमची बँक कधीही तुमचा OTP मागणार नाही."],
        ["If a message rushes you, slow down.", "अगर कोई संदेश जल्दबाज़ी कराए, तो रुक जाएं।", "संदेश घाई करायला लावत असेल, तर थांबा."],
        ["You never need a PIN to receive money.", "पैसा पाने के लिए कभी पिन नहीं लगता।", "पैसे मिळवण्यासाठी कधीच पिन लागत नाही."],
        ["Call back on a number you already trust.", "उसी नंबर पर वापस कॉल करें जिस पर आपको पहले से भरोसा है।", "आधीपासून विश्वासाच्या नंबरवरच परत कॉल करा."],
        ["Police never arrest anyone on a video call.", "पुलिस कभी वीडियो कॉल पर गिरफ्तार नहीं करती।", "पोलीस कधीही व्हिडिओ कॉलवर अटक करत नाहीत."]]
QTYPES = [["Spot the real clue", "असली संकेत पहचानें", "खरी खूण ओळखा"], ["What would you do next?", "अब आप क्या करेंगे?", "आता तुम्ही काय कराल?"],
          ["True or false?", "सही या गलत?", "बरोबर की चूक?"], ["Tell the difference", "फ़र्क पहचानें", "फरक ओळखा"],
          ["Real-life moment", "असल ज़िंदगी का पल", "खऱ्या आयुष्यातील क्षण"]]
QOK = [["Good eye — that’s the real clue.", "बढ़िया नज़र — यही असली संकेत है।", "छान निरीक्षण — हीच खरी खूण आहे."],
       ["Exactly the safe move.", "बिल्कुल, यही सुरक्षित कदम है।", "अगदी बरोबर, हेच सुरक्षित पाऊल आहे."],
       ["Right — that’s a common myth.", "सही — यह एक आम गलतफहमी है।", "बरोबर — हा एक सामान्य गैरसमज आहे."],
       ["Spot on — you know the difference.", "बिल्कुल सही — आप फ़र्क समझते हैं।", "अचूक — तुम्हाला फरक समजतो."],
       ["Well handled. That’s exactly what to do.", "बहुत अच्छे। ठीक यही करना चाहिए।", "छान हाताळलेत. नेमके हेच करायला हवे."]]
EXAMPLES = [
    (["Bank KYC SMS", "बैंक KYC SMS", "बँक KYC SMS"],
     ["Dear Customer, your bank account will be blocked today. Update your KYC now: http://kyc-update-bank.co.in/verify",
      "प्रिय ग्राहक, आपका बैंक खाता आज बंद हो जाएगा। अभी अपना KYC अपडेट करें: http://kyc-update-bank.co.in/verify",
      "प्रिय ग्राहक, तुमचे बँक खाते आज बंद होईल. आत्ताच तुमचे KYC अपडेट करा: http://kyc-update-bank.co.in/verify"]),
    (["Parcel on hold", "पार्सल रुका है", "पार्सल अडकले"],
     ["Your parcel is on hold. Pay ₹25 redelivery fee within 2 hours: bit.ly/parcel-help",
      "आपका पार्सल रुका हुआ है। 2 घंटे में ₹25 री-डिलीवरी फ़ीस भरें: bit.ly/parcel-help",
      "तुमचे पार्सल अडकले आहे. 2 तासांत ₹25 री-डिलिव्हरी शुल्क भरा: bit.ly/parcel-help"]),
    (["Message from family", "परिवार का संदेश", "कुटुंबाचा संदेश"],
     ["Hi Maa, reached office safely. Will call you in the evening.", "नमस्ते मां, ऑफिस ठीक से पहुंच गया। शाम को फोन करूंगा।",
      "नमस्कार आई, ऑफिसला नीट पोहोचलो. संध्याकाळी फोन करतो."]),
]
ELEC = ["Dear Customer, your electricity will be disconnected tonight at 9:30 pm because your last bill was not updated. Call our officer immediately on 98XXXXXX21.",
        "प्रिय ग्राहक, आपका पिछला बिल अपडेट नहीं हुआ है, इसलिए आज रात 9:30 बजे आपकी बिजली काट दी जाएगी। तुरंत हमारे अधिकारी को 98XXXXXX21 पर कॉल करें।",
        "प्रिय ग्राहक, तुमचे मागील बिल अपडेट न झाल्यामुळे आज रात्री 9:30 वाजता तुमची वीज कापली जाईल. आमच्या अधिकाऱ्याला तातडीने 98XXXXXX21 वर कॉल करा."]
