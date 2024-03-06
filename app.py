import streamlit as st
from pathlib import Path
import google.generativeai as genai

# Google GenerativeAI 설정
def configure_genai():
    genai.configure(api_key="AIzaSyCr0VjXZqCdd0BR3nPCjCzmSgA9GJk4JfA")
    generation_config = {
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 4096,
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    return model

# Streamlit 웹 애플리케이션 설정
def main():
    st.title("이미지로 다양한 용도 제안하기")

    model = configure_genai()

    uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # 이미지를 저장합니다.
        with open("uploaded_image.png", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 이미지 검증
        img_path = Path("uploaded_image.png")
        if not img_path.exists():
            st.error("이미지를 찾을 수 없습니다.")
            return

        image_parts = [
            {"mime_type": uploaded_file.type, "data": img_path.read_bytes()},
        ]

        prompt_parts = [
            "이미지의 물건을 다양한 용도를 제시해줘. 가장 기본적인 용도부터, 정말 이색적인 사용처도 제시해줘.",
            image_parts[0],
        ]

        # Generative AI 모델을 사용해 콘텐츠 생성
        response = model.generate_content(prompt_parts)
        
        # 결과 표시
        st.write(response.text)

if __name__ == "__main__":
    main()
