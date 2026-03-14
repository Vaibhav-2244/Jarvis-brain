def load_knowledge():
    with open("data/knowledge_base.txt", "r", encoding="utf-8") as f:
        return f.read()

def retrieve_context():
    return load_knowledge()
