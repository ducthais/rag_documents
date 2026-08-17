Ứng dụng chatbot AI nội bộ, cho phép tải lên tài liệu (PDF, CSV) và hỏi đáp dựa trên nội dung tài liệu — trải nghiệm tương tự ChatGPT.

## Tính năng chính

- **Chat thông minh** — Hỏi đáp dựa trên tài liệu, streaming response 
- **Hỗ trợ nhiều định dạng** — PDF và CSV
- **Đa hội thoại** — Tạo, đổi tên, xóa nhiều cuộc trò chuyện, lưu lịch sử bằng SQLite
- **Conversational RAG** — Hiểu ngữ cảnh hội thoại (hỏi nối tiếp vẫn hiểu)
- **Quản lý tài liệu** — Xem danh sách, xóa tài liệu đã tải trực tiếp trên giao diện
- **Xuất PDF** — Xuất cuộc trò chuyện ra file PDF
- **Chống bịa đặt** — Prompt engineering chặt chẽ, chỉ trả lời từ tài liệu
- **Chống trùng lặp** — Upload cùng file nhiều lần không bị nhân bản dữ liệu
- **Onboarding** — Cấu hình API key trực tiếp trên giao diện

## Kiến trúc hệ thống

```
Người dùng → Upload tài liệu → Parser (PDF/CSV) → Chunking → Embedding (BGE-M3) → ChromaDB
Người dùng → Đặt câu hỏi → Rephrase Query → Vector Search → Context → Gemini LLM → Trả lời
```

## Cấu trúc dự án

```
rag_agent/
├── app.py                          # Giao diện Streamlit chính
├── requirements.txt                # Danh sách thư viện
├── .env.example                    # Mẫu cấu hình API key
├── src/
│   ├── data_ingestion/
│   │   ├── pdf_parser.py           # Đọc và chunk PDF
│   │   ├── csv_parser.py           # Đọc CSV
│   │   └── router.py               # Định tuyến theo loại file
│   ├── vector_store/
│   │   └── chroma_utils.py         # Quản lý ChromaDB
│   ├── generation/
│   │   └── llm_service.py          # Kết nối Gemini LLM
│   ├── chat_manager.py             # Quản lý hội thoại (SQLite)
│   └── styles.py                   # Custom CSS
└── data/
    ├── raw/                        # Thư mục chứa tài liệu gốc
    └── processed/                  # Thư mục chứa dữ liệu đã xử lý
```

## Hướng dẫn cài đặt

### Yêu cầu
- Python 3.10+
- Google API Key (miễn phí tại [Google AI Studio](https://aistudio.google.com/app/apikey))

### Các bước cài đặt

```bash
# 1. Clone repository
git clone https://github.com/ducthais/rag_documents.git
cd rag_documents

# 2. Tạo virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Cài đặt thư viện
pip install -r requirements.txt

# 4. Tạo file .env từ mẫu
cp .env.example .env
# Sau đó mở file .env và dán API key của bạn vào

# 5. Chạy ứng dụng
streamlit run app.py
```

> **Lưu ý:** Nếu bạn chưa cấu hình API key trong file `.env`, ứng dụng sẽ hiển thị màn hình hướng dẫn nhập key trực tiếp trên giao diện.

## Công nghệ sử dụng

| Thành phần | Công nghệ |
|:---|:---|
| LLM | Google Gemini 2.5 Flash |
| Embedding | BAAI/bge-m3 (HuggingFace) |
| Vector Database | ChromaDB |
| Framework | LangChain |
| Giao diện | Streamlit |
| Lưu trữ chat | SQLite |
| Export | fpdf2 |