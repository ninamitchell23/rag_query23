import streamlit as st
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

client = chromadb.HttpClient(host="chromadb", port=8000)

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

def process_uploaded_file(file_path):
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    vectordb.add_documents(chunks)
    vectordb.persist()

# Sidebar: Chat History
#st.sidebar.title(" Upload a Text File")
#uploaded_file = st.sidebar.file_uploader("Upload `.txt` file", type="txt")

#if uploaded_file is not None:
    #with open("uploaded_temp.txt", "wb") as f:
    #    f.write(uploaded_file.getbuffer())
    #process_uploaded_file("uploaded_temp.txt")
    #st.sidebar.success(" File uploaded and indexed!")
    #st.rerun()

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

        # Set selected index to latest and clear input
        st.session_state.selected_question_index = len(st.session_state.messages) - 1
        st.session_state.user_input = ""

# Safely show selected or last message after processing
if st.session_state.messages:
    selected_index = st.session_state.selected_question_index or len(st.session_state.messages) - 1
    selected = st.session_state.messages[selected_index]

    st.markdown(f"**Question:** {selected['question']}")
    st.markdown(f"**Answer:** {selected['answer']}")
