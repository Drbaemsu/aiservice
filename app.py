import streamlit as st
import json
import requests
from datetime import datetime
import hmac
import hashlib
from pytz import timezone

def generate_signature(client_id, client_secret):
    # timestamp 생성
    timestamp = datetime.now(timezone("Asia/Seoul")).strftime("%Y%m%d%H%M%S%f")[:-3] 

    # HMAC 기반 signature 생성
    signature = hmac.new(
        key=client_secret.encode("UTF-8"), msg=f"{client_id}:{timestamp}".encode("UTF-8"), digestmod=hashlib.sha256
    ).hexdigest()
    
    return timestamp, signature

def summarize_text(text):
    client_id = "glabs_90c977135989838aecbed6b72387cfd1477a1b13e5c305967d9677afa3f7133c"
    client_secret = "6d7b882c6a47197940391de3a031ba960cf9e8a2fb8fadc9ddc56a89c0734aa7"
    client_key = "a2000a6b-66fb-548e-ace1-3cdde3a9cb71"

    timestamp, signature = generate_signature(client_id, client_secret)

    url = "https://aiapi.genielabs.ai/kt/nlp/summarize-news"
    headers = {
        "x-client-key": client_key,
        "x-client-signature": signature,
        "x-auth-timestamp": timestamp,
        "Content-Type": "application/json",
        "charset": "utf-8",
    }  

    body = json.dumps({"text": text, "beam_size": 3})
    
    response = requests.post(url, data=body, headers=headers, timeout=60)
    
    if response.status_code == 200:
        try:
            result = response.json()
            return result["result"]["summary"] if "result" in result else "요약 결과가 없습니다."
        except json.decoder.JSONDecodeError:
            return "요약 결과를 가져오는 중 오류가 발생했습니다."
    else:
        return "요약 결과를 가져오는 중 오류가 발생했습니다."

def main():
    st.title("텍스트 요약 프로그램")
    
    text_input = st.text_area("텍스트를 입력하세요", height=200)
    if st.button("요약하기"):
        if not text_input:
            st.warning("입력된 텍스트가 없습니다.")
        else:
            summary_result = summarize_text(text_input)
            st.subheader("요약 결과:")
            st.write(summary_result)

if __name__ == "__main__":
    main()
