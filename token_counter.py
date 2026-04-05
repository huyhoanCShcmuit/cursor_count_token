from mcp.server.fastmcp import FastMCP
import tiktoken
import json
import os

mcp = FastMCP("NotionLightServer")

@mcp.tool()
def process_and_count_tokens(user_input: str, read_files: list[str]) -> str:
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        
        # 1. Đếm token của Input
        input_token_count = len(encoding.encode(user_input))
        
        # 2. Xử lý và đếm token của các File
        files_detail = []
        total_files_token = 0
        
        # --- DANH SÁCH CÁC FILE KHÔNG TÍNH TOKEN ---
        ignored_files = {".cursorrules", "token_counter.py", "cursor_request_log.json"}
        
        for file_path in read_files:
            # Lấy tên file từ đường dẫn (ví dụ: /Users/huy.../token_counter.py -> token_counter.py)
            file_name = os.path.basename(file_path)
            
            # Nếu tên file nằm trong danh sách cấm, gán 0 token và bỏ qua bước đọc file
            if file_name in ignored_files:
                files_detail.append({
                    "file_path": file_path,
                    "tokens": 0,
                    "status": "skipped (ngoại trừ)"
                })
                continue
                
            try:
                # Nếu không bị cấm thì tiến hành đọc và đếm token bình thường
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    file_tokens = len(encoding.encode(content))
                    total_files_token += file_tokens
                    
                    files_detail.append({
                        "file_path": file_path,
                        "tokens": file_tokens,
                        "status": "success"
                    })
                else:
                    files_detail.append({
                        "file_path": file_path,
                        "tokens": 0,
                        "status": "file_not_found"
                    })
            except Exception as e:
                files_detail.append({
                    "file_path": file_path,
                    "tokens": 0,
                    "status": f"error: {str(e)}"
                })

        # 3. Đóng gói dữ liệu để ghi log
        log_data = {
            "input_nhan_duoc": user_input,
            "token_input": input_token_count,
            "token_files_tong": total_files_token,
            "chi_tiet_files": files_detail
        }
        
        # Đường dẫn tuyệt đối tĩnh chốt cứng
        log_file = "/Users/huy-hoannguyen/Documents/uit/cursor_mcp_call/cursor_request_log.json"
        
        # --- ĐÃ SỬA THÀNH 'w' ĐỂ GHI ĐÈ FILE CŨ ---
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(log_data, ensure_ascii=False, indent=2) + "\n")
            
        return f"Đã ghi đè log thành công. Input: {input_token_count} tokens. Tổng token các file hợp lệ: {total_files_token}."
        
    except Exception as e:
        return f"Đã xảy ra lỗi khi chạy tool: {str(e)}"

if __name__ == "__main__":
    mcp.run()