# WebDev Chat

## Description

This Gradio application helps you with any architecture of your web application, using 16 specialised agents, from Frontend Architect all the way to LLM Fine-tuning Architect. Note : it is made to design your app **NOT** edit code.

It is a Python-based web development chat application that uses OpenAI's SDK, it uses a triage agent to determine which specialist agent to use based on the user's question.

## Architecture

The application consists of the following main components:

*   `app.py`: Contains the Gradio interface and the logic for running the agents.
*   `main.py`: Imports the agents.
*   `agents.py`: Defines the agents and their instructions.

The application uses the following key libraries:

*   `gradio`: For the chat interface.
*   `openai`: For interacting with the OpenAI API.
*   `pydantic`: For data validation.
*   `python-dotenv`: For loading environment variables.

The application uses a triage agent to route questions to specialist agents. The available agents are:

*   Frontend Architect
*   Backend Architect
*   Database Architect
*   API Architect
*   Security Architect
*   DevOps Architect
*   Scalability Architect
*   Performance Architect
*   Cloud Architect
*   Mobile Architect
*   LLM Application Architect
*   LLM Tooling Architect
*   MCP Server Architect
*   Prompt Engineering Architect
*   LLM Data Architect
*   LLM Fine-tuning Architect

## Installation

1.  Clone the repository:

    ```bash
    git clone [repository URL]
    ```
2.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3.  Configure the environment variables:

    *   Copy `.env.example` to `.env`.
    *   Update the `.env` file with your OpenAI API key:

        ```
        OPENAI_API_KEY=your_api_key_here
        ```

## Usage

1.  Run the application:

    ```bash
    python app.py
    ```
2.  Open the application in your web browser.
3.  Enter your OpenAI API key in the web interface if it is not already set in the `.env` file.
4.  Ask questions about web development in the chat interface.