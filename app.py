import streamlit as st
import random, re
from datetime import datetime

st.set_page_config(page_title="Mera Chatbot", page_icon="🤖")
st.title("🤖 Mera Chatbot")
st.write("Hello! 'hello', 'joke', 'calc 12*3', 'game guess' likh kar try karein.")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.name = None
    st.session_state.todos = []
    st.session_state.secret = random.randint(1, 20)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])

user = st.chat_input("Yahan likhein...")

if user:
    st.session_state.messages.append({"role": "user", "text": user})
    with st.chat_message("user"):
        st.write(user)
    low = user.lower()
    plain = low.strip(" !.?,")
    
    if plain in ("hello", "hi", "hey", "salam", "aoa", "assalamualaikum"):
        reply = f"Hello {st.session_state.name}! How are you?" if st.session_state.name else "Hello! How are you?"
    elif "how are you" in low or "kaise ho" in low:
        reply = "I am fine. What about you?"
    elif plain in ("fine", "good", "great", "theek", "ok", "okay", "acha", "mast"):
        reply = "That's great! Aur batao, kya karna hai?"
    elif low.startswith("my name is "):
        st.session_state.name = user[11:].strip().title()
        reply = f"Nice to meet you, {st.session_state.name}!"
    elif "who am i" in low:
        reply = f"You are {st.session_state.name}." if st.session_state.name else "Abhi pata nahi. 'my name is ...' likhein."
    elif "joke" in low:
        reply = random.choice(["Programmer ko chai kyun pasand hai? Kyunke wo Java peeta hai!", "Computer ne doctor ko kya kaha? Mujhe virus ho gaya hai!", "Bug aur feature mein kya farq hai? Documentation!"])
    elif "quote" in low:
        reply = random.choice(["Mehnat kabhi bekaar nahi jati.", "Har bada program ek chhote Hello World se shuru hota hai.", "Seekhte raho, bante raho."])
    elif "time" in low:
        reply = datetime.now().strftime("It is %I:%M %p")
    elif "date" in low:
        reply = datetime.now().strftime("Today is %d %B %Y")
    elif "day" in low:
        reply = datetime.now().strftime("Aaj %A hai.")
    elif low.startswith("calc ") or re.fullmatch(r"[\d\s\.\+\-\*/\^\(\)%x]+", low) and any(c in low for c in "+-*/"):
        try:
            expr = low.replace("calc ", "").replace("x", "*").replace("^", "**")
            reply = f"Jawab: {eval(expr, {'__builtins__': {}}, {})}"
        except:
            reply = "Expression samajh nahi aaya."
    elif "km to miles" in low:
        try:
            v = float(re.findall(r"\d+", low)[0])
            reply = f"{v} km = {v*0.621371:.2f} miles"
        except:
            reply = "Aise likhein: 10 km to miles"
    elif "flip" in low and "coin" in low:
        reply = random.choice(["Heads (chit)", "Tails (pat)"])
    elif "roll" in low and "dice" in low:
        reply = f"Dice par aaya: {random.randint(1,6)}"
    elif low.startswith("random "):
        nums = re.findall(r"\d+", low)
        reply = f"Random number: {random.randint(int(nums[0]), int(nums[1]))}" if len(nums)>=2 else "Aise likhein: random 1 100"
    elif low.startswith("password"):
        nums = re.findall(r"\d+", low)
        length = int(nums[0]) if nums else 12
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*"
        reply = "Password: " + "".join(random.choice(chars) for _ in range(length))
    elif low.startswith("todo add "):
        st.session_state.todos.append(user[9:].strip())
        reply = f"Add ho gaya: {user[9:].strip()}"
    elif low == "todo list":
        if not st.session_state.todos:
            reply = "To-do list khali hai."
        else:
            reply = "To-do list:\n" + "\n".join([f"{i}. {t}" for i, t in enumerate(st.session_state.todos, 1)])
    elif low == "game guess":
        reply = "1 se 20 ke beech number guess karein! Sirf number likhein."
        st.session_state.playing = True
    elif low == "bye":
        reply = "Goodbye! Have a nice day."
    else:
        if st.session_state.get("playing") and plain.isdigit():
            g = int(plain)
            secret = st.session_state.secret
            if g == secret:
                reply = f"Wah! Sahi jawab {secret} tha. Jeet gaye! Naya game ke liye 'game guess' likhein."
                st.session_state.secret = random.randint(1,20)
                st.session_state.playing = False
            elif g > secret:
                reply = "Zyada hai! Dobara try karein."
            else:
                reply = "Kam hai! Dobara try karein."
        else:
            reply = "Sorry, I don't understand. 'hello', 'joke', 'calc 12*3', 'game guess' try karein."

    st.session_state.messages.append({"role": "assistant", "text": reply})
    with st.chat_message("assistant"):
        st.write(reply)
