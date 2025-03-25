# extract_table_keywords.py
import pdfplumber

def extract_univ_names_from_table(pdf_path):
    univ_names = set()

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    for cell in row:
                        if cell and "대" in cell:  # "대학", "대"로 끝나는 필터링
                            cell = cell.strip()
                            # 너무 긴 이름 제외, 단과대학 아닌 항목 제외 (예: "공과대학")
                            if len(cell) <= 6 and "대학" in cell and not "과" in cell:
                                univ_names.add(cell)

    return sorted(univ_names)

# 사용 예시
if __name__ == "__main__":
    keywords = extract_univ_names_from_table("data/input.pdf")
    print("📋 추출된 대학 키워드:")
    for kw in keywords:
        print(f"'{kw}',")
    print(f"\n총 {len(keywords)}개 대학 추출됨.")