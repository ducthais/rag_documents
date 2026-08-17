import os
# pyrefly: ignore [missing-import]
from langchain_google_genai import ChatGoogleGenerativeAI
# pyrefly: ignore [missing-import]
from langchain_core.prompts import ChatPromptTemplate
# pyrefly: ignore [missing-import]
from langchain_core.output_parsers import StrOutputParser

class LLMManager:
    def __init__(self, model_name = "gemini-2.5-flash"):
        # Create connection
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY does not exist.")
        print(f"Loading LLM model: {model_name}")

        #Loading Genmini
        self.llm = ChatGoogleGenerativeAI(
            model = model_name,
            temperature = 0.2, # need correctly
            max_tokens = 1024
        )

        # Convert text
        self.output_parser = StrOutputParser()

        # Set up promtly
        self.prompt_template = self.create_rag_prompt()

    def create_rag_prompt(self):
        #Promt RAG
        template = """
        Bạn là một trợ lý ảo nội bộ thông minh và tận tụy của công ty.
        Nhiệm vụ của bạn là trả lời các câu hỏi của người dùng dựa TRÊN các tài liệu được cung cấp bên dưới.
        
        NGUYÊN TẮC QUAN TRỌNG NHẤT:
        1. CHỈ sử dụng thông tin từ phần "TÀI LIỆU CUNG CẤP" (Context) để trả lời.
        2. Nếu trong tài liệu không có thông tin, hãy trung thực trả lời: "Dựa trên tài liệu hiện tại, tôi không có đủ thông tin để trả lời câu hỏi này." 
        3. Tuyệt đối KHÔNG TỰ BỊA ĐẶT (hallucinate) thông tin.
        4. Trình bày câu trả lời rõ ràng, dùng bullet point (gạch đầu dòng) nếu cần thiết.

        TÀI LIỆU CUNG CẤP (Context):
        {context}
        
        =======================
        CÂU HỎI CỦA NGƯỜI DÙNG:
        {question}
        
        CÂU TRẢ LỜI CỦA BẠN:
        """
        return ChatPromptTemplate.from_template(template)
    
    def generate_answer(self, query: str, retrieved_docs: list) -> str:
        # 1. Convert docs to text
        context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

        # 2. Build chain in langchain: prompt -> llmm -> output
        chain = self.prompt_template | self.llm | self.output_parser

        # 3. Active 
        print("Thinkng...")
        response = chain.invoke({
            "context" : context_text,
            "question" : query
        }) 
        return response