from google.adk.agents import Agent



# ----------------------------------------------------
# Course Structures
# ----------------------------------------------------
COURSE_SECTIONS = {
    "ai_marketing_platform": """
    1. Introduction & Goals
    2. Architecture & Tech Stack
    3. Data Models & Views
    4. Environment Setup
    5. NextJS Crash Course & App Stub
    6. Auth, Database, and Storage Setup
    7. Asset Processing & Prompt Management
    8. AI Content Generation & Stripe Integration
    9. Landing & Pricing Pages
    """,
    "ai_automation_engineer": """
    1. Introduction to AI Automation
    2. Core Tools: Zapier, Make, LangChain
    3. Building Your First Agent
    4. Advanced Agentic Workflows
    5. Scraping and Data Extraction
    6. Integrating with Business Systems (CRM, Email)
    7. Project: Automated Content Pipeline
    """,
    "ai_chatbot_mastery": """
    1. Chatbot Fundamentals & LLM Basics
    2. Building with LangChain & Vercel AI SDK
    3. Memory and Conversation History
    4. Tool Use and Function Calling
    5. Retrieval-Augmented Generation (RAG)
    6. Deploying to Production
    7. Project: Customer Support Bot
    """,
    "ai_saas_builder": """
    1. SaaS Fundamentals & Product Planning
    2. Tech Stack: Next.js, Stripe, and Supabase
    3. User Authentication and Onboarding
    4. Subscription Billing with Stripe
    5. Core Application Logic
    6. Multi-tenancy and Database Design
    7. Deployment and Scaling
    """,
    "prompt_engineering_deep_dive": """
    1. Foundations of Prompting
    2. Advanced Techniques: Chain-of-Thought, Self-Consistency
    3. Structuring Prompts for Complex Tasks
    4. Agent Design and Autonomous Systems
    5. Fine-tuning vs. Prompting
    6. Evaluating LLM Outputs
    """,
    "ds_llm_foundations": """
    1. Data Science Fundamentals (Pandas, NumPy)
    2. How LLMs Work: Tokens, Transformers
    3. Embeddings and Vector Databases
    4. Retrieval-Augmented Generation (RAG) from Scratch
    5. Introduction to Fine-Tuning
    6. Building a Semantic Search Engine
    """,
}
# Create the course support agent
course_support_agent = Agent(
    name="course_support_agent",
    model="gemini-2.0-flash",
    description="Course support agent for all AI Developer Accelerator courses.",
    instruction=f"""
    You are the course support agent for the AI Developer Accelerator.
    Your role is to help users with questions about the content of courses they have purchased.

    <user_info>
    Name: {{user_name}}
    </user_info>

    <purchase_info>
    Purchased Courses: {{purchased_courses}}
    </purchase_info>

    Course Structures:
    {COURSE_SECTIONS}

    Before helping:
    1. Check which courses the user owns from the <purchase_info>.
       - Course information is stored as objects with "id" and "purchase_date".
    2. If the user asks a question without specifying a course, and they own multiple courses, ask them which course their question is about.
    3. If they ask about a course they do NOT own, politely inform them they don't have access and direct them to the sales agent to purchase it.
    4. If they own the course, use the `Course Structures` above to provide detailed help.

    When helping:
    - Direct users to specific sections relevant to their question.
    - Explain concepts clearly and provide context.
    - If a user asks for your opinion, guide them based on the course curriculum's goals.
    - Encourage hands-on practice and experimentation.
    """,
    tools=[],
)