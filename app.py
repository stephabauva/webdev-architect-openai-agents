import gradio as gr
import asyncio
import os
from dotenv import load_dotenv
from agents import Runner, triage_agent, trace

# Load environment variables from .env file if it exists
load_dotenv()

# Global variable to store the API key
api_key = os.environ.get("OPENAI_API_KEY", "")

# Print a message if no API key is found
if not api_key:
    print("No API key found in environment variables or .env file.")
    print("Please add your API key to the .env file or enter it in the web interface.")

async def chat_response(message, history=None, key=None):
    """Process the user's message and return a response from the OpenAI API."""
    try:
        # Set the API key in the environment if provided
        if key and key.strip():
            os.environ["OPENAI_API_KEY"] = key.strip()
        
        # Check if API key is set
        if not os.environ.get("OPENAI_API_KEY"):
            return "Error: OpenAI API key is not set. Please enter your API key in the field below.", "No agent used"
        
        # Call the Runner with the triage agent
        with trace("Triage workflow"):
            result = await Runner.run(triage_agent, message)
        return result
    except Exception as e:
        print(f"Error in chat_response: {e}")
        return RunResult(final_output=f"Error: {str(e)}", agent_used="Error")

if __name__ == "__main__":
    print("Starting WebDev Chat application...")
    try:
        # Create a simple Gradio chat interface
        with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="gray")) as demo:
            gr.Markdown("# WebDev Chat")
            
            # API Key input (with password masking)
            with gr.Accordion("API Key Settings", open=not api_key):
                api_key_input = gr.Textbox(
                    value=api_key,
                    placeholder="Enter your OpenAI API key here...",
                    label="OpenAI API Key",
                    type="password",
                    info="Your API key will only be used for this session and won't be stored permanently."
                )
                save_key_btn = gr.Button("Save API Key", variant="primary")
            
            # Create a two-column layout
            with gr.Row():
                # Left column for chat
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(height=500)
                    msg = gr.Textbox(placeholder="Ask a question about web development...", container=False)
                    
                    with gr.Row():
                        submit_btn = gr.Button("Send", variant="primary")
                        clear_btn = gr.Button("Clear", variant="secondary")
                
                # Right column for agent information
                with gr.Column(scale=1):
                    gr.Markdown("## Agent Information")
                    agent_info = gr.Textbox(
                        label="Current Agent",
                        value="No agent used yet",
                        interactive=False
                    )
                    
                    # Add descriptions of available agents
                    gr.Markdown("### Available Agents")
                    agent_descriptions = "<ul>"
                    for agent in [triage_agent] + triage_agent.handoffs:
                        agent_descriptions += f"<li><strong>{agent.name}</strong>: {agent.handoff_description if agent.handoff_description else 'Main triage agent'}</li>"
                    agent_descriptions += "</ul>"
                    gr.Markdown(agent_descriptions)
            
            # Function to save the API key to both environment and .env file
            def save_api_key(key):
                if key and key.strip():
                    # Save to environment variable for current session
                    os.environ["OPENAI_API_KEY"] = key.strip()
                    
                    try:
                        # Save to .env file for persistence
                        with open('.env', 'w') as f:
                            f.write(f"OPENAI_API_KEY={key.strip()}")
                        return "API key saved successfully to .env file!"
                    except Exception as e:
                        print(f"Error saving to .env file: {e}")
                        return "API key saved to session only. Could not save to .env file."
                return "Please enter a valid API key."
            
            # Connect the save button to the save function
            save_key_btn.click(save_api_key, inputs=[api_key_input], outputs=[gr.Textbox(label="Status")])
            
            async def respond(message, chat_history, key):
                if not message:
                    return "", chat_history
                
                # Add user message to chat history
                chat_history.append((message, ""))
                return "", chat_history
            
            async def bot_response(chat_history, key):
                if not chat_history:
                    return chat_history, "No agent used"
                
                # Get the last user message
                last_user_message = chat_history[-1][0]
                
                # Get response from the agent using the provided API key
                run_result = await chat_response(last_user_message, None, key)
                
                # Update the last message in chat history with the response
                chat_history[-1] = (last_user_message, run_result.final_output)
                return chat_history, f"{run_result.agent_used}"
            
            # Set up the message submission flow
            msg.submit(
                respond, [msg, chatbot, api_key_input], [msg, chatbot]
            ).then(
                bot_response, [chatbot, api_key_input], [chatbot, agent_info]
            )
            
            # Set up the button click events
            submit_btn.click(
                respond, [msg, chatbot, api_key_input], [msg, chatbot]
            ).then(
                bot_response, [chatbot, api_key_input], [chatbot, agent_info]
            )
            
            # Clear button functionality
            clear_btn.click(lambda: (None, None, "No agent used"), None, [msg, chatbot, agent_info])
        
        # Launch the Gradio interface
        print("Launching Gradio interface...")
        demo.launch(
            share=False,
            show_error=True
        )
    except Exception as e:
        print(f"Error in application: {e}")