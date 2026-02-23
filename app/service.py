from datetime import datetime
from .tavily_tool import search_web
from .agent import generate_report
from .database import reports_collection
from .embeddings import generate_embedding
import numpy as np


class ResearchService:

    def process_query(self, query, chat_history=None):

        # ---- Build Conversation Context ----
        conversation_context = ""

        if chat_history:
            for message in chat_history:
                # message is a Pydantic ChatMessage object
                if message.role == "user":
                    conversation_context += f"User: {message.content}\n"
                else:
                    conversation_context += f"Assistant: {message.content}\n"

        # ---- Web Search ----
        web_results = search_web(query)

        # ---- Generate Report ----
        report_text = generate_report(
            query=query,
            web_data=web_results,
            conversation_context=conversation_context
        )

        # ---- Generate Embedding ----
        embedding = generate_embedding(report_text)

        # ---- Convert chat_history to dict for MongoDB ----
        chat_history_dict = []
        if chat_history:
            chat_history_dict = [msg.dict() for msg in chat_history]

        # ---- Store in DB ----
        report_doc = {
            "query": query,
            "report": report_text,
            "chat_history": chat_history_dict,
            "sources": web_results,
            "embedding": embedding,
            "timestamp": datetime.utcnow()
        }

        result = reports_collection.insert_one(report_doc)
        report_doc["_id"] = str(result.inserted_id)

        return report_doc


    # ---------------------------------------------------------
    # SEMANTIC SEARCH
    # ---------------------------------------------------------

    def semantic_search(self, query):

        query_embedding = generate_embedding(query)

        if not query_embedding:
            return []

        query_vec = np.array(query_embedding)
        results = []

        for doc in reports_collection.find():

            if "embedding" not in doc:
                continue

            try:
                doc_vec = np.array(doc["embedding"])

                if np.linalg.norm(query_vec) == 0 or np.linalg.norm(doc_vec) == 0:
                    continue

                similarity = np.dot(query_vec, doc_vec) / (
                    np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
                )

                if similarity > 0.70:
                    results.append((similarity, doc))

            except Exception:
                continue

        results.sort(key=lambda x: x[0], reverse=True)

        final_results = []
        for score, doc in results[:3]:
            doc["_id"] = str(doc["_id"])
            final_results.append(doc)

        return final_results
