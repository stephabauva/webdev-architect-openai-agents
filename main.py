from agents import Agent, InputGuardrail,GuardrailFunctionOutput, Runner
from pydantic import BaseModel
import asyncio

class WebdevOutput(BaseModel):
    is_webdev: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about web application development.",
    output_type=WebdevOutput,
)

# math_tutor_agent = Agent(
#     name="Math Tutor",
#     handoff_description="Specialist agent for math questions",
#     instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
# )

# history_tutor_agent = Agent(
#     name="History Tutor",
#     handoff_description="Specialist agent for historical questions",
#     instructions="You provide assistance with historical queries. Explain important events and context clearly.",
# )

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

async def webdev_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(WebdevOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_webdev,
    )

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

async def main():
    result = await Runner.run(triage_agent, "how can i optimize my prompt ?")
    print(result.final_output)

    result = await Runner.run(triage_agent, "what is a database ?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())