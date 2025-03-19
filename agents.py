from pydantic import BaseModel
import asyncio
from typing import List, Callable, Optional, Any, Dict, Type, Union
import time

class GuardrailFunctionOutput:
    def __init__(self, output_info: BaseModel, tripwire_triggered: bool):
        self.output_info = output_info
        self.tripwire_triggered = tripwire_triggered

class InputGuardrail:
    def __init__(self, guardrail_function: Callable):
        self.guardrail_function = guardrail_function

class Agent:
    def __init__(
        self,
        name: str,
        instructions: str,
        handoffs: Optional[List["Agent"]] = None,
        input_guardrails: Optional[List[InputGuardrail]] = None,
        output_type: Optional[Type[BaseModel]] = None,
        handoff_description:str = ""
    ):
        self.name = name
        self.instructions = instructions
        self.handoffs = handoffs if handoffs is not None else []
        self.input_guardrails = input_guardrails if input_guardrails is not None else []
        self.output_type = output_type
        self.handoff_description = handoff_description

class RunResult:
    def __init__(self, final_output: Any, agent_used: Optional[str] = None):
        self.final_output = final_output
        self.agent_used = agent_used
    
    def final_output_as(self, output_type: Type[BaseModel]):
        return output_type(**self.final_output)

class trace:
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        self.start_time = time.time()
        print(f"Starting trace: {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        duration = end_time - self.start_time
        print(f"Trace '{self.name}' finished in {duration:.4f} seconds")

import os
from openai import AsyncOpenAI

class Runner:
    @staticmethod
    async def run(agent: Agent, input_data: str, context: Optional[Dict] = None):
        """
        Run the agent with the given input data and context.
        
        Args:
            agent: The agent to run
            input_data: The user's input message
            context: Optional context information
            
        Returns:
            RunResult containing the agent's response and which agent was used
        """
        try:
            # Initialize the OpenAI client
            client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            
            # Track which agent is being used
            current_agent = agent
            agent_used = agent.name
            
            # For the triage agent, determine which specialist agent to use
            if agent.name == "Triage Agent" and agent.handoffs:
                # First, check if the input passes the guardrails
                for guardrail in agent.input_guardrails:
                    # This is a simplified version - in a real implementation,
                    # you would actually call the guardrail function
                    pass
                
                # Prepare the system message for triage
                triage_system_message = {
                    "role": "system",
                    "content": f"""
                    {agent.instructions}
                    
                    You must select the most appropriate specialist agent to handle this query.
                    Available agents:
                    {', '.join([a.name + ': ' + a.handoff_description for a in agent.handoffs])}
                    
                    Respond ONLY with the name of the agent that should handle this query.
                    """
                }
                
                # Prepare the user message
                triage_user_message = {
                    "role": "user",
                    "content": input_data
                }
                
                # Call the OpenAI API for triage
                triage_response = await client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[triage_system_message, triage_user_message],
                    temperature=0.3,
                    max_tokens=100
                )
                
                # Extract the selected agent name
                selected_agent_name = triage_response.choices[0].message.content.strip()
                
                # Find the corresponding agent object
                for handoff_agent in agent.handoffs:
                    if handoff_agent.name.lower() in selected_agent_name.lower():
                        current_agent = handoff_agent
                        agent_used = handoff_agent.name
                        break
            
            # Prepare the system message with the selected agent's instructions
            system_message = {
                "role": "system",
                "content": current_agent.instructions
            }
            
            # Prepare the user message
            user_message = {
                "role": "user",
                "content": input_data
            }
            
            # Call the OpenAI API with the selected agent
            response = await client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[system_message, user_message],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract the response content
            response_content = response.choices[0].message.content
            
            # If the agent has an output type, try to parse the response
            if current_agent.output_type:
                try:
                    # For now, just return the raw text since we're not formatting as JSON
                    return RunResult(final_output=response_content, agent_used=agent_used)
                except Exception as e:
                    print(f"Error parsing response as {current_agent.output_type.__name__}: {e}")
                    return RunResult(final_output=response_content, agent_used=agent_used)
            
            return RunResult(final_output=response_content, agent_used=agent_used)
        except Exception as e:
            print(f"Error in Runner.run: {e}")
            return RunResult(final_output=f"Error: {str(e)}", agent_used="Error")

# Define WebdevOutput model
class WebdevOutput(BaseModel):
    is_webdev: bool
    reasoning: str

# Define all agents
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about web application development.",
    output_type=WebdevOutput,
)

frontend_architect_agent = Agent(
    name="Frontend Architect",
    handoff_description="Specialist agent for frontend architecture and UI/UX design.",
    instructions="You are the Frontend Architect. You define the overall structure, design patterns, and technology stack for the client-side of web applications. Focus on creating responsive, accessible, and performant user interfaces. Guide on frontend frameworks, component libraries, state management, and build processes. Explain your reasoning for architectural decisions and provide examples of best practices.",
)

backend_architect_agent = Agent(
    name="Backend Architect",
    handoff_description="Specialist agent for backend architecture and server-side logic.",
    instructions="You are the Backend Architect. You design the application's server-side architecture, choose appropriate languages, frameworks, and server technologies. Define how the application processes requests, manages data, and interacts with other services. Prioritize scalability, reliability, and maintainability. Explain your architectural choices and provide examples of robust backend designs.",
)

database_architect_agent = Agent(
    name="Database Architect",
    handoff_description="Specialist agent for database design and data management.",
    instructions="You are the Database Architect. You design and implement database schemas, choose the right database technology, and define data access patterns. Ensure data integrity, performance, scalability, and security. Advise on data modeling, query optimization, and database management strategies. Explain your database design rationale and provide examples of efficient data management.",
)

api_architect_agent = Agent(
    name="API Architect",
    handoff_description="Specialist agent for API design and integration.",
    instructions="You are the API Architect. You design and document application programming interfaces (APIs), ensuring they are well-defined, secure, and easy to use. Decide on API styles, data formats, and authentication mechanisms. Create robust and efficient communication channels. Explain your API design principles and provide examples of well-structured APIs.",
)

security_architect_agent = Agent(
    name="Security Architect",
    handoff_description="Specialist agent for web application security.",
    instructions="You are the Security Architect. You identify potential security risks, design security measures, and ensure security best practices are followed. Advise on authentication, authorization, data encryption, and protection against common web attacks. Explain your security recommendations and provide examples of secure coding practices.",
)

devops_architect_agent = Agent(
    name="DevOps Architect",
    handoff_description="Specialist agent for development, deployment, and operations processes.",
    instructions="You are the DevOps Architect. You design and implement CI/CD pipelines, infrastructure automation, and monitoring systems. Focus on improving the efficiency, speed, and reliability of the software delivery process. Explain your DevOps strategies and provide examples of effective automation techniques.",
)

scalability_architect_agent = Agent(
    name="Scalability Architect",
    handoff_description="Specialist agent for application scalability.",
    instructions="You are the Scalability Architect. You design the application architecture to handle increasing user traffic and data loads without compromising performance or stability. Consider horizontal and vertical scaling, load balancing, and caching. Explain your scalability strategies and provide examples of scalable system designs.",
)

performance_architect_agent = Agent(
    name="Performance Architect",
    handoff_description="Specialist agent for application performance optimization.",
    instructions="You are the Performance Architect. You identify performance bottlenecks, recommend optimization techniques, and ensure the application meets required performance metrics. Advise on code optimization, database query tuning, and efficient resource utilization. Explain your performance optimization recommendations and provide examples of performance best practices.",
)

cloud_architect_agent = Agent(
    name="Cloud Architect",
    handoff_description="Specialist agent for cloud infrastructure and services.",
    instructions="You are the Cloud Architect. You design and implement the application's infrastructure using cloud services. Choose appropriate cloud resources, manage costs, and ensure the application leverages cloud benefits like scalability and reliability. Explain your cloud architecture decisions and provide examples of effective cloud resource utilization.",
)

mobile_architect_agent = Agent(
    name="Mobile Architect",
    handoff_description="Specialist agent for mobile application architecture.",
    instructions="You are the Mobile Architect. You design the architecture for mobile applications (native, hybrid, or PWA) that interact with the web application's backend. Consider mobile-specific challenges like offline capabilities, push notifications, and device features. Explain your mobile architecture approaches and provide examples of robust mobile designs.",
)

llm_application_architect_agent = Agent(
    name="LLM Application Architect",
    handoff_description="Specialist agent for integrating Large Language Models into web applications.",
    instructions="You are the LLM Application Architect. You design the architecture of web applications that leverage Large Language Models for various functionalities. You determine how LLMs will be integrated with other components, considering factors like data flow, user interaction, and cost efficiency. Explain your integration strategies and provide examples of effective LLM application designs.",
)

llm_tooling_architect_agent = Agent(
    name="LLM Tooling Architect",
    handoff_description="Specialist agent for designing and building tools for Large Language Models.",
    instructions="You are the LLM Tooling Architect. You design and develop tools that extend the capabilities of Large Language Models. This includes creating functions, APIs, or other mechanisms that allow LLMs to interact with external systems, access specific data, or perform specialized tasks. Explain your tool design principles and provide examples of useful LLM tools.",
)

mcp_server_architect_agent = Agent(
    name="MCP Server Architect",
    handoff_description="Specialist agent for designing and implementing Model Context Protocol servers.",
    instructions="You are the MCP Server Architect. You design and implement servers that adhere to the Model Context Protocol. This involves defining how context is managed, shared, and updated between different parts of the application and the Large Language Model. Ensure the server is scalable, reliable, and efficient in handling context. Explain your MCP server design choices and provide details on its implementation.",
)

prompt_engineering_architect_agent = Agent(
    name="Prompt Engineering Architect",
    handoff_description="Specialist agent for designing effective prompts for Large Language Models.",
    instructions="You are the Prompt Engineering Architect. You specialize in crafting effective and efficient prompts that guide Large Language Models to produce desired outputs. This includes understanding different prompting techniques, designing prompt templates, and optimizing prompts for specific tasks and models. Explain your prompt design strategies and provide examples of well-engineered prompts.",
)

llm_data_architect_agent = Agent(
    name="LLM Data Architect",
    handoff_description="Specialist agent for managing and preparing data for Large Language Models.",
    instructions="You are the LLM Data Architect. You are responsible for the data pipelines and storage solutions required for training and using Large Language Models. This includes data collection, cleaning, preprocessing, and formatting to ensure high-quality data for the LLMs. Explain your data management strategies and provide examples of effective data preparation techniques for LLMs.",
)

llm_fine_tuning_architect_agent = Agent(
    name="LLM Fine-tuning Architect",
    handoff_description="Specialist agent for fine-tuning Large Language Models for specific tasks.",
    instructions="You are the LLM Fine-tuning Architect. You design and oversee the process of fine-tuning pre-trained Large Language Models on specific datasets to improve their performance on targeted tasks. This includes selecting appropriate datasets, defining fine-tuning parameters, and evaluating the results. Explain your fine-tuning methodologies and provide examples of successful fine-tuning strategies.",
)

# Define guardrail function
async def webdev_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(WebdevOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_webdev,
    )

# Define triage agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's web development question",
    handoffs=[frontend_architect_agent,
              backend_architect_agent,
              database_architect_agent,
              api_architect_agent,
              security_architect_agent,
              devops_architect_agent,
              scalability_architect_agent,
              performance_architect_agent,
              cloud_architect_agent,
              mobile_architect_agent,
              llm_application_architect_agent,
              llm_tooling_architect_agent,
              mcp_server_architect_agent,
              prompt_engineering_architect_agent,
              llm_data_architect_agent,
              llm_fine_tuning_architect_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=webdev_guardrail),
    ],
)