# Agent Selector Application

The Agent Selector application is a Python script built using Streamlit that helps users select the best agents for a given task. It leverages various components, including document processing, identity mapping, and a question-answering model.

## How to Use

1. **Install Dependencies:**
   Ensure you have the required Python packages installed. You can install them using the following command:
    ```bash
   pip install -r requirements.txt
    ```

2. **Set Up Environment Variables:**
Create a .env file in the project directory and set your OpenAI API key. For example:
    ```makefile
    OPENAI_KEY=your_api_key_here
    ```

3. **Run the Application:**
    Execute the following command in the terminal:
    ```bash
    streamlit run app.py
    ```

4. **Input Task Query:** 
    Enter the task description in the provided text area and click the "Select agent" button.

5. **View Results:**
The application will display the selected agents based on the input task query.

## Components

1. **DocumentProcessor Class**
- Loads documents from a specified directory.
- Splits documents into smaller chunks using a text splitter.

2. **EmbeddingsProcessor Class**
- Creates a Chroma database from a list of documents using SentenceTransformer embeddings.
3. **IdentityMapper Class**
- Maps names and phone numbers to unique IDs and replaces IDs with corresponding names and phone numbers.
4. **AIModelProcessor Class**
- Processes AI models for question-answering tasks using the ChatOpenAI model.
5. **Main Function (main)**
- Configures logging.
- Creates a user interface using Streamlit.
- Processes documents and identities, runs a question-answering chain, and displays the selected agents.

## Logging

- Logging is configured to record information in both the console and a log file (logfile.log).

## Error Handling

- Exception handling is implemented to capture and log any errors that occur during execution.
# Important Note

- Ensure that you have a valid OpenAI API key and have permission to use the specified model.
