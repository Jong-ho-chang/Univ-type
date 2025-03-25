# extract_keywords.py
import fitz  # PyMuPDF

def extract_univ_keywords(pdf_path):
    doc = fitz.open(pdf_path)
    found_keywords = set()

    for page in doc:
        text = page.get_text()
        lines = text.split('\n')
        for line in lines:
            # '대학'이 포함된 줄만 수집
            if "대학" in line:
                # 대학 이름만 남기기 위한 간단한 필터
                words = line.strip().split()
                for word in words:
                    if "대학" in word and len(word) <= 6:
                        found_keywords.add(word)

    return sorted(found_keywords)

# 사용 예시
if __name__ == "__main__":
    pdf_path = "data/input.pdf"
    keywords = extract_univ_keywords(pdf_path)
    
    print("📋 추출된 대학 키워드:")
    for kw in keywords:
        print(f"'{kw}',")

    print(f"\n총 {len(keywords)}개 대학 추출됨.")