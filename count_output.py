import sys
import tiktoken

def count_manual_output():
    print("=" * 60)
    print("🤖 CÔNG CỤ ĐẾM TOKEN OUTPUT THỦ CÔNG")
    print("=" * 60)
    print("BƯỚC 1: Paste (dán) toàn bộ câu trả lời của AI xuống bên dưới.")
    print("BƯỚC 2: Nhấn Enter (để xuống dòng mới).")
    print("BƯỚC 3: Nhấn tổ hợp phím 'Ctrl + D' (trên Mac) để chốt và đếm.")
    print("-" * 60 + "\n")
    
    try:
        # sys.stdin.read() cho phép đọc văn bản có rất nhiều dòng
        output_text = sys.stdin.read()
        
        # Nếu người dùng không nhập gì mà bấm Ctrl+D luôn
        if not output_text.strip():
            print("\n❌ Bạn chưa dán nội dung nào cả!")
            return

        # Khởi tạo bộ đếm token
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = len(encoding.encode(output_text))
        
        print("\n\n" + "="*60)
        print("🎉 KẾT QUẢ ĐẾM:")
        print("-" * 60)
        # In ra 100 ký tự đầu để xác nhận
        preview = output_text.strip()[:100].replace('\n', ' ')
        print(f"Trích đoạn: {preview}...")
        print(f"✅ TỔNG SỐ TOKEN: {tokens}")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        # Xử lý khi người dùng bấm Ctrl + C để thoát
        print("\nĐã hủy đếm token.")

if __name__ == "__main__":
    count_manual_output()