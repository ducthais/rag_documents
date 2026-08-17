"""
Custom CSS styles cho ứng dụng RAG Assistant.
Giao diện chuyên nghiệp, hiện đại, hỗ trợ Dark/Light theme.
"""

def get_custom_css():
    return """
    <style>
    /* ===== GOOGLE FONTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ===== GLOBAL RESET ===== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ===== MAIN CONTAINER ===== */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 900px;
    }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 10px;
        color: #e0e0e0 !important;
        transition: all 0.2s ease;
        font-size: 0.85rem;
        padding: 0.5rem 1rem;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.15);
        border-color: rgba(255,255,255,0.25);
        transform: translateY(-1px);
    }

    /* Primary button in sidebar (New Chat) */
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white !important;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(102,126,234,0.5);
        transform: translateY(-2px);
    }

    /* ===== CHAT MESSAGES ===== */
    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        animation: fadeInUp 0.3s ease-out;
        border: none;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ===== CHAT INPUT ===== */
    [data-testid="stChatInput"] {
        border-radius: 24px !important;
    }

    [data-testid="stChatInput"] textarea {
        border-radius: 24px !important;
        border: 2px solid rgba(102,126,234,0.3) !important;
        padding: 0.75rem 1.25rem !important;
        font-size: 0.95rem !important;
        transition: border-color 0.3s ease !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.15) !important;
    }

    /* ===== EXPANDER (Sources) ===== */
    .streamlit-expanderHeader {
        font-size: 0.85rem;
        font-weight: 500;
        color: #667eea;
        border-radius: 8px;
    }

    /* ===== WELCOME PAGE ===== */
    .welcome-container {
        text-align: center;
        padding: 4rem 2rem;
    }

    .welcome-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .welcome-subtitle {
        color: #888;
        font-size: 1rem;
        margin-bottom: 2.5rem;
    }

    /* ===== SUGGESTION CARDS ===== */
    .suggestion-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        max-width: 600px;
        margin: 0 auto;
    }

    .suggestion-card {
        background: rgba(102,126,234,0.08);
        border: 1px solid rgba(102,126,234,0.15);
        border-radius: 12px;
        padding: 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
    }

    .suggestion-card:hover {
        background: rgba(102,126,234,0.15);
        border-color: rgba(102,126,234,0.3);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.1);
    }

    .suggestion-icon {
        font-size: 1.3rem;
        margin-bottom: 0.4rem;
    }

    .suggestion-text {
        font-size: 0.85rem;
        color: #555;
        line-height: 1.4;
    }

    /* ===== TOAST & ALERTS ===== */
    .stToast {
        border-radius: 12px !important;
    }

    .stAlert {
        border-radius: 12px !important;
    }

    /* ===== POPOVER ===== */
    [data-testid="stPopover"] > button {
        border-radius: 20px !important;
        border: 1px solid rgba(102,126,234,0.3) !important;
        color: #667eea !important;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    [data-testid="stPopover"] > button:hover {
        background: rgba(102,126,234,0.08) !important;
        border-color: #667eea !important;
    }

    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        border-radius: 12px;
    }

    /* ===== ONBOARDING CARD ===== */
    .onboarding-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.05) 0%, rgba(118,75,162,0.05) 100%);
        border: 1px solid rgba(102,126,234,0.2);
        border-radius: 16px;
        padding: 2rem;
        max-width: 500px;
        margin: 4rem auto;
        text-align: center;
    }

    .onboarding-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 0.5rem;
    }

    .onboarding-desc {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }

    /* ===== SIDEBAR SECTIONS ===== */
    .sidebar-section-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: rgba(255,255,255,0.4) !important;
        margin: 1rem 0 0.5rem 0;
        font-weight: 600;
    }

    /* ===== ELAPSED TIME ===== */
    .elapsed-time {
        font-size: 0.75rem;
        color: #999;
        margin-top: 0.25rem;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(102,126,234,0.3);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(102,126,234,0.5);
    }

    /* ===== CONVERSATION HISTORY ITEM ===== */
    .chat-history-item {
        padding: 0.5rem 0.75rem;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.2s ease;
        margin-bottom: 2px;
        font-size: 0.85rem;
        color: #ccc;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .chat-history-item:hover {
        background: rgba(255,255,255,0.08);
    }

    .chat-history-item.active {
        background: rgba(102,126,234,0.2);
        color: white;
    }
    </style>
    """
