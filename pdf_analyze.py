import fitz

def extract_data(file_path):
    doc = fitz.open(file_path)
    count = 0
    for page in doc:
        # ページ内のすべてのテキストブロックを取得
        blocks = page.get_text("blocks")
        for block in blocks:
            # ブロック内のテキストと座標を取得
            block_text = block[4]
            block_rect = block[:4]
            # 特定のマークが含まれているかをチェック
            if "●" in block_text:
                # 座標を取得
                x0, y0, x1, y1 = block_rect
                # バウンディングボックスの中心座標を計算
                center_x = (x0 + x1) / 2
                center_y = (y0 + y1) / 2
                print(f"マークの中心座標: ({center_x}, {center_y})")
                count += 1
    return count

pdf_path = "PORT28001010001.pdf"
pdf_data = extract_data(pdf_path)
print(pdf_data)