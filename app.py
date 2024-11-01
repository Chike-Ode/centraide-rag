import streamlit as st
import os

st.set_page_config(
    page_title="Éko",
    page_icon="logo.png"
)

st.sidebar.image("logo.png", caption="Bâtir des communautés inclusives", width=300)

st.title("Éko")
st.markdown(
    """
    <div class="credit">
        Built by <a href="https://www.chikeodenigbo.com" target="_blank">Chike Odenigbo</a>, Senior AI Systems Engineer
    </div>
    """,
    unsafe_allow_html=True
)

def main():
    language = ["Français", "English"]
    boroughs = [
        "Le Sud Ouest",
        "Cote-des-Neiges/Notre-Dame-de-Grace",
        "Ville-Marie", 
        "Le Plateau Mont-Royal", 
        "Mercier-Hochelaga-Maisonneuve"
    ]

    with st.sidebar.form(key='api_key_form'):
        st.header("OpenAI API Key")
        pword = st.text_input("OpenAI API Key:", type="password")
        selected_language = st.selectbox("Language:", language)
        selected_borough = st.selectbox("Location:", boroughs)
        submit_button = st.form_submit_button(label='Submit')

    if submit_button or len(pword) > 0:
        if pword == "test":
            os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
            openai_api_key = st.secrets["OPENAI_API_KEY"]
        else:
            os.environ['OPENAI_API_KEY'] = pword
            openai_api_key = pword

        header = "Learn about homelessness in your area." if selected_language == 'English' else "Obtenez des réponses sur l’itinérance dans votre région."
        preoccupation = "Share your concerns here" if selected_language == 'English' else "Partagez vos préoccupations ici"
        st.header(header)

        # Initialize the language model
        llm = ChatOpenAI(temperature=0.7, api_key=openai_api_key)

        prompt_template = {
            "Français": (
                "Vous êtes un expert de l’itinérance à Montréal. Voici quelques exemples de questions que vous avez reçues :\n\n"
                "1. \"Pourquoi y a-t-il tant de sans-abri dans ma rue?\"\n"
                "   Réponse : C'est un problème complexe... \n\n"
                "2. \"Que fait la ville pour aider les sans-abri?\"\n"
                "   Réponse : La ville met en place des programmes... \n\n"
                "En fonction du contexte donné, répondez de manière empathique :\n"
                "Contexte : {context}\n"
                "Question : {question}\n"
            ),
            "English": (
                "You are an expert on homelessness in Montreal. Here are some example questions you have received:\n\n"
                "1. \"Why are there so many homeless people in my neighborhood?\"\n"
                "   Response: It's a complex issue... \n\n"
                "2. \"What is the city doing to help the homeless?\"\n"
                "   Response: The city has implemented programs... \n\n"
                "Based on the provided context, please respond empathetically:\n"
                "Context: {context}\n"
                "Question: {question}\n"
            )
        }[selected_language]

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if question := st.chat_input(preoccupation):
            st.chat_message("user").markdown(question)
            st.session_state.messages.append({"role": "user", "content": question})

            # Here we would call the LLM with the context and question
            context = "User has concerns about homelessness in their area."  # Example context
            full_prompt = prompt_template.format(context=context, question=question)
            response = llm(full_prompt)

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    else:
        st.warning("Please enter your OpenAI API Key to use the app.")

if __name__ == "__main__":
    main()


# import streamlit as st
# from langchain import hub
# from langchain_community.vectorstores import FAISS, Chroma
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.prompts import PromptTemplate
# import os

# st.set_page_config(
#     page_title="Éko",
#     page_icon="logo.png"  # Use .ico format for best compatibility
# )

# st.markdown(
#     """
#     <style>
#     body {
#         font-family: 'Arial', sans-serif;
#     }
#     .logo {
#         display: block;
#         margin: 0 auto;
#         opacity: 0;
#         animation: fadeIn 2s forwards;
#     }
#     .credit {
#         font-size: 12px;  /* Smaller font size */
#         text-align: left;  /* Left aligned */
#         margin-bottom: 20px;  /* Space below the credit */
#     }
#     @keyframes fadeIn {
#         to {
#             opacity: 1;
#         }
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Load logo
# logo_url = "logo.png"  # Update with your logo path or URL

# # Display logo with animation
# st.sidebar.image(logo_url, caption="Bâtir des communautés inclusives", width=300)

# st.title("Éko")
# st.markdown(
#     """
#     <div class="credit">
#         Built by <a href="https://www.chikeodenigbo.com" target="_blank">Chike Odenigbo</a>, Senior AI Systems Engineer
#     </div>
#     """,
#     unsafe_allow_html=True
# )
# # st.header("Obtenez des réponses sur l’itinérance dans votre région.")

# def main():
#     # Sample data for language and boroughs
#     language = [
#         "Français",
#         "English"
#     ]

#     boroughs = [
#         "Le Sud Ouest",
#         "Cote-des-Neiges/Notre-Dame-de-Grace",
#         "Ville-Marie", 
#         "Le Plateau Mont-Royal", 
#         "Mercier-Hochelaga-Maisonneuve"
#     ]

#     # Create a form for user input in the sidebar
#     with st.sidebar.form(key='api_key_form'):
#         st.header("OpenAI API Key")
#         pword = st.text_input("OpenAI API Key:", type="password")
        
#         # Shelter selection
#         selected_language = st.selectbox("Language:", language)
            
#         # Borough selection
#         selected_borough = st.selectbox("Location:", boroughs)

#         submit_button = st.form_submit_button(label='Submit')

#     # Check if the form was submitted
#     if submit_button or len(pword) > 0:
#         # Set the API key based on user input
#         if pword == "test":
#             os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
#             openai_api_key = st.secrets["OPENAI_API_KEY"]
#         else:
#             os.environ['OPENAI_API_KEY'] = pword
#             openai_api_key = pword
#         if selected_language == 'English':
#             header = "Learn about homelessness in your area."
#             preoccupation = "Share your concerns here"
#         else:
#             header = "Obtenez des réponses sur l’itinérance dans votre région."
#             preoccupation = "Partagez vos préoccupations ici"
#         st.header(header)
#         # Initialize the language model with the provided API key
#         llm = ChatOpenAI(temperature=0.7, api_key=openai_api_key)

#         # Load documents
#         file_path = "BENOIT LABRE.pdf"  # Update with your actual file path
#         loader = PyPDFLoader(file_path)
#         docs = loader.load()

#         # Split documents for processing
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#         splits = text_splitter.split_documents(docs)

#         # Initialize the vector store
#         vectorstore = FAISS.from_documents(splits, embedding=OpenAIEmbeddings(api_key=openai_api_key))

#         # Set up the retriever and prompt template
#         retriever = vectorstore.as_retriever()

#         prompt_templates = {
#             "Français": PromptTemplate(
#                 input_variables=["context", "question"],
#                 template=(  
#                     "Vous êtes un expert de l’itinérance à Montréal et vous entendez des plaintes sur les itinérants par les personnes qui vivent dans la communauté. Ton nom est Éko. En fonction du contexte fourni et de vos connaissances, veuillez répondre à la question brièvement:\n\n"
#                     "Contexte : {context}\n\n"
#                     "Question : {question}\n\n"
#                     "Veuillez fournir une réponse empathique aux préoccupations des sans-abri et de la personne qui pose la question quand la question est chargée d'émotion. Répondez de manière appropriée en fonction du niveau d’émotion de la question, c'est a dire, une question qui n'est pas charger d'emotion et repondu normalement. Si la question n’est pas liée à l'itinérance, répondez normalement sans trop d'empathie et renseignez-vous davantage sur leurs préoccupations. Si la question n'est pas sur l'itinerance repond normalement et pas comme un expert sur l'itinerance. Inclut seulement la reponse et rien d'autre ne mentionne pas que cest la reponse."
#                 )
#             ),
#             "English": PromptTemplate(
#                 input_variables=["context", "question"],
#                 template=(  
#                     "You are an expert on homelessness  in Montreal and you hear complaints about homeless people from residents of the community. Your name is Éko Based on the provided context and your knowledge, please answer the following question concisely:\n\n"
# "Context: {context}\n\n"
# "Question: {question}\n\n"
# "Provide an empathetic response based on how emotionally charged the question or concern is. If the question is not emotionally charged, respond normally. If the question is not related to homelessness, answer normally without empathy and inquire further about their concerns. If the question is not about homelessness, respond normally and not as an expert on homelessness. Include only the response and nothing else do not write that this is the response."
#                 )
#             )
#         }

#         # Select the appropriate prompt template based on the chosen language
#         prompt_template = prompt_templates[selected_language]
        
#         def format_docs(docs):
#             return "\n\n".join(doc.page_content for doc in docs)

#         rag_chain = (
#             {"context": retriever | format_docs, "question": RunnablePassthrough()}
#             | prompt_template
#             | llm
#             | StrOutputParser()
#         )

#         # Initialize chat history
#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         # Display chat messages from history on app rerun
#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#         # React to user input
#         if question := st.chat_input(preoccupation):
#             st.chat_message("user").markdown(question)
#             st.session_state.messages.append({"role": "user", "content": question})

#             response = rag_chain.invoke(question)
            
#             with st.chat_message("assistant"):
#                 st.markdown(response)
#             st.session_state.messages.append({"role": "assistant", "content": response})

#     else:
#         if selected_language == 'English':
#             st.warning("Please enter your OpenAI API Key to use the app.")
#         else:
#             st.warning("Veuillez saisir votre clé API OpenAI pour utiliser l’application.")

# if __name__ == "__main__":
#     main()
