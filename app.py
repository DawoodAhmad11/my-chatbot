"""
Dawood AI PRO MAX - Offline Smart Chatbot (Streamlit)
Run:  streamlit run dawood_ai_fixed.py
"""

import ast
import datetime
import operator
import random
import re

import streamlit as st

# ============== PAGE SETTINGS ==============

st.set_page_config(
    page_title="Dawood AI PRO MAX",
    page_icon="🤖",
    layout="centered"
)

# Pakistan ka time (UTC+5, DST nahi). Server kisi bhi country mein ho, time sahi aayega.
PKT = datetime.timezone(datetime.timedelta(hours=5), "PKT")

DEFAULT_NAME = "Dost"

WELCOME = (
    "Assalam-o-Alaikum! Main Dawood AI hun. 😊 Mujhse kuch bhi pucho!\n\n"
    "Commands dekhne ke liye `help` likho."
)


def now_pk():
    return datetime.datetime.now(PKT)


# ============== KNOWLEDGE DATABASE ==============

KNOWLEDGE = {
    "python": "Python aik popular programming language hai. Iska use AI, websites, automation aur software development mein hota hai.",
    "variable": "Variable aik container hota hai jo data store karta hai. Example: name = 'Dawood'",
    "loop": "Loop ka use instructions ko baar baar repeat karne ke liye hota hai. Python mein for aur while loops hain.",
    "function": "Function reusable code ka block hota hai. Python mein def keyword se function banate hain.",
    "list": "Python list multiple values store karti hai. Example: fruits = ['Apple', 'Mango', 'Banana']",
    "artificial intelligence": "Artificial Intelligence (AI) computer science ki field hai jisme machines ko intelligent tasks perform karna sikhaya jata hai.",
    "machine learning": "Machine Learning AI ki branch hai jisme computer data se patterns seekhta hai.",
    "computer": "Computer aik electronic machine hai jo input leti hai, data process karti hai aur output deti hai.",
    "hardware": "Hardware computer ke physical parts hote hain, jaise keyboard, mouse, monitor aur CPU.",
    "software": "Software programs aur instructions ka collection hai jo computer ko kaam karne ke liye guide karta hai.",
    "operating system": "Operating System hardware aur software resources manage karta hai. Examples: Windows, Linux aur Android.",
    "internet": "Internet duniya bhar ke computers aur devices ka network hai.",
    "database": "Database organized information ka collection hota hai jahan data store aur manage hota hai.",
    "information system": "Information System people, hardware, software, data aur procedures ka combination hai.",
    "binary": "Binary number system base 2 hota hai. Is mein sirf 0 aur 1 digits use hote hain.",
    "decimal": "Decimal number system base 10 hota hai. Is mein 0 se 9 tak digits use hote hain.",
    "pn junction diode": "PN Junction Diode aik semiconductor device hai jo P-type aur N-type materials se banta hai. Ye current ko mainly aik direction mein pass karta hai.",
    "electric current": "Electric current electric charges ke flow ko kehte hain. Iski SI unit Ampere (A) hai.",
    "voltage": "Voltage do points ke darmiyan electric potential difference hai. Iski unit Volt (V) hai.",
    "resistance": "Resistance current ke flow ki opposition karta hai. Iski unit Ohm hai.",
    "ohm law": "Ohm's Law: V = I × R. Yahan V voltage, I current aur R resistance hai.",
    "kvl": "Kirchhoff Voltage Law ke mutabiq closed loop mein tamam voltage rises aur drops ka algebraic sum zero hota hai.",
    "kcl": "Kirchhoff Current Law ke mutabiq junction par entering current ka sum leaving current ke sum ke barabar hota hai.",
    "gravity": "Gravity aik natural force hai jo objects ko aik doosre ki taraf attract karti hai.",
    "photosynthesis": "Photosynthesis woh process hai jisme plants sunlight, water aur carbon dioxide se glucose banate hain aur oxygen release karte hain.",
    "human heart": "Human heart aik muscular organ hai jo blood ko poore body mein pump karta hai.",
    "solar system": "Solar System mein Sun aur uske gird orbit karne wale 8 planets aur doosre celestial objects shamil hain.",
    "pakistan": "Pakistan South Asia ka aik mulk hai. Iska capital Islamabad hai. Pakistan 14 August 1947 ko azaad hua.",
    "lahore": "Lahore Punjab ka capital hai. Badshahi Mosque, Minar-e-Pakistan aur Lahore Fort mashhoor jagahen hain.",
    "islam": "Islam aik monotheistic religion hai. Musalman aik Allah par iman rakhte hain aur Prophet Muhammad (PBUH) ko Allah ka aakhri Rasool mante hain.",
    "quran": "Holy Quran Islam ki muqaddas kitab hai jo Prophet Muhammad (PBUH) par nazil hui.",
    "english": "English aik international language hai jo education, communication aur business mein use hoti hai.",
    "communication": "Communication information, ideas aur feelings share karne ka process hai.",
    "democracy": "Democracy aik system of government hai jisme log apne representatives elect karte hain.",
    "capital of pakistan": "Pakistan ka capital Islamabad hai.",
    "largest planet": "Jupiter hamare Solar System ka sab se bara planet hai.",
    "fastest animal": "Cheetah zameen par sab se tez daurne wala animal hai.",
    "water formula": "Water ka chemical formula H2O hai.",
    "human body": "Human body mein adult insan ke aam tor par 206 bones hoti hain.",
    # ---- naye topics ----
    "cpu": "CPU (Central Processing Unit) computer ka dimagh hota hai jo instructions execute karta hai.",
    "ram": "RAM computer ki temporary (volatile) memory hai. Power band hone par RAM ka data khatam ho jata hai.",
    "algorithm": "Algorithm kisi masle ko hal karne ke steps ka clear aur tarteeb wala set hota hai.",
    "html": "HTML (HyperText Markup Language) web pages ka structure banane ki language hai.",
    "sql": "SQL (Structured Query Language) databases se data nikalne aur manage karne ki language hai.",
    "network": "Computer network aise devices ka group hai jo aapas mein data share karte hain. Examples: LAN aur WAN.",
    "resistor": "Resistor aik electronic component hai jo circuit mein current ko limit karta hai. Iski value Ohm mein hoti hai.",
    "capacitor": "Capacitor aik electronic component hai jo electric charge ko electric field mein store karta hai. Iski unit Farad (F) hai.",
    "transistor": "Transistor semiconductor device hai jo signal ko amplify ya switch karne ke liye use hota hai.",
}

# Doosre naam / short forms jo asal topic ki taraf le jaate hain
ALIASES = {
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "os": "operating system",
    "ohm's law": "ohm law",
    "ohms law": "ohm law",
    "ohm ka qanoon": "ohm law",
    "kirchhoff voltage law": "kvl",
    "kirchhoff's voltage law": "kvl",
    "kirchhoff current law": "kcl",
    "kirchhoff's current law": "kcl",
    "diode": "pn junction diode",
    "pn diode": "pn junction diode",
    "current": "electric current",
    "ohm": "resistance",
    "islamabad": "capital of pakistan",
    "heart": "human heart",
    "planet": "solar system",
    "biggest planet": "largest planet",
    "bara planet": "largest planet",
    "sab se bara planet": "largest planet",
    "pakistan ka capital": "capital of pakistan",
    "pakistan ki capital": "capital of pakistan",
    "sab se tez animal": "fastest animal",
    "sab se tez janwar": "fastest animal",
    "formula of water": "water formula",
    "pani ka formula": "water formula",
    "h2o": "water formula",
    "bone": "human body",
    "holy quran": "quran",
    "quraan": "quran",
}

# "aur batao" / "explain more" par ye extra detail milti hai
MORE_INFO = {
    "python": "Python ko Guido van Rossum ne banaya aur ye pehli dafa 1991 mein release hui. Iski syntax asaan hai, isliye beginners ke liye acchi language hai. Popular libraries: NumPy, Pandas, Django aur Streamlit.",
    "variable": "Python mein variable ki type khud decide hoti hai. Examples: age = 20 (int), price = 9.5 (float), name = 'Ali' (str), ok = True (bool). Variable ka naam number se shuru nahi ho sakta.",
    "loop": "for loop: `for i in range(5): print(i)` 0 se 4 tak print karta hai. while loop jab tak condition True ho chalta rehta hai. break loop rok deta hai aur continue current round skip karta hai.",
    "function": "Example: `def add(a, b): return a + b`. Phir add(2, 3) call karne par 5 milta hai. Function code ko dobara use karne ke qabil banata hai.",
    "list": "List mein index 0 se shuru hota hai: fruits[0] pehla item hai. append() naya item add karta hai, remove() item hata deta hai aur len(fruits) items ginta hai.",
    "artificial intelligence": "AI ki examples: voice assistants, face recognition, YouTube/Netflix recommendations aur chatbots. AI ki aik major branch Machine Learning hai.",
    "machine learning": "ML mein model data se seekhta hai. Types: Supervised (labeled data), Unsupervised (bina labels ke patterns) aur Reinforcement Learning (reward se seekhna).",
    "computer": "Computer ke 4 basic kaam hain: Input, Processing, Output aur Storage. CPU computer ka processing wala hissa hai.",
    "hardware": "Hardware ki categories: input devices (keyboard, mouse), output devices (monitor, printer), processing (CPU) aur storage (HDD/SSD, RAM).",
    "software": "Software do main types ka hota hai: System software (jaise Operating System) aur Application software (jaise browser, Word).",
    "operating system": "OS ke kaam: memory management, process management, file management aur device management. Examples: Windows, Linux, macOS, Android.",
    "internet": "Internet par data packets ki shakal mein travel karta hai. Websites dekhne ke liye browser aur HTTP/HTTPS jaise protocols use hote hain.",
    "database": "Database mein data tables (rows aur columns) mein store hota hai. SQL se data insert, read, update aur delete kiya jata hai. Examples: MySQL, PostgreSQL, SQLite.",
    "binary": "Binary ko decimal mein badalne ke liye har bit ko 2 ki power se multiply karte hain. Example: 1011 = 8 + 0 + 2 + 1 = 11.",
    "decimal": "Decimal ko binary mein badalne ke liye number ko baar baar 2 se divide karte hain aur remainders neeche se upar parhte hain. Example: 10 = 1010 (binary).",
    "ohm law": "Formulas: V = I × R, I = V / R, R = V / I. Example: V = 12 V aur R = 4 Ω ho to I = 3 A. Khud try karo: `ohm v=12 r=4`",
    "voltage": "Voltage ko voltmeter se measure karte hain jo circuit mein parallel lagta hai. 1 Volt = 1 Joule per Coulomb.",
    "electric current": "Current ko ammeter se measure karte hain jo circuit mein series mein lagta hai. Conventional current positive se negative terminal ki taraf maani jati hai.",
    "resistance": "Resistance conductor ki length, area aur material par depend karta hai: R = ρL/A. Series mein resistors jama hote hain: R = R1 + R2.",
    "pn junction diode": "Forward bias mein diode current pass karta hai (silicon diode par takreeban 0.7 V par). Reverse bias mein bohat kam leakage current hota hai.",
    "kvl": "Example: 12 V battery series mein 2 resistors par 5 V aur 7 V drop karti hai: 12 - 5 - 7 = 0, yani loop ka algebraic sum zero hai.",
    "kcl": "Example: junction par 5 A aur 3 A andar aa rahe hon to bahar jane wala total current 8 A hoga.",
    "gravity": "Zameen par gravity ki acceleration takreeban 9.8 m/s² hai. Newton ke mutabiq force F = G·m1·m2 / r² hota hai.",
    "photosynthesis": "Equation: 6CO2 + 6H2O + light → C6H12O6 + 6O2. Ye process chloroplast mein hota hai jahan chlorophyll sunlight absorb karta hai.",
    "human heart": "Heart ke 4 chambers hote hain: 2 atria (upar) aur 2 ventricles (neeche). Aam adult ka heart aik minute mein takreeban 60 se 100 dafa dhadakta hai.",
    "solar system": "8 planets (Sun se door hote hue): Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.",
    "pakistan": "Pakistan mein 4 provinces hain: Punjab, Sindh, Khyber Pakhtunkhwa aur Balochistan. Qaumi zaban Urdu hai.",
    "lahore": "Lahore Punjab ka sab se bara shehar hai. Walled City, Shalimar Gardens aur Lahore Fort yahan ki mashhoor jagahen hain.",
    "islam": "Islam ke 5 arkaan hain: Kalima (Shahada), Namaz, Roza, Zakat aur Hajj.",
    "quran": "Quran 114 surahs par mushtamil hai aur ye takreeban 23 saal mein nazil hua.",
    "english": "English mein 26 letters hain aur ye duniya mein sab se ziada seekhi jane wali zubanon mein se aik hai.",
    "communication": "Communication ke main elements: sender, message, channel, receiver aur feedback.",
    "democracy": "Democracy mein log vote ke zariye apni government chunte hain. Pakistan mein parliamentary democracy ka nizam hai.",
    "capital of pakistan": "Islamabad aik planned shehar hai jo 1960 ki dehai mein basaya gaya. Is se pehle Karachi Pakistan ka capital tha.",
    "largest planet": "Jupiter diameter mein Earth se takreeban 11 guna bara hai aur is ke 90 se ziada moons confirm ho chuke hain.",
    "fastest animal": "Cheetah takreeban 100 km/h tak ki raftar se daur sakta hai, lekin sirf chhote fasle ke liye.",
    "water formula": "H2O mein 2 hydrogen atoms aur 1 oxygen atom hota hai. Pani normal pressure par 0°C par jamta aur 100°C par ubalta hai.",
    "human body": "Bachon mein bones ziada (takreeban 300) hoti hain jo bare hone par aapas mein jud kar 206 reh jati hain.",
}

# ============== JOKES ==============

JOKES = [
    "Teacher: Homework kahan hai? Student: Sir, homework ghar par reh gaya! 😂",
    "Computer ne doctor se kaha: Mujhe virus ho gaya hai! 😂",
    "Teacher: 2 aur 2 kitne? Student: Sir, depend karta hai kis subject mein! 😂",
    "Programmer chai kyun peeta hai? Kyun ke usay Java pasand hai! 😂",
    "Student: Sir mujhe kuch samajh nahi aaya. Teacher: Mujhe bhi! 😂",
]

# ============== QUIZ ==============

QUIZ = [
    {"q": "Voltage ki unit kya hai?", "a": ["volt", "volts", "v"], "show": "Volt (V)"},
    {"q": "Resistance ki unit kya hai?", "a": ["ohm", "ohms", "ω"], "show": "Ohm"},
    {"q": "Electric current ki SI unit kya hai?", "a": ["ampere", "amperes", "amp", "amps"], "show": "Ampere (A)"},
    {"q": "Binary number system ka base kitna hota hai?", "a": ["2", "two", "do"], "show": "2"},
    {"q": "Decimal number system ka base kitna hota hai?", "a": ["10", "ten", "das"], "show": "10"},
    {"q": "Pakistan ka capital kya hai?", "a": ["islamabad"], "show": "Islamabad"},
    {"q": "Lahore kis province ka capital hai?", "a": ["punjab"], "show": "Punjab"},
    {"q": "Pani ka chemical formula kya hai?", "a": ["h2o"], "show": "H2O"},
    {"q": "Solar System mein kitne planets hain?", "a": ["8", "eight", "aath"], "show": "8"},
    {"q": "Solar System ka sab se bara planet kaunsa hai?", "a": ["jupiter"], "show": "Jupiter"},
    {"q": "Adult insan mein kitni bones hoti hain?", "a": ["206"], "show": "206"},
    {"q": "Python mein function banane ke liye kaunsa keyword use hota hai?", "a": ["def"], "show": "def"},
    {"q": "Zameen par sab se tez daurne wala animal kaunsa hai?", "a": ["cheetah"], "show": "Cheetah"},
    {"q": "Pakistan kis tareekh ko azaad hua?", "a": ["14 august", "14th august", "august 14", "14 aug"], "show": "14 August 1947"},
]

# ============== HELP ==============

HELP = """**Main ye sab kar sakta hoon:**

- 📚 **Knowledge:** python, loop, AI, database, voltage, ohm law, kvl, pakistan... (poori list ke liye `topics` likho)
- 📖 **Follow-up:** kisi topic ke baad `aur batao` likho
- ➕ **Calculator:** `12*(3+4)`, `5 plus 3`, `multiply 6 by 7`
- ⚡ **Ohm's Law:** `ohm v=12 r=4` ya `12 volt 4 ohm`
- 🔄 **Converter:** `10 km to miles`, `100 c to f`, `5 kg to lbs`
- 🧠 **Quiz:** `quiz` likho
- 🎲 **Fun:** `joke`, `flip coin`, `dice`
- 🕒 **Time/Date:** `time kya hai`, `aaj ki date`
- 👤 **Naam:** `mera naam Ali`, phir `mera naam kya hai`
"""

# ============== SAFE CALCULATOR ==============

NUM = r"\d+(?:\.\d+)?"

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _check_result(value):
    if isinstance(value, complex):
        raise ValueError("Complex numbers supported nahi")
    if abs(value) > 1e100:
        raise ValueError("Result bohat bara hai")
    return value


def calculate(expression):
    expression = expression.strip()
    if not expression or len(expression) > 100:
        raise ValueError("Expression khali ya bohat lamba")

    tree = ast.parse(expression, mode="eval")

    if sum(1 for _ in ast.walk(tree)) > 60:
        raise ValueError("Expression bohat complex")

    def solve(node):
        if isinstance(node, ast.Expression):
            return solve(node.body)

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float) and abs(node.value) <= 1e15:
                return node.value
            raise ValueError("Invalid number")

        if isinstance(node, ast.BinOp):
            op = OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError("Invalid operator")

            a = solve(node.left)
            b = solve(node.right)

            if isinstance(node.op, ast.Pow) and abs(b) > 1000:
                raise ValueError("Power bohat bari")

            return _check_result(op(a, b))

        if isinstance(node, ast.UnaryOp):
            op = OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError("Invalid operator")
            return _check_result(op(solve(node.operand)))

        raise ValueError("Invalid expression")

    return solve(tree)


def fmt(n):
    """Number ko saaf shakal mein dikhata hai (5.0 -> 5, 0.30000000000000004 -> 0.3)."""
    if isinstance(n, float):
        if n.is_integer() and abs(n) < 1e15:
            return str(int(n))
        return "{:.10g}".format(n)
    return str(n)


def safe_calc(expression):
    """Returns (status, value). status: ok / zero / bad."""
    try:
        return "ok", calculate(expression)
    except ZeroDivisionError:
        return "zero", None
    except (ValueError, SyntaxError, OverflowError, RecursionError, MemoryError):
        return "bad", None


def calc_reply(expression, on_bad):
    status, value = safe_calc(expression)
    if status == "ok":
        return "**Answer: {}** ✅".format(fmt(value))
    if status == "zero":
        return "Zero se divide nahi kar sakte."
    return on_bad


SYMBOL_MATH_RE = re.compile(r"[\d\s+\-*/().%^x×÷]+")


def symbol_math(msg):
    expr = msg.rstrip("=? ").strip()
    if not SYMBOL_MATH_RE.fullmatch(expr):
        return None
    if not re.search(r"\d", expr) or not re.search(r"[+\-*/%^x×÷]", expr):
        return None

    expr = expr.replace("^", "**").replace("×", "*").replace("÷", "/")
    expr = re.sub(r"(?<=\d)\s*x\s*(?=\d)", "*", expr)
    return calc_reply(expr, "Ye expression samajh nahi aaya. Example: `12*(3+4)`")


WORD_TRIGGER_RE = re.compile(
    r"\b(?:plus|minus|multiply|multiplied|times|divide|divided|jama|zarb|taqseem|tafreeq|into|add|subtract)\b"
)

WORD_PREFIX = [
    (r"\b(?:multiply|zarb)\s+(" + NUM + r")\s+(?:by|aur|and|ko|se|with)\s+(" + NUM + ")", "{0}*{1}"),
    (r"\b(?:add|jama)\s+(" + NUM + r")\s+(?:and|aur|to|ko|with)\s+(" + NUM + ")", "{0}+{1}"),
    (r"\b(?:divide|taqseem)\s+(" + NUM + r")\s+(?:by|se|with)\s+(" + NUM + ")", "{0}/{1}"),
    (r"\bsubtract\s+(" + NUM + r")\s+from\s+(" + NUM + ")", "{1}-{0}"),
]

WORD_INFIX = [
    (r"\b(?:multiplied by|multiplied|multiply|times|into|zarb)\b", "*"),
    (r"\b(?:divided by|divided|divide|taqseem)\b", "/"),
    (r"\b(?:plus|jama)\b", "+"),
    (r"\b(?:minus|tafreeq)\b", "-"),
]


def word_math(msg):
    if not re.search(r"\d", msg) or not WORD_TRIGGER_RE.search(msg):
        return None

    expr = None
    for pattern, template in WORD_PREFIX:
        m = re.search(pattern, msg)
        if m:
            expr = template.format(*m.groups())
            break

    if expr is None:
        text = msg
        for pattern, symbol in WORD_INFIX:
            text = re.sub(pattern, " " + symbol + " ", text)
        m = re.search(NUM + r"(?:\s*[+\-*/]\s*" + NUM + ")+", text)
        if m:
            expr = m.group(0)

    if expr is None:
        return None
    return calc_reply(expr, None)


# ============== OHM'S LAW ==============

def parse_ohm(msg):
    vals = {}

    for key, num in re.findall(r"(?<![a-z])([vir])\s*=\s*(" + NUM + ")", msg):
        vals.setdefault(key, float(num))

    # Pehle "12 volt", "4 ohm" jaise (number pehle, unit baad mein)
    for num, unit in re.findall(r"(" + NUM + r")\s*(volts?|amps?|amperes?|ohms?|ω)(?![a-z])", msg):
        key = "v" if unit.startswith("volt") else "i" if unit.startswith("amp") else "r"
        vals.setdefault(key, float(num))

    # Phir "voltage 12", "current 3" jaise (lafz pehle, number baad mein)
    for word, num in re.findall(r"\b(voltage|current|resistance)\s*(?:=|:|is)?\s*(" + NUM + ")", msg):
        key = {"voltage": "v", "current": "i", "resistance": "r"}[word]
        vals.setdefault(key, float(num))

    for num, unit in re.findall(r"(?<![a-z\d.])(" + NUM + r")(v|a)\b", msg):
        vals.setdefault("v" if unit == "v" else "i", float(num))

    return vals


OHM_CONTEXT_RE = re.compile(
    r"\b(?:ohm|ohms|ohm's|voltage|current|resistance|volts?|amps?|amperes?)\b|(?<![a-z])[vir]\s*="
)


def ohm_reply(msg):
    if not OHM_CONTEXT_RE.search(msg):
        return None

    vals = parse_ohm(msg)
    if len(vals) < 2:
        return None
    if len(vals) == 3:
        return "Teeno values mil gayi hain. Sirf do dein (V, I ya R mein se), teesri main nikaal dunga."

    V, I, R = vals.get("v"), vals.get("i"), vals.get("r")

    if V is not None and R is not None:
        if R <= 0:
            return "Resistance zero ya negative nahi ho sakti."
        I = V / R
    elif V is not None and I is not None:
        if I == 0:
            return "Current zero ho to resistance calculate nahi ho sakti."
        R = V / I
        if R <= 0:
            return "In values se resistance positive nahi aati. Values check karo."
    else:
        if R <= 0:
            return "Resistance zero ya negative nahi ho sakti."
        V = I * R

    P = V * I
    return (
        "⚡ **Ohm's Law**\n\n"
        "- Voltage (V) = {} V\n"
        "- Current (I) = {} A\n"
        "- Resistance (R) = {} Ω\n"
        "- Power (P = V × I) = {} W"
    ).format(fmt(V), fmt(I), fmt(R), fmt(P))


# ============== UNIT CONVERTER ==============

UNIT_ALIASES = {
    "mile": "miles", "kilometer": "km", "kilometers": "km", "kilometre": "km",
    "lb": "lbs", "pounds": "lbs", "pound": "lbs",
    "celsius": "c", "fahrenheit": "f",
    "meter": "m", "meters": "m", "metre": "m",
    "foot": "feet", "ft": "feet", "inches": "inch", "in": "inch",
}

CONVERSIONS = {
    ("km", "miles"): lambda v: v * 0.621371,
    ("miles", "km"): lambda v: v / 0.621371,
    ("kg", "lbs"): lambda v: v * 2.20462,
    ("lbs", "kg"): lambda v: v / 2.20462,
    ("c", "f"): lambda v: v * 9 / 5 + 32,
    ("f", "c"): lambda v: (v - 32) * 5 / 9,
    ("m", "feet"): lambda v: v * 3.28084,
    ("feet", "m"): lambda v: v / 3.28084,
    ("cm", "inch"): lambda v: v / 2.54,
    ("inch", "cm"): lambda v: v * 2.54,
}

KNOWN_UNITS = set(u for pair in CONVERSIONS for u in pair)

CONVERT_RE = re.compile(
    r"(?:convert\s+)?(-?" + NUM + r")\s*([a-z]+)\s+(?:to|in|ko|mein|me)\s+([a-z]+)\b"
)


def convert_reply(msg):
    m = CONVERT_RE.search(msg)
    if not m:
        return None

    value = float(m.group(1))
    src = UNIT_ALIASES.get(m.group(2), m.group(2))
    dst = UNIT_ALIASES.get(m.group(3), m.group(3))

    if src not in KNOWN_UNITS or dst not in KNOWN_UNITS:
        return None

    fn = CONVERSIONS.get((src, dst))
    if fn is None:
        return "Ye conversion mujhe nahi aati. `help` mein supported units dekho."

    return "🔄 {} {} = **{}** {}".format(fmt(value), src, fmt(fn(value)), dst)


# ============== KNOWLEDGE SEARCH ==============

TERMS = {}
for _key in KNOWLEDGE:
    TERMS[_key] = _key
for _alias, _key in ALIASES.items():
    TERMS[_alias] = _key

# Lambe terms pehle check hote hain, taake "capital of pakistan" ka jawab "pakistan" se pehle mile.
TERM_PATTERNS = sorted(
    (
        (re.compile(r"(?<![a-z0-9])" + re.escape(term) + r"(?:s|es)?(?![a-z0-9])"), term, key)
        for term, key in TERMS.items()
    ),
    key=lambda item: -len(item[1]),
)


def exact_topic(msg):
    for pattern, _term, key in TERM_PATTERNS:
        if pattern.search(msg):
            return key
    return None


def osa_distance(a, b):
    """Edit distance jisme 2 letters ki ulat-palat (pyhton -> python) bhi 1 ginti hai."""
    la, lb = len(a), len(b)
    d = [[0] * (lb + 1) for _ in range(la + 1)]
    for i in range(la + 1):
        d[i][0] = i
    for j in range(lb + 1):
        d[0][j] = j
    for i in range(1, la + 1):
        for j in range(1, lb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d[la][lb]


FUZZY_TERMS = [(t, k) for t, k in TERMS.items() if " " not in t and len(t) >= 5]


def fuzzy_topic(msg):
    """Spelling ki chhoti galti (jaise 'pyhton') pakadta hai. Sirf 5+ letters ke lafzon par."""
    best = None
    for token in set(re.findall(r"[a-z]+", msg)):
        if len(token) < 5:
            continue
        for term, key in FUZZY_TERMS:
            if abs(len(token) - len(term)) > 1 or token == term:
                continue
            dist = osa_distance(token, term)
            if dist <= 1 and (best is None or len(term) > len(best[1])):
                best = (key, term)
    return best


def topic_reply(topic, wants_more):
    if wants_more:
        extra = MORE_INFO.get(topic)
        if extra:
            return "📖 **{}**\n\n{}".format(topic.title(), extra)
        return KNOWLEDGE[topic] + "\n\n(Is topic ki mazeed detail abhi meri knowledge mein nahi hai.)"
    return KNOWLEDGE[topic]


# ============== QUIZ LOGIC ==============

def start_quiz(state):
    asked = state["quiz_asked"]
    pool = [i for i in range(len(QUIZ)) if i not in asked]
    if not pool:
        del asked[:]
        pool = list(range(len(QUIZ)))
    idx = random.choice(pool)
    asked.append(idx)
    state["quiz_current"] = idx
    return "🧠 **Quiz:** {}\n\n(Jawab likho. `skip` se chhor do, `stop` se quiz band.)".format(QUIZ[idx]["q"])


def check_quiz(state, msg):
    item = QUIZ[state["quiz_current"]]

    if re.search(r"\b(?:stop|exit|quit|band|bas)\b", msg):
        state["quiz_current"] = None
        return "Quiz band kar diya. Tumhara score: **{}/{}** 🏆".format(state["quiz_score"], state["quiz_total"])

    state["quiz_current"] = None
    state["quiz_total"] += 1
    score = "Score: **{}/{}**".format(state["quiz_score"], state["quiz_total"])

    if re.search(r"\b(?:skip|next|pata nahi|nahi pata|dont know|don't know)\b", msg):
        return "Koi baat nahi! Sahi jawab: **{}**.\n\n{}\n\nAgle sawal ke liye `quiz` likho.".format(item["show"], score)

    correct = any(
        re.search(r"(?<![a-z0-9])" + re.escape(ans) + r"(?![a-z0-9])", msg)
        for ans in item["a"]
    )

    if correct:
        state["quiz_score"] += 1
        score = "Score: **{}/{}**".format(state["quiz_score"], state["quiz_total"])
        return "✅ Bilkul sahi! Shabash!\n\n{}\n\nAgle sawal ke liye `quiz` likho.".format(score)

    return "❌ Galat. Sahi jawab: **{}**.\n\n{}\n\nAgle sawal ke liye `quiz` likho.".format(item["show"], score)


# ============== NAME HANDLING ==============

NAME_QUERY_RE = re.compile(
    r"\bmera (?:naam|name) (?:kya|kia)\b|\bwhat(?:'s| is) my name\b|\bwho am i\b|\bmain kaun\b|\bmy name\?"
)
NAME_SET_RE = re.compile(r"(?:mera naam|mera name|my name is)\s+(.+)", re.IGNORECASE)
NAME_STOPWORDS = {"kya", "kia", "nahi", "kaun", "kon", "what", "who", "hai"}


def clean_name(text):
    text = re.sub(r"[.!?,\s]+$", "", text.strip())
    text = re.sub(r"\s+(?:hai|hay|hy|he|is)$", "", text, flags=re.IGNORECASE).strip()
    return text


def valid_name(text):
    if not re.fullmatch(r"[A-Za-z؀-ۿ' \-]{2,30}", text):
        return False
    if len(text.split()) > 4:
        return False
    return text.lower() not in NAME_STOPWORDS


# ============== INTENT PATTERNS ==============

TIME_RE = re.compile(
    r"\b(?:kitne baje|what time|what(?: is|'s) the time|current time|abhi time|time kya|time kitna"
    r"|time batao|time bata|waqt kya|waqt kitna|waqt batao)\b|^(?:time|waqt)\??$"
)
DATE_RE = re.compile(
    r"\b(?:today'?s date|what(?: is|'s) the date|current date|aaj ki date|aaj ki tarikh|aaj ki tareekh"
    r"|date kya|tarikh kya|tareekh kya|what day|which day|kaun sa din|kon sa din|konsa din|aaj kya din|din kya)\b"
    r"|^(?:date|tarikh|tareekh)\??$"
)
FOLLOW_RE = re.compile(
    r"\b(?:explain more|more info|more details?|aur batao|aur btao|aur bataiye|mazeed|mazid|detail mein|tafseel)\b"
)
FOLLOW_LOOSE_RE = re.compile(r"(?:explain|samjhao|aur|more)[?!. ]*")


def has_word(msg, *words):
    return any(re.search(r"\b" + re.escape(w) + r"\b", msg) for w in words)


# ============== SMART ANSWER ENGINE ==============

def get_answer(question, state):
    raw = question.strip()
    msg = re.sub(r"\s+", " ", raw.lower().replace("’", "'"))
    name = state["user_name"]

    if not msg:
        return "Kuch likho to sahi! 😊"

    # Quiz chal raha ho to agla message uska jawab hai
    if state.get("quiz_current") is not None:
        return check_quiz(state, msg)

    # Help / topics
    if re.fullmatch(r"(?:help|madad|commands?|menu|what can you do|kya kar sakte ho|tum kya kar sakte ho)[?!. ]*", msg):
        return HELP

    if re.fullmatch(r"(?:topics?|topics list|list of topics|sab topics)[?!. ]*", msg):
        return "📚 **Main in topics ke bare mein bata sakta hoon:**\n\n" + ", ".join(
            sorted(k.title() for k in KNOWLEDGE)
        )

    # Name
    if re.fullmatch(r"(?:mera (?:naam|name)|my name is)[!. ]*", msg):
        return "Naam bhi likho, jaise: `mera naam Ali`"

    if NAME_QUERY_RE.search(msg):
        if name == DEFAULT_NAME:
            return "Abhi tumne apna naam nahi bataya. Likho: `mera naam Ali` 😊"
        return "Tumhara naam **{}** hai. 😊".format(name)

    match = NAME_SET_RE.search(raw)
    if match:
        new_name = clean_name(match.group(1))
        if valid_name(new_name):
            state["user_name"] = new_name.title()
            return "Wah {}! Ab main tumhe isi naam se bulaunga. 😊".format(state["user_name"])
        return "Naam sahi se likho, jaise: `mera naam Ali`"

    # Greetings
    if "assalam" in msg or re.search(r"\b(?:salam|salaam|aoa)\b", msg):
        return "Walaikum Assalam {}! Kya haal hai? 😊".format(name)

    if re.fullmatch(r"(?:hi+|hello+|hey+|helo|hola|good (?:morning|evening|afternoon))(?: there| dost| bro| yaar)?[!. ]*", msg):
        return "Hello {}! Kaise ho?".format(name)

    if re.search(r"\bhow are you\b|\bhow r u\b|\bkaise ho\b|\bkaisay ho\b|\bkya haal\b", msg):
        return "Main theek hun {}! Tum sunao?".format(name)

    if re.search(r"\bwho are you\b|\btum kaun ho\b|\baap kaun hain\b|\bwhat is your name\b|\btumhara naam\b", msg):
        return "Main Dawood AI PRO MAX hun. Mujhe Python se banaya gaya hai."

    # Thanks / bye
    if re.search(r"\bthank(?:s| you)?\b|\bshukriya\b|\bshukria\b|\bjazak", msg):
        return "Koi baat nahi {}! 😊".format(name)

    if re.search(r"\b(?:bye|goodbye|allah hafiz|khuda hafiz|good night|shab bakhair)\b", msg):
        return "Allah Hafiz {}! Khush raho. 😊".format(name)

    # Date and time (Pakistan time)
    if TIME_RE.search(msg):
        return now_pk().strftime("Abhi Pakistan mein time %I:%M %p hai. ⏰")

    if DATE_RE.search(msg):
        return now_pk().strftime("Aaj %d %B %Y, %A hai. 📅")

    # Calculators
    reply = symbol_math(msg)
    if reply:
        return reply

    reply = word_math(msg)
    if reply:
        return reply

    # Ohm's law solver and unit converter
    reply = ohm_reply(msg)
    if reply:
        return reply

    reply = convert_reply(msg)
    if reply:
        return reply

    # Quiz
    if has_word(msg, "quiz"):
        return start_quiz(state)

    # Fun
    if has_word(msg, "joke", "jokes", "funny", "hasao", "latifa", "lateefa"):
        return random.choice(JOKES)

    if re.search(r"\bcoin\b|\bsikka\b", msg):
        return "🪙 " + random.choice(["Heads (Chit)", "Tails (Pat)"])

    if has_word(msg, "dice", "pasa"):
        return "🎲 Dice par aaya: **{}**".format(random.randint(1, 6))

    if has_word(msg, "sad", "udaas", "motivation", "motivate", "himmat"):
        return "{}, himmat rakho! Har din kuch naya seekhne ka mauqa hota hai. Tum mehnat jari rakho! 💪".format(name)

    # Knowledge
    topic = exact_topic(msg)
    wants_more = bool(FOLLOW_RE.search(msg))

    if topic is None and (wants_more or FOLLOW_LOOSE_RE.fullmatch(msg)):
        wants_more = True
        topic = state.get("last_topic") or None
        if not topic:
            return "Kis topic ke bare mein mazeed janna chahte ho?"

    if topic:
        state["last_topic"] = topic
        return topic_reply(topic, wants_more)

    fuzzy = fuzzy_topic(msg)
    if fuzzy:
        key, term = fuzzy
        state["last_topic"] = key
        return "Shayad tum **{}** ke bare mein pooch rahe ho:\n\n{}".format(term, KNOWLEDGE[key])

    # Default
    ideas = ", ".join(random.sample(sorted(KNOWLEDGE), 5))
    return (
        "Interesting question, {}! 🤔\n\n"
        "Mere offline knowledge mein iska exact jawab available nahi hai. "
        "Sawal simple words mein likho ya topic ka naam batao.\n\n"
        "Try karo: {}  |  `help` likho sab commands ke liye."
    ).format(name, ideas)


# ============== SESSION MEMORY ==============

def reset_chat(state):
    state["messages"] = [{"role": "assistant", "content": WELCOME}]
    state["last_topic"] = ""
    state["quiz_current"] = None
    state["quiz_asked"] = []
    state["quiz_score"] = 0
    state["quiz_total"] = 0


def init_state(state):
    if "messages" not in state:
        state["messages"] = [{"role": "assistant", "content": WELCOME}]
    if "user_name" not in state:
        state["user_name"] = DEFAULT_NAME
    if "last_topic" not in state:
        state["last_topic"] = ""
    if "quiz_current" not in state:
        state["quiz_current"] = None
    if "quiz_asked" not in state:
        state["quiz_asked"] = []
    if "quiz_score" not in state:
        state["quiz_score"] = 0
    if "quiz_total" not in state:
        state["quiz_total"] = 0


def chat_as_text(messages):
    lines = []
    for m in messages:
        who = "Aap" if m["role"] == "user" else "Dawood AI"
        lines.append("{}: {}".format(who, m["content"]))
    return "\n\n".join(lines)


# ============== PAGE ==============

st.title("🤖 Dawood AI PRO MAX")
st.caption("Offline Smart Chatbot | No API Required")

init_state(st.session_state)

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Dawood AI se kuch bhi pucho...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    reply = get_answer(user_input, st.session_state)

    st.session_state["messages"].append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

# ============== SIDEBAR ==============

with st.sidebar:
    st.header("🤖 Dawood AI")
    st.write("Naam: **{}**".format(st.session_state["user_name"]))

    if st.session_state["quiz_total"] > 0:
        st.write("Quiz score: **{}/{}**".format(
            st.session_state["quiz_score"], st.session_state["quiz_total"]
        ))

    st.button("🗑️ Chat clear karo", on_click=reset_chat, args=(st.session_state,))

    st.download_button(
        "⬇️ Chat download karo",
        data=chat_as_text(st.session_state["messages"]),
        file_name="dawood_ai_chat.txt",
        mime="text/plain",
    )

    with st.expander("📚 Topics"):
        st.write(", ".join(sorted(k.title() for k in KNOWLEDGE)))

    st.caption("Tip: `help` likho.")

# ============== END ==============
 Ye code sai ha
