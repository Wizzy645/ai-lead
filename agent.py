# agent.py
import os
from dotenv import load_dotenv
from typing import TypedDict

# --- NEW SUPPORT BRAIN IMPORTS ---
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_qdrant import QdrantVectorStore
# ---------------------------------

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

class AgentState(TypedDict):
    customer_id: str
    message: str
    category: str
    company_name: str
    budget: str
    final_response: str

# --- 1. THE CHAT MODEL ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# --- 2. THE VECTOR DATABASE CONNECTION ---
print("🔌 Connecting to Local Support Database...")
embeddings = FastEmbedEmbeddings()
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    path="./qdrant_db",
    collection_name="support_manual"
)
# This tool grabs the top 2 most relevant paragraphs from the manual
retriever = vector_store.as_retriever(search_kwargs={"k": 2}) 


# --- 3. PYDANTIC SCHEMAS ---
class IntentClassification(BaseModel):
    category: str = Field(description="Must be either 'sales', 'support', or 'other'")

class SalesExtraction(BaseModel):
    company_name: str = Field(description="The name of the company")
    budget: str = Field(description="The budget amount, keep the currency symbol")

# --- 4. THE GRAPH NODES ---
def categorize_message(state: AgentState):
    print(f"\n[AI Node] Categorizing message from {state['customer_id']}...")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an intelligent router. Classify the user's message as 'sales', 'support', or 'other'."),
        ("human", "{message}")
    ])
    chain = prompt | llm.with_structured_output(IntentClassification)
    result = chain.invoke({"message": state["message"]})
    print(f" -> Result: It's a {result.category.upper()} inquiry.")
    return {"category": result.category}

def extract_sales_data(state: AgentState):
    print(f"[AI Node] Extracting Sales Data...")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract the company name and budget from the sales inquiry."),
        ("human", "{message}")
    ])
    chain = prompt | llm.with_structured_output(SalesExtraction)
    result = chain.invoke({"message": state["message"]})
    print(f" -> Extracted: Company='{result.company_name}', Budget='{result.budget}'")
    return {
        "company_name": result.company_name,
        "budget": result.budget,
        "final_response": "Sales lead processed successfully."
    }

def process_support(state: AgentState):
    print(f"[AI Node] Searching the manual for an answer...")
    question = state["message"]
    
    # 1. Search the Qdrant database for the answer
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # 2. Tell the AI to read the manual chunks and answer the user
    prompt_template = f"""You are a helpful technical support agent.
    Answer the user's question using ONLY the context provided below from our official manual.
    If the answer is not in the context, politely say you don't know and will escalate the ticket.

    Context from Manual:
    {context}

    User Question: {question}

    Answer:"""
    
    response = llm.invoke(prompt_template)
    print(f" -> Answer formulated: {response.content[:50]}...") # Print a preview
    
    return {"final_response": response.content}

# --- 5. THE GRAPH ROUTING LOGIC ---
def route_message(state: AgentState):
    if state["category"] == "sales":
        return "extract_sales"
    elif state["category"] == "support":
        return "process_support"
    else:
        return "end"

# --- 6. BUILD THE GRAPH ---
agent_builder = StateGraph(AgentState)

agent_builder.add_node("categorize", categorize_message)
agent_builder.add_node("extract_sales", extract_sales_data)
agent_builder.add_node("process_support", process_support) # Added the new node

agent_builder.set_entry_point("categorize")

agent_builder.add_conditional_edges(
    "categorize",
    route_message,
    {
        "extract_sales": "extract_sales",
        "process_support": "process_support", # Route to support!
        "end": END
    }
)

agent_builder.add_edge("extract_sales", END)
agent_builder.add_edge("process_support", END)

agent_app = agent_builder.compile()