import streamlit as st
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
import logging
import re
import os

load_dotenv()


class DocumentProcessor:
    def __init__(self, directory):
        self.directory = directory

    def load_documents(self):
        try:
            loader = DirectoryLoader(self.directory)
            documents = loader.load()
            return documents
        except Exception as e:
            logging.error(f"Error loading documents: {str(e)}", exc_info=True)
            raise

    def split_docs(self, documents, chunk_size=1000, chunk_overlap=20):
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )
            docs = text_splitter.split_documents(documents)
            return docs
        except Exception as e:
            logging.error(f"Error splitting documents: {str(e)}", exc_info=True)
            raise


class EmbeddingsProcessor:
    def __init__(self):
        try:
            self.embeddings = SentenceTransformerEmbeddings()
        except Exception as e:
            logging.error(f"Error initializing embeddings: {str(e)}", exc_info=True)
            raise

    def create_chroma_database(self, docs):
        try:
            db = Chroma.from_documents(docs, self.embeddings)
            return db
        except Exception as e:
            logging.error(f"Error creating Chroma database: {str(e)}", exc_info=True)
            raise


class IdentityMapper:
    def __init__(self):
        try:
            self.name_id_mapping = {}
            self.phone_id_mapping = {}
            self.unique_id_counter = 1
            self.unique_phone_counter = 1
        except Exception as e:
            logging.error(f"Error initializing IdentityMapper: {str(e)}", exc_info=True)
            raise

    def replace_name(self, match):
        try:
            name = match.group(1)
            if name not in self.name_id_mapping:
                self.name_id_mapping[name] = f"ID_{self.unique_id_counter}"
                self.unique_id_counter += 1
            return f'"name": "{self.name_id_mapping[name]}",'
        except Exception as e:
            logging.error(f"Error replacing name: {str(e)}", exc_info=True)
            raise

    def replace_phone(self, match):
        try:
            phone = match.group(1)
            if phone not in self.phone_id_mapping:
                self.phone_id_mapping[phone] = f"ID_{self.unique_phone_counter}"
                self.unique_phone_counter += 1
            return f'"phone": "{self.phone_id_mapping[phone]}",'
        except Exception as e:
            logging.error(f"Error replacing phone: {str(e)}", exc_info=True)
            raise

    def replace_id(self, match):
        try:
            extracted_id = int(match.group(1))

            for entry in self.id_name_list:
                if entry["id"] == f"ID_{extracted_id}":
                    name = entry["name"]
                    break
            else:
                name = "Unknown"

            for entry in self.id_phone_list:
                if entry["id"] == f"ID_{extracted_id}":
                    phone = entry["phone"]
                    break
            else:
                phone = "N/A"

            return f"{name} (Phone: {phone})"
        except Exception as e:
            logging.error(f"Error replacing ID: {str(e)}", exc_info=True)
            raise


class AIModelProcessor:
    def __init__(self, model_name):
        try:
            self.llm = ChatOpenAI(
                model_name=model_name, openai_api_key=os.getenv("OPENAI_KEY")
            )
        except Exception as e:
            logging.error(
                f"Error initializing AIModelProcessor: {str(e)}", exc_info=True
            )
            raise

    def run_qa_chain(self, chain, query, input_documents):
        try:
            answer = chain.run(input_documents=input_documents, question=query)
            return answer
        except Exception as e:
            logging.error(f"Error running QA chain: {str(e)}", exc_info=True)
            raise


def main():
    """
    The `main()` function is a Python function that configures logging, creates a user interface for
    inputting a task query, processes documents and identities, runs a question-answering chain,
    replaces IDs in the answer, and displays the selected agents.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logfile.log"),
        ],
    )   
    st.title("Agent Selector")

    # Input query from user
    query = f"{st.text_area('Enter the task you have:')}. Which two agents are the best for this?"

    if st.button("Select agent"):
        try:
            # Process documents
            directory = "agents"
            document_processor = DocumentProcessor(directory)
            documents = document_processor.load_documents()
            docs = document_processor.split_docs(documents)

            # Create Chroma database
            chroma_processor = EmbeddingsProcessor()
            db = chroma_processor.create_chroma_database(docs)

            # Search for matching documents
            matching_docs = db.similarity_search(query)

            # Process identities
            identity_mapper = IdentityMapper()
            document = matching_docs[0].page_content
            name_pattern = re.compile(r'"name": "(.*?)",')
            phone_pattern = re.compile(r'"phone": "(.*?)",')
            modified_document = name_pattern.sub(identity_mapper.replace_name, document)
            modified_document = phone_pattern.sub(
                identity_mapper.replace_phone, modified_document
            )
            identity_mapper.id_name_list = [
                {"id": id, "name": name}
                for name, id in identity_mapper.name_id_mapping.items()
            ]
            identity_mapper.id_phone_list = [
                {"id": id, "phone": phone}
                for phone, id in identity_mapper.phone_id_mapping.items()
            ]
            matching_docs[0].page_content = modified_document

            # Run QA chain
            model_processor = AIModelProcessor(model_name="gpt-3.5-turbo")
            chain = load_qa_chain(
                model_processor.llm, chain_type="stuff", verbose=False
            )
            answer = model_processor.run_qa_chain(
                chain, query, input_documents=matching_docs
            )

            # Replace IDs in the answer
            pattern = r"ID_(\d+)"
            updated_answer = re.sub(pattern, identity_mapper.replace_id, answer)

            # Display the result
            st.subheader("Selected Agents:")
            st.write(updated_answer)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}", exc_info=True)
            st.error(f"Error running QA chain: {str(e)}")


if __name__ == "__main__":
    main()
