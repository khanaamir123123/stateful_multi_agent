
from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


# ----------------------------------------------------
# Course Catalog (Editable)
# ----------------------------------------------------
COURSE_CATALOG = {
    "ai_marketing_platform": {
        "name": "Fullstack AI Marketing Platform",
        "price": 149,
        "value_proposition": "Learn to build AI-powered marketing automation apps",
        "includes": "6 weeks of group support with weekly coaching calls",
    },
    "ai_automation_engineer": {
        "name": "AI Automation Engineer Bootcamp",
        "price": 199,
        "value_proposition": "Master AI workflow automation for real businesses",
        "includes": "Automation templates, project-based training, community support",
    },
    "ai_chatbot_mastery": {
        "name": "AI Chatbot Mastery",
        "price": 129,
        "value_proposition": "Build advanced LLM chatbots with memory, tools, and actions",
        "includes": "Deployment training + prebuilt bot templates",
    },
    "ai_saas_builder": {
        "name": "AI SaaS Builder Accelerator",
        "price": 249,
        "value_proposition": "Learn to build and launch your own AI SaaS startup",
        "includes": "Product planning, payments, auth, billing, and deployment",
    },
    "prompt_engineering_deep_dive": {
        "name": "Prompt Engineering Deep Dive",
        "price": 79,
        "value_proposition": "Master advanced prompting, agents, and LLM optimization",
        "includes": "100+ prompt patterns and real-world examples",
    },
    "ds_llm_foundations": {
        "name": "Data Science & LLM Foundations",
        "price": 99,
        "value_proposition": "Learn data fundamentals, embeddings, RAG, and LLM internals",
        "includes": "Beginner-friendly structured curriculum",
    },
}


# ----------------------------------------------------
# Generic Purchase Tool
# ----------------------------------------------------
def purchase_course(tool_context: ToolContext, course_id: str) -> dict:
    """
    Purchases ANY course from the COURSE_CATALOG.
    Updates state with purchase information.
    """
    if course_id not in COURSE_CATALOG:
        return {"status": "error", "message": f"Course ID '{course_id}' does not exist."}

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Retrieve current purchased courses
    purchased = tool_context.state.get("purchased_courses", [])
    owned_ids = [c["id"] for c in purchased if isinstance(c, dict)]

    # Check if user already owns it
    if course_id in owned_ids:
        return {"status": "error", "message": "You already own this course!"}

    # Add new purchased course
    purchased.append({"id": course_id, "purchase_date": current_time})
    tool_context.state["purchased_courses"] = purchased

    # Update interaction history
    history = tool_context.state.get("interaction_history", [])
    history.append(
        {
            "action": "purchase_course",
            "course_id": course_id,
            "timestamp": current_time,
        }
    )
    tool_context.state["interaction_history"] = history

    return {
        "status": "success",
        "message": f"Successfully purchased {COURSE_CATALOG[course_id]['name']}!",
        "course_id": course_id,
        "timestamp": current_time,
    }


# ----------------------------------------------------
# Format Course Catalog for Agent Instructions
# ----------------------------------------------------
def format_course_list():
    text = ""
    for cid, info in COURSE_CATALOG.items():
        text += f"""
- Name: {info['name']}
  ID: {cid}
  Price: ${info['price']}
  Value Proposition: {info['value_proposition']}
  Includes: {info['includes']}
"""
    return text


COURSE_LIST_TEXT = format_course_list()


# ----------------------------------------------------
# Sales Agent Definition
# ----------------------------------------------------
sales_agent = Agent(
    name="sales_agent",
    model="gemini-2.0-flash",
    description="Sales agent for the AI Developer Accelerator community.",
    instruction=f"""
You are a sales agent for the AI Developer Accelerator community, handling sales for all courses.

<user_info>
Name: {{user_name}}
</user_info>

<purchase_info>
Purchased Courses: {{purchased_courses}}
</purchase_info>

<interaction_history>
{{interaction_history}}
</interaction_history>

Available Courses:
{COURSE_LIST_TEXT}

When interacting with users:

1. Always check if the user already owns a course.
   - Purchased courses are stored as objects with "id" and "purchase_date".
   - Compare based on the course ID.

2. If the user already owns the course:
   - Remind them they already have access.
   - Ask if they need help with any specific module, feature, or lesson.
   - Direct them to course support for technical or learning questions.

3. If the user does NOT own the course:
   - Explain the course value (from the Course Catalog above).
   - Mention the price.
   - If they say they want to buy:
       - Use the purchase_course tool with the correct course_id.
       - Confirm the purchase.
       - Offer to help them get started with the first steps.

4. After every interaction:
   - The system will automatically track state & history.

Remember:
- Be friendly, helpful, and non-pushy.
- Highlight practical skills and real-world outcomes.
- Emphasize hands-on learning and real application building.
""",
    tools=[purchase_course],
)