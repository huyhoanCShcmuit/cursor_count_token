import streamlit as st
import json
import os
import tiktoken

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Cursor Token Tracker", page_icon="📊", layout="centered")
st.title("📊 Giao diện Thống kê Token Cursor")
st.markdown("Dashboard tổng hợp tự động lượng token sử dụng cho mỗi lần gửi yêu cầu.")

# Đường dẫn tĩnh tới file JSON (như đã cấu hình trong MCP)
JSON_FILE_PATH = "/Users/huy-hoannguyen/Documents/uit/cursor_mcp_call/cursor_request_log.json"

# --- PHẦN 1: DỮ LIỆU TỰ ĐỘNG TỪ MCP (INPUT & FILES) ---
st.header("1. Ngữ cảnh đầu vào (Tự động)")

input_tokens = 0
file_tokens = 0

if os.path.exists(JSON_FILE_PATH):
    try:
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            input_tokens = data.get("token_input", 0)
            file_tokens = data.get("token_files_tong", 0)
            
            # Hiển thị số liệu nổi bật
            col1, col2 = st.columns(2)
            col1.metric(label="💬 Token Câu hỏi (Input)", value=input_tokens)
            col2.metric(label="📁 Token Các file đã đọc", value=file_tokens)
            
            # Mở rộng để xem chi tiết
            with st.expander("Xem chi tiết nội dung đã gửi"):
                st.markdown("**Câu hỏi của bạn:**")
                st.info(data.get("input_nhan_duoc", ""))
                
                st.markdown("**Danh sách file đã đọc:**")
                st.json(data.get("chi_tiet_files", []))
                
    except Exception as e:
        st.error(f"Lỗi khi đọc file JSON: {e}")
else:
    st.warning("⏳ Chưa có dữ liệu. Hãy đặt câu hỏi trong Cursor để MCP tạo file log nhé.")


# --- PHẦN 2: DỮ LIỆU THỦ CÔNG (OUTPUT) ---
st.divider()
st.header("2. Trả lời của AI (Thủ công)")
st.markdown("Paste câu trả lời của AI vào đây để đếm số token Output.")

output_text = st.text_area("Nội dung AI trả lời:", height=200, placeholder="Paste văn bản vào đây...")

output_tokens = 0
if output_text.strip():
    # Khởi tạo bộ đếm
    encoding = tiktoken.get_encoding("cl100k_base")
    output_tokens = len(encoding.encode(output_text))
    st.metric(label="🤖 Token Câu trả lời (Output)", value=output_tokens)


# --- PHẦN 3: TỔNG KẾT ---
st.divider()
total_tokens = input_tokens + file_tokens + output_tokens

st.subheader("🎯 TỔNG TOKEN SỬ DỤNG LẦN NÀY:")
# Hiển thị tổng số cực to và rõ ràng
st.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>{total_tokens:,} Tokens</h1>", unsafe_allow_html=True)