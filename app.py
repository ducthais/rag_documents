# pyrefly: ignore [missing-import]
import streamlit as st
import os
import tempfile
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# API key
load_dotenv()

from src.data_ingestion.router import ingest_documents
from src.vector_store.chroma_utils import VectorStoreManager
from src.generation.llm_service import LLMManager

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Trợ lý AI",
    layout="wide"
)

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []
if "db_manager" not in st.session_state:
    st.session_state.db_manager = VectorStoreManager(embedding_type="huggingface")
if "llm_manager" not in st.session_state:
    st.session_state.llm_manager = LLMManager(model_name="gemini-2.5-flash")


def process_uploaded_files(uploaded_files):
    with st.spinner("Thinking..."):
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                chunks = ingest_documents(tmp_file_path)
                st.session_state.db_manager.add_documents_to_db(chunks)
                st.toast(f"Đã tải xong: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Lỗi khi xử lý {uploaded_file.name}: {str(e)}")
            finally:
                os.unlink(tmp_file_path)

# SIDEBAR
with st.sidebar:
    # New chat button
    if st.button("New Chat", use_container_width=True, type="primary"):
        st.session_state.messages = [] # Clear current messages
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='color: gray; font-size: 14px;'>Hôm nay</p>", unsafe_allow_html=True)
    
    # Hiển thị tiêu đề lịch sử chat (Lấy câu hỏi đầu tiên làm tiêu đề)
    if len(st.session_state.messages) > 0:
        # Lấy tin nhắn người dùng đầu tiên
        first_user_msg = next((m["content"] for m in st.session_state.messages if m["role"] == "user"), "Cuộc trò chuyện hiện tại")
        # Rút gọn chuỗi nếu dài quá
        title = first_user_msg[:25] + "..." if len(first_user_msg) > 25 else first_user_msg
        st.button(f"{title}", use_container_width=True)
    else:
        st.caption("Chưa có cuộc trò chuyện nào.")


# Tình huống 1: Chưa có tin nhắn (Màn hình Welcome)
if len(st.session_state.messages) == 0:
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #4A4A4A;'>Tôi có thể giúp gì cho bạn?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Vui lòng đính kèm tài liệu ở nút phía dưới trước khi đặt câu hỏi</p>", unsafe_allow_html=True)

# Tình huống 2: Đang có tin nhắn (Hiển thị Lịch sử)
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("Sources"):
                    for source in message["sources"]:
                        st.write(f"- {source}")


# Khung đính kèm tài liệu (Popover) - Bỏ điều kiện if đi để nó LUÔN HIỂN THỊ
with st.popover("Đính kèm tài liệu"):
    st.caption("Tài liệu mới sẽ được thêm vào hệ thống kiến thức.")
    files = st.file_uploader("Tải thêm PDF, CSV", type=['pdf', 'csv'], accept_multiple_files=True, key="add_more")
    if st.button("Xử lý", key="process_more", use_container_width=True):
        if files:
            process_uploaded_files(files)
        else:
            st.warning("Vui lòng chọn file!")

# Khung Chat chính
if prompt := st.chat_input("Nhập câu hỏi của bạn (ví dụ: Quy định nghỉ phép là gì?)..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Đang suy nghĩ..."):
            try:
                retrieved_docs = st.session_state.db_manager.search_similar_documents(prompt, k=3)
                
                if not retrieved_docs:
                    response_text = "Dựa trên các tài liệu bạn đã tải lên, tôi không tìm thấy thông tin nào để trả lời câu hỏi này."
                    source_list = []
                    st.markdown(response_text)
                else:
                    response_text = st.session_state.llm_manager.generate_answer(prompt, retrieved_docs)
                    st.markdown(response_text)
                    
                    source_list = list(set([os.path.basename(doc.metadata.get('source', 'Unknown')) for doc in retrieved_docs]))
                    with st.expander("Nguồn tham khảo"):
                        for source in source_list:
                            st.write(f"- {source}")
                            
            except Exception as e:
                 response_text = f"Đã xảy ra lỗi: {str(e)}"
                 source_list = []
                 st.error(response_text)
                 
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response_text,
        "sources": source_list
    })