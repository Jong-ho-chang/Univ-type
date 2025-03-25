def extract_univ_pages(pdf_path, output_dir, keywords):
    import fitz
    from pathlib import Path
    from PIL import Image

    doc = fitz.open(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 키워드별 등장 페이지 번호 저장
    keyword_pages = {kw: [] for kw in keywords}

    for page_num, page in enumerate(doc):
        text = page.get_text()
        for kw in keywords:
            if kw in text:
                keyword_pages[kw].append(page_num)

    for kw, pages in keyword_pages.items():
        if not pages:
            print(f"⚠️ '{kw}' 관련 페이지를 찾을 수 없습니다.")
            continue

        # 연속된 페이지 범위로 나누기
        ranges = []
        temp = [pages[0]]
        for i in range(1, len(pages)):
            if pages[i] == pages[i - 1] + 1:
                temp.append(pages[i])
            else:
                ranges.append(temp)
                temp = [pages[i]]
        ranges.append(temp)

        # 가장 긴 연속 범위 선택
        best_range = max(ranges, key=lambda r: len(r))
        print(f"🔍 '{kw}' 가장 유력한 구간: {best_range}")

        images = []
        for page_number in best_range:
            try:
                pix = doc[page_number].get_pixmap(dpi=200)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(img)
            except Exception as e:
                print(f"⚠️ 페이지 {page_number + 1}에서 이미지 생성 실패: {e}")

        if images:
            total_height = sum(img.height for img in images)
            max_width = max(img.width for img in images)
            merged_img = Image.new("RGB", (max_width, total_height), color=(255, 255, 255))

            y = 0
            for img in images:
                merged_img.paste(img, (0, y))
                y += img.height

            merged_img.save(output_dir / f"{kw}.png")
            print(f"✅ '{kw}' 이미지 저장 완료")
        else:
            print(f"⚠️ '{kw}' 범위에 이미지가 없습니다. 키워드 또는 PDF 구조를 확인하세요.")