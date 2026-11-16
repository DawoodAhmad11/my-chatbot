import streamlit as st
import random
import re
import datetime

st.set_page_config(page_title="Dawood AI PRO MAX", page_icon="🤖")
st.title("🤖 Dawood AI PRO MAX")
st.caption("Offline Smart Chatbot | No API Required | Made by Dawood")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "name" not in st.session_state:
    st.session_state.name = ""
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0

jokes = [
    "Teacher: Tum late kyun aaye? Student: Sir, board par likha tha 'School Ahead', main aage chala gaya! 😂",
    "Ek admi ne pucha: Tum itne patle kyun ho? Dusra bola: Main khana kam, tension zyada khata hun! 😅",
    "Computer se pucha: Tum thakte nahi? Bola: Main to sota bhi nahi, bas Restart hota hun! 💻",
    "Doctor: Tumhe kya hua? Mareez: Mujhe bhoolne ki bimari hai. Doctor: Kab se? Mareez: Kab se kya? 🤣",
]

facts = [
    "Honey kabhi kharab nahi hota, 3000 saal purana honey bhi khaya ja sakta hai!",
    "Octopus ke 3 dil hote hain!",
    "Pakistan ka qaumi janwar Markhor hai.",
    "Chand par pehla qadam Neil Armstrong ne 1969 me rakha tha.",
]

quiz_questions = [
    ("Pakistan ka capital kya hai?", ["Karachi", "Lahore", "Islamabad", "Quetta"], "Islamabad"),
    ("2 + 2 x 2 = ?", ["6", "8", "4", "10"], "6"),
    ("Duniya ka sab se bara samandar kaunsa hai?", ["Atlantic", "Indian", "Pacific", "Arctic"], "Pacific"),
    ("Pakistan kab azad hua?", ["1945", "1947", "1950", "1948"], "1947"),
    ("Computer ka dimagh kise kehte hain?", ["RAM", "CPU", "Keyboard", "Mouse"], "CPU"),
]
def get_reply(user_input):
    text = user_input.lower().strip()
    name = st.session_state.name

    if st.session_state.quiz:
        q, opts, ans = st.session_state.quiz
        for o in opts:
            if o.lower() in text:
                st.session_state.quiz_total += 1
                st.session_state.quiz = None
                if o.lower() == ans.lower():
                    st.session_state.quiz_score += 1
                    return f"✅ Sahi jawab! Score: {st.session_state.quiz_score}/{st.session_state.quiz_total}. Agla ke liye 'quiz' likho."
                else:
                    return f"❌ Ghalat! Sahi jawab tha: {ans}. Score: {st.session_state.quiz_score}/{st.session_state.quiz_total}."
        return "Option me se ek likho, jese 'Islamabad'"

    if text in ["help", "madad", "menu"]:
        return "Main ye sab kar sakta hun 🤖:\n1. help\n2. joke\n3. fact\n4. quiz\n5. score\n6. time / date\n7. calc 12*3\n8. 10 km to miles\n9. mera naam Dawood hai"

    if text in ["hi", "hello", "salam", "aoa", "assalam o alaikum"]:
        if name:
            return f"Assalam-o-Alaikum {name}! Kaise ho? 😊 'help' likho."
        return "Assalam-o-Alaikum! Kaise ho? 😊 Apna naam batao, jese 'mera naam Dawood hai'"

    if text in ["fine", "theek", "acha hun"]:
        return "MashAllah! Bohat acha! 😊 Ab 'joke' ya 'quiz' likho."

    if "joke" in text:
        return random.choice(jokes)
    if "fact" in text:
        return "💡 Fact: " + random.choice(facts)
    if text == "quiz":
        q, opts, ans = random.choice(quiz_questions)
        st.session_state.quiz = (q, opts, ans)
        opt_text = "\n".join([f"{i+1}. {o}" for i, o in enumerate(opts)])
        return f"🎯 Quiz Time!\n\n{q}\n\n{opt_text}\n\nJawab likho!"
    if text == "score":
        return f"🏆 Score: {st.session_state.quiz_score}/{st.session_state.quiz_total}"
    if text == "time":
        return f"Time hai: {datetime.datetime.now().strftime('%I:%M %p')}"
    if text == "date":
        return f"Date hai: {datetime.datetime.now().strftime('%d %B %Y')}"
    if text == "clear":
        st.session_state.messages = []
        return "Chat saaf kar di! ✨"
            if text.startswith("calc"):
        try:
            expr = user_input[4:].strip().replace("x", "*")
            return f"🧮 {expr} = {eval(expr)}"
        except:
            return "Aise likho: calc 12*3"

    if " to " in text:
        try:
            m = re.match(r"(\d+\.?\d*)\s*(\w+)\s+to\s+(\w+)", text)
            if m:
                val = float(m.group(1))
                frm = m.group(2).lower()
                to = m.group(3).lower()
                conv = {("km", "miles"): val * 0.621371, ("miles", "km"): val * 1.60934, ("kg", "pounds"): val * 2.20462, ("pounds", "kg"): val * 0.453592}
                if (frm, to) in conv:
                    return f"🔄 {val} {frm} = {round(conv[(frm, to)], 2)} {to}"
        except:
            pass

    if "mera naam" in text:
        n = user_input.lower().replace("mera naam", "").strip().title()
        st.session_state.name = n
        return f"Wah {n}! Bohat acha naam hai. Yaad rakh lunga! 😊"

    if text == "dawood":
        st.session_state.name = "Dawood"
        return "Dawood! Mera malik! 🔥 Hukum karo!"
    if "bye" in text or "allah hafiz" in text:
        return "Allah Hafiz! 👋 Phir milenge."
    if "kaun ho" in text or "tum kaun" in text:
        return "Main Dawood AI PRO MAX hun! 🤖 Dawood ne mujhe banaya hai."
    return "Samajh nahi aaya. 'help' likho 😊"

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("😂 Joke"):
        st.session_state.messages.append({"role": "user", "content": "joke"})
        st.session_state.messages.append({"role": "assistant", "content": get_reply("joke")})
        st.rerun()
with col2:
    if st.button("🎯 Quiz"):
        st.session_state.messages.append({"role": "user", "content": "quiz"})
        st.session_state.messages.append({"role": "assistant", "content": get_reply("quiz")})
        st.rerun()
with col3:
    if st.button("🗑️ Clear"):
        st.session_state.messages = []
        st.session_state.quiz = None
        st.rerun()

st.divider()
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

prompt = st.chat_input("Yahan likhein...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": get_reply(prompt)})
    st.rerun()
