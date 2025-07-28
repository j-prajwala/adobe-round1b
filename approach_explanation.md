## Adobe India Hackathon 2025 – Round 1B
### Persona-Driven Document Intelligence – Approach Explanation

#### 🔍 Problem Overview

The task is to create an intelligent system that analyzes a collection of documents and extracts the most relevant sections and sub-sections based on a defined **persona** and their **job-to-be-done**. The system must be domain-agnostic, scalable to various document types (e.g., research papers, textbooks, reports), and operate without internet access.

---

#### 🧠 Key Design Philosophy

Our solution emphasizes:
- **Generic adaptability:** No domain-specific logic.
- **Lightweight processing:** All models are under 1GB and CPU-friendly.
- **Relevance-driven ranking:** Sections are prioritized based on semantic similarity with persona goals.

---

#### 📥 Inputs

- A folder of 3–10 PDF documents (`input_docs/`)
- `persona.txt`: Description of the user's role and expertise
- `job.txt`: Concrete task the user is trying to achieve

---

#### ⚙️ Processing Pipeline

1. **PDF Parsing (PyMuPDF)**  
   - Each PDF is opened and analyzed page by page.
   - Text blocks are scanned and filtered (ignoring short lines).
   - Candidates for “sections” are chosen from lines with ≥30 characters.

2. **Section Relevance Ranking (TF-IDF)**  
   - Each line is compared to a composite query: `persona + job`.
   - We use `TfidfVectorizer` to calculate cosine similarity.
   - The top 10 most relevant lines across all PDFs are selected as **sections**.
   - These are stored with document name, page number, section title, and importance score.

3. **Sub-Section Analysis**  
   - Each selected section is further split into sub-parts (if possible).
   - Sub-chunks (≥40 characters) are scored based on similarity to the `job`.
   - Top 3 relevant sub-sections per section are returned.

---

#### 📤 Output

- A single JSON file (`output/result.json`) with:
  - Metadata (documents, persona, job, timestamp)
  - Extracted sections (with importance rank)
  - Sub-section refinement (chunks most relevant to the task)

---

#### 💡 Why This Works

- TF-IDF scoring is fast, interpretable, and sufficient for semantic filtering.
- The system handles any document domain because it treats content generically.
- All logic runs in under 60 seconds for 3–5 documents using CPU only.

---

#### 🛠️ Tools & Constraints

- Python 3.10
- PyMuPDF for PDF text extraction
- Scikit-learn for TF-IDF vectorization
- Dockerized with `--platform=linux/amd64`
- Model size well under 1GB
- No external API or internet access

---

#### ✅ Future Enhancements

- Replace TF-IDF with a small embedding model (e.g., MiniLM) for better semantic understanding.
- Improve section chunking using font/style cues or layout models.
- Add visualization to show why a section was selected (for transparency).

---
