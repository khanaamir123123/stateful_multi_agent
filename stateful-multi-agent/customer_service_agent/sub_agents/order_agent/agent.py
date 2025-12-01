from datetime import datetime, timedelta

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


# ----------------------------------------------------
# Course Catalog
# ----------------------------------------------------
COURSE_CATALOG = {
    "ai_marketing_platform": {
        "name": "Fullstack AI Marketing Platform",
        "price": 149,
    },
    "ai_automation_engineer": {
        "name": "AI Automation Engineer Bootcamp",
        "price": 199,
    },
    "ai_chatbot_mastery": {
        "name": "AI Chatbot Mastery",
        "price": 129,
    },
    "ai_saas_builder": {
        "name": "AI SaaS Builder Accelerator",
        "price": 249,
    },
    "prompt_engineering_deep_dive": {
        "name": "Prompt Engineering Deep Dive",
        "price": 79,
    },
    "ds_llm_foundations": {
        "name": "Data Science & LLM Foundations",
        "price": 99,
    },
}


def get_current_time() -> dict:
    """Get the current time in the format YYYY-MM-DD HH:MM:SS"""
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }



def refund_course(tool_context: ToolContext, course_id: str) -> dict:
    """
    Simulates refunding a specific course if owned and within the 30-day policy.
    Updates state by removing the course from purchased_courses.
    """
    if course_id not in COURSE_CATALOG:
        return {"status": "error", "message": f"Course ID '{course_id}' does not exist."}

    current_time = datetime.now()
    course_to_refund = None
    course_found = False

    # Get current purchased courses
    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    # Find the course and check ownership
    for course in current_purchased_courses:
        if isinstance(course, dict) and course.get("id") == course_id:
            course_found = True
            course_to_refund = course
            break

    if not course_found:
        return {
            "status": "error",
            "message": "You don't own this course, so it can't be refunded.",
        }

    # Check if the purchase is within the 30-day refund window
    purchase_date = datetime.strptime(
        course_to_refund["purchase_date"], "%Y-%m-%d %H:%M:%S"
    )
    if (current_time - purchase_date) > timedelta(days=30):
        return {
            "status": "error",
            "message": "This course was purchased more than 30 days ago and is no longer eligible for a refund.",
        }

    # Create new list without the course to be refunded
    new_purchased_courses = [
        c for c in current_purchased_courses if not (isinstance(c, dict) and c.get("id") == course_id)
    ]

    # Update purchased courses in state
    tool_context.state["purchased_courses"] = new_purchased_courses

    # Update interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])
    current_interaction_history.append(
        {
            "action": "refund_course",
            "course_id": course_id,
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    )
    tool_context.state["interaction_history"] = current_interaction_history

    course_name = COURSE_CATALOG[course_id]["name"]
    course_price = COURSE_CATALOG[course_id]["price"]

    return {
        "status": "success",
        "message": f"""Successfully refunded the {course_name} course!
         Your ${course_price} will be returned to your original payment method within 3-5 business days.""",
        "course_id": course_id,
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

# Create the order agent
order_agent = Agent(
    name="order_agent",
    model="gemini-2.0-flash",
    description="Order agent for viewing purchase history and processing refunds",
    instruction="""
    You are the order agent for the AI Developer Accelerator community.
    Your role is to help users view their purchase history, course access, and process refunds for any of our courses.

    <user_info>
    Name: {user_name}
    </user_info>

    <purchase_info>
    Purchased Courses: {purchased_courses}
    </purchase_info>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    When users ask about their purchases:
    1. Check their course list from the purchase info above.
       - Course information is stored as objects with "id" and "purchase_date" properties.
    2. Format the response clearly, showing which courses they own and when they were purchased.

    When users request a refund for a specific course:
    1. First, ask which course they would like to refund if they haven't specified.
    2. Verify they own the course they want to refund by checking the purchase info.
    3. If they own it, use the `refund_course` tool with the correct `course_id`.
       - The tool will automatically check if the purchase is within the 30-day refund period.
       - If the tool returns an error about the 30-day policy, inform the user they are not eligible.
       - If the refund is successful, confirm it with the user.
    4. If they don't own the course, inform them they can't get a refund for a course they haven't purchased.

    If they haven't purchased any courses:
    - Let them know they don't have any courses yet.
    - Suggest talking to the sales agent to learn about our courses.

    Remember:
    - Be clear, professional, and helpful.
    - Always mention our 30-day money-back guarantee when relevant.
    """,
    tools=[refund_course, get_current_time],
)