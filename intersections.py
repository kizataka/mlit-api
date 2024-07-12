import fitz  # PyMuPDF

def get_column_coordinates_and_widths(pdf_path, column_titles):
    # PDFを読み込む
    doc = fitz.open(pdf_path)
    page = doc[0]  # 1ページ目を取得

    # ページのサイズを取得
    page_width = page.rect.width
    page_height = page.rect.height

    column_coordinates = {}
    
    # 各見出しの位置を取得
    for title in column_titles:
        text_instances = page.search_for(title)
        if text_instances:
            rect = text_instances[0]  # 最初のインスタンスを使用
            x0, y0 = rect.x0, rect.y0
            x1, y1 = rect.x1, rect.y1
            column_coordinates[title] = (x0, x1)
        else:
            column_coordinates[title] = None

    # 各列の幅を計算
    column_widths = {}
    sorted_titles = sorted(column_titles, key=lambda t: column_coordinates[t][0] if column_coordinates[t] else float('inf'))

    for i in range(len(sorted_titles) - 1):
        title = sorted_titles[i]
        next_title = sorted_titles[i + 1]
        if column_coordinates[title] and column_coordinates[next_title]:
            width = column_coordinates[next_title][0] - column_coordinates[title][0]
            column_widths[title] = width

    # 最後の列の幅を計算（ページの右端までの幅）
    last_title = sorted_titles[-1]
    if column_coordinates[last_title]:
        width = page_width - column_coordinates[last_title][0]
        column_widths[last_title] = width

    return column_coordinates, column_widths, (page_width, page_height)

# 列の見出しをリストで指定
column_titles = [
    "深さ", "孔内水位", "土質記号", "土質名", "試料番号", "粒度組成", 
    "液性限界", "塑性限界", "自然含水比", "湿潤密度", "土粒子の密度", 
    "間隙比", "N値", "一軸圧縮強さ", "圧密降伏応力", "圧縮指数", 
    "内部摩擦角", "粘着力"
]

# PDFファイルのパスを指定
pdf_path = "PORT28001010001.pdf"
column_coordinates, column_widths, page_size = get_column_coordinates_and_widths(pdf_path, column_titles)

print("各列のx座標の範囲: ")
for title, coords in column_coordinates.items():
    if coords:
        print(f"{title}の列のx座標は {coords[0]} から {coords[1]}")
    else:
        print(f"{title}の列の見出しが見つかりませんでした。")

print("\n各列の幅: ")
for title, width in column_widths.items():
    print(f"{title}の列の幅は {width} ポイント")

print("\nPDFページのサイズ: ")
print(f"幅: {page_size[0]} ポイント")
print(f"高さ: {page_size[1]} ポイント")
