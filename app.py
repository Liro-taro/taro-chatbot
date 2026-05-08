import streamlit as st
import requests
import os


st.set_page_config(
    page_title="哆啦A梦AI助手",
    page_icon="🔔",
    layout="wide",
    # initial_sidebar_state="collapsed"
)

def set_bg_gif(gif_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{gif_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

doraemon_gif = ("https://s1.aigei.com/src/img/gif/bd/bdd5637cc572409e90b03e821119512b.gif?"
                "imageMogr2/auto-orient/thumbnail/!282x282r/gravity/Center/crop/282x282/quality/"
                "85/%7CimageView2/2/w/282&e=2051020800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL"
                ":0Ra0NYuDmZI834zZFR5P1O4RrGc=")
set_bg_gif(doraemon_gif)


st.markdown("""
<style>
.main { 
    background-color: #f0f7ff;
}
.title-text {
    font-size: 38px;
    font-weight: bold;
    color: #0091ff;
    text-align: center;
    margin-bottom: 10px;
}
.gif-center {
    text-align: center;
    margin: 15px 0 25px 0;
}

.ai-chat {
    background-color: #e6f4ff;
    padding: 16px;
    border-radius: 20px;
    margin: 8px 0;
}

.user-chat {
    background-color: #d1eaff;
    padding: 16px;
    border-radius: 20px;
    margin: 8px 0;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="title-text">🔔 哆啦A梦</div>', unsafe_allow_html=True)


st.markdown(
    '<div class="gif-center"><img src="https://s1.aigei.com/src/img/gif/00/00cd7fff1d304dbc8a1c12566174861b.gif?e=2051020800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:GvOR8FcmSxVA-PDuhmZGSUFoOFU=" width="320"></div>',
    unsafe_allow_html=True
)


api_key = st.secrets.get("DASHSCOPE_API_KEY", os.getenv("DASHSCOPE_API_KEY", ""))
api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
model = "qwen-turbo"

def doraemon_chat(history_list):
    if not api_key:
        return "❌ 还没配置通义千问API密钥，请到Streamlit后台Secrets填写"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "input": {"messages": history_list},
        "parameters": {"temperature": 0.7, "max_tokens": 800}
    }
    try:
        res = requests.post(api_url, headers=headers, json=data, timeout=30)
        res.raise_for_status()
        return res.json()["output"]["text"]
    except Exception as e:
        return f"⚠ 出错啦：{str(e)}"


if "msg_list" not in st.session_state:
    st.session_state.msg_list = [
        {"role":"system","content":"你是可爱的哆啦A梦，说话温柔可爱、语气童真，记住用户前面说的所有话，连贯聊天。"}
    ]


user_input = st.chat_input("向哆啦A梦提问吧...")

if user_input:
    st.session_state.msg_list.append({"role":"user","content":user_input})
    ai_reply = doraemon_chat(st.session_state.msg_list)
    st.session_state.msg_list.append({"role":"assistant","content":ai_reply})

for item in st.session_state.msg_list:
    role = item["role"]
    content = item["content"]
    if role == "system":
        continue
    if role == "user":
        st.markdown(f'<div class="user-chat">{content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-chat">🐱 {content}</div>', unsafe_allow_html=True)
