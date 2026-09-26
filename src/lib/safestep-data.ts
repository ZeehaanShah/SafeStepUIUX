export type TermCategory = "Messages" | "Calls" | "Online" | "Payments";

export type Term = {
  id: string;
  name: string;
  category: TermCategory;
  icon: string;
  meaning: string;
  example: string;
  safety: string;
  scenarioId?: string;
};

export const terms: Term[] = [
  {
    id: "phishing",
    name: "Phishing",
    category: "Messages",
    icon: "mail-hook",
    meaning:
      "A fake message, email, or website that looks real, designed to trick you into clicking a link, sharing personal details, or entering your password.",
    example:
      "An SMS or email pretending to be from your bank saying 'Your account will be blocked, click here to verify.'",
    safety:
      "Never click links in unexpected messages. Go to the official app or website directly instead.",
    scenarioId: "delivery-message",
  },
  {
    id: "smishing",
    name: "Smishing",
    category: "Messages",
    icon: "phone-mail",
    meaning: "Phishing that happens through SMS text messages instead of email.",
    example:
      "A text saying you've won a prize or that your parcel delivery failed, with a link to click.",
    safety:
      "Delete suspicious texts with links. Legitimate companies rarely ask you to click links in a text message.",
    scenarioId: "delivery-message",
  },
  {
    id: "vishing",
    name: "Vishing",
    category: "Calls",
    icon: "phone-warning",
    meaning:
      "A scam call where someone pretends to be from your bank, the police, or a company to trick you into sharing information or money over the phone.",
    example:
      "A caller claiming to be from your bank, asking for your OTP or card PIN to 'verify your account.'",
    safety:
      "Banks and government offices never ask for your OTP, PIN, or password on a call. Hang up and call the official number yourself.",
    scenarioId: "bank-call",
  },
  {
    id: "deepfake",
    name: "Deepfake",
    category: "Calls",
    icon: "face-question",
    meaning:
      "A fake video or voice recording made using AI that looks and sounds like a real person, but isn't actually them.",
    example:
      "A video call that looks and sounds like your grandson asking for money urgently, but it's actually a scammer using AI.",
    safety:
      "If a video or voice call feels urgent or asks for money, hang up and call the person back on their known number to confirm.",
    scenarioId: "grandson-emergency",
  },
  {
    id: "otp-fraud",
    name: "OTP Fraud",
    category: "Calls",
    icon: "lock-dots",
    meaning:
      "When someone tricks you into sharing the one-time password (OTP) sent to your phone, then uses it to access your account or complete a transaction.",
    example:
      "A caller says there's a 'refund' waiting and asks you to read out the OTP you just received.",
    safety: "Never share your OTP with anyone, even if they claim to be from your bank.",
    scenarioId: "bank-call",
  },
  {
    id: "digital-arrest",
    name: "Digital Arrest Scam",
    category: "Calls",
    icon: "video-badge",
    meaning:
      "A scam where fraudsters pretend to be police or government officers on a video call, falsely claiming you're under investigation, and pressure you to pay money immediately to avoid arrest.",
    example:
      "A video call from someone in a police uniform saying a parcel with illegal items was found in your name, and you must pay a fine right now.",
    safety:
      "Real police never make arrests or demand money over a video call. Hang up and visit your local police station if concerned.",
    scenarioId: "police-video-call",
  },
  {
    id: "qr-scam",
    name: "QR Code Scam",
    category: "Payments",
    icon: "qr-warning",
    meaning:
      "A scam using fake QR codes that, when scanned, send money OUT of your account instead of into it, or take you to a fake website.",
    example:
      "A shop's real QR code covered with a fake sticker, so your payment goes to the scammer's account instead of the shop's.",
    safety:
      "To RECEIVE money, you never need to scan a QR code or enter your PIN — only to SEND money.",
    scenarioId: "qr-refund",
  },
  {
    id: "card-skimming",
    name: "ATM Card Skimming",
    category: "Payments",
    icon: "card-warning",
    meaning:
      "When scammers attach a hidden device to an ATM's card slot to copy your card's details, often combined with a hidden camera or fake keypad to steal your PIN.",
    example:
      "A small device fitted over the real card slot, or a sticker with a fake 'helpline number' placed on the ATM by scammers.",
    safety:
      "Cover the keypad when entering your PIN, and check if the card slot looks loose or unusual before inserting your card.",
    scenarioId: "atm-helper",
  },
];

export const termCategories: Array<"All" | TermCategory> = [
  "All",
  "Messages",
  "Calls",
  "Online",
  "Payments",
];

export type Scenario = {
  id: string;
  title: string;
  icon: string;
  blurb: string;
  situation: string;
  options: Array<{
    label: string;
    safe: boolean;
    feedback: string;
  }>;
  badge: string;
};

export const scenarios: Scenario[] = [
  {
    id: "bank-call",
    title: "The Bank Call",
    icon: "phone-warning",
    blurb: "Someone calls saying they're from your bank.",
    situation:
      "A caller says he's from your bank and asks for the OTP just sent to your phone, to verify your account. What do you do?",
    options: [
      {
        label: "Read out the OTP so the account isn't blocked",
        safe: false,
        feedback:
          "Let's look at this together — a real bank will never ask for your OTP. It's safest to hang up and call the number printed on your card.",
      },
      {
        label: "Hang up and call the number printed on my bank card",
        safe: true,
        feedback: "Good instinct! Banks never ask for your OTP on a call.",
      },
    ],
    badge: "Calm Caller",
  },
  {
    id: "grandson-emergency",
    title: "The Grandson Emergency",
    icon: "face-question",
    blurb: "An urgent call from someone who sounds like family.",
    situation:
      "You get a video call that looks and sounds like your grandson. He says he's in trouble and needs money sent right now. What do you do?",
    options: [
      {
        label: "Send the money immediately — he sounds upset",
        safe: false,
        feedback:
          "Let's look at this together — urgency is the oldest trick there is. Hanging up and calling him back on his usual number keeps everyone safe.",
      },
      {
        label: "Hang up and call him back on his usual number",
        safe: true,
        feedback: "You're doing great. Calling back on a known number confirms who you're speaking to.",
      },
    ],
    badge: "Steady Heart",
  },
  {
    id: "delivery-message",
    title: "The Delivery Message",
    icon: "phone-mail",
    blurb: "A text about a parcel that couldn't be delivered.",
    situation:
      "A text message says your parcel delivery failed and asks you to click a link to reschedule it. What do you do?",
    options: [
      {
        label: "Open the courier's own app or website myself",
        safe: true,
        feedback: "Nicely done. Going to the official app directly avoids fake links entirely.",
      },
      {
        label: "Tap the link in the message to reschedule",
        safe: false,
        feedback:
          "Let's look at this together — links in unexpected texts often lead to fake pages. Opening the courier's own app is the safe route.",
      },
    ],
    badge: "Link Spotter",
  },
  {
    id: "police-video-call",
    title: "The Police Video Call",
    icon: "video-badge",
    blurb: "A uniformed caller claims you're under investigation.",
    situation:
      "Someone in a police uniform video-calls you, says a parcel in your name held illegal items, and demands a fine right now. What do you do?",
    options: [
      {
        label: "Pay the fine to avoid trouble",
        safe: false,
        feedback:
          "Let's look at this together — real police never collect fines on a video call. Ending the call is always allowed.",
      },
      {
        label: "End the call and visit my local police station if worried",
        safe: true,
        feedback: "Exactly right. Real police never demand money over a video call.",
      },
    ],
    badge: "Clear Head",
  },
  {
    id: "qr-refund",
    title: "The QR Code Refund",
    icon: "qr-warning",
    blurb: "A seller sends a QR code to 'return' your money.",
    situation:
      "An online seller says your refund is ready and sends a QR code for you to scan and enter your UPI PIN. What do you do?",
    options: [
      {
        label: "Refuse — receiving money never needs a PIN",
        safe: true,
        feedback: "Well spotted. Scanning a code and entering a PIN only ever sends money out.",
      },
      {
        label: "Scan it and enter my PIN to collect the refund",
        safe: false,
        feedback:
          "Let's look at this together — entering your PIN sends money away, it never brings money in.",
      },
    ],
    badge: "Payment Guard",
  },
  {
    id: "atm-helper",
    title: "The Helpful Stranger at the ATM",
    icon: "card-warning",
    blurb: "A stranger offers to help when the machine stalls.",
    situation:
      "The ATM seems stuck and a friendly stranger offers to help if you hand over your card and PIN. What do you do?",
    options: [
      {
        label: "Keep my card, cancel, and ask the bank staff inside",
        safe: true,
        feedback: "That's the safe choice. Your card and PIN stay with you, always.",
      },
      {
        label: "Let them help — they seem to know the machine",
        safe: false,
        feedback:
          "Let's look at this together — no one needs your card or PIN to help you, not even bank staff.",
      },
    ],
    badge: "Careful Step",
  },
];

export const mockUser = {
  name: "Asha",
  phoneMasked: "+91 •••• ••34 21",
  language: "English",
};

export const weekDots = [true, true, false, true, false, false, false];
export const weekDayLabels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
