import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def words_table(words):
    rows = [
        "| Kannada | Hindi Pronunciation | Hindi Meaning | English Meaning | Bangalore Usage |",
        "|---|---|---|---|---|",
    ]
    rows += [f"| {w[0]} | {w[1]} | {w[2]} | {w[3]} | {w[4]} |" for w in words]
    return "\n".join(rows)


def bullets(items):
    return "\n".join(f"{i + 1}. {x}" for i, x in enumerate(items))


def lesson_md(s):
    return f"""# Lesson {s['n']:03d}: {s['title']}

## Quick Recall

Say in Kannada:

{bullets(s['recall'])}

## New Words

### Must Memorize

{words_table(s['words'])}

## Main Pattern

### Kannada Sentence

{s['sentence']}

### Hindi Pronunciation

{s['pron']}

### Meaning

Hindi: {s['hi']}

English: {s['en']}

## Word-by-Word Breakdown

| Word | Hindi Meaning | English Meaning |
|---|---|---|
{chr(10).join(f"| {a} | {b} | {c} |" for a, b, c in s['breakdown'])}

## Sentence Construction Logic

{s['logic']}

## Reusable Pattern

`{s['pattern']}`

Examples:

{chr(10).join(f"- {x}" for x in s['examples'])}

## Guided Practice

Build these in Kannada:

{bullets(s['guided_prompts'])}

## Production Practice

Say these in Kannada:

{bullets(s['production_prompts'])}

## Real-Life Bangalore Roleplay

{s['roleplay_prompt']}

## Quiz

{bullets(s['quiz_prompts'])}

## Add These To Your Notes

Add:

{chr(10).join(f"- {x}" for x in s['notes'])}
"""


def answer_md(s):
    return f"""# Lesson {s['n']:03d} Answers

## Guided Practice Answers

{bullets(s['guided_answers'])}

## Production Practice Sample Answers

{bullets(s['production_answers'])}

## Roleplay Sample

{s['roleplay_answer']}

## Quiz Answers

{bullets(s['quiz_answers'])}

## Natural Bangalore Versions

- {s['natural']}

## Common Mistakes

- {s['mistake']}
"""


COMMON = {
    "naan": ("मैं", "I"),
    "neevu": ("आप", "you"),
    "nimma": ("आपका", "your"),
    "nanna": ("मेरा", "my"),
    "nanage": ("मुझे", "to me"),
    "nimge": ("आपको", "to you"),
    "idu": ("यह", "this"),
    "idannu": ("इसे", "this object"),
    "adannu": ("उसे", "that object"),
    "illi": ("यहां", "here"),
    "alli": ("वहां/में", "there/in"),
    "office": ("ऑफिस", "office"),
    "kannada": ("कन्नड़", "Kannada"),
    "bangalore": ("बंगलौर", "Bangalore"),
    "payment": ("पेमेंट", "payment"),
    "traffic": ("ट्रैफिक", "traffic"),
    "fan": ("पंखा", "fan"),
    "weekend": ("वीकेंड", "weekend"),
    "order": ("ऑर्डर", "order"),
    "work": ("काम", "work"),
    "late": ("देर", "late"),
    "gate": ("गेट", "gate"),
    "water": ("पानी", "water"),
    "coffee": ("कॉफी", "coffee"),
    "tea": ("चाय", "tea"),
    "barthini": ("मैं आऊंगा", "I will come"),
    "barthira": ("आएंगे?", "will you come?"),
    "hogbeku": ("जाना है", "need to go"),
    "barbeku": ("आना है", "need to come"),
    "beku": ("चाहिए", "want/need"),
    "beda": ("नहीं चाहिए", "do not want"),
    "madi": ("कीजिए", "do"),
    "madbeku": ("करना है", "need to do"),
    "madthini": ("मैं करूंगा", "I will do"),
    "ideya": ("है क्या?", "is there?"),
    "illa": ("नहीं", "no/not there"),
    "ide": ("है", "is there"),
    "aagide": ("हो गया है", "is done"),
    "bandilla": ("नहीं आया", "has not arrived"),
    "hogide": ("गया है", "has gone"),
    "hode": ("मैं गया", "I went"),
    "bande": ("मैं आया", "I came"),
    "konde": ("मैंने खरीदा", "I bought"),
    "togonde": ("मैंने लिया", "I took"),
    "kotte": ("मैंने दिया", "I gave"),
    "nodide": ("मैंने देखा", "I saw"),
    "helide": ("मैंने बताया", "I told"),
    "hogthini": ("मैं जाता हूं", "I go/will go"),
    "aagilla": ("नहीं हुआ", "not done"),
    "aaytu": ("हो गया", "happened/done"),
    "agalla": ("नहीं होता", "does not happen/work"),
    "jaasti": ("ज्यादा", "too much"),
    "swalpa": ("थोड़ा", "little/please"),
    "naale": ("कल", "tomorrow"),
    "beligge": ("सुबह", "morning"),
    "ninne": ("कल बीता", "yesterday"),
    "avru": ("वे/वह आदर से", "he/she respectfully"),
    "ge": ("को/के लिए", "to/for"),
    "yaava": ("कौन सा", "which"),
    "yaavaga": ("कब", "when"),
    "hege": ("कैसा", "how"),
    "enu": ("क्या", "what"),
    "en": ("क्या", "what"),
    "eshtu": ("कितना", "how much"),
    "gotha": ("पता है", "know"),
    "gothilla": ("पता नहीं", "do not know"),
    "ishta": ("पसंद", "like"),
    "chennagide": ("अच्छा है", "is good"),
    "madthira": ("करते हैं?", "do you do?"),
    "aamele": ("बाद में", "later"),
    "amele": ("बाद में", "later"),
    "aadmele": ("के बाद", "after"),
    "kalisi": ("भेजिए", "send"),
    "heli": ("बताइए", "tell"),
    "kodi": ("दीजिए", "give"),
    "banni": ("आइए", "come"),
    "hogi": ("जाइए", "go"),
}


def auto_breakdown(s):
    lookup = dict(COMMON)
    for word, pron, hi, en, example in s["words"]:
        lookup[word.lower()] = (hi, en)
        parts = word.lower().split()
        if len(parts) > 1:
            for part in parts:
                lookup.setdefault(part, (hi, en))
    tokens = [t.strip(".,?") for t in s["sentence"].split()]
    rows = []
    used = set()
    for token in tokens:
        key = token.lower()
        if not key or key in used:
            continue
        used.add(key)
        hi, en = lookup.get(key, ("संदर्भ शब्द", "context word"))
        rows.append((token, hi, en))
    return rows or s["breakdown"]


lessons = [
    {
        "n": 25,
        "title": "My Name, Your Name",
        "recall": ["Who are you?", "Tell the name.", "I am coming now."],
        "words": [
            ("nanna", "नन्न", "मेरा", "my", "Nanna name Rahul."),
            ("nimma", "निम्म", "आपका", "your", "Nimma name enu?"),
            ("hesaru", "हेसरु", "नाम", "name", "Nanna hesaru Shafique."),
            ("ooru", "ऊरु", "शहर/गांव", "native place/town", "Nimma ooru elli?"),
            ("kelasa", "केलस", "काम", "work", "Nimma kelasa enu?"),
        ],
        "sentence": "Nimma name enu?",
        "pron": "निम्म नेम एनु?",
        "hi": "आपका नाम क्या है?",
        "en": "What is your name?",
        "breakdown": [("nimma", "आपका", "your"), ("name", "नाम", "name"), ("enu", "क्या", "what")],
        "logic": "Use `nimma` for your and `nanna` for my. Put the thing first, then `enu` for what.",
        "pattern": "Nimma ___ enu? / Nanna ___ ___",
        "examples": ["Nimma name enu?", "Nanna name Rahul.", "Nimma kelasa enu?", "Nanna ooru Delhi."],
        "guided_prompts": ["What is your name?", "My name is Rahul.", "What is your work?", "My native place is Delhi."],
        "guided_answers": ["Nimma name enu?", "Nanna name Rahul.", "Nimma kelasa enu?", "Nanna ooru Delhi."],
        "production_prompts": ["Ask a neighbour their name.", "Tell your name.", "Ask someone their work.", "Ask where their native place is."],
        "production_answers": ["Nimma name enu?", "Nanna name Shafique.", "Nimma kelasa enu?", "Nimma ooru elli?"],
        "roleplay_prompt": "You meet a neighbour in the lift. Ask their name and tell your name.",
        "roleplay_answer": "Nimma name enu?\n\nNanna name Shafique.",
        "quiz_prompts": ["What does `nanna` mean?", "What does `nimma` mean?", "Say: What is your name?", "Say: My work is office."],
        "quiz_answers": ["my", "your", "Nimma name enu?", "Nanna kelasa office."],
        "notes": ["nanna = my", "nimma = your", "Nimma ___ enu? = What is your ___?", "Nanna ___ ___ = My ___ is ___"],
        "natural": "Nimma name enu? is common; `hesaru` is Kannada, but `name` is also natural in Bangalore.",
        "mistake": "Do not use `neevu name`; use `nimma name` for your name.",
    },
    {
        "n": 26,
        "title": "What Are You Doing?",
        "recall": ["What is your name?", "Who is he/she?", "I will do it."],
        "words": [
            ("enu madthira", "एनु मद्तिरा", "क्या करेंगे/करते हैं?", "what do you do?", "Neevu enu madthira?"),
            ("enu madthidira", "एनु मद्तिदिरा", "क्या कर रहे हैं?", "what are you doing?", "Neevu enu madthidira?"),
            ("work madthini", "वर्क मद्तिनी", "मैं काम करता हूं", "I work", "Naan work madthini."),
            ("study madthini", "स्टडी मद्तिनी", "मैं पढ़ता हूं", "I study", "Naan study madthini."),
            ("IT", "आईटी", "आईटी", "IT", "Naan IT alli work madthini."),
        ],
        "sentence": "Neevu enu madthidira?",
        "pron": "नीवु एनु मद्तिदिरा?",
        "hi": "आप क्या कर रहे हैं?",
        "en": "What are you doing?",
        "breakdown": [("neevu", "आप", "you"), ("enu", "क्या", "what"), ("madthidira", "कर रहे हैं", "are doing")],
        "logic": "`madthira` asks about what someone does generally. `madthidira` asks what they are doing now.",
        "pattern": "Neevu enu madthidira?",
        "examples": ["Neevu enu madthidira?", "Naan work madthini.", "Naan study madthini.", "Naan IT alli work madthini."],
        "guided_prompts": ["What are you doing?", "I work.", "I study.", "I work in IT."],
        "guided_answers": ["Neevu enu madthidira?", "Naan work madthini.", "Naan study madthini.", "Naan IT alli work madthini."],
        "production_prompts": ["Ask a colleague what they are doing.", "Say you work.", "Say you work in office.", "Ask what work they do."],
        "production_answers": ["Neevu enu madthidira?", "Naan work madthini.", "Naan office alli work madthini.", "Neevu enu madthira?"],
        "roleplay_prompt": "A neighbour asks what you do. Answer simply and ask them back.",
        "roleplay_answer": "Naan IT alli work madthini. Neevu enu madthira?",
        "quiz_prompts": ["What does `madthidira` ask?", "Say: I work in office.", "Say: What do you do?", "Say: I study."],
        "quiz_answers": ["What are you doing?", "Naan office alli work madthini.", "Neevu enu madthira?", "Naan study madthini."],
        "notes": ["Neevu enu madthidira? = What are you doing?", "Neevu enu madthira? = What do you do?", "Naan ___ madthini = I do ___"],
        "natural": "People may ask `Enu madthira?` casually; context tells whether it means work or current action.",
        "mistake": "Do not mix `madthira` and `madthini`: one is you, one is I.",
    },
    {
        "n": 27,
        "title": "Eating And Drinking",
        "recall": ["I want more water.", "Is coffee available?", "Enough."],
        "words": [
            ("oota", "ऊटा", "खाना", "meal/food", "Oota aayta?"),
            ("tindi", "तिंडि", "नाश्ता", "snack/breakfast", "Tindi beku."),
            ("kudithini", "कुडितिनी", "मैं पीता हूं", "I drink", "Coffee kudithini."),
            ("tinithini", "तिनितिनी", "मैं खाता हूं", "I eat", "Tindi tinithini."),
            ("aayta", "आय्ता", "हो गया?", "done?", "Oota aayta?"),
        ],
        "sentence": "Oota aayta?",
        "pron": "ऊटा आय्ता?",
        "hi": "खाना हो गया?",
        "en": "Did you eat? / Is food done?",
        "breakdown": [("oota", "खाना", "meal"), ("aayta", "हो गया?", "done?")],
        "logic": "`aayta?` asks if something is done. `Oota aayta?` is a common friendly question.",
        "pattern": "___ aayta?",
        "examples": ["Oota aayta?", "Payment aayta?", "Work aayta?", "Bill aayta?"],
        "guided_prompts": ["Did you eat?", "Payment done?", "Work done?", "I drink coffee."],
        "guided_answers": ["Oota aayta?", "Payment aayta?", "Work aayta?", "Coffee kudithini."],
        "production_prompts": ["Ask a colleague if they ate.", "Say you want breakfast/snack.", "Say you drink tea.", "Ask if payment is done."],
        "production_answers": ["Oota aayta?", "Tindi beku.", "Tea kudithini.", "Payment aayta?"],
        "roleplay_prompt": "At office, a colleague asks if you ate. Say no, you want tindi.",
        "roleplay_answer": "Illa, tindi beku.",
        "quiz_prompts": ["What does `oota` mean?", "What does `aayta` mean?", "Say: Work done?", "Say: I eat tindi."],
        "quiz_answers": ["meal/food", "done?", "Work aayta?", "Tindi tinithini."],
        "notes": ["Oota aayta? = Did you eat?", "___ aayta? = Is ___ done?", "kudithini = I drink", "tinithini = I eat"],
        "natural": "Oota aayta? is a very common social question, like Hindi `khana hua?`.",
        "mistake": "Do not translate literally with `eat happened`; just use `Oota aayta?`.",
    },
    {
        "n": 28,
        "title": "Housekeeping Instructions",
        "recall": ["Come here.", "Do this.", "Wait a little."],
        "words": [
            ("clean madi", "क्लीन माडि", "साफ कीजिए", "clean", "Room clean madi."),
            ("haaki", "हाकि", "डालिए/रखिए", "put", "Dustbin alli haaki."),
            ("tegedi", "तेगेदि", "निकालिए", "remove/take out", "Idannu tegedi."),
            ("dustbin", "डस्टबिन", "कूड़ादान", "dustbin", "Dustbin elli?"),
            ("floor", "फ्लोर", "फर्श", "floor", "Floor clean madi."),
        ],
        "sentence": "Room clean madi.",
        "pron": "रूम क्लीन माडि.",
        "hi": "कमरा साफ कीजिए.",
        "en": "Please clean the room.",
        "breakdown": [("room", "कमरा", "room"), ("clean madi", "साफ कीजिए", "clean/do clean")],
        "logic": "Use the object first, then the action. English action words plus `madi` are common for household instructions.",
        "pattern": "Object + action madi",
        "examples": ["Room clean madi.", "Floor clean madi.", "Dustbin alli haaki.", "Idannu tegedi."],
        "guided_prompts": ["Clean the room.", "Clean the floor.", "Put it in dustbin.", "Remove this."],
        "guided_answers": ["Room clean madi.", "Floor clean madi.", "Dustbin alli haaki.", "Idannu tegedi."],
        "production_prompts": ["Ask housekeeping to clean the room.", "Ask where the dustbin is.", "Say put this there.", "Say remove this packet."],
        "production_answers": ["Room clean madi.", "Dustbin elli?", "Idannu alli haaki.", "Idannu packet tegedi."],
        "roleplay_prompt": "Housekeeping comes. Give two simple instructions politely.",
        "roleplay_answer": "Room clean madi. Dustbin alli haaki.",
        "quiz_prompts": ["What does `haaki` mean?", "What does `tegedi` mean?", "Say: Clean floor.", "Say: Put this there."],
        "quiz_answers": ["put", "remove/take out", "Floor clean madi.", "Idannu alli haaki."],
        "notes": ["Room clean madi = Clean the room", "___ alli haaki = Put in ___", "Idannu tegedi = Remove this"],
        "natural": "Room clean madi is natural spoken Bangalore Kannada with English `clean`.",
        "mistake": "Keep instructions short; long English-style sentences are harder to understand.",
    },
    {
        "n": 29,
        "title": "Maintenance And Staff Requests",
        "recall": ["Will you come now?", "I will do it later.", "Show the room."],
        "words": [
            ("check madi", "चेक माडि", "चेक कीजिए", "check", "Idu check madi."),
            ("fix madi", "फिक्स माडि", "ठीक कीजिए", "fix", "Fan fix madi."),
            ("repair madi", "रिपेयर माडि", "मरम्मत कीजिए", "repair", "Door repair madi."),
            ("fan", "फैन", "पंखा", "fan", "Fan work agalla."),
            ("door", "डोर", "दरवाज़ा", "door", "Door close agalla."),
        ],
        "sentence": "Idu check madi.",
        "pron": "इदु चेक माडि.",
        "hi": "यह चेक कीजिए.",
        "en": "Please check this.",
        "breakdown": [("idu", "यह", "this"), ("check madi", "चेक कीजिए", "check")],
        "logic": "For staff requests, combine the object with `check/fix/repair madi`.",
        "pattern": "Object + check/fix/repair madi",
        "examples": ["Idu check madi.", "Fan fix madi.", "Door repair madi.", "Ivaga barthira?"],
        "guided_prompts": ["Check this.", "Fix the fan.", "Repair the door.", "Will you come now?"],
        "guided_answers": ["Idu check madi.", "Fan fix madi.", "Door repair madi.", "Ivaga barthira?"],
        "production_prompts": ["Ask maintenance to check this.", "Ask them to fix the fan.", "Ask if they will come later.", "Say door repair is needed."],
        "production_answers": ["Idu check madi.", "Fan fix madi.", "Later barthira?", "Door repair beku."],
        "roleplay_prompt": "Call maintenance for a fan problem. Ask them to come now and check it.",
        "roleplay_answer": "Fan fix madi. Ivaga barthira? Idu check madi.",
        "quiz_prompts": ["Say: Repair the door.", "Say: Check this.", "What does `fan` mean?", "Say: Will you come later?"],
        "quiz_answers": ["Door repair madi.", "Idu check madi.", "fan", "Later barthira?"],
        "notes": ["Idu check madi = Check this", "Fan fix madi = Fix the fan", "Door repair madi = Repair the door"],
        "natural": "English repair words are normal with apartment maintenance staff.",
        "mistake": "Use `madi` for polite requests, not bare English commands.",
    },
    {
        "n": 30,
        "title": "Office And Neighbour Intro",
        "recall": ["What is your work?", "Did you eat?", "My name is Shafique."],
        "words": [
            ("illi irthini", "इल्लि इर्तिनी", "मैं यहां रहता हूं", "I stay/live here", "Naan illi irthini."),
            ("new", "न्यू", "नया", "new", "Naan illi new."),
            ("same floor", "सेम फ्लोर", "एक ही फ्लोर", "same floor", "Naan same floor alli."),
            ("nice", "नाइस", "अच्छा", "nice", "Nice meet madiddu."),
            ("meet madi", "मीट माडि", "मिलिए", "meet", "Aamele meet madi."),
        ],
        "sentence": "Naan illi irthini.",
        "pron": "नान् इल्लि इर्तिनी.",
        "hi": "मैं यहां रहता हूं.",
        "en": "I live/stay here.",
        "breakdown": [("naan", "मैं", "I"), ("illi", "यहां", "here"), ("irthini", "रहता हूं", "stay/live")],
        "logic": "`irthini` means I stay/live/am there. Use it for where you live or are based.",
        "pattern": "Naan ___ alli/illi irthini",
        "examples": ["Naan illi irthini.", "Naan apartment alli irthini.", "Naan same floor alli.", "Naan illi new."],
        "guided_prompts": ["I live here.", "I live in apartment.", "I am on same floor.", "I am new here."],
        "guided_answers": ["Naan illi irthini.", "Naan apartment alli irthini.", "Naan same floor alli.", "Naan illi new."],
        "production_prompts": ["Tell a neighbour you live here.", "Say you are new here.", "Say you are on same floor.", "Ask their name."],
        "production_answers": ["Naan illi irthini.", "Naan illi new.", "Naan same floor alli.", "Nimma name enu?"],
        "roleplay_prompt": "Meet a neighbour. Say your name, that you live here, and ask their name.",
        "roleplay_answer": "Nanna name Shafique. Naan illi irthini. Nimma name enu?",
        "quiz_prompts": ["What does `irthini` mean?", "Say: I am new here.", "Say: I live in apartment.", "Say: What is your name?"],
        "quiz_answers": ["I stay/live", "Naan illi new.", "Naan apartment alli irthini.", "Nimma name enu?"],
        "notes": ["Naan illi irthini = I live/stay here", "Naan illi new = I am new here", "Naan same floor alli = I am on same floor"],
        "natural": "Naan illi new is mixed but understandable and common for beginners in Bangalore.",
        "mistake": "Do not overbuild introductions; short clear lines sound more natural.",
    },
]

more_lessons = [
    (31, "Today, Tomorrow, Yesterday", "Ivattu office hogbeku.", "इवत्तु ऑफिस होग्बेकु.", "आज ऑफिस जाना है.", "I need to go to office today.", [("ivattu","इवत्तु","आज","today","Ivattu barthini."),("naale","नाले","कल","tomorrow","Naale barthini."),("ninne","निन्ने","कल बीता","yesterday","Ninne payment aayta?"),("beligge","बेळिग्गे","सुबह","morning","Beligge barthini."),("sanje","संजे","शाम","evening","Sanje barthini.")], "Time + sentence", ["Ivattu office hogbeku.", "Naale barthini.", "Ninne payment aayta?", "Sanje meet madi."], ["Today I need to go to office.", "I will come tomorrow.", "Payment happened yesterday?", "Meet in evening."], ["Ivattu office hogbeku.", "Naale barthini.", "Ninne payment aayta?", "Sanje meet madi."], "Tell security you will come tomorrow morning.", "Naale beligge barthini."),
    (32, "At What Time?", "Yaava time barthira?", "याव टाइम बर्तिरा?", "किस टाइम आएंगे?", "At what time will you come?", [("yaava time","याव टाइम","किस समय","what time","Yaava time barthira?"),("ghante","घंटे","बजे","o'clock/hour","Three ghante."),("half hour","हाफ आवर","आधा घंटा","half hour","Half hour alli barthini."),("early","अर्ली","जल्दी","early","Early barthira?"),("late","लेट","देर","late","Late agutte.")], "Yaava time + action?", ["Yaava time barthira?", "Three ghante barthini.", "Half hour alli barthini.", "Late agutte."], ["What time will you come?", "I will come at three.", "I will come in half hour.", "It will be late."], ["Yaava time barthira?", "Three ghante barthini.", "Half hour alli barthini.", "Late agutte."], "Ask maintenance what time they will come.", "Yaava time barthira?"),
    (33, "When Will It Happen?", "Yaavaga barthira?", "यावाग बर्तिरा?", "कब आएंगे?", "When will you come?", [("yaavaga","यावाग","कब","when","Yaavaga barthira?"),("iga","इगा","अभी","now","Iga banni."),("amele","आमेले","बाद में","later/after","Amele madthini."),("munche","मुन्चे","पहले","before","Munche call madi."),("ready","रेडी","तैयार","ready","Ready aayta?")], "Yaavaga ___?", ["Yaavaga barthira?", "Iga banni.", "Amele madthini.", "Munche call madi."], ["When will you come?", "Come now.", "I will do later.", "Call before."], ["Yaavaga barthira?", "Iga banni.", "Amele madthini.", "Munche call madi."], "Ask a delivery agent when he will come, then say call before coming.", "Yaavaga barthira? Baro munche call madi."),
    (34, "Daily Routine", "Daily office hogthini.", "डेली ऑफिस होग्तिनी.", "मैं रोज़ ऑफिस जाता हूं.", "I go to office daily.", [("daily","डेली","रोज़","daily","Daily office hogthini."),("sometimes","समटाइम्स","कभी-कभी","sometimes","Sometimes metro hogthini."),("usually","यूज़ुअली","आमतौर पर","usually","Usually cab beda."),("weekend","वीकेंड","सप्ताहांत","weekend","Weekend mane alli."),("busy irthini","बिज़ी इर्तिनी","व्यस्त रहता हूं","I am busy","Naan busy irthini.")], "Frequency + action", ["Daily office hogthini.", "Sometimes metro hogthini.", "Usually cab beda.", "Weekend mane alli."], ["I go to office daily.", "Sometimes I go by metro.", "Usually cab not wanted.", "Weekend at home."], ["Daily office hogthini.", "Sometimes metro hogthini.", "Usually cab beda.", "Weekend mane alli."], "Tell a neighbour your daily routine in two lines.", "Daily office hogthini. Weekend mane alli irthini."),
    (35, "Already And Not Yet", "Payment aagide.", "पेमेंट आगिदे.", "पेमेंट हो गया है.", "Payment is done.", [("aagide","आगिदे","हो गया है","is done/has happened","Payment aagide."),("innuu illa","इन्नू इल्ला","अभी नहीं","not yet","Innuu illa."),("mugitu","मुगितु","खत्म हुआ","finished","Work mugitu."),("start aagide","स्टार्ट आगिदे","शुरू हुआ","has started","Class start aagide."),("finish aagilla","फिनिश आगिल्ला","खत्म नहीं हुआ","not finished","Work finish aagilla.")], "___ aagide / ___ aagilla", ["Payment aagide.", "Work mugitu.", "Innuu illa.", "Work finish aagilla."], ["Payment is done.", "Work finished.", "Not yet.", "Work not finished."], ["Payment aagide.", "Work mugitu.", "Innuu illa.", "Work finish aagilla."], "Security asks if payment is done. Say yes, payment is done.", "Haudu, payment aagide."),
    (36, "Plans Combo", "Naale beligge barthini.", "नाले बेळिग्गे बर्तिनी.", "मैं कल सुबह आऊंगा.", "I will come tomorrow morning.", [("plan","प्लैन","योजना","plan","Plan enu?"),("free","फ्री","खाली","free", "Naale free ideya?"),("meet","मीट","मिलना","meet","Naale meet madi."),("confirm madi","कन्फर्म माडि","पक्का कीजिए","confirm","Time confirm madi."),("cancel madi","कैंसल माडि","रद्द कीजिए","cancel","Booking cancel madi.")], "Time + action", ["Naale beligge barthini.", "Sanje meet madi.", "Time confirm madi.", "Booking cancel madi."], ["I will come tomorrow morning.", "Meet in evening.", "Confirm time.", "Cancel booking."], ["Naale beligge barthini.", "Sanje meet madi.", "Time confirm madi.", "Booking cancel madi."], "Make a plan with a colleague for tomorrow evening.", "Naale sanje meet madi. Time confirm madi."),
    (37, "Not Working", "Fan work agalla.", "फैन वर्क आगल्ला.", "पंखा काम नहीं कर रहा.", "The fan is not working.", [("work agalla","वर्क आगल्ला","काम नहीं करता","not working","Fan work agalla."),("open agalla","ओपन आगल्ला","नहीं खुलता","does not open","Door open agalla."),("close agalla","क्लोज़ आगल्ला","बंद नहीं होता","does not close","Door close agalla."),("problem ide","प्रॉब्लम इदे","समस्या है","there is a problem","Problem ide."),("urgent","अर्जेंट","तुरंत","urgent","Urgent check madi.")], "___ agalla", ["Fan work agalla.", "Door open agalla.", "Door close agalla.", "Problem ide."], ["Fan not working.", "Door does not open.", "Door does not close.", "There is a problem."], ["Fan work agalla.", "Door open agalla.", "Door close agalla.", "Problem ide."], "Call maintenance and explain fan problem.", "Fan work agalla. Problem ide. Urgent check madi."),
    (38, "Water, Electricity, Internet", "Internet work agalla.", "इंटरनेट वर्क आगल्ला.", "इंटरनेट काम नहीं कर रहा.", "Internet is not working.", [("current","करंट","बिजली","electricity","Current illa."),("internet","इंटरनेट","इंटरनेट","internet","Internet work agalla."),("water supply","वॉटर सप्लाई","पानी सप्लाई","water supply","Water supply illa."),("light","लाइट","लाइट","light","Light work agalla."),("switch","स्विच","स्विच","switch","Switch check madi.")], "Utility + problem", ["Current illa.", "Water supply illa.", "Internet work agalla.", "Switch check madi."], ["No electricity.", "No water supply.", "Internet not working.", "Check switch."], ["Current illa.", "Water supply illa.", "Internet work agalla.", "Switch check madi."], "Tell apartment staff there is no water supply.", "Water supply illa. Please check madi."),
    (39, "Please Check And Fix", "Technician kalisi.", "टेक्नीशियन कळिसि.", "टेक्नीशियन भेजिए.", "Send a technician.", [("technician","टेक्नीशियन","तकनीशियन","technician","Technician kalisi."),("plumber","प्लंबर","प्लंबर","plumber","Plumber beku."),("electrician","इलेक्ट्रीशियन","इलेक्ट्रीशियन","electrician","Electrician kalisi."),("service","सर्विस","सेवा","service","Service beku."),("slot","स्लॉट","समय स्लॉट","slot","Slot ideya?")], "Person + kalisi", ["Technician kalisi.", "Plumber beku.", "Electrician kalisi.", "Slot ideya?"], ["Send technician.", "Need plumber.", "Send electrician.", "Is there a slot?"], ["Technician kalisi.", "Plumber beku.", "Electrician kalisi.", "Slot ideya?"], "Ask for electrician and ask when they will come.", "Electrician kalisi. Yaavaga barthira?"),
    (40, "Bring, Send, Tell", "Key tagondu banni.", "की तगोंडु बन्नि.", "चाबी लेकर आइए.", "Bring the key.", [("tagondu banni","तगोंडु बन्नि","लेकर आइए","bring","Key tagondu banni."),("kalisi","कळिसि","भेजिए","send","Photo kalisi."),("heli","हेळि","बताइए","tell","Problem heli."),("key","की","चाबी","key","Key elli?"),("photo","फोटो","फोटो","photo","Photo kalisi.")], "___ tagondu banni", ["Key tagondu banni.", "Photo kalisi.", "Problem heli.", "Bill tagondu banni."], ["Bring key.", "Send photo.", "Tell problem.", "Bring bill."], ["Key tagondu banni.", "Photo kalisi.", "Problem heli.", "Bill tagondu banni."], "Ask security to bring the key and call after reaching.", "Key tagondu banni. Reach aadmele call madi."),
    (41, "Delivery Problem", "Parcel bandilla.", "पार्सल बन्दिल्ला.", "पार्सल नहीं आया.", "Parcel has not arrived.", [("parcel","पार्सल","पार्सल","parcel","Parcel bandilla."),("order","ऑर्डर","ऑर्डर","order","Order elli?"),("missing","मिसिंग","गायब","missing","Item missing."),("wrong item","रॉन्ग आइटम","गलत सामान","wrong item","Wrong item bandide."),("return madi","रिटर्न माडि","वापस कीजिए","return","Return madi.")], "___ bandide / bandilla", ["Parcel bandide.", "Parcel bandilla.", "Wrong item bandide.", "Return madi."], ["Parcel arrived.", "Parcel has not arrived.", "Wrong item came.", "Return it."], ["Parcel bandide.", "Parcel bandilla.", "Wrong item bandide.", "Return madi."], "Tell delivery support that wrong item came.", "Wrong item bandide. Return madi."),
    (42, "Polite Complaint", "Swalpa help madi.", "स्वल्प हेल्प माडि.", "थोड़ी मदद कीजिए.", "Please help a little.", [("help madi","हेल्प माडि","मदद कीजिए","help","Swalpa help madi."),("complaint","कम्प्लेंट","शिकायत","complaint","Complaint madbeku."),("manager","मैनेजर","मैनेजर","manager","Manager yaaru?"),("matadi","माताडि","बात कीजिए","speak/talk","Manager jothe matadi."),("jothe","जोते","के साथ","with","Avru jothe matadi.")], "___ jothe matadi", ["Swalpa help madi.", "Complaint madbeku.", "Manager yaaru?", "Manager jothe matadi."], ["Please help.", "Need to complain.", "Who is manager?", "Speak with manager."], ["Swalpa help madi.", "Complaint madbeku.", "Manager yaaru?", "Manager jothe matadi."], "At a store, politely ask for help and manager.", "Swalpa help madi. Manager yaaru? Avru jothe matadbeku."),
    (43, "I Went, I Came", "Naan office ge hode.", "नान् ऑफिस गे होदे.", "मैं ऑफिस गया.", "I went to office.", [("hode","होदे","मैं गया","I went","Naan office ge hode."),("bande","बन्दे","मैं आया","I came","Naan ninne bande."),("manege","मनेगे","घर को","to home","Manege hode."),("office ge","ऑफिस गे","ऑफिस को","to office","Office ge hode."),("apas bandide","वापस बन्दिदे","वापस आया है","came back/has returned","Parcel apas bandide.")], "Naan ___ ge hode / Naan ___ bande", ["Naan office ge hode.", "Naan manege hode.", "Ninne bande.", "Naale barthini."], ["I went to office.", "I went home.", "I came yesterday.", "I will come tomorrow."], ["Naan office ge hode.", "Naan manege hode.", "Ninne bande.", "Naale barthini."], "Tell a colleague you went home yesterday.", "Ninne manege hode."),
    (44, "I Bought And Took", "Idannu konde.", "इदन्नु कोंडे.", "मैंने इसे खरीदा.", "I bought this.", [("konde","कोंडे","मैंने खरीदा","I bought","Idannu konde."),("togonde","तगोंडे","मैंने ले लिया","I took","Idannu togonde."),("kotte","कोट्टे","मैंने दिया","I gave","Bill kotte."),("market","मार्केट","बाज़ार","market","Market alli konde."),("medicine","मेडिसिन","दवा","medicine","Medicine konde.")], "Object + konde/togonde/kotte", ["Idannu konde.", "Idannu togonde.", "Bill kotte.", "Medicine konde."], ["I bought this.", "I took this.", "I gave bill.", "I bought medicine."], ["Idannu konde.", "Idannu togonde.", "Bill kotte.", "Medicine konde."], "Tell someone you bought medicine from market.", "Market alli medicine konde."),
    (45, "I Saw, Called, Told", "Naan avru nodide.", "नान् अव्रु नोडिदे.", "मैंने उन्हें देखा.", "I saw him/her.", [("nodide","नोडिदे","मैंने देखा","I saw","Naan avru nodide."),("call madide","कॉल मडिदे","कॉल किया","called","Naan call madide."),("helide","हेळिदे","मैंने बताया","I told","Naan helide."),("message madide","मेसेज मडिदे","मैसेज किया","messaged","Message madide."),("reply illa","रिप्लाई इल्ला","जवाब नहीं","no reply","Reply illa.")], "Naan ___ madide / Naan ___ helide", ["Naan call madide.", "Naan message madide.", "Naan helide.", "Reply illa."], ["I called.", "I messaged.", "I told.", "No reply."], ["Naan call madide.", "Naan message madide.", "Naan helide.", "Reply illa."], "Tell delivery support you called but no reply.", "Naan call madide. Reply illa."),
    (46, "What Happened?", "En aaytu?", "एन आय्तु?", "क्या हुआ?", "What happened?", [("en aaytu","एन आय्तु","क्या हुआ","what happened","En aaytu?"),("yake","याके","क्यों","why","Yake late?"),("late aaytu","लेट आय्तु","देर हुई","became late","Late aaytu."),("miss aaytu","मिस आय्तु","छूट गया","missed","Call miss aaytu."),("cancel aaytu","कैंसल आय्तु","रद्द हुआ","got cancelled","Booking cancel aaytu.")], "___ aaytu?", ["En aaytu?", "Yake late?", "Call miss aaytu.", "Booking cancel aaytu."], ["What happened?", "Why late?", "Call missed.", "Booking got cancelled."], ["En aaytu?", "Yake late?", "Call miss aaytu.", "Booking cancel aaytu."], "Ask driver why he is late and what happened.", "Yake late? En aaytu?"),
    (47, "Because And So", "Traffic jaasti, late aaytu.", "ट्रैफिक जास्ति, लेट आय्तु.", "ट्रैफिक ज्यादा था, देर हो गई.", "Traffic was heavy, so it got late.", [("adakke","अदक्के","इसलिए","so/therefore","Adakke late aaytu."),("because","बिकॉज़","क्योंकि","because","Traffic because late aaytu."),("reason","रीज़न","कारण","reason","Reason enu?"),("problem aaytu","प्रॉब्लम आय्तु","समस्या हुई","problem happened","Problem aaytu."),("sorry","सॉरी","माफ़ कीजिए","sorry","Sorry, late aaytu.")], "Reason, result", ["Traffic jaasti, late aaytu.", "Adakke late aaytu.", "Reason enu?", "Sorry, late aaytu."], ["Traffic heavy, got late.", "So it got late.", "What is reason?", "Sorry, got late."], ["Traffic jaasti, late aaytu.", "Adakke late aaytu.", "Reason enu?", "Sorry, late aaytu."], "Explain to a colleague why you are late.", "Sorry, traffic jaasti. Adakke late aaytu."),
    (48, "Past Story Combo", "Ninne market ge hode.", "निन्ने मार्केट गे होदे.", "कल मार्केट गया.", "Yesterday I went to market.", [("market ge","मार्केट गे","बाज़ार को","to market","Market ge hode."),("alli","अल्लि","वहां/में","there/at","Alli medicine konde."),("amele","आमेले","फिर","then/after","Amele manege bande."),("friend","फ्रेंड","दोस्त","friend","Friend jothe hode."),("jothe","जोते","के साथ","with","Friend jothe.")], "Past sequence: time + place + action", ["Ninne market ge hode.", "Alli medicine konde.", "Amele manege bande.", "Friend jothe hode."], ["Yesterday I went to market.", "Bought medicine there.", "Then came home.", "Went with friend."], ["Ninne market ge hode.", "Alli medicine konde.", "Amele manege bande.", "Friend jothe hode."], "Say a simple 3-line story about going to market yesterday.", "Ninne market ge hode. Alli medicine konde. Amele manege bande."),
    (49, "I Like, I Do Not Like", "Nanage coffee ishta.", "ननगे कॉफी इष्ट.", "मुझे कॉफी पसंद है.", "I like coffee.", [("nanage","ननगे","मुझे","to me/I", "Nanage ishta."),("ishta","इष्ट","पसंद","like","Coffee ishta."),("ishta illa","इष्ट इल्ला","पसंद नहीं","do not like","Tea ishta illa."),("tumba","तुम्ब","बहुत","very", "Tumba ishta."),("food","फूड","खाना","food","Food ishta.")], "Nanage ___ ishta", ["Nanage coffee ishta.", "Nanage tea ishta illa.", "Tumba ishta.", "Food ishta."], ["I like coffee.", "I do not like tea.", "Like very much.", "Like food."], ["Nanage coffee ishta.", "Nanage tea ishta illa.", "Tumba ishta.", "Food ishta."], "Tell a colleague you like coffee but not tea.", "Nanage coffee ishta. Tea ishta illa."),
    (50, "Good, Bad, Tasty", "Coffee chennagide.", "कॉफी चेन्नागिदे.", "कॉफी अच्छी है.", "Coffee is good.", [("chennagide","चेन्नागिदे","अच्छा है","is good","Coffee chennagide."),("chennagilla","चेन्नागिल्ला","अच्छा नहीं","not good","Idu chennagilla."),("ruchi","रुचि","स्वाद","taste","Ruchi chennagide."),("tasty","टेस्टी","स्वादिष्ट","tasty","Tasty ide."),("spicy","स्पाइसी","तीखा","spicy","Spicy jaasti.")], "___ chennagide", ["Coffee chennagide.", "Idu chennagilla.", "Ruchi chennagide.", "Spicy jaasti."], ["Coffee is good.", "This is not good.", "Taste is good.", "Too spicy."], ["Coffee chennagide.", "Idu chennagilla.", "Ruchi chennagide.", "Spicy jaasti."], "At a restaurant, say the food is good but too spicy.", "Food chennagide. Spicy jaasti."),
    (51, "Easy And Difficult", "Kannada swalpa kashta.", "कन्नडा स्वल्प कष्ट.", "कन्नड़ थोड़ा कठिन है.", "Kannada is a little difficult.", [("sulabha","सुलभ", "आसान", "easy", "Idu sulabha."),("kashta","कष्ट","मुश्किल","difficult","Kannada kashta."),("artha aaytu","अर्थ आय्तु","समझ आया","understood","Artha aaytu."),("artha agilla","अर्थ आगिल्ला","समझ नहीं आया","did not understand","Artha agilla."),("slow aagi","स्लो आगि","धीरे से","slowly","Slow aagi heli.")], "___ sulabha/kashta", ["Idu sulabha.", "Kannada swalpa kashta.", "Artha aaytu.", "Slow aagi heli."], ["This is easy.", "Kannada is a little difficult.", "Understood.", "Tell slowly."], ["Idu sulabha.", "Kannada swalpa kashta.", "Artha aaytu.", "Slow aagi heli."], "Tell someone you did not understand and ask them to speak slowly.", "Artha agilla. Slow aagi heli."),
    (52, "Which Do You Prefer?", "Nimge yaavdu ishta?", "निमगे याव्दु इष्ट?", "आपको कौन सा पसंद है?", "Which one do you like?", [("nimge","निमगे","आपको","to you","Nimge ishta?"),("yaavdu","याव्दु","कौन सा","which one","Yaavdu beku?"),("better","बेटर","बेहतर","better","Idu better."),("option","ऑप्शन","विकल्प","option","Option ideya?"),("choose madi","चूज़ माडि","चुनिए","choose","Yaavdu choose madi.")], "Nimge ___ ishta?", ["Nimge coffee ishta?", "Nimge yaavdu ishta?", "Yaavdu beku?", "Idu better."], ["Do you like coffee?", "Which one do you like?", "Which one do you want?", "This is better."], ["Nimge coffee ishta?", "Nimge yaavdu ishta?", "Yaavdu beku?", "Idu better."], "Ask a friend which food they like.", "Nimge yaavdu food ishta?"),
    (53, "Feeling Okay", "Nanage tired aagide.", "ननगे टायर्ड आगिदे.", "मैं थक गया हूं.", "I am tired.", [("tired aagide","टायर्ड आगिदे","थक गया","tired","Nanage tired aagide."),("hungry","हंग्री","भूख लगी","hungry","Nanage hungry."),("sleepy","स्लीपी","नींद आ रही","sleepy","Nanage sleepy."),("okay ide","ओके इदे","ठीक है","is okay","Nanage okay ide."),("health","हेल्थ","तबीयत","health","Health sari illa.")], "Nanage ___", ["Nanage tired aagide.", "Nanage hungry.", "Nanage sleepy.", "Health sari illa."], ["I am tired.", "I am hungry.", "I am sleepy.", "Health is not okay."], ["Nanage tired aagide.", "Nanage hungry.", "Nanage sleepy.", "Health sari illa."], "Tell a colleague you are tired and will come later.", "Nanage tired aagide. Aamele barthini."),
    (54, "Opinion Combo", "Nanage idu chennagide.", "ननगे इदु चेन्नागिदे.", "मुझे यह अच्छा लगा.", "I think this is good.", [("nanage anisutte","ननगे अनिसुत्ते","मुझे लगता है","I feel/think","Nanage anisutte."),("correct","करेक्ट","सही","correct","Idu correct."),("wrong","रॉन्ग","गलत","wrong","Idu wrong."),("okay","ओके","ठीक","okay","Idu okay."),("try madi","ट्राई माडि","कोशिश कीजिए","try","Try madi.")], "Nanage ___ anisutte", ["Nanage idu chennagide anisutte.", "Idu correct.", "Idu wrong.", "Try madi."], ["I feel this is good.", "This is correct.", "This is wrong.", "Try."], ["Nanage idu chennagide anisutte.", "Idu correct.", "Idu wrong.", "Try madi."], "Give an opinion about a route being better.", "Nanage idu route better anisutte."),
    (55, "Where Are You From?", "Neevu ellinda?", "नीवु एल्लिन्दा?", "आप कहां से हैं?", "Where are you from?", [("ellinda","एल्लिन्दा","कहां से","from where","Neevu ellinda?"),("Delhi inda","दिल्ली इन्दा","दिल्ली से","from Delhi","Naan Delhi inda."),("Bangalore alli","बैंगलोर अल्लि","बंगलौर में","in Bangalore","Bangalore alli irthini."),("eshtu varsha","एष्टु वर्ष","कितने साल","how many years","Eshtu varsha?"),("varsha","वर्ष","साल","year","Two varsha.")], "Neevu ellinda?", ["Neevu ellinda?", "Naan Delhi inda.", "Bangalore alli irthini.", "Eshtu varsha?"], ["Where are you from?", "I am from Delhi.", "I live in Bangalore.", "How many years?"], ["Neevu ellinda?", "Naan Delhi inda.", "Bangalore alli irthini.", "Eshtu varsha?"], "Tell a neighbour you are from Delhi and live in Bangalore.", "Naan Delhi inda. Bangalore alli irthini."),
    (56, "Family Talk", "Nimma family illi ideya?", "निम्म फैमिली इल्लि इदेया?", "आपकी फैमिली यहां है क्या?", "Is your family here?", [("family","फैमिली","परिवार","family","Family illi ideya?"),("parents","पेरेंट्स","माता-पिता","parents","Parents Delhi alli."),("wife","वाइफ","पत्नी","wife","Wife illi."),("husband","हज़्बैंड","पति","husband","Husband office alli."),("kids","किड्स","बच्चे","kids","Kids school alli.")], "Nimma family ___?", ["Nimma family illi ideya?", "Parents Delhi alli.", "Kids school alli.", "Family Bangalore alli."], ["Is your family here?", "Parents are in Delhi.", "Kids are at school.", "Family is in Bangalore."], ["Nimma family illi ideya?", "Parents Delhi alli.", "Kids school alli.", "Family Bangalore alli."], "Ask a colleague if their family is in Bangalore.", "Nimma family Bangalore alli ideya?"),
    (57, "Languages", "Kannada swalpa barutte.", "कन्नडा स्वल्प बरुत्ते.", "थोड़ी कन्नड़ आती है.", "I know a little Kannada.", [("barutte","बरुत्ते","आता है","know/comes","Kannada barutte."),("baralla","बरल्ला","नहीं आता","do not know","Kannada baralla."),("Hindi barutte","हिंदी बरुत्ते","हिंदी आती है","know Hindi","Hindi barutte."),("English barutte","इंग्लिश बरुत्ते","अंग्रेज़ी आती है","know English","English barutte."),("kalithidini","कलितिदिनी","सीख रहा हूं","learning","Kannada kalithidini.")], "Language + barutte/baralla", ["Kannada swalpa barutte.", "Hindi barutte.", "English barutte.", "Kannada kalithidini."], ["I know little Kannada.", "I know Hindi.", "I know English.", "I am learning Kannada."], ["Kannada swalpa barutte.", "Hindi barutte.", "English barutte.", "Kannada kalithidini."], "Tell a shopkeeper you are learning Kannada and ask them to speak slowly.", "Kannada kalithidini. Slow aagi heli."),
    (58, "Weekend And Hobbies", "Weekend en madthira?", "वीकेंड एन मद्तिरा?", "वीकेंड पर क्या करते हैं?", "What do you do on weekends?", [("hobby","हॉबी","शौक","hobby","Nimma hobby enu?"),("movie","मूवी","फिल्म","movie","Movie nodthini."),("walk","वॉक","चलना","walk","Walk hogthini."),("gym","जिम","जिम","gym","Gym hogthini."),("rest","रेस्ट","आराम","rest","Rest madthini.")], "Weekend ___ madthira?", ["Weekend en madthira?", "Movie nodthini.", "Walk hogthini.", "Rest madthini."], ["What do you do on weekend?", "I watch movie.", "I go for walk.", "I rest."], ["Weekend en madthira?", "Movie nodthini.", "Walk hogthini.", "Rest madthini."], "Ask a friend their weekend plan and say you will rest.", "Weekend en madthira? Naan rest madthini."),
    (59, "Invite And Meet", "Coffee ge barthira?", "कॉफी गे बर्तिरा?", "कॉफी के लिए आएंगे?", "Will you come for coffee?", [("ge","गे","को/के लिए","to/for","Coffee ge barthira?"),("together","टुगेदर","साथ में","together","Together hogona."),("hogona","होगोणा","चलें","let us go","Coffee ge hogona."),("barona","बरोणा","आएं","let us come","Naale barona."),("free ideya","फ्री इदेया","खाली हैं क्या","are you free?","Sanje free ideya?")], "___ ge hogona/barthira?", ["Coffee ge barthira?", "Coffee ge hogona.", "Sanje free ideya?", "Together hogona."], ["Will you come for coffee?", "Let us go for coffee.", "Are you free evening?", "Let us go together."], ["Coffee ge barthira?", "Coffee ge hogona.", "Sanje free ideya?", "Together hogona."], "Invite a colleague for tea in the evening.", "Sanje free ideya? Tea ge hogona?"),
    (60, "Small Talk Combo", "Bangalore hege ide?", "बैंगलोर हेगे इदे?", "बंगलौर कैसा है?", "How is Bangalore?", [("hege","हेगे","कैसा","how","Bangalore hege ide?"),("weather","वेदर","मौसम","weather","Weather chennagide."),("area","एरिया","इलाका","area","Area chennagide."),("safe","सेफ","सुरक्षित","safe","Area safe ide."),("expensive","एक्सपेंसिव","महंगा","expensive","Bangalore expensive.")], "___ hege ide?", ["Bangalore hege ide?", "Weather chennagide.", "Area safe ide.", "Bangalore expensive."], ["How is Bangalore?", "Weather is good.", "Area is safe.", "Bangalore is expensive."], ["Bangalore hege ide?", "Weather chennagide.", "Area safe ide.", "Bangalore expensive."], "Have small talk with a neighbour about Bangalore and weather.", "Bangalore hege ide? Weather chennagide."),
    (61, "Natural Short Replies", "Gotha.", "गोत्ता.", "पता है.", "I know.", [("gotha","गोत्ता","पता है","know","Nanage gotha."),("gothilla","गोत्तिल्ला","पता नहीं","do not know","Nanage gothilla."),("beda bidi","बेडा बिडि","रहने दीजिए","leave it","Beda bidi."),("aaytu","आय्तु","हो गया/ठीक","done/okay","Aaytu."),("nodona","नोडोणा","देखते हैं","let us see","Nodona.")], "Short reply", ["Gotha.", "Gothilla.", "Beda bidi.", "Aaytu."], ["Know.", "Do not know.", "Leave it.", "Done/okay."], ["Gotha.", "Gothilla.", "Beda bidi.", "Aaytu."], "Practice short replies to driver questions.", "Gotha. Aaytu. Beda bidi."),
    (62, "Speak Slowly, Repeat", "Innondu sala heli.", "इन्नोंदु सल हेळि.", "एक बार और बताइए.", "Please say one more time.", [("innondu","इन्नोंदु","एक और","one more","Innondu tea kodi."),("sala","सल","बार","time/turn","Innondu sala heli."),("repeat madi","रिपीट माडि","दोहराइए","repeat","Repeat madi."),("clear aagi","क्लियर आगि","साफ़ से","clearly","Clear aagi heli."),("kelistilla","केलिस्तिल्ला","सुनाई नहीं दे रहा","cannot hear","Kelistilla.")], "Request clarification", ["Innondu sala heli.", "Repeat madi.", "Clear aagi heli.", "Kelistilla."], ["Say one more time.", "Repeat.", "Say clearly.", "Cannot hear."], ["Innondu sala heli.", "Repeat madi.", "Clear aagi heli.", "Kelistilla."], "On a noisy call, ask the delivery agent to repeat clearly.", "Kelistilla. Innondu sala clear aagi heli."),
    (63, "Fast Shopkeeper Replies", "Ide, togoli.", "इदे, तगोळि.", "है, ले लीजिए.", "It is there, take it.", [("togoli","तगोळि","ले लीजिए","take it","Ide, togoli."),("illa saar","इल्ला सार","नहीं सर","not there sir","Illa saar."),("baralla","बरल्ला","नहीं आता","will not come/know","Stock baralla."),("naale banni","नाले बन्नि","कल आइए","come tomorrow","Naale banni."),("cash only","कैश ओनली","सिर्फ नकद","cash only","Cash only.")], "Listen for reply chunks", ["Ide, togoli.", "Illa saar.", "Naale banni.", "Cash only."], ["It is there, take it.", "Not there sir.", "Come tomorrow.", "Cash only."], ["Ide, togoli.", "Illa saar.", "Naale banni.", "Cash only."], "Shopkeeper says item is not there and asks you to come tomorrow. Respond okay.", "Sari. Naale barthini."),
    (64, "Fast Auto Replies", "Baralla.", "बरल्ला.", "नहीं आएगा.", "Will not come.", [("baralla","बरल्ला","नहीं आएगा","will not come","Meter alli baralla."),("extra beku","एक्स्ट्रा बेकु","एक्स्ट्रा चाहिए","extra needed","Extra beku."),("traffic ide","ट्रैफिक इदे","ट्रैफिक है","traffic is there","Traffic ide."),("door illa","डोर इल्ला","रास्ता नहीं","no route/opening","Door illa."),("illi beda","इल्लि बेडा","यहां नहीं","not here","Illi beda.")], "Driver reply chunks", ["Baralla.", "Extra beku.", "Traffic ide.", "Illi beda."], ["Will not come.", "Need extra.", "There is traffic.", "Not here."], ["Baralla.", "Extra beku.", "Traffic ide.", "Illi beda."], "Driver asks extra. Refuse politely and say meter only.", "Extra beda. Meter alli barthira?"),
    (65, "Fast Staff Replies", "Swalpa time beku.", "स्वल्प टाइम बेकु.", "थोड़ा समय चाहिए.", "Need some time.", [("time beku","टाइम बेकु","समय चाहिए","need time","Swalpa time beku."),("ivaga busy","इवाग बिज़ी","अभी व्यस्त","busy now","Ivaga busy."),("aamele barthini","आमेले बर्तिनी","बाद में आऊंगा","will come later","Aamele barthini."),("nodthini","नोड्तिनी","देखूंगा","I will see/check","Nodthini."),("helthini","हेल्तिनी","बताऊंगा","I will tell","Helthini.")], "Staff reply chunks", ["Swalpa time beku.", "Ivaga busy.", "Aamele barthini.", "Nodthini."], ["Need some time.", "Busy now.", "Will come later.", "I will check."], ["Swalpa time beku.", "Ivaga busy.", "Aamele barthini.", "Nodthini."], "Maintenance says he will come later. Ask what time.", "Sari. Yaava time barthira?"),
    (66, "Natural Variant Practice", "Ondu nimisha.", "ओन्दु निमिष.", "एक मिनट.", "One minute.", [("ondu nimisha","ओन्दु निमिष","एक मिनट","one minute","Ondu nimisha kaayiri."),("sari sari","सरी सरी","ठीक ठीक","okay okay","Sari sari."),("bartha ide","बर्ता इदे","आ रहा है","is coming","Cab bartha ide."),("hogtha ide","होग्ता इदे","जा रहा है","is going","Traffic slow hogtha ide."),("madbeku","मड्बेकु","करना है","need to do","Payment madbeku.")], "Natural variants", ["Ondu nimisha kaayiri.", "Cab bartha ide.", "Payment madbeku.", "Sari sari."], ["Wait one minute.", "Cab is coming.", "Need to pay.", "Okay okay."], ["Ondu nimisha kaayiri.", "Cab bartha ide.", "Payment madbeku.", "Sari sari."], "Ask someone to wait one minute because payment is needed.", "Ondu nimisha kaayiri. Payment madbeku."),
    (67, "Full Auto Ride", "Koramangala hogbeku.", "कोरमंगला होग्बेकु.", "कोरमंगला जाना है.", "Need to go to Koramangala.", [("Koramangala","कोरमंगला","कोरमंगला","Koramangala","Koramangala hogbeku."),("meter only","मीटर ओनली","सिर्फ मीटर","meter only","Meter only."),("signal","सिग्नल","सिग्नल","signal","Signal alli left."),("drop madi","ड्रॉप माडि","छोड़िए","drop","Gate alli drop madi."),("receipt beda","रिसीट बेडा","रसीद नहीं चाहिए","receipt not needed","Receipt beda.")], "Full ride chunks", ["Koramangala hogbeku.", "Meter only.", "Signal alli left.", "Gate alli drop madi."], ["Need to go Koramangala.", "Meter only.", "Left at signal.", "Drop at gate."], ["Koramangala hogbeku.", "Meter only.", "Signal alli left.", "Gate alli drop madi."], "Give a full auto instruction from pickup to drop.", "Koramangala hogbeku. Meter only. Signal alli left. Gate alli drop madi."),
    (68, "Full Grocery Visit", "List alli idu ideya?", "लिस्ट अल्लि इदु इदेया?", "लिस्ट में यह है क्या?", "Is this on the list?", [("list","लिस्ट","सूची","list","List alli ideya?"),("milk","मिल्क","दूध","milk","Milk ideya?"),("bread","ब्रेड","ब्रेड","bread","Bread kodi."),("eggs","एग्स","अंडे","eggs","Eggs beku."),("total","टोटल","कुल","total","Total eshtu?")], "Shopping sequence", ["Milk ideya?", "Bread kodi.", "Eggs beku.", "Total eshtu?"], ["Is milk available?", "Give bread.", "Want eggs.", "Total how much?"], ["Milk ideya?", "Bread kodi.", "Eggs beku.", "Total eshtu?"], "Buy milk, bread, eggs and ask total.", "Milk ideya? Bread kodi. Eggs beku. Total eshtu?"),
    (69, "Full Apartment Repair", "Bathroom leak aagide.", "बाथरूम लीक आगिदे.", "बाथरूम में लीकेज है.", "Bathroom is leaking.", [("bathroom","बाथरूम","बाथरूम","bathroom","Bathroom alli problem."),("leak aagide","लीक आगिदे","लीक हो रहा","is leaking","Pipe leak aagide."),("pipe","पाइप","पाइप","pipe","Pipe check madi."),("smell","स्मेल","बदबू","smell","Smell jaasti."),("immediate","इमीडिएट","तुरंत","immediate","Immediate barbeku.")], "Repair sequence", ["Bathroom leak aagide.", "Pipe check madi.", "Plumber kalisi.", "Immediate barbeku."], ["Bathroom is leaking.", "Check pipe.", "Send plumber.", "Need to come immediately."], ["Bathroom leak aagide.", "Pipe check madi.", "Plumber kalisi.", "Immediate barbeku."], "Report a bathroom leak and ask for plumber.", "Bathroom leak aagide. Plumber kalisi. Immediate barbeku."),
    (70, "Full Delivery Confusion", "Order wrong address ge hogide.", "ऑर्डर रॉन्ग अड्रेस गे होगिदे.", "ऑर्डर गलत पते पर गया है.", "Order went to wrong address.", [("wrong address","रॉन्ग अड्रेस","गलत पता","wrong address","Wrong address ge hogide."),("correct address","करेक्ट अड्रेस","सही पता","correct address","Correct address kalisi."),("agent","एजेंट","एजेंट","agent","Agent call madide."),("reschedule","रीशेड्यूल","फिर से समय तय","reschedule","Reschedule madi."),("refund","रिफंड","पैसे वापस","refund","Refund beku.")], "Delivery recovery", ["Wrong address ge hogide.", "Correct address kalisi.", "Agent call madide.", "Reschedule madi."], ["Went to wrong address.", "Send correct address.", "Called agent.", "Reschedule."], ["Wrong address ge hogide.", "Correct address kalisi.", "Agent call madide.", "Reschedule madi."], "Explain delivery went to wrong address and ask to reschedule.", "Order wrong address ge hogide. Reschedule madi."),
    (71, "Full Restaurant Order", "Menu kodi.", "मेन्यू कोडि.", "मेन्यू दीजिए.", "Give the menu.", [("menu","मेन्यू","मेन्यू","menu","Menu kodi."),("veg","वेज","शाकाहारी","veg","Veg ideya?"),("non-veg","नॉन-वेज","मांसाहारी","non-veg","Non-veg beda."),("less spicy","लेस स्पाइसी","कम तीखा","less spicy","Less spicy madi."),("parcel madi","पार्सल माडि","पैक कर दीजिए","pack as parcel","Parcel madi.")], "Restaurant sequence", ["Menu kodi.", "Veg ideya?", "Less spicy madi.", "Parcel madi."], ["Give menu.", "Is veg available?", "Make less spicy.", "Pack parcel."], ["Menu kodi.", "Veg ideya?", "Less spicy madi.", "Parcel madi."], "Order veg food, less spicy, and ask for bill.", "Menu kodi. Veg ideya? Less spicy madi. Bill kodi."),
    (72, "Social Chat Final Combo", "Kannada practice madbeku.", "कन्नडा प्रैक्टिस मड्बेकु.", "कन्नड़ प्रैक्टिस करनी है.", "I need to practice Kannada.", [("practice","प्रैक्टिस","अभ्यास","practice","Kannada practice madbeku."),("friend aagona","फ्रेंड आगोणा","दोस्त बनें","let us become friends","Friend aagona."),("contact","कॉन्टैक्ट","संपर्क","contact","Contact kalisi."),("matadona","माताडोणा","बात करें","let us talk","Kannada alli matadona."),("slowly slowly","स्लोली स्लोली","धीरे-धीरे","slowly", "Slowly slowly kalithini.")], "___ madbeku / ___ alli matadona", ["Kannada practice madbeku.", "Kannada alli matadona.", "Friend aagona.", "Slowly slowly kalithini."], ["Need to practice Kannada.", "Let us speak in Kannada.", "Let us become friends.", "I am learning slowly."], ["Kannada practice madbeku.", "Kannada alli matadona.", "Friend aagona.", "Slowly slowly kalithini."], "Tell a new friend you want to practice Kannada and speak slowly.", "Kannada practice madbeku. Kannada alli matadona. Slow aagi heli."),
]

for n, title, sentence, pron, hi, en, words, pattern, examples, prompts, answers, role_prompt, role_answer in more_lessons:
    lessons.append({
        "n": n,
        "title": title,
        "recall": [],
        "words": words,
        "sentence": sentence,
        "pron": pron,
        "hi": hi,
        "en": en,
        "breakdown": [(sentence.split()[0], "मुख्य शब्द", "main word"), (" ".join(sentence.split()[1:]), "वाक्य का बाकी भाग", "rest of sentence")],
        "logic": f"This lesson extends the reusable pattern `{pattern}`. Keep the sentence short first, then add time/place/person words.",
        "pattern": pattern,
        "examples": examples,
        "guided_prompts": prompts,
        "guided_answers": answers,
        "production_prompts": [],
        "production_answers": [],
        "roleplay_prompt": role_prompt,
        "roleplay_answer": role_answer,
        "quiz_prompts": [],
        "quiz_answers": [],
        "notes": [f"{pattern} = core pattern", sentence, *[x for x in examples[:2] if x != sentence]],
        "natural": f"`{sentence}` is a practical Bangalore sentence; the English loan words are acceptable where locals use them.",
        "mistake": "Do not force a long sentence. Build two short sentences if needed.",
    })


def enrich_generated_lessons():
    for i, s in enumerate(lessons):
        if s["n"] < 31:
            continue

        prev = lessons[i - 1]
        prev_examples = prev.get("examples", [])
        s["recall"] = [
            prev_examples[0] if len(prev_examples) > 0 else "Ask one old question.",
            prev_examples[1] if len(prev_examples) > 1 else "Make one old request.",
            prev_examples[2] if len(prev_examples) > 2 else "Use one old location or time sentence.",
        ]

        prompts = s["guided_prompts"]
        answers = s["guided_answers"]
        s["production_prompts"] = [
            f"In a real Bangalore situation: {prompts[0]}",
            f"Change the place/person/item and say: {prompts[1]}",
            f"Use as the next line in a short conversation: {prompts[2]}",
            f"Combine old knowledge with today: {prompts[3]}",
        ]
        s["production_answers"] = answers[:]

        s["quiz_prompts"] = [
            f"Say: {prompts[0]}",
            f"Say: {prompts[1]}",
            f"Say: {prompts[2]}",
            f"Say: {prompts[3]}",
        ]
        s["quiz_answers"] = answers[:]


enrich_generated_lessons()


for s in lessons:
    if s["breakdown"] and s["breakdown"][0][1] == "मुख्य शब्द":
        s["breakdown"] = auto_breakdown(s)
    (ROOT / "lessons" / f"lesson-{s['n']:03d}.md").write_text(lesson_md(s), encoding="utf-8")
    (ROOT / "answers" / f"lesson-{s['n']:03d}-answers.md").write_text(answer_md(s), encoding="utf-8")


checkpoint_ranges = [
    (2, 13, 24, "Buying, payment, auto, cab, route, and pickup/drop"),
    (3, 25, 36, "People, work, daily actions, time, plans, and routine"),
    (4, 37, 48, "Problems, requests, delivery issues, and past events"),
    (5, 49, 60, "Preferences, opinions, feelings, and social conversation"),
    (6, 61, 72, "Natural speech, listening variants, and full scenarios"),
]

checkpoint_situations = {
    2: [
        "At a grocery shop, ask how much an item is and say you will take it.",
        "Ask if UPI is available and say you do not have cash.",
        "Ask for one packet, then ask for a receipt.",
        "Tell an auto driver you need to go to office by meter.",
        "Tell a cab driver the pickup is outside the gate.",
        "Tell a driver to go slowly because traffic is heavy.",
        "Ask which route the driver knows.",
        "Tell the driver to call after reaching.",
    ],
    3: [
        "Introduce yourself to a neighbour.",
        "Ask someone their name and work.",
        "Ask a colleague if they ate.",
        "Give two housekeeping instructions.",
        "Ask maintenance to check and fix a fan.",
        "Say you live here and are new here.",
        "Say you will come tomorrow morning.",
        "Ask what time someone will come.",
    ],
    4: [
        "Explain that the fan is not working.",
        "Say there is no water supply.",
        "Ask for an electrician or plumber.",
        "Ask someone to bring a key.",
        "Explain that a parcel has not arrived.",
        "Politely ask for help and the manager.",
        "Say you went to market yesterday and bought medicine.",
        "Explain that traffic was heavy, so you were late.",
    ],
    5: [
        "Say what food or drink you like and do not like.",
        "Say the food is good but too spicy.",
        "Say you did not understand and ask them to speak slowly.",
        "Ask which option someone likes.",
        "Say you are tired and will come later.",
        "Ask where someone is from.",
        "Say you know Hindi and English and are learning Kannada.",
        "Invite a colleague for tea or coffee.",
    ],
    6: [
        "Reply with short natural answers: know, do not know, okay, leave it.",
        "Ask someone to repeat clearly one more time.",
        "Understand a shopkeeper saying the item is not there.",
        "Refuse an auto driver's extra charge politely.",
        "Ask maintenance what time they will come after they say they are busy.",
        "Handle a full auto ride from pickup to drop.",
        "Handle a full restaurant order.",
        "Tell a new friend you want to practice Kannada.",
    ],
}

checkpoint_roleplays = {
    2: ["Full grocery purchase", "Auto meter negotiation", "Cab pickup confusion"],
    3: ["Neighbour introduction", "Housekeeping visit", "Planning tomorrow's timing"],
    4: ["Apartment repair complaint", "Delivery problem", "Explaining why you were late"],
    5: ["Restaurant opinion chat", "New colleague small talk", "Coffee invite"],
    6: ["Fast shopkeeper replies", "Full auto ride", "Final social chat"],
}

for idx, start, end, theme in checkpoint_ranges:
    p = ROOT / "checkpoints" / f"checkpoint-{idx:02d}-lessons-{start:03d}-to-{end:03d}.md"
    situations = checkpoint_situations[idx]
    roleplays = checkpoint_roleplays[idx]
    p.write_text(f"""# Checkpoint {idx:02d}: Lessons {start:03d}-{end:03d}

Theme: {theme}.

Use this with a practice assistant. Do not include answers in the same session.

## Part 1: Pattern Recall

Say 12 sentences from memory using patterns from Lessons {start:03d}-{end:03d}.

Requirements:

- 3 questions.
- 3 requests or commands.
- 2 negative sentences.
- 2 time/place sentences.
- 2 sentences about yourself.

## Part 2: Situation Response

Respond in Kannada:

{bullets(situations)}

## Part 3: Roleplays

### Roleplay A: {roleplays[0]}

Handle one full daily-life conversation using only short Kannada lines.

### Roleplay B: {roleplays[1]}

Ask 5 follow-up questions without switching to English/Hindi.

### Roleplay C: {roleplays[2]}

Explain one problem or plan in 5 simple Kannada sentences.

## Part 4: Listening Prediction

Ask your practice assistant to say fast natural versions from this range. You should identify the meaning and reply naturally.

## Part 5: Build Your Own

Create 15 original Kannada sentences from this checkpoint range and combine them with older patterns.
""", encoding="utf-8")

if os.environ.get("SKIP_TRACKING_APPEND") == "1":
    raise SystemExit(0)


with (ROOT / "tracking" / "daily-review.md").open("a", encoding="utf-8") as f:
    f.write("""

## Lessons 025-072 High-Value Review

### Social And Identity

- Nanna name ___.
- Nimma name enu?
- Naan illi irthini.
- Neevu ellinda?
- Kannada swalpa barutte.
- Kannada kalithidini.

### Work, Food, Routine

- Neevu enu madthidira?
- Naan office alli work madthini.
- Oota aayta?
- Daily office hogthini.
- Naale beligge barthini.
- Yaava time barthira?

### Problems And Requests

- Fan work agalla.
- Water supply illa.
- Internet work agalla.
- Idu check madi.
- Technician kalisi.
- Swalpa help madi.

### Past And Explanation

- Ninne marketge hogidde.
- Idannu kondide.
- Naan call madide.
- En aaytu?
- Traffic jaasti, late aaytu.
- Adakke late aaytu.

### Opinions And Social Kannada

- Nanage coffee ishta.
- Idu chennagide.
- Artha agilla. Slow aagi heli.
- Nimge yaavdu ishta?
- Bangalore hege ide?
- Coffee ge hogona?

### Natural Speech Survival

- Gotha.
- Gothilla.
- Beda bidi.
- Innondu sala heli.
- Kelistilla.
- Ondu nimisha kaayiri.
""")

with (ROOT / "tracking" / "patterns.md").open("a", encoding="utf-8") as f:
    f.write("""

## Lessons 025-072 Pattern Bank

### Identity And Social

- Nanna ___ ___ = My ___ is ___
- Nimma ___ enu? = What is your ___?
- Neevu ellinda? = Where are you from?
- Naan ___ inda = I am from ___
- Kannada swalpa barutte = I know a little Kannada

### Time And Routine

- Time + sentence: Ivattu office hogbeku
- Yaavaga ___? = When ___?
- Yaava time ___? = What time ___?
- Daily/Sometimes/Usually + action

### Problems

- ___ agalla = ___ does not work/happen
- ___ illa = no ___
- Object + check/fix/repair madi
- Person + kalisi = send person
- ___ tagondu banni = bring ___

### Past

- Naan ___ hogidde = I went to ___
- Object + kondide = bought object
- Naan call/message madide = I called/messaged
- En aaytu? = What happened?
- Reason + adakke + result

### Opinions

- Nanage ___ ishta = I like ___
- Nanage ___ ishta illa = I do not like ___
- ___ chennagide = ___ is good
- Artha aaytu/agilla = understood/did not understand
- Nimge yaavdu ishta? = Which one do you like?

### Natural Speech

- Innondu sala heli = Say one more time
- Slow aagi heli = Say slowly
- Beda bidi = Leave it/no need
- Aaytu = Done/okay
- Nodona = Let us see
""")

with (ROOT / "tracking" / "survival-dialogues.md").open("a", encoding="utf-8") as f:
    f.write("""

## Neighbour Intro

You: Nanna name Shafique. Naan illi irthini.

Neighbour: Nimma ooru elli?

You: Naan Delhi inda. Kannada kalithidini.

## Maintenance Problem

You: Fan work agalla. Idu check madi.

Staff: Ivaga busy.

You: Sari. Yaava time barthira?

## Delivery Problem

You: Order wrong address ge hogide.

Agent: Location kalisi.

You: Correct address kalisthini. Reschedule madi.

## Social Invite

You: Sanje free ideya?

Friend: Haudu.

You: Coffee ge hogona?

## Clarification

Speaker: Fast Kannada line.

You: Artha agilla. Innondu sala slow aagi heli.
""")

with (ROOT / "tracking" / "vocab.md").open("a", encoding="utf-8") as f:
    f.write("""

## Lessons 025-072 Must Review Words

nanna, nimma, hesaru, ooru, kelasa, oota, tindi, aayta, clean madi, check madi, fix madi, irthini, ivattu, naale, ninne, yaavaga, daily, aagide, agalla, current, internet, technician, tagondu banni, parcel, complaint, hogidde, kondide, nodide, en aaytu, adakke, ishta, chennagide, kashta, artha agilla, nimge, hege, ellinda, barutte, hogona, gotha, gothilla, innondu sala, kelistilla.
""")

with (ROOT / "tracking" / "pronunciation.md").open("a", encoding="utf-8") as f:
    f.write("""

## Lessons 025-072

### Common Fast Spoken Endings

- `madthini`: मद्तिनी
- `madthira`: मद्तिरा
- `hogidde`: होगिद्दे
- `aaytu`: आय्तु
- `agalla`: आगल्ला

### Useful Listening Chunks

Practice these as whole sounds:

- En aaytu?
- Artha agilla.
- Innondu sala heli.
- Swalpa time beku.
- Beda bidi.
- Kannada swalpa barutte.
""")
