import streamlit as st
from query import rag_chain

st.set_page_config(page_title="Clean Chat UI", layout="wide")


# ---- Dummy Answer Function ---- #
def get_answer(query: str) -> str:
    answer =  rag_chain.invoke(query)
    return answer.content


# ---- Session State ---- #
if "history" not in st.session_state:
    st.session_state.history = []


# ---- Minimal CSS ---- #
st.markdown("""
<style>
    .history-box {
        background: #f8f8f8;
        border: 1px solid #ddd;
        height: 85vh;
        padding: 10px;
        border-radius: 8px;
        overflow-y: auto;
    }
    .history-item {
        background: #fff;
        border: 1px solid #e0e0e0;
        padding: 6px;
        margin-bottom: 6px;
        border-radius: 6px;
        font-size: 0.85rem;
    }
    .chat-container {
        height: 75vh;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 8px;
        overflow-y: auto;
        background: #ffffff;
    }
</style>
""", unsafe_allow_html=True)


# ---- Layout ---- #
col1, col2 = st.columns([1, 2])

# Left Column - History
with col1:
    st.subheader("History")
    # st.markdown('<div class="history-box">', unsafe_allow_html=True)
    for i, msg in enumerate(st.session_state.history):
        st.markdown(
            f"<div class='history-item'>{i+1}. {msg['role'].title()}</div>",
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Right Column - Chat UI
with col2:
    st.subheader("Chat")

    chat_container = st.container()
    with chat_container:
        # st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        # 👇 THIS is the important fix!
        for msg in st.session_state.history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Input field
    if prompt := st.chat_input("Type here..."):
        st.session_state.history.append({"role": "user", "content": prompt})
        st.session_state.history.append({"role": "assistant", "content": get_answer(prompt)})
        st.rerun()
