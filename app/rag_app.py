import streamlit as st
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

st.markdown(
    """
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #8B4513;
        color: white;
    }

    /* All sidebar buttons default */
    [data-testid="stSidebar"] button {
        background-color: #A0522D;
        color: white;
    }

    /* Clear History button: first button inside sidebar */
    [data-testid="stSidebar"] button:first-of-type {
        background-color: #D2B48C !important;  /* light brown */
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Load environment variables
load_dotenv()

# Initialize LLM (Groq)
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("GROQ_MODEL")
)

# Load the persisted vector store
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(
    persist_directory="./chroma",
    embedding_function=embedding_model
)
retriever = vectordb.as_retriever()

# Build the RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_question_index" not in st.session_state:
    st.session_state.selected_question_index = None
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Sidebar: Chat History
st.sidebar.title("Chat History")

if st.sidebar.button("🗑️ Clear History"):
    st.session_state.messages = []
    st.session_state.selected_question_index = None
    st.rerun()

for i, chat in enumerate(st.session_state.messages):
    if st.sidebar.button(chat["question"], key=f"q_{i}"):
        st.session_state.selected_question_index = i

# Main UI
# Display title with image using columns
col1, col2 = st.columns([1, 5])
with col1:
    st.image("images/margaret.jpg")
with col2:
    st.title(" Book: Maid Margaret of Galloway")
    st.write("The Life Story Of Whom Four Centuries Have called *The Fair Maid Of Galloway*")

# User input box + Send button
st.session_state.user_input = st.text_input(" Ask anything about *Maid Margaret of Galloway*!:", value=st.session_state.user_input, key="user_input_box")

if st.button("Send"):
    query = st.session_state.user_input.strip()
    if query:
        with st.spinner("Thinking..."):
            result = qa_chain.invoke(query)

            # Store question and answer
            st.session_state.messages.append({
                "question": query,
                "answer": result["result"],
                "sources": result["source_documents"]
            })
            st.session_state.selected_question_index = len(st.session_state.messages) - 1
            st.session_state.user_input = ""  # Clear the input box
            st.rerun()

# Show current or selected answer
if st.session_state.selected_question_index is not None:
    selected = st.session_state.messages[st.session_state.selected_question_index]
    #st.markdown(f"###  Question:\n{selected['question']}")
    st.markdown(f"###  Answer:\n{selected['answer']}")

    #with st.expander(" View Source Chunks"):
        #for i, doc in enumerate(selected["sources"]):
        #    st.markdown(f"**Chunk {i+1}:**\n{doc.page_content[:300]}...")
