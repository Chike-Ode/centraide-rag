# import streamlit as st

# from langchain import hub
# # from langchain_chroma import Chroma
# from langchain_community.vectorstores import FAISS,Chroma
# from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
# import os

# # pword = st.sidebar.text_input("Enter your OpenAI API Key or Password:", type="password")
# # if pword == "test":
# #     os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
# #     openai_api_key = st.secrets["OPENAI_API_KEY"]
# # else:
# #     os.environ['OPENAI_API_KEY'] = pword
# #     openai_api_key = pword
# st.title("Homelessness Support App")

# # Sample data for language and boroughs (you can expand this list)
# language = [
#     "Hope Haven",
#     "Safe Harbor Shelter",
#     "Community Comfort Center",
#     "The Warm Welcome",
#     "Second Chance Shelter",
#     "Unity House",
#     "The Refuge Lodge",
#     "Peaceful Pathway Shelter",
#     "Caring Hearts Haven",
#     "New Beginnings Shelter",
#     "The Healing Place",
#     "Serenity Shelter",
#     "Light House Shelter",
#     "Compassion Corner",
#     "The Nesting Place",
#     "The Open Door Shelter",
#     "Oasis of Hope",
#     "Together We Rise Shelter",
#     "Shelter of Support",
#     "Friendship Haven"
# ]

# boroughs = [
#     "Borough 1",
#     "Borough 2",
#     "Borough 3",
#     # Add more boroughs as needed
# ]

# with st.sidebar.form(key='api_key_form'):
#     st.header("Enter your OpenAI API Key or Password")
#     pword = st.text_input("OpenAI API Key or Password:", type="password")
#     submit_button = st.form_submit_button(label='Submit')
#     # Shelter selection
#     selected_language = st.selectbox("Select a Shelter:", language)
        
#     # Borough selection
#     selected_borough = st.selectbox("Select a Borough:", boroughs)

#     # Check if the form was submitted
# if submit_button:
#     if pword == "test":
#         os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
#         openai_api_key = st.secrets["OPENAI_API_KEY"]
#     else:
#         os.environ['OPENAI_API_KEY'] = pword
#         openai_api_key = pword

# llm = ChatOpenAI(temperature=0.7, api_key=openai_api_key)# Create RAG
# file_path = "centraide-homeless-examples.pdf"
# loader = PyPDFLoader(file_path)
# docs = loader.load()

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(docs)
# # st.info(splits)
# # vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(api_key=openai_api_key))
# vectorstore = FAISS.from_documents(splits, embedding=OpenAIEmbeddings(api_key=openai_api_key))

# # Retrieve and generate using the relevant snippets of the blog.
# retriever = vectorstore.as_retriever()
# # 2. Incorporate the retriever into a question-answering chain.
# prompt_template = PromptTemplate(
#     input_variables=["context", "question"],
#     template=(
#         "You are an expert on homelessness. Based on the provided context, please answer the following question in detail:\n\n"
#         "Context: {context}\n\n"
#         "Question: {question}\n\n"
#         "Please provide a comprehensive response, including causes, impacts, and potential solutions."
#     )
# )


# # prompt = hub.pull("rlm/rag-prompt")


# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)


# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt_template
#     | llm
#     | StrOutputParser()
# )



# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # React to user input
# if question := st.chat_input("Share your concerns here"):
#     # Display user message in chat message container
#     st.chat_message("user").markdown(question)
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": question})

#     response = rag_chain.invoke(question) #f"Echo: {prompt}"
    
#     # response = llm.invoke(question) #f"Echo: {prompt}"
#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         st.markdown(response)
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})
    
    
    
    
    
    
    
    
    
    
    
    


import streamlit as st
from langchain import hub
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
import os


st.set_page_config(
    page_title="Éko",
    page_icon="logo.png"  # Use .ico format for best compatibility
)

st.markdown(
    """
    <style>
    .stChatMessage {
        background-color: #f0f0f0;
        border-radius: 5px;
        padding: 10px;
    }
    .stSidebar {
        background-color: #f7f7f7;
        border-right: 2px solid #e0e0e0;
    }
    body {
        font-family: 'Arial', sans-serif;
    }
    .logo {
        display: block;
        margin: 0 auto;
        opacity: 0;
        animation: fadeIn 2s forwards;
    }
    @keyframes fadeIn {
        to {
            opacity: 1;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load logo
logo_url = "logo.png"  # Update with your logo path or URL

# Display logo with animation
# st.image(logo_url, caption="Support for Homelessness", width=300)
st.sidebar.image(logo_url, caption="Bâtir des communautés inclusives", width=300)
# st.sidebar.markdown(
#     f"<div style='text-align: center;'><img src='{logo_url}' style='width: 200px;'></div>",
#     unsafe_allow_html=True
# )

st.title("Éko")
st.header("Obtenez des réponses sur l’itinérance dans votre région.")

def main():
    # Sample data for language and boroughs
    language = [
        "Français",
        "English"
    ]

    boroughs = [
        "Le Sud Ouest",
        "Cote-des-Neiges/Notre-Dame-de-Grace",
        "Ville-Marie", 
        "Le Plateau Mont-Royal", 
        "Mercier-Hochelaga-Maisonneuve"
    ]

    # Create a form for user input in the sidebar
    with st.sidebar.form(key='api_key_form'):
        st.header("OpenAI API Key")
        pword = st.text_input("OpenAI API Key:", type="password")
        
        # Shelter selection
        selected_language = st.selectbox("Language:", language)
            
        # Borough selection
        selected_borough = st.selectbox("Location:", boroughs)

        submit_button = st.form_submit_button(label='Submit')

    # Check if the form was submitted
    if submit_button or len(pword)>0:
        # Set the API key based on user input
        if pword == "test":
            os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
            openai_api_key = st.secrets["OPENAI_API_KEY"]
        else:
            os.environ['OPENAI_API_KEY'] = pword
            openai_api_key = pword

        # Initialize the language model with the provided API key
        llm = ChatOpenAI(temperature=0.7, api_key=openai_api_key)

        # Load documents
        file_path = "BENOIT LABRE.pdf" #"centraide-homeless-examples2.pdf"
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # Split documents for processing
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # Initialize the vector store
        vectorstore = FAISS.from_documents(splits, embedding=OpenAIEmbeddings(api_key=openai_api_key))

        # Set up the retriever and prompt template
        retriever = vectorstore.as_retriever()
        # prompt_template = PromptTemplate(
        #     input_variables=["context", "question"],
        #     template=(
        #         "You are an expert on homelessness in Montreal. Based on the provided context and your knowledge, please answer the following question in detail:\n\n"
        #         "Context: {context}\n\n"
        #         "Question: {question}\n\n"
        #         "Please provide a comprehensive response, including causes, impacts, and potential solutions."
        #     )
        # )

        
        prompt_templates = {
            "Français": PromptTemplate(
                input_variables=["context", "question"],
                template=(
                    "Vous êtes un expert de l’itinérance à Montréal et vous entendez des préoccupations concernant l’impact de l’itinérance sur les personnes vivant dans la communauté.. En fonction du contexte fourni et de vos connaissances, veuillez répondre à la question suivante brièvement:\n\n"
                    "Contexte : {context}\n\n"
                    "Question : {question}\n\n"
                    "Veuillez fournir une réponse empathique aux préoccupations des sans-abri et de la personne qui pose la question. Si la question n’est pas liée au contexte, renseignez-vous davantage sur leurs préoccupations."
                )
            ),
            "English": PromptTemplate(
                input_variables=["context", "question"],
                template=(
                    "You are an expert on homelessness in Montreal and you hear concerns about homeless impact on people living in the community. Based on the provided context and your knowledge, please answer the following question concisely:\n\n"
                    "Context: {context}\n\n"
                    "Question: {question}\n\n"
                    "Please provide an empathetic response for both the homeless and the inquirer's concerns. If the question is not related to the context inquire more on their concerns."
                )
            )
        }

        # Select the appropriate prompt template based on the chosen language
        prompt_template = prompt_templates[selected_language]
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt_template
            | llm
            | StrOutputParser()
        )

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if question := st.chat_input("Partagez vos préoccupations ici"):
            st.chat_message("user").markdown(question)
            st.session_state.messages.append({"role": "user", "content": question})

            response = rag_chain.invoke(question)
            
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    else:
        if selected_language=='English':
            st.warning("Please enter your OpenAI API Key to use the app.")
        else:
            st.warning("Veuillez saisir votre clé API OpenAI pour utiliser l’application.")

if __name__ == "__main__":
    main()
