# pip install langchain langchain-mistralai python-dotenv
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Define the LangChain-compatible LLM
llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0.3,
)

# ✅ Agents need a prompt with a MessagesPlaceholder for agent_scratchpad
def make_agent_prompt(system_msg: str):
    return ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),  # required for tool-calling agents
    ])

# First Agent — Search
def build_search_agent():
    prompt = make_agent_prompt("You are a web search agent. Use the web_search tool to find relevant information.")
    agent = create_tool_calling_agent(llm=llm, tools=[web_search], prompt=prompt)
    return AgentExecutor(agent=agent, tools=[web_search], verbose=True)

# Second Agent — Reader
def build_reader_agent():
    prompt = make_agent_prompt("You are a URL reader agent. Use scrape_url to extract content from web pages.")
    agent = create_tool_calling_agent(llm=llm, tools=[scrape_url], prompt=prompt)
    return AgentExecutor(agent=agent, tools=[scrape_url], verbose=True)

# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()