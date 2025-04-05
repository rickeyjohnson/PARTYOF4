from google import genai
from google.genai import types
from API_KEY import API_KEY
def generate_prompt(employee_profile, performance_review_responses, self_assessment_responses, peer_review_responses):
    prompt = f"""
    Based on the following responses to performance, self-assessment, and peer reviews, as well as the employee profile, please generate a comprehensive and detailed summary of the employee's overall performance, contributions, and areas for improvement. The employee's profile and feedback should be analyzed holistically to provide a thorough assessment.

    **Employee Profile:**
    Name: {employee_profile['name']}
    Role: {employee_profile['role']}
    Department: {employee_profile['department']}
    Skills: {', '.join(employee_profile['skills'])}
    Years of Experience: {employee_profile['years_experience']}

    **Performance Review Q&A:**
    {performance_review_responses}

    **Self-Assessment Q&A:**
    {self_assessment_responses}

    **Peer Review Q&A:**
    {peer_review_responses}

    Please ensure the following in your summary:
    1. **Strengths and Key Contributions**: Highlight the employee's key strengths and notable contributions to their role. Use specific examples from the reviews to illustrate these strengths.
    2. **Areas for Development**: Clearly identify areas where the employee may need to improve or focus on. Provide actionable recommendations for development.
    3. **Skills Impact**: Emphasize the skills the employee has demonstrated and how they have contributed to their performance.
    4. **Overall Summary**: Provide an overall evaluation of the employee’s performance, including notable achievements or challenges, and how they impact the employee’s future potential.
    
    Please ensure the summary is clear, specific, and paints a well-rounded picture of the employee's performance.
    """
    
    return prompt

def generate_employee_profile_summary(employee_profile, performance_review_responses, self_assessment_responses, peer_review_responses):
    # Generate the prompt for the LLM
    prompt = generate_prompt(employee_profile, performance_review_responses, self_assessment_responses, peer_review_responses)

    # Simulating an API call to the LLM (this would be replaced by a real API call in production)
    # For now, we'll return a simulated response based on the prompt.
    summary = call_llm(prompt=prompt)
    return summary
    
def call_llm(prompt):
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are an internal AI within Chevron. You are tasked with creating an employee profile for the given employee, and create a profile for them to find the job that best suits them. Please answer with professional language."),
        contents=prompt
    )
    return response.text