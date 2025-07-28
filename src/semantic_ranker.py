# src/semantic_ranker.py

from sentence_transformers import SentenceTransformer, util

# Load a small, CPU-friendly model
model = SentenceTransformer("all-MiniLM-L6-v2")

def rerank_sections(sections, job_description, top_k=10):
    if not sections:
        return []

    section_texts = [s["refined_text"] for s in sections]
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    section_embeddings = model.encode(section_texts, convert_to_tensor=True)

    scores = util.cos_sim(job_embedding, section_embeddings)[0]  # Similarity w.r.t job
    ranked = sorted(zip(scores, sections), key=lambda x: x[0], reverse=True)

    # Update importance_rank to semantic score
    return [
        {
            **section,
            "importance_rank": float(score)
        }
        for score, section in ranked[:top_k]
    ]
