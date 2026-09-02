
from collections import Counter
import math

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap 
    return chunks

def build_vocabulary(documents):
    vocab = set()
    
    for doc in documents:
        vocab.update(doc.lower().split())

    return sorted(vocab)

def compute_tf(text, vocabs):
    words = text.lower().split()
    count = Counter(words)
    total = len(words)
    if total == 0:
        return [0.0] * len(vocabs)
    return [count.get(word, 0) / total for word in vocabs]

def compute_idf(documents, vocabs):
    n = len(documents)
    idf = []

    for word in vocabs:
        doc_count = sum(
            1 for doc in documents
            if word in doc.lower().split()
        )

        idf.append(
            math.log((n + 1) / (doc_count + 1)) + 1
        )

    return idf

def tfidf_embed(text, vocabs, idf):
    tf = compute_tf(text, vocabs)
    return [
        t * i
        for t, i in zip(tf, idf)
    ]

def binary_bow_embed(text, vocabs):
    words = set(text.lower().split())
    return [
        1 if word in words else 0
        for word in vocabs
    ]

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def search(query_embedding, stored_embeddings, top_k=5):
    scores = []
    for i, emb in enumerate(stored_embeddings):
        sim = cosine_similarity(query_embedding, emb)
        scores.append((i, sim))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]

def build_rag_prompt(query, retrieved_chunks):
    context = "\n\n---\n\n".join(
        f"[Source {i+1}]\n{chunk}"
        for i, chunk in enumerate(retrieved_chunks)
    )
    return f"""Answer the question based ONLY on the following context.
If the context doesn't contain enough information, say "I don't have enough information to answer that."

Context:
{context}

Question: {query}

Answer:"""

class RAGPipeline:
    def __init__(self, chunk_size=200, overlap=50, top_k=5, binary_embeded=False):
        self.chunks = []
        self.sources = []
        self.embeddings = []
        self.vocab = []
        self.idf = []
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.top_k = top_k
        self.binary_embeded = binary_embeded

    def index(self, documents, docNames):
        all_chunks = []
        sources = []
        for doc, name in zip(documents, docNames):
            new_chunks = chunk_text(doc, self.chunk_size, self.overlap)
            all_chunks.extend(new_chunks)
            for _ in new_chunks:
                sources.append(name)
        self.chunks = all_chunks
        self.sources = sources
        self.vocab = build_vocabulary(all_chunks)
        self.idf = compute_idf(all_chunks, self.vocab)
        self.embeddings = [
            tfidf_embed(chunk, self.vocab, self.idf) if not self.binary_embeded else binary_bow_embed(chunk, self.vocab)
            for chunk in all_chunks
        ]

    def query(self, question):
        query_emb = tfidf_embed(question, self.vocab, self.idf) if not self.binary_embeded else binary_bow_embed(question, self.vocab)
        results = search(query_emb, self.embeddings, self.top_k)
        retrieved = [(self.chunks[i], score) for i, score in results]
        names = [self.sources[i] for i, score in results]
        prompt = build_rag_prompt(
            question, [chunk for chunk, _ in retrieved]
        )
        return prompt, retrieved, names

def simple_generate(prompt, retrieved_chunks, names):
    query_section = prompt.lower().split("question:")[-1]
    query_words = set(query_section.split())

    stop_words = {
        "the", "a", "an", "is", "are", "was", "were",
        "what", "how", "why", "when", "where",
        "do", "does", "for", "of", "in", "to",
        "and", "or", "on", "at", "by", "it", "its",
        "this", "that"
    }

    query_words = query_words - stop_words

    best_sentence = ""
    best_score = 0
    best_sentence_source = ''

    for retrieved_chunk, retrieved_source in zip(retrieved_chunks, names):
        chunk = retrieved_chunk[0]
        for sentence in chunk.split("."):
            sentence = sentence.strip()

            if len(sentence) < 10:
                continue

            words = set(sentence.lower().split())
            overlap = len(query_words & words)

            if overlap > best_score:
                best_score = overlap
                best_sentence = sentence
                best_sentence_source = retrieved_source

    return (
        (best_sentence, best_sentence_source)
        if best_sentence
        else ("I don't have enough information.", '')
    )

# text = "apple orange apple"
text = read_text_file("knowledge.txt")
business = read_text_file("business.txt")
company = read_text_file("company.txt")
chunk_size = 50
overlap = 10
# TF_IDF Rag
rag = RAGPipeline(chunk_size=chunk_size, overlap=overlap, top_k=3)
rag.index([text, business, company], ['knowledge.txt', 'business.txt', 'company.txt'])

# Binary Rag
rag_bi = RAGPipeline(chunk_size=chunk_size, overlap=overlap, top_k=3, binary_embeded=True)
rag_bi.index([text, business, company], ['knowledge.txt', 'business.txt', 'company.txt'])

tests = [
    {
        "question": "khách trả hàng",
        "answer": "khách trả hàng sau 7 ngày kể từ ngày nhận hàng"
    },
    {
        "question": "Đơn hàng trên 5000000đ",
        "answer": "Đơn hàng trên 5000000đ phải được quản lý duyệt trước khi xuất kho"
    },
    {
        "question": "Để nói một từ",
        "answer": "Để nói một từ, bạn sử dụng tới 70 lớp cơ"
    },
    {
        "question": "Nữ hoàng Elizabeth",
        "answer": "Nữ hoàng Elizabeth đệ nhất I tự coi mình là người mẫu mực"
    },
    {
        "question": "Nếu tồn kho",
        "answer": "Nếu tồn kho cửa hàng thấp hơn mức tối thiểu"
    },
    {
        "question": "Mỗi một lục địa",
        "answer": "Mỗi một lục địa đều có một thành phố mang tên Rome"
    },  
    {
        "question": "công nợ",
        "answer": "Khách hàng có công nợ quá hạn trên 30 ngày không được tạo thêm đơn mua chịu"
    },
    {
        "question": "Trái đất",
        "answer": "Trái đất là hành tinh duy nhất không được đặt theo tên một vị thần"
    },
    {
        "question": "Iceland",
        "answer": "Ở Iceland, sở hữu một chú chó cảnh là phạm pháp"
    },
    {
        "question": "Mắt lừa",
        "answer": "Mắt lừa được tạo hóa “sắp xếp” ở vị trí thuận"
    },          
]

success = 0
success_bi = 0
for test in tests:
    query = test["question"]

    prompt, retrieved, names = rag.query(query)
    (best_sentence, best_sentence_source) = simple_generate(prompt, retrieved, names)
    print('TF-IDF Rag: ', best_sentence, 'source: ', best_sentence_source)
    success += 1 if test["answer"] in best_sentence else 0

    prompt_bi, retrieved_bi, names_bi = rag_bi.query(query)
    (best_sentence_bi, best_sentence_source_bi) = simple_generate(prompt_bi, retrieved_bi, names_bi)
    print('Binary Rag: ', best_sentence_bi, 'source: ', best_sentence_source_bi)
    success_bi += 1 if test["answer"] in best_sentence_bi else 0
    print('-------------')

print('Total:', len(tests))
print('TF-IDF Rag: ', success )
print('Binary Rag: ', success_bi )


