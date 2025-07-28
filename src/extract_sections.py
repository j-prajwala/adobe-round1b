import fitz  # PyMuPDF
import os
from sklearn.feature_extraction.text import TfidfVectorizer


def extract_relevant_sections(pdf_path, persona, job):
    doc = fitz.open(pdf_path)
    sections = []
    subsection_analysis = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for b in blocks:
            if b['type'] != 0:
                continue
            for line in b.get("lines", []):
                line_text = " ".join(span["text"] for span in line.get("spans", []))
                line_text = line_text.strip()
                if not line_text or len(line_text) < 30:
                    continue

                score = relevance_score(line_text, persona, job)
                if score >= 0.2:
                    sections.append({
                        "document": os.path.basename(pdf_path),
                        "page_number": page_num + 1,
                        "section_title": line_text,
                        "importance_rank": round(score, 3)
                    })

                    # Extract subsection chunks
                    refined = extract_subsections(line_text, persona, job)
                    for chunk in refined:
                        subsection_analysis.append({
                            "document": os.path.basename(pdf_path),
                            "page_number": page_num + 1,
                            "refined_text": chunk
                        })

    # Rank top N sections
    sections = sorted(sections, key=lambda x: x["importance_rank"], reverse=True)[:10]

    return sections, subsection_analysis


def relevance_score(text, persona, job):
    combined = persona + " " + job
    vectorizer = TfidfVectorizer().fit([combined, text])
    vecs = vectorizer.transform([combined, text])
    return (vecs[0] @ vecs[1].T).toarray()[0][0]


def extract_subsections(text, persona, job):
    chunks = [p.strip() for p in text.split("\n") if len(p.strip()) > 40]
    if not chunks:
        return []

    vectorizer = TfidfVectorizer().fit([job] + chunks)
    job_vec = vectorizer.transform([job])
    chunk_vecs = vectorizer.transform(chunks)

    scores = (chunk_vecs @ job_vec.T).toarray().flatten()
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)

    return [r[0] for r in ranked[:3]]  # Top 3 relevant chunks
