import type { L } from "./i18n";

export type TermCategory = "Messages" | "Calls" | "Online" | "Payments";

export const categoryLabels: Record<"All" | TermCategory, L> = {
  All: { en: "All", hi: "सभी" },
  Messages: { en: "Messages", hi: "संदेश" },
  Calls: { en: "Calls", hi: "कॉल" },
  Online: { en: "Online", hi: "ऑनलाइन" },
  Payments: { en: "Payments", hi: "भुगतान" },
};

export type LookLike = {
  kind: "sms" | "call" | "video" | "qr" | "atm";
  header: L;
  body: L;
  flag: L;
};

export type Term = {
  id: string;
  name: L;
  category: TermCategory;
  icon: string;
  meaning: L;
  example: L;
  remember: L[];
  lookLike: LookLike;
  fact: L;
  scenarioId?: string;
};

export const terms: Term[] = [
  {
    id: "phishing",
    name: { en: "Phishing", hi: "फ़िशिंग" },
    category: "Messages",
    icon: "mail-hook",
    meaning: {
      en: "A fake message, email, or website that looks real, designed to trick you into clicking a link, sharing personal details, or entering your password.",
      hi: "एक नकली संदेश जो असली जैसा दिखता है, जो आपको किसी लिंक पर क्लिक करने या जानकारी साझा करने के लिए धोखा देने की कोशिश करता है।",
    },
    example: {
      en: "An SMS or email pretending to be from your bank saying 'Your account will be blocked, click here to verify.'",
      hi: "बैंक की तरफ से आया एक SMS या ईमेल जिसमें लिखा हो 'आपका खाता बंद हो जाएगा, यहां क्लिक करके सत्यापित करें।'",
    },
    remember: [
      { en: "Don't click links in unexpected messages", hi: "अनजान संदेशों में दिए गए लिंक पर क्लिक न करें" },
      { en: "Go to the official app directly instead", hi: "इसकी जगह सीधे आधिकारिक ऐप खोलें" },
      { en: "When in doubt, call the company using the number on your card, not the message", hi: "शक हो तो कंपनी को अपने कार्ड पर लिखे नंबर पर कॉल करें, संदेश वाले नंबर पर नहीं" },
    ],
    lookLike: {
      kind: "sms",
      header: { en: "Unknown sender", hi: "अनजान नंबर" },
      body: { en: "Your account will be blocked! Click here:", hi: "आपका खाता बंद हो जाएगा! यहां क्लिक करें:" },
      flag: { en: "bank-verify-now.xyz/login", hi: "bank-verify-now.xyz/login" },
    },
    fact: {
      en: "Scammers can copy a bank's logo and colours perfectly — a familiar look is never proof a message is real.",
      hi: "ठग बैंक का लोगो और रंग हूबहू कॉपी कर सकते हैं — जाना-पहचाना रूप कभी भी असली होने का सबूत नहीं है।",
    },
    scenarioId: "delivery-message",
  },
  {
    id: "smishing",
    name: { en: "Smishing", hi: "स्मिशिंग" },
    category: "Messages",
    icon: "phone-mail",
    meaning: {
      en: "Phishing that happens through SMS text messages instead of email.",
      hi: "यह फ़िशिंग है जो ईमेल की जगह SMS टेक्स्ट संदेशों के ज़रिए होती है।",
    },
    example: {
      en: "A text saying you've won a prize or that your parcel delivery failed, with a link to click.",
      hi: "एक टेक्स्ट जिसमें कहा गया हो कि आपने इनाम जीता है या आपका पार्सल डिलीवरी विफल हो गई, साथ में एक लिंक।",
    },
    remember: [
      { en: "Delete suspicious texts that contain links", hi: "लिंक वाले संदिग्ध टेक्स्ट डिलीट कर दें" },
      { en: "Check deliveries in the courier's own app", hi: "डिलीवरी की जानकारी कूरियर के अपने ऐप में देखें" },
      { en: "Never reply — it tells scammers your number is active", hi: "जवाब न दें — इससे ठग को पता चलता है कि आपका नंबर चालू है" },
    ],
    lookLike: {
      kind: "sms",
      header: { en: "VK-PARCEL", hi: "VK-PARCEL" },
      body: { en: "Your parcel is held. Pay ₹50 to release today:", hi: "आपका पार्सल रुका है। आज छुड़ाने के लिए ₹50 भरें:" },
      flag: { en: "parcel-help.link/pay", hi: "parcel-help.link/pay" },
    },
    fact: {
      en: "Scam texts are sent in bulk to random numbers — getting one doesn't mean you did anything wrong.",
      hi: "धोखे वाले टेक्स्ट एक साथ हज़ारों अनजान नंबरों पर भेजे जाते हैं — ऐसा संदेश आने का मतलब यह नहीं कि आपने कोई गलती की।",
    },
    scenarioId: "delivery-message",
  },
  {
    id: "vishing",
    name: { en: "Vishing", hi: "विशिंग" },
    category: "Calls",
    icon: "phone-warning",
    meaning: {
      en: "A scam call where someone pretends to be from your bank, the police, or a company to trick you into sharing information or money over the phone.",
      hi: "एक धोखाधड़ी वाली कॉल जिसमें कोई व्यक्ति आपके बैंक, पुलिस, या किसी कंपनी से होने का दिखावा करता है ताकि फोन पर जानकारी या पैसे ऐंठ सके।",
    },
    example: {
      en: "A caller claiming to be from your bank, asking for your OTP or card PIN to 'verify your account.'",
      hi: "एक कॉलर जो आपके बैंक से होने का दावा करता है और 'खाता सत्यापित करने' के लिए आपका OTP या कार्ड पिन मांगता है।",
    },
    remember: [
      { en: "Banks never ask for your OTP, PIN, or password on a call", hi: "बैंक कभी भी कॉल पर OTP, पिन या पासवर्ड नहीं मांगते" },
      { en: "Hang up and call the number on your card yourself", hi: "फोन काटें और खुद अपने कार्ड पर लिखे नंबर पर कॉल करें" },
    ],
    lookLike: {
      kind: "call",
      header: { en: "Incoming call · Unknown", hi: "आने वाली कॉल · अनजान" },
      body: { en: "“This is your bank's security team. Please confirm your card number.”", hi: "“मैं आपके बैंक की सुरक्षा टीम से बोल रहा हूं। अपना कार्ड नंबर बताइए।”" },
      flag: { en: "They called you — you didn't call them", hi: "उन्होंने आपको कॉल किया — आपने नहीं" },
    },
    fact: {
      en: "Real banks never call asking for your PIN or OTP — not even to 'verify' your identity.",
      hi: "असली बैंक कभी भी पिन या OTP मांगने के लिए कॉल नहीं करते — 'पहचान पक्की करने' के लिए भी नहीं।",
    },
    scenarioId: "bank-call",
  },
  {
    id: "deepfake",
    name: { en: "Deepfake", hi: "डीपफेक" },
    category: "Calls",
    icon: "face-question",
    meaning: {
      en: "A fake video or voice recording made using AI that looks and sounds like a real person, but isn't actually them.",
      hi: "AI का उपयोग करके बनाया गया एक नकली वीडियो या आवाज़ जो किसी असली व्यक्ति जैसा दिखता और सुनाई देता है, लेकिन वह असल में वह व्यक्ति नहीं होता।",
    },
    example: {
      en: "A video call that looks and sounds like your grandson asking for money urgently, but it's actually a scammer using AI.",
      hi: "एक वीडियो कॉल जो आपके पोते जैसी दिखती और सुनाई देती है, जिसमें तुरंत पैसे मांगे जाते हैं, लेकिन असल में यह AI का उपयोग करने वाला एक धोखेबाज़ होता है।",
    },
    remember: [
      { en: "Urgent money requests are the real red flag, not video quality", hi: "असली खतरे का संकेत है अचानक पैसे की मांग, वीडियो की क्वालिटी नहीं" },
      { en: "Hang up and call back on their usual saved number", hi: "फोन काटें और उनके सेव किए हुए नंबर पर वापस कॉल करें" },
      { en: "Be wary if they ask you to keep it secret", hi: "अगर वे बात छुपाने को कहें, तो सावधान हो जाएं" },
    ],
    lookLike: {
      kind: "video",
      header: { en: "Video call · “Grandson”", hi: "वीडियो कॉल · “पोता”" },
      body: { en: "“Dadi, I'm in trouble. Please send money now — don't tell anyone.”", hi: "“दादी, मैं मुसीबत में हूं। अभी पैसे भेज दो — किसी को मत बताना।”" },
      flag: { en: "Urgent + secret = pause and call back", hi: "जल्दबाज़ी + छुपाना = रुकें और वापस कॉल करें" },
    },
    fact: {
      en: "AI voice copying now needs only a few seconds of someone's voice — a family 'safe word' can help you check.",
      hi: "AI से किसी की आवाज़ कॉपी करने के लिए अब बस कुछ सेकंड की रिकॉर्डिंग काफ़ी है — परिवार का एक 'गुप्त शब्द' पहचान में मदद कर सकता है।",
    },
    scenarioId: "grandson-emergency",
  },
  {
    id: "otp-fraud",
    name: { en: "OTP Fraud", hi: "OTP धोखाधड़ी" },
    category: "Calls",
    icon: "lock-dots",
    meaning: {
      en: "When someone tricks you into sharing the one-time password (OTP) sent to your phone, then uses it to access your account or complete a transaction.",
      hi: "जब कोई आपको आपके फोन पर आए वन-टाइम पासवर्ड (OTP) को साझा करने के लिए धोखा देता है, फिर उसका उपयोग आपके खाते तक पहुंचने या लेन-देन पूरा करने के लिए करता है।",
    },
    example: {
      en: "A caller says there's a 'refund' waiting and asks you to read out the OTP you just received.",
      hi: "एक कॉलर कहता है कि एक 'रिफंड' आपका इंतज़ार कर रहा है और आपसे अभी मिला OTP पढ़ने के लिए कहता है।",
    },
    remember: [
      { en: "Never share an OTP with anyone, for any reason", hi: "किसी भी वजह से OTP किसी को न बताएं" },
      { en: "An OTP you didn't ask for means someone is trying your account", hi: "बिना मांगे OTP आए तो समझें कोई आपके खाते में घुसने की कोशिश कर रहा है" },
      { en: "If you shared one by mistake, call your bank right away", hi: "गलती से बता दिया हो तो तुरंत बैंक को कॉल करें" },
    ],
    lookLike: {
      kind: "sms",
      header: { en: "BANK-ALERT", hi: "BANK-ALERT" },
      body: { en: "Your OTP is 482 913. Do not share it with anyone.", hi: "आपका OTP 482 913 है। इसे किसी के साथ साझा न करें।" },
      flag: { en: "Caller: “Just read me that code for your refund”", hi: "कॉलर: “रिफंड के लिए बस वो कोड बता दीजिए”" },
    },
    fact: {
      en: "The OTP message itself says 'do not share' — a caller asking for it is telling you they're not your bank.",
      hi: "OTP वाले संदेश में खुद लिखा होता है 'किसी से साझा न करें' — जो कॉलर इसे मांगता है, वह आपका बैंक नहीं है।",
    },
    scenarioId: "bank-call",
  },
  {
    id: "digital-arrest",
    name: { en: "Digital Arrest Scam", hi: "डिजिटल अरेस्ट स्कैम" },
    category: "Calls",
    icon: "video-badge",
    meaning: {
      en: "A scam where fraudsters pretend to be police or government officers on a video call, falsely claiming you're under investigation, and pressure you to pay money immediately to avoid arrest.",
      hi: "एक धोखाधड़ी जिसमें ठग वीडियो कॉल पर पुलिस या सरकारी अधिकारी होने का दिखावा करते हैं, झूठा दावा करते हैं कि आप जांच के दायरे में हैं, और गिरफ्तारी से बचने के लिए तुरंत पैसे देने का दबाव डालते हैं।",
    },
    example: {
      en: "A video call from someone in a police uniform saying a parcel with illegal items was found in your name, and you must pay a fine right now.",
      hi: "पुलिस की वर्दी में किसी व्यक्ति की वीडियो कॉल यह कहते हुए कि आपके नाम पर एक पार्सल में अवैध सामान मिला है, और आपको अभी जुर्माना देना होगा।",
    },
    remember: [
      { en: "Real police never arrest or collect money over a video call", hi: "असली पुलिस वीडियो कॉल पर न गिरफ्तार करती है, न पैसे लेती है" },
      { en: "You can always hang up — it is never 'evidence of guilt'", hi: "आप हमेशा फोन काट सकते हैं — यह कभी 'गुनाह का सबूत' नहीं होता" },
      { en: "Visit your local police station if you're worried", hi: "चिंता हो तो अपने नज़दीकी थाने जाएं" },
    ],
    lookLike: {
      kind: "video",
      header: { en: "Video call · “Police Officer”", hi: "वीडियो कॉल · “पुलिस अधिकारी”" },
      body: { en: "“A parcel in your name had illegal items. Pay the fine now or be arrested.”", hi: "“आपके नाम के पार्सल में अवैध सामान मिला है। अभी जुर्माना भरें वरना गिरफ्तारी होगी।”" },
      flag: { en: "Payment to avoid arrest = scam", hi: "गिरफ्तारी से बचने के लिए पैसे = धोखा" },
    },
    fact: {
      en: "There is no such thing as a 'digital arrest' in Indian law — arrests always happen in person.",
      hi: "भारतीय कानून में 'डिजिटल अरेस्ट' जैसी कोई चीज़ नहीं है — गिरफ्तारी हमेशा आमने-सामने होती है।",
    },
    scenarioId: "police-video-call",
  },
  {
    id: "qr-scam",
    name: { en: "QR Code Scam", hi: "QR कोड स्कैम" },
    category: "Payments",
    icon: "qr-warning",
    meaning: {
      en: "A scam using fake QR codes that, when scanned, send money OUT of your account instead of into it, or take you to a fake website.",
      hi: "नकली QR कोड का उपयोग करने वाला एक स्कैम जो स्कैन करने पर पैसे आपके खाते में आने की बजाय बाहर भेज देता है, या आपको एक नकली वेबसाइट पर ले जाता है।",
    },
    example: {
      en: "A shop's real QR code covered with a fake sticker, so your payment goes to the scammer's account instead of the shop's.",
      hi: "दुकान का असली QR कोड एक नकली स्टिकर से ढका हुआ, ताकि आपका भुगतान दुकान की बजाय ठग के खाते में जाए।",
    },
    remember: [
      { en: "To RECEIVE money, you never scan a code or enter a PIN", hi: "पैसे पाने के लिए कभी कोड स्कैन या पिन डालने की ज़रूरत नहीं होती" },
      { en: "Check the name on your payment screen before confirming", hi: "भुगतान से पहले स्क्रीन पर दिख रहा नाम ज़रूर जांचें" },
    ],
    lookLike: {
      kind: "qr",
      header: { en: "Scan to pay", hi: "भुगतान के लिए स्कैन करें" },
      body: { en: "Paying: “R K Traders”?", hi: "भुगतान: “R K Traders”?" },
      flag: { en: "Sticker looks stuck on top of another", hi: "स्टिकर किसी दूसरे स्टिकर के ऊपर चिपका लगता है" },
    },
    fact: {
      en: "Entering your UPI PIN always sends money out — no genuine refund or prize ever needs it.",
      hi: "UPI पिन डालने से पैसे हमेशा बाहर जाते हैं — किसी असली रिफंड या इनाम के लिए इसकी ज़रूरत नहीं होती।",
    },
    scenarioId: "shop-qr",
  },
  {
    id: "card-skimming",
    name: { en: "ATM Card Skimming", hi: "ATM कार्ड स्किमिंग" },
    category: "Payments",
    icon: "card-warning",
    meaning: {
      en: "When scammers attach a hidden device to an ATM's card slot to copy your card's details, often combined with a hidden camera or fake keypad to steal your PIN.",
      hi: "जब ठग आपके कार्ड की जानकारी कॉपी करने के लिए ATM के कार्ड स्लॉट में एक छिपा हुआ उपकरण लगाते हैं, अक्सर एक छिपे हुए कैमरे या नकली कीपैड के साथ जो आपका पिन चुराता है।",
    },
    example: {
      en: "A small device fitted over the real card slot, or a sticker with a fake 'helpline number' placed on the ATM by scammers.",
      hi: "असली कार्ड स्लॉट के ऊपर लगा एक छोटा उपकरण, या ठगों द्वारा ATM पर लगाया गया एक नकली 'हेल्पलाइन नंबर' वाला स्टिकर।",
    },
    remember: [
      { en: "Cover the keypad every time you enter your PIN", hi: "पिन डालते समय हर बार कीपैड ढकें" },
      { en: "A loose or odd card slot? Use a different ATM", hi: "कार्ड स्लॉट ढीला या अजीब लगे? दूसरा ATM इस्तेमाल करें" },
      { en: "Ignore helpline stickers — use the number from your card", hi: "हेल्पलाइन स्टिकर पर भरोसा न करें — कार्ड पर लिखा नंबर इस्तेमाल करें" },
    ],
    lookLike: {
      kind: "atm",
      header: { en: "ATM", hi: "ATM" },
      body: { en: "Helpline: 98XXX XXXXX", hi: "हेल्पलाइन: 98XXX XXXXX" },
      flag: { en: "Card slot sticks out and feels loose", hi: "कार्ड स्लॉट बाहर निकला और ढीला लगता है" },
    },
    fact: {
      en: "Hidden cameras are often fitted to the ATM itself — covering the keypad helps even when nobody is nearby.",
      hi: "छिपे कैमरे अक्सर ATM पर ही लगे होते हैं — आसपास कोई न हो तब भी कीपैड ढकना काम आता है।",
    },
    scenarioId: "shop-qr",
  },
];

export const termCategories: Array<"All" | TermCategory> = [
  "All",
  "Messages",
  "Calls",
  "Online",
  "Payments",
];

export const genericFacts: L[] = [
  {
    en: "Real banks will NEVER call you asking for your PIN or OTP — not even to 'verify' your identity.",
    hi: "असली बैंक कभी भी आपका पिन या OTP मांगने के लिए कॉल नहीं करेंगे — 'पहचान पक्की करने' के लिए भी नहीं।",
  },
  {
    en: "Pausing for just one minute before acting on an urgent message stops most scams — urgency is their main tool.",
    hi: "किसी जल्दबाज़ी वाले संदेश पर कुछ करने से पहले बस एक मिनट रुकना ज़्यादातर धोखों को रोक देता है — जल्दबाज़ी ही उनका सबसे बड़ा हथियार है।",
  },
];

export type Scenario = {
  id: string;
  title: L;
  icon: string;
  blurb: L;
  situation: L;
  options: Array<{ label: L; safe: boolean }>;
  correctFeedback: L;
  incorrectFeedback: L;
  topic: L;
  badge: string;
};

export const scenarios: Scenario[] = [
  {
    id: "bank-call",
    title: { en: "The Bank Call", hi: "बैंक की कॉल" },
    icon: "phone-warning",
    blurb: { en: "Someone calls saying they're from your bank.", hi: "कोई कॉल करके कहता है कि वह आपके बैंक से है।" },
    situation: {
      en: "A caller says he's from your bank and asks for the OTP just sent to your phone, to verify your account. What do you do?",
      hi: "एक आदमी फोन करके कहता है कि वह आपके बैंक से है, और खाता वेरिफ़ाई करने के लिए अभी आपके फोन पर आया OTP मांगता है। आप क्या करेंगे?",
    },
    options: [
      { label: { en: "Read out the OTP so the account isn't blocked", hi: "OTP बता दूं ताकि खाता बंद न हो" }, safe: false },
      { label: { en: "Hang up and call the number printed on my bank card", hi: "फोन काटकर अपने बैंक कार्ड पर लिखे नंबर पर कॉल करूं" }, safe: true },
    ],
    correctFeedback: { en: "Good instinct! Banks never ask for your OTP on a call.", hi: "बहुत अच्छा सोचा! बैंक कभी भी फोन पर OTP नहीं मांगते।" },
    incorrectFeedback: {
      en: "If you read out the OTP, the scammer can complete a transaction on your account within seconds — that's exactly why they create urgency.",
      hi: "अगर आप OTP बता देते, तो ठग कुछ ही सेकंड में आपके खाते से पैसे निकाल सकता था — इसीलिए वे इतनी जल्दबाज़ी मचाते हैं।",
    },
    topic: { en: "calls asking for your OTP", hi: "OTP मांगने वाली कॉल" },
    badge: "Calm Caller",
  },
  {
    id: "grandson-emergency",
    title: { en: "The Grandson Emergency", hi: "पोते की इमरजेंसी" },
    icon: "face-question",
    blurb: { en: "An urgent call from someone who sounds like family.", hi: "परिवार जैसी आवाज़ में एक जल्दबाज़ी वाली कॉल।" },
    situation: {
      en: "You get a video call that looks and sounds like your grandson. He says he's in trouble and needs money sent right now. What do you do?",
      hi: "आपको एक वीडियो कॉल आती है जो बिल्कुल आपके पोते जैसी दिखती और सुनाई देती है। वह कहता है कि वह मुसीबत में है और उसे अभी पैसे चाहिए। आप क्या करेंगे?",
    },
    options: [
      { label: { en: "Send the money immediately — he sounds upset", hi: "तुरंत पैसे भेज दूं — वह परेशान लग रहा है" }, safe: false },
      { label: { en: "Hang up and call him back on his usual number", hi: "फोन काटकर उसके हमेशा वाले नंबर पर वापस कॉल करूं" }, safe: true },
    ],
    correctFeedback: { en: "Exactly right. Calling back on a known number confirms who you're speaking to.", hi: "बिल्कुल सही। जाने-पहचाने नंबर पर वापस कॉल करने से पता चल जाता है कि असल में कौन बात कर रहा है।" },
    incorrectFeedback: {
      en: "AI can now copy a face and voice. The money would go straight to a scammer, and your grandson might not even know it happened.",
      hi: "अब AI से चेहरा और आवाज़ दोनों नकल हो सकते हैं। पैसे सीधे ठग के पास जाते, और आपके पोते को पता भी नहीं चलता।",
    },
    topic: { en: "urgent family calls asking for money", hi: "पैसे मांगने वाली परिवार की जल्दबाज़ी वाली कॉल" },
    badge: "Steady Heart",
  },
  {
    id: "delivery-message",
    title: { en: "The Delivery Message", hi: "डिलीवरी का मैसेज" },
    icon: "phone-mail",
    blurb: { en: "A text about a parcel that couldn't be delivered.", hi: "ऐसे पार्सल का मैसेज जो डिलीवर नहीं हो पाया।" },
    situation: {
      en: "A text message says your parcel delivery failed and asks you to click a link to reschedule it. What do you do?",
      hi: "एक मैसेज आता है कि आपका पार्सल डिलीवर नहीं हो पाया, और दोबारा मंगाने के लिए एक लिंक पर क्लिक करने को कहता है। आप क्या करेंगे?",
    },
    options: [
      { label: { en: "Tap the link in the message to reschedule", hi: "मैसेज वाले लिंक पर क्लिक करके दोबारा मंगाऊं" }, safe: false },
      { label: { en: "Open the courier's own app or website myself", hi: "खुद कूरियर का अपना ऐप या वेबसाइट खोलूं" }, safe: true },
    ],
    correctFeedback: { en: "Nicely done. Going to the official app directly avoids fake links entirely.", hi: "बढ़िया! सीधे असली ऐप खोलने से नकली लिंक का खतरा ही खत्म हो जाता है।" },
    incorrectFeedback: {
      en: "Links in unexpected texts often open fake pages that ask for card details or a small 'fee' — and then take much more.",
      hi: "अनजान मैसेज के लिंक अक्सर नकली पेज खोलते हैं जो कार्ड की जानकारी या छोटी-सी 'फ़ीस' मांगते हैं — और फिर बहुत ज़्यादा ले जाते हैं।",
    },
    topic: { en: "delivery texts with links", hi: "लिंक वाले डिलीवरी मैसेज" },
    badge: "Link Spotter",
  },
  {
    id: "shop-qr",
    title: { en: "The Shop QR Code", hi: "दुकान का QR कोड" },
    icon: "qr-warning",
    blurb: { en: "Something looks off about the QR sticker on the counter.", hi: "काउंटर पर लगा QR स्टिकर कुछ अजीब लग रहा है।" },
    situation: {
      en: "You're paying a shopkeeper using a QR code taped to the counter. Right before you scan, you notice the sticker looks slightly crooked, like it's stuck on top of something else. What do you do?",
      hi: "आप दुकान के काउंटर पर चिपके QR कोड से पैसे देने वाले हैं। स्कैन करने से ठीक पहले आप देखते हैं कि स्टिकर थोड़ा टेढ़ा है, जैसे किसी और चीज़ के ऊपर चिपकाया गया हो। आप क्या करेंगे?",
    },
    options: [
      { label: { en: "Scan it anyway — it's just for paying, should be fine", hi: "फिर भी स्कैन कर दूं — बस पैसे ही तो देने हैं" }, safe: false },
      {
        label: {
          en: "Ask the shopkeeper to confirm the amount and name on the payment screen before confirming, or use their printed bill instead",
          hi: "पैसे भेजने से पहले दुकानदार से स्क्रीन पर रकम और नाम पक्का करवाऊं, या उनके छपे बिल वाला तरीका अपनाऊं",
        },
        safe: true,
      },
    ],
    correctFeedback: { en: "Smart catch. Always check the name that appears on your payment screen matches the shop before confirming.", hi: "बहुत समझदारी! भुगतान से पहले हमेशा देखें कि स्क्रीन पर दुकान का ही नाम दिख रहा है।" },
    incorrectFeedback: {
      en: "A fake sticker placed over the real QR code sends your payment to a scammer's account instead of the shop's — and once sent, that money is very hard to get back.",
      hi: "असली QR कोड के ऊपर लगा नकली स्टिकर आपके पैसे दुकान की जगह ठग के खाते में भेज देता है — और एक बार पैसे चले गए, तो वापस मिलना बहुत मुश्किल होता है।",
    },
    topic: { en: "QR code tricks", hi: "QR कोड वाले धोखे" },
    badge: "Sharp Eye",
  },
  {
    id: "computer-help",
    title: { en: "The Free Computer Help", hi: "कंप्यूटर की मुफ़्त मदद" },
    icon: "phone-warning",
    blurb: { en: "A virus warning pop-up with a number to call.", hi: "वायरस की चेतावनी जिसमें कॉल करने का नंबर दिया है।" },
    situation: {
      en: "A pop-up on your computer says it has a virus and gives a phone number to call for 'free help.' You call, and the person asks you to install an app so they can 'fix it remotely.' What do you do?",
      hi: "आपके कंप्यूटर पर एक पॉप-अप आता है कि इसमें वायरस है, और 'मुफ़्त मदद' के लिए एक नंबर देता है। आप कॉल करते हैं, तो सामने वाला कहता है कि एक ऐप डाल लीजिए ताकि वह 'दूर से ठीक' कर सके। आप क्या करेंगे?",
    },
    options: [
      { label: { en: "Install the app so they can fix it quickly", hi: "ऐप डाल दूं ताकि वे जल्दी ठीक कर दें" }, safe: false },
      {
        label: {
          en: "Hang up and close the pop-up — real antivirus warnings don't ask you to call a phone number",
          hi: "फोन काटकर पॉप-अप बंद कर दूं — असली एंटीवायरस कभी फोन करने को नहीं कहता",
        },
        safe: true,
      },
    ],
    correctFeedback: { en: "Exactly. Genuine security warnings never ask you to call a number or install remote-access software.", hi: "बिल्कुल सही। असली सुरक्षा चेतावनी कभी नंबर पर कॉल करने या दूर से चलाने वाला ऐप डालने को नहीं कहती।" },
    incorrectFeedback: {
      en: "Installing that app gives a stranger full control of your computer — they can see your banking details, photos, and passwords, all while you watch.",
      hi: "वह ऐप डालते ही किसी अनजान को आपके कंप्यूटर का पूरा कंट्रोल मिल जाता है — वह आपकी बैंक की जानकारी, फोटो और पासवर्ड सब देख सकता है, आपकी आंखों के सामने।",
    },
    topic: { en: "fake virus warnings and 'remote help'", hi: "नकली वायरस चेतावनी और 'दूर से मदद'" },
    badge: "Screen Guardian",
  },
  {
    id: "investment-group",
    title: { en: "The Investment Group", hi: "निवेश वाला ग्रुप" },
    icon: "mail-hook",
    blurb: { en: "A WhatsApp group full of 'huge profit' screenshots.", hi: "'भारी मुनाफ़े' के स्क्रीनशॉट से भरा WhatsApp ग्रुप।" },
    situation: {
      en: "Someone adds you to a WhatsApp group where everyone is posting screenshots of huge profits from an 'investment expert.' They ask you to send money to join. What do you do?",
      hi: "कोई आपको एक WhatsApp ग्रुप में जोड़ देता है जहां सब लोग किसी 'निवेश एक्सपर्ट' से हुए भारी मुनाफ़े के स्क्रीनशॉट डाल रहे हैं। वे आपसे जुड़ने के लिए पैसे भेजने को कहते हैं। आप क्या करेंगे?",
    },
    options: [
      { label: { en: "Send a small amount first to see if it really works", hi: "पहले थोड़े पैसे भेजकर देखूं कि सच में काम करता है या नहीं" }, safe: false },
      {
        label: {
          en: "Leave the group — real investments are never guaranteed, and strangers don't hand out free profits",
          hi: "ग्रुप छोड़ दूं — असली निवेश में कोई गारंटी नहीं होती, और अनजान लोग मुफ़्त में मुनाफ़ा नहीं बांटते",
        },
        safe: true,
      },
    ],
    correctFeedback: { en: "Well spotted. If an investment promises guaranteed high returns with no risk, that's the biggest red flag of all.", hi: "खूब पहचाना! अगर कोई निवेश बिना जोखिम के पक्का बड़ा मुनाफ़ा देने का वादा करे, तो यही सबसे बड़ा खतरे का संकेत है।" },
    incorrectFeedback: {
      en: "Those 'profit screenshots' are usually fake, posted by the scammers themselves to build trust before asking for larger amounts.",
      hi: "वे 'मुनाफ़े के स्क्रीनशॉट' ज़्यादातर नकली होते हैं, जिन्हें ठग खुद डालते हैं ताकि भरोसा जीतकर बाद में बड़ी रकम मांग सकें।",
    },
    topic: { en: "'guaranteed profit' investment groups", hi: "'पक्के मुनाफ़े' वाले निवेश ग्रुप" },
    badge: "Wise Investor",
  },
  {
    id: "police-video-call",
    title: { en: "The Police Video Call", hi: "पुलिस की वीडियो कॉल" },
    icon: "video-badge",
    blurb: { en: "A uniformed caller claims you're under investigation.", hi: "वर्दी वाला व्यक्ति कहता है कि आपकी जांच चल रही है।" },
    situation: {
      en: "Someone in a police uniform video-calls you, says a parcel in your name held illegal items, and demands a fine right now. What do you do?",
      hi: "पुलिस की वर्दी में कोई आपको वीडियो कॉल करता है, कहता है कि आपके नाम के पार्सल में गैरकानूनी सामान मिला है, और अभी जुर्माना भरने को कहता है। आप क्या करेंगे?",
    },
    options: [
      { label: { en: "Pay the fine to avoid trouble", hi: "मुसीबत से बचने के लिए जुर्माना भर दूं" }, safe: false },
      { label: { en: "End the call and visit my local police station if worried", hi: "कॉल काट दूं, और चिंता हो तो अपने नज़दीकी थाने जाऊं" }, safe: true },
    ],
    correctFeedback: { en: "Exactly right. Real police never demand money over a video call.", hi: "बिल्कुल सही। असली पुलिस कभी वीडियो कॉल पर पैसे नहीं मांगती।" },
    incorrectFeedback: {
      en: "Once you pay, the 'officer' usually invents a new charge and asks for more — the fear is what keeps people paying.",
      hi: "एक बार पैसे दे दिए, तो वह 'अधिकारी' अक्सर कोई नया इल्ज़ाम बनाकर और पैसे मांगता है — डर ही लोगों से पैसे निकलवाता रहता है।",
    },
    topic: { en: "fake police video calls", hi: "नकली पुलिस वीडियो कॉल" },
    badge: "Clear Head",
  },
];

export const mockUser = {
  name: { en: "Meena", hi: "मीना" } as L,
  phoneMasked: "+91 •••• ••34 21",
};

/** Mock earlier-in-the-week activity (Mon–Sun) merged with real recorded activity. */
export const mockWeek: Array<{ check: boolean; practice: boolean }> = [
  { check: true, practice: false },
  { check: true, practice: true },
  { check: false, practice: false },
  { check: true, practice: true },
  { check: false, practice: false },
  { check: false, practice: false },
  { check: false, practice: false },
];
export const mockCounts = { checks: 5, scenarios: 3 };
export const weekDayLabels: L[] = [
  { en: "Mon", hi: "सोम" },
  { en: "Tue", hi: "मंगल" },
  { en: "Wed", hi: "बुध" },
  { en: "Thu", hi: "गुरु" },
  { en: "Fri", hi: "शुक्र" },
  { en: "Sat", hi: "शनि" },
  { en: "Sun", hi: "रवि" },
];
