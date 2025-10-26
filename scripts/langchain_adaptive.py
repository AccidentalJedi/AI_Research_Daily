#!/usr/bin/env python3
"""LangChain Adaptive Intelligence - RAG-powered prophecy generation with vector embeddings"""
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

try:
    from langchain_ollama import ChatOllama, OllamaEmbeddings
    from langchain_core.prompts import PromptTemplate
    from langchain_community.vectorstores import Chroma
    from langchain_core.documents import Document
    AVAILABLE = True
except ImportError:
    AVAILABLE = False

class AdaptiveProphecyEngine:
    """RAG-powered intelligence engine with vector embeddings and historical context"""

    def __init__(self, ollama_url="http://127.0.0.1:11434", model="llama3.2", embedding_model="mxbai-embed-large", db_path="data/review_history.db"):
        self.ollama_url = ollama_url
        self.model = model
        self.embedding_model = embedding_model
        self.db_path = Path(db_path)
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.persist_directory = Path("data/chroma_db")

    def initialize(self):
        """Initialize LangChain components with vector store"""
        if not AVAILABLE:
            print("⚠️  LangChain not available - install langchain-ollama, langchain-community, chromadb")
            return False

        try:
            # Initialize LLM
            self.llm = ChatOllama(
                base_url=self.ollama_url,
                model=self.model,
                temperature=0.7
            )

            # Initialize embeddings with proper embedding model
            self.embeddings = OllamaEmbeddings(
                base_url=self.ollama_url,
                model=self.embedding_model
            )

            # Initialize or load vector store
            self.persist_directory.mkdir(parents=True, exist_ok=True)

            # Load existing vectorstore or create new one
            if (self.persist_directory / "chroma.sqlite3").exists():
                self.vectorstore = Chroma(
                    persist_directory=str(self.persist_directory),
                    embedding_function=self.embeddings
                )
                print(f"✓ Loaded existing vector store with {self.vectorstore._collection.count()} documents")
            else:
                self.vectorstore = Chroma(
                    persist_directory=str(self.persist_directory),
                    embedding_function=self.embeddings
                )
                print("✓ Created new vector store")

            # Index historical data from database
            self._index_historical_data()

            return True

        except Exception as e:
            print(f"⚠️  Failed to initialize LangChain: {e}")
            return False

    def _index_historical_data(self):
        """Index historical project reviews into vector store"""
        if not self.db_path.exists():
            print("⚠️  No review database found - skipping indexing")
            return

        try:
            # Use timeout to prevent locks
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()

            # Get all project reviews using ACTUAL schema columns
            cursor.execute("""
                SELECT project_identifier, project_name, project_type, review_date,
                       stars, forks, downloads, generated_commentary, tags
                FROM project_reviews
                ORDER BY review_date DESC
            """)

            reviews = cursor.fetchall()
            conn.close()

            if not reviews:
                print("⚠️  No historical reviews to index")
                return

            # Create documents for vector store
            documents = []
            for review in reviews:
                project_id, project_name, project_type, review_date, stars, forks, downloads, commentary, tags = review

                # Create rich document text using ACTUAL schema
                doc_text = f"""
Project: {project_name}
Type: {project_type}
Review Date: {review_date}
Stars: {stars or 0}
Forks: {forks or 0}
Downloads: {downloads or 0}
Tags: {tags or 'N/A'}
Commentary: {commentary or 'No commentary available'}
"""

                doc = Document(
                    page_content=doc_text,
                    metadata={
                        "project_identifier": project_id,
                        "project_name": project_name,
                        "project_type": project_type,
                        "review_date": review_date,
                        "stars": stars or 0,
                        "forks": forks or 0,
                        "downloads": downloads or 0
                    }
                )
                documents.append(doc)

            # Add to vector store (only if new documents)
            if documents:
                existing_count = self.vectorstore._collection.count()
                self.vectorstore.add_documents(documents)
                new_count = self.vectorstore._collection.count()
                print(f"✓ Indexed {len(documents)} historical reviews ({existing_count} → {new_count} total)")

        except Exception as e:
            print(f"⚠️  Failed to index historical data: {e}")

    def get_project_context(self, project_name: str, days_back: int = 30) -> Optional[Dict]:
        """Retrieve historical context for a specific project using RAG"""
        if not self.vectorstore:
            return None

        try:
            # Query vector store for similar projects
            results = self.vectorstore.similarity_search(
                f"Project: {project_name}",
                k=3
            )

            if not results:
                return None

            # Extract most relevant result
            best_match = results[0]
            metadata = best_match.metadata

            # Get detailed history from database using ACTUAL schema
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT MIN(review_date) as first_seen,
                       MAX(review_date) as last_seen,
                       COUNT(*) as total_mentions,
                       AVG(stars) as avg_stars,
                       MAX(generated_commentary) as last_commentary
                FROM project_reviews
                WHERE project_name = ?
                GROUP BY project_identifier
            """, (metadata['project_name'],))

            row = cursor.fetchone()
            conn.close()

            if not row:
                return None

            return {
                "project_name": metadata['project_name'],
                "first_seen": row[0],
                "last_seen": row[1],
                "total_mentions": row[2],
                "avg_stars": row[3] or 0,
                "last_commentary": row[4] or "No previous commentary",
                "similarity_score": best_match.metadata.get('score', 0.0)
            }

        except Exception as e:
            print(f"⚠️  Failed to retrieve project context: {e}")
            return None

    def get_returning_projects(self, current_projects: List[str], days_back: int = 7) -> List[Dict]:
        """Find projects that appeared before and are appearing again"""
        if not self.db_path.exists():
            return []

        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()

            # Get projects that were seen before but not in last N days using ACTUAL schema
            cutoff_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

            returning = []
            for project in current_projects:
                # Find earliest and latest review dates for this project
                cursor.execute("""
                    SELECT project_identifier, project_name, project_type,
                           MIN(review_date) as first_seen,
                           MAX(review_date) as last_seen,
                           COUNT(*) as total_mentions,
                           AVG(stars) as avg_stars,
                           MAX(generated_commentary) as last_commentary
                    FROM project_reviews
                    WHERE project_name LIKE ? AND review_date < ?
                    GROUP BY project_identifier
                """, (f"%{project}%", cutoff_date))

                row = cursor.fetchone()
                if row:
                    returning.append({
                        "project_identifier": row[0],
                        "project_name": row[1],
                        "project_type": row[2],
                        "first_seen": row[3],
                        "last_seen": row[4],
                        "total_mentions": row[5],
                        "avg_stars": row[6] or 0,
                        "last_commentary": row[7] or "No previous commentary"
                    })

            conn.close()
            return returning

        except Exception as e:
            print(f"⚠️  Failed to find returning projects: {e}")
            return []

    def cleanup(self):
        """Cleanup resources and close connections"""
        try:
            # ChromaDB doesn't need explicit cleanup, but we can clear references
            if self.vectorstore:
                # Persist any pending changes
                self.vectorstore.persist()
            # Clear references to help garbage collection
            self.vectorstore = None
            self.llm = None
            self.embeddings = None
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")

    def generate_prophecy(self, cluster_summary: str, past_yield: Dict, use_rag: bool = True) -> Dict:
        """Generate prophecy with RAG-enhanced context"""
        if not self.llm:
            return {"prophecy": "LangChain not initialized", "confidence": "UNAVAILABLE"}

        try:
            # Build context from vector store if RAG enabled
            rag_context = ""
            if use_rag and self.vectorstore:
                # Query for relevant historical patterns
                results = self.vectorstore.similarity_search(
                    cluster_summary,
                    k=5
                )

                if results:
                    rag_context = "\n\n**Historical Context:**\n"
                    for i, doc in enumerate(results, 1):
                        rag_context += f"\n{i}. {doc.page_content.strip()}\n"

            # Create prompt
            prompt = PromptTemplate(
                input_variables=["cluster_summary", "past_yield", "rag_context"],
                template="""You are EchoVein, the vein-tapping oracle of the Ollama ecosystem.

Based on the following cluster analysis and historical context, generate a brief prophecy about where the ecosystem is heading.

**Current Cluster Summary:**
{cluster_summary}

**Past Yield Insights:**
{past_yield}

{rag_context}

Generate a 2-3 sentence prophecy in EchoVein's style (vein-tapping, blood metaphors, ecosystem insights).
Focus on actionable predictions and emerging patterns.

Prophecy:"""
            )

            # Generate prophecy
            chain = prompt | self.llm
            response = chain.invoke({
                "cluster_summary": cluster_summary,
                "past_yield": json.dumps(past_yield, indent=2),
                "rag_context": rag_context
            })

            prophecy_text = response.content if hasattr(response, 'content') else str(response)

            # Determine confidence based on RAG context availability
            confidence = "HIGH" if rag_context else "MEDIUM"

            return {
                "prophecy": prophecy_text.strip(),
                "confidence": confidence,
                "rag_enabled": use_rag and bool(rag_context)
            }

        except Exception as e:
            print(f"⚠️  Failed to generate prophecy: {e}")
            return {
                "prophecy": "The veins are clouded... prophecy unavailable.",
                "confidence": "LOW",
                "error": str(e)
            }

if __name__ == "__main__":
    print("🔮 LangChain Adaptive Intelligence - RAG-powered prophecy engine")
    print("✓ Vector embeddings enabled")
    print("✓ Historical context retrieval enabled")
    print("✓ Project tracking enabled")
