import os
import sys


from fastapi import FastAPI, Request, Response, Form

# Try importing required libraries
try:
    from crewai import Agent, Task, Crew, Process, LLM
except ImportError:
    print("Error: Required libraries not found. Run pip install -r requirements.txt")
    sys.exit(1)

app = FastAPI(
    title="Autonomous Estate Operations Pipeline API",
    description="A live REST API mapping unstructured text into operational insights."
)

if "GROQ_API_KEY" not in os.environ:
    print("WARNING: GROQ_API_KEY not found in environment variables.")

try:
    # CrewAI 1.x uses its own built-in LLM wrapper (backed by LiteLLM)
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        temperature=0.7
    )
except Exception as e:
    print(f"Error initializing LLM: {str(e)}")

# ==========================
# 1. Communications Ingestion Agent
# ==========================
ingestion_agent = Agent(
    role="Communications Ingestion",
    goal="Parse raw messages from the homestay owner to strictly separate food/menu items from document/compliance requests.",
    backstory="An expert in reading unstructured, messy communications and systematically categorizing information into actionable streams. You never lose a single detail.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# ==========================
# 2. Business Operations Agent
# ==========================
operations_agent = Agent(
    role="Business Operations",
    goal="Enforce business rules, standardize pricing, write appetizing menu descriptions, handle infant dietary needs, and determine required documents.",
    backstory="A seasoned hospitality manager. You price standard meals strictly between ₹800 and ₹2500 INR. If an infant is mentioned, you ALWAYS append high-quality, safe, pureed alternative options to the menu. You handle strict compliance and documentation perfectly.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# ==========================
# 3. Digital Clerk Agent
# ==========================
clerk_agent = Agent(
    role="Digital Clerk",
    goal="Generate a pristine, formatted Markdown file containing the final system update.",
    backstory="A meticulous digital clerk who transforms operational data into beautifully structured Markdown documents. You take pride in neat sections, clear headings, and flawless formatting. You NEVER output conversational filler.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# ==========================
# Define Tasks
# ==========================
ingestion_task = Task(
    description="""Read the following raw message and extract the information into two distinct, clear streams:
    1. Food and menu requirements
    2. Guest document and compliance requests
    
    Raw Message:
    "{message}"
    """,
    expected_output="A structured summary with two distinct sections: 'Food/Menu Items' and 'Document/Compliance Requests', detailing exactly what is requested.",
    agent=ingestion_agent
)

operations_task = Task(
    description="""Take the output from the Ingestion Agent. 
    For the food/menu stream: 
    1. Write beautifully appetizing, premium descriptions for the menu items to make them sound like they belong in a 5-star resort.
    2. Assign realistic pricing in Indian Rupees (₹). ALL prices MUST strictly be between ₹800 and ₹2500.
    3. Note any special dietary requirements. IF an infant is mentioned, explicitly offer customized, safe pureed versions of the meals.
    
    For the document stream: 
    1. Identify exactly which legal documents (e.g., Passports, Visas, government ID) are required based on the guest details and origin mentioned. 
    2. Provide clear, straightforward instructions for the guest on what to submit.
    """,
    expected_output="A polished document containing a 'Premium Menu' section with beautiful descriptions, ₹ pricing, explicit pureed options (if infant mentioned), and a 'Compliance Directives' section.",
    agent=operations_agent
)

clerk_task = Task(
    description="""Take the Operations Agent's output and format it into a pristine Markdown report. 
    DO NOT output any conversational text like "Here is the report...". ONLY output the raw markdown.
    Your output MUST contain exactly two main sections using H1 headers:
    
    # Digital Menu Update
    (Format the menu beautifully here as a list or table, ready for UI display or sending to guests. Make sure INR (₹) prices and any infant pureed options are clearly formatted.)
    
    # Document Compliance Checklist
    (Format the compliance requirements as a clear checklist using markdown bullet points for the incoming guests)
    """,
    expected_output="A clean, highly structured Markdown text containing exactly the '# Digital Menu Update' and '# Document Compliance Checklist' sections.",
    agent=clerk_agent
)

# ==========================
# Assemble the Crew
# ==========================
crew = Crew(
    agents=[ingestion_agent, operations_agent, clerk_agent],
    tasks=[ingestion_task, operations_task, clerk_task],
    process=Process.sequential,
    verbose=True
)

@app.post("/process-update")
async def process_update(Body: str = Form(...)):
    print(f"VERIFIED MESSAGE CONTENT: {Body}")
    if not Body:
        return Response(content="<Response><Message>Error: Empty body.</Message></Response>", media_type="application/xml")
        
    # Kick off the crew
    result = crew.kickoff(inputs={'message': Body})
    
    # Extract the raw string from the CrewOutput object
    final_text = result.raw
    
    # Wrap in CDATA to prevent XML parser crashes from LLM Markdown characters
    twiml_response = f"""
    <Response>
        <Message><![CDATA[{final_text}]]></Message>
    </Response>
    """
    
    return Response(content=twiml_response, media_type="application/xml")


# This allows running the application directly via `python main.py`
if __name__ == "__main__":
    import uvicorn
    # Using 8000 as default host port
    print("Starting Autonomous Estate API Server on port 8000...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
