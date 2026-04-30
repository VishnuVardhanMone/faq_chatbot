import json
import numpy as np
from collections import defaultdict
from sentence_transformers import SentenceTransformer

# Load FAQ data
with open("faqs.json", "r") as f:
    faqs = json.load(f)

# Load model
model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')

# Prepare data
questions = []
answers = []
intents = []

for faq in faqs:
    for pair in faq["qa_pairs"]:
        questions.append(pair["q"])
        answers.append(pair["a"])
        intents.append(faq["intent"])

# Encode all questions
question_vectors = model.encode(questions, normalize_embeddings=True)

# Build intent → indices map
intent_to_indices = defaultdict(list)
for i, intent in enumerate(intents):
    intent_to_indices[intent].append(i)

# Context memory
last_intent = None


def get_answer(user_query):
    global last_intent

    user_query = user_query.lower().strip()

    # Empty input
    if not user_query:
        last_intent = None
        return "Please enter a valid question."

    # Encode query
    query_vec = model.encode([user_query], normalize_embeddings=True)

    # global search (always)
    global_similarity = np.dot(query_vec, question_vectors.T)
    global_best_index = global_similarity.argmax()
    global_best_score = global_similarity.max()
    global_intent = intents[global_best_index]

    # context search (if exists)
    if last_intent in intent_to_indices:
        indices = intent_to_indices[last_intent]
        sub_vectors = question_vectors[indices]

        similarity = np.dot(query_vec, sub_vectors.T)
        best_local_index = similarity.argmax()
        context_score = similarity.max()
        context_index = indices[best_local_index]
    else:
        context_score = -1
        context_index = None

    # intent switching logic
    if context_index is not None and context_score >= global_best_score - 0.1:
        # stay in context
        best_index = context_index
        best_score = context_score
        detected_intent = last_intent
    else:
        # switch to global
        best_index = global_best_index
        best_score = global_best_score
        detected_intent = global_intent

    # Score boosting for short follow-ups
    if last_intent and len(user_query.split()) <= 2 and detected_intent == last_intent:
        if best_score > 0.4:
            best_score += 0.1

    # Debug prints
    print("\nQuery:", user_query)
    print("Intent:", detected_intent)
    print("Score:", round(float(best_score), 2))

    # Update context
    if best_score > 0.5:
        last_intent = detected_intent
    else:
        last_intent = None

    # Response logic
    if best_score > 0.7:
        return answers[best_index]

    elif best_score > 0.4:
        return f"Did you mean: {questions[best_index]}?"

    else:
        return "I'm not sure I understand. Ask about refunds, delivery, or orders."


# Run chatbot
while True:
    query = input("\nYou: ")
    print("Bot:", get_answer(query))