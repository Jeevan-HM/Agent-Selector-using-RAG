# 🚀 Agent Selector Application 🚀

Welcome to the Agent Selector Application repository! This Python-based application is your one-stop solution to select the best agents for a given task. It uses document processing, identity mapping, and a question-answering model to provide you with the best results. 🕵️‍♀️🕵️‍♂️

## 📁 Repository Structure 📁

Here's a quick overview of the main files in this repository:

1. **Agent Selector Application**: The main Python script that does all the heavy lifting. It processes documents, maps identities, runs a question-answering chain, and displays the selected agents. 📚🔍
2. **requirements.txt**: A list of all Python dependencies required for the software to run properly. 📝
3. **app.py**: A Python script that uses various classes and methods to process documents, create embeddings, map identities, and run a question-answering chain using an AI model. 🧠
4. **README copy.md**: This very file you're reading right now! It provides an overview of the application, its repository structure, how to get started, and important notes. 📖
5. **test.py**: A test suite for the EmbeddingsProcessor class from the app module. It ensures everything is working as expected. 🧪
6. **agents.txt**: A text file containing information about various agents, including their names, phone numbers, skills, and restrictions. 🕵️‍♀️🕵️‍♂️

## 🚀 Getting Started 🚀

To get started with the Agent Selector Application, follow these steps:

1. Install Dependencies: Run `pip install -r requirements.txt` in your terminal to install all necessary Python packages. 📦
2. Set Up Environment Variables: Set your OpenAI API key as an environment variable using `OPENAI_KEY=your_api_key_here`. 🔑
3. Run the Application: Finally, run the application using `streamlit run app.py`. 🚀

## 📝 Notes 📝

- Logging is configured to record information in both the console and a log file (logfile.log). 📝
- Exception handling is implemented to capture and log any errors that occur during execution. 🛠️
- Ensure that you have a valid OpenAI API key and have permission to use the specified model. 🔑

## 📚 Documentation 📚

For more detailed information about each file and its functions, please refer to the individual file summaries above. 📖

## 🎉 Conclusion 🎉

That's it! You're all set to use the Agent Selector Application. We hope you find it useful and easy to use. If you have any questions or run into any issues, feel free to open an issue. Happy agent hunting! 🎉🕵️‍♀️🕵️‍♂️