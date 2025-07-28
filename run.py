import os
import json
from datetime import datetime
from src.extract_sections import extract_relevant_sections


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def main():
    input_dir = "input_docs"
    output_path = "output/result.json"

    persona = read_file("persona.txt")
    job = read_file("job.txt")

    documents = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]

    all_sections = []
    all_subsections = []

    for doc in documents:
        doc_path = os.path.join(input_dir, doc)
        print(f"[INFO] Processing {doc_path}...")

        sections, subsections = extract_relevant_sections(doc_path, persona, job)
        all_sections.extend(sections)
        all_subsections.extend(subsections)

    output = {
        "metadata": {
            "input_documents": documents,
            "persona": persona,
            "job_to_be_done": job,
            "timestamp": datetime.now().isoformat()
        },
        "extracted_sections": all_sections,
        "subsection_analysis": all_subsections
    }

    os.makedirs("output", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"[✅] Saved result to {output_path}")


if __name__ == "__main__":
    main()
