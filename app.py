import streamlit as st
import requests

st.set_page_config(page_title="在线聊天AI", page_icon="🤖")

# 初始化聊天记录
if "msg" not in st.session_state:
    st.session_state.msg = [
        {"role":"assistant", "content":"你好～我是AI聊天助手，随时可以聊天😊"}
    ]

# 侧边栏
with st.sidebar:
    st.title("聊天AI")
    if st.button("清空对话"):
        st.session_state.msg = [{"role":"assistant", "content":"已清空，重新开始聊天吧～"}]
        st.rerun()

# 展示聊天记录
for m in st.session_state.msg:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 免费公共AI接口（不用你任何密钥）
def get_ai_reply(text):
    url = "https://api.qingyunke.com/api.php?key=free&appid=0&msg=" + text
    res = requests.get(url).json()
    return res.get("content", "我暂时没法回答哦")

# 输入对话
if prompt := st.chat_input("在这里输入想说的话..."):
    # 用户消息
    st.session_state.msg.append({"role":"user", "content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI回复
    with st.chat_message("assistant"):
        with st.spinner("AI思考中..."):
            reply = get_ai_reply(prompt)
        st.markdown(reply)
    st.session_state.msg.append({"role":"assistant", "content":reply})