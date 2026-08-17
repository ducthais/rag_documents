
import sqlite3
import json
import uuid
import os
from datetime import datetime


class ChatManager:
    def __init__(self, db_path="./chat_history.db"):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        """Tạo connection mới cho mỗi thao tác (thread-safe cho Streamlit)."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Khởi tạo bảng conversations và messages nếu chưa tồn tại."""
        conn = self._get_conn()
        try:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL DEFAULT 'Cuộc trò chuyện mới',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    sources TEXT DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_messages_conv_id ON messages(conversation_id);
            """)
            conn.commit()
        finally:
            conn.close()


    def create_conversation(self, title="Cuộc trò chuyện mới"):
        """Tạo cuộc trò chuyện mới, trả về ID."""
        conv_id = str(uuid.uuid4())[:8]
        conn = self._get_conn()
        try:
            conn.execute(
                "INSERT INTO conversations (id, title) VALUES (?, ?)",
                (conv_id, title)
            )
            conn.commit()
        finally:
            conn.close()
        return conv_id

    def get_all_conversations(self):
        """Lấy tất cả cuộc trò chuyện, sắp xếp mới nhất trước."""
        conn = self._get_conn()
        try:
            rows = conn.execute(
                "SELECT * FROM conversations ORDER BY updated_at DESC"
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def get_conversation(self, conv_id):
        """Lấy thông tin 1 cuộc trò chuyện."""
        conn = self._get_conn()
        try:
            row = conn.execute(
                "SELECT * FROM conversations WHERE id = ?", (conv_id,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def rename_conversation(self, conv_id, new_title):
        """Đổi tên cuộc trò chuyện."""
        conn = self._get_conn()
        try:
            conn.execute(
                "UPDATE conversations SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (new_title, conv_id)
            )
            conn.commit()
        finally:
            conn.close()

    def delete_conversation(self, conv_id):
        """Xóa cuộc trò chuyện và tất cả tin nhắn."""
        conn = self._get_conn()
        try:
            conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
            conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
            conn.commit()
        finally:
            conn.close()


    def add_message(self, conv_id, role, content, sources=None):
        """Thêm tin nhắn vào cuộc trò chuyện."""
        sources_json = json.dumps(sources or [], ensure_ascii=False)
        conn = self._get_conn()
        try:
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content, sources) VALUES (?, ?, ?, ?)",
                (conv_id, role, content, sources_json)
            )
            # Cập nhật updated_at của conversation
            conn.execute(
                "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (conv_id,)
            )

            # Tự động đặt tiêu đề = câu hỏi đầu tiên
            if role == "user":
                msg_count = conn.execute(
                    "SELECT COUNT(*) FROM messages WHERE conversation_id = ? AND role = 'user'",
                    (conv_id,)
                ).fetchone()[0]
                if msg_count == 1:
                    title = content[:30] + "..." if len(content) > 30 else content
                    conn.execute(
                        "UPDATE conversations SET title = ? WHERE id = ?",
                        (title, conv_id)
                    )

            conn.commit()
        finally:
            conn.close()

    def get_messages(self, conv_id):
        """Lấy tất cả tin nhắn của cuộc trò chuyện."""
        conn = self._get_conn()
        try:
            rows = conn.execute(
                "SELECT role, content, sources, created_at FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
                (conv_id,)
            ).fetchall()
            messages = []
            for row in rows:
                msg = dict(row)
                msg["sources"] = json.loads(msg["sources"])
                messages.append(msg)
            return messages
        finally:
            conn.close()

    # ===== EXPORT TO PDF =====

    def export_to_pdf(self, conv_id, output_path=None):
        """Xuất cuộc trò chuyện ra file PDF. Trả về đường dẫn file."""
        # pyrefly: ignore [missing-import]
        from fpdf import FPDF

        conv = self.get_conversation(conv_id)
        messages = self.get_messages(conv_id)

        if not conv:
            raise ValueError(f"Không tìm thấy cuộc trò chuyện: {conv_id}")

        if output_path is None:
            output_path = f"chat_export_{conv_id}.pdf"

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()

        # Thêm font Unicode (hỗ trợ tiếng Việt)
        font_dir = os.path.join(os.path.dirname(__file__), "fonts")
        font_path = os.path.join(font_dir, "DejaVuSans.ttf")
        font_bold_path = os.path.join(font_dir, "DejaVuSans-Bold.ttf")

        # Kiểm tra font DejaVu hoặc font Arial có sẵn trên Windows
        win_arial = "C:/Windows/Fonts/arial.ttf"
        win_arial_bold = "C:/Windows/Fonts/arialbd.ttf"

        if os.path.exists(font_path):
            pdf.add_font("CustomFont", "", font_path)
            pdf.add_font("CustomFont", "B", font_bold_path)
            font_name = "CustomFont"
        elif os.path.exists(win_arial):
            pdf.add_font("CustomFont", "", win_arial)
            if os.path.exists(win_arial_bold):
                pdf.add_font("CustomFont", "B", win_arial_bold)
            else:
                pdf.add_font("CustomFont", "B", win_arial)
            font_name = "CustomFont"
        else:
            font_name = "Helvetica"

        # Tiêu đề
        pdf.set_font(font_name, "B", 16)
        pdf.cell(0, 12, conv.get("title", "Cuộc trò chuyện"), ln=True, align="C")

        pdf.set_font(font_name, "", 9)
        pdf.set_text_color(130, 130, 130)
        created_at = conv.get("created_at", "")
        pdf.cell(0, 8, f"Ngày tạo: {created_at}", ln=True, align="C")
        pdf.ln(8)

        # Nội dung tin nhắn
        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            # Header
            if role == "user":
                pdf.set_font(font_name, "B", 11)
                pdf.set_text_color(102, 126, 234)
                pdf.cell(0, 8, "Người dùng:", ln=True)
            else:
                pdf.set_font(font_name, "B", 11)
                pdf.set_text_color(118, 75, 162)
                pdf.cell(0, 8, "Trợ lý AI:", ln=True)

            # Content
            pdf.set_font(font_name, "", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 6, content)

            # Sources
            sources = msg.get("sources", [])
            if sources:
                pdf.set_font(font_name, "", 8)
                pdf.set_text_color(130, 130, 130)
                pdf.cell(0, 6, f"Nguồn: {', '.join(sources)}", ln=True)

            pdf.ln(4)

        pdf.output(output_path)
        return output_path
