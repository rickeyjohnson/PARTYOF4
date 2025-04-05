# ai_summary_generator.py
def create_full_summary_prompt(employee_name, role, department, feedback_sources):
    prompt = f"""
        You are an HR AI assistant tasked with generating a comprehensive employee profile based on multi-source feedback.

        Employee Details:
        - Name: {employee_name}
        - Role: {role}
        - Department: {department}

        Below is structured feedback from different perspectives.

        --- Manager Feedback ---
        {feedback_sources.get('manager', 'No manager feedback provided.')}

        --- Peer Feedback ---
        {feedback_sources.get('peer', 'No peer feedback provided.')}

        --- Self-Assessment ---
        {feedback_sources.get('self', 'No self-assessment provided.')}

        Instructions:
        1. Create a 4–6 sentence summary of the employee’s performance using all perspectives.
        2. Highlight the employee’s strengths, recent achievements, and collaboration style.
        3. Include any noted areas for improvement.
        4. Offer development suggestions or future growth opportunities.
        5. Use a clear, professional, and concise tone suitable for HR reports.

        Respond ONLY with the final summary.
    """

    return prompt


def generate_fake_ai_summary(prompt):
    
    return (
        "Jane consistently demonstrates strong collaboration, attention to detail, "
        "and a proactive approach to her responsibilities. Her manager notes excellent leadership "
        "in cross-functional projects, while peers appreciate her supportive nature and clarity in communication. "
        "Jane acknowledges the need to delegate more effectively and pursue more strategic responsibilities. "
        "Continued focus on mentoring and developing strategic thinking will elevate her impact even further."
    )


# Example test run
if __name__ == "__main__":
    example_feedback = {
        "manager": """Q: How would you rate the employee’s productivity?\nA: 5/5\nQ: Key Strengths?\nA: Leadership, planning, team mentoring.""",
        "peer": """Q: What is it like working with the employee?\nA: Jane is very communicative and great in team projects.""",
        "self": """Q: What do you want to improve?\nA: I want to delegate more and take on bigger initiatives."""
    }

    prompt = create_full_summary_prompt(
        employee_name="Jane Doe",
        role="Product Manager",
        department="Product",
        feedback_sources=example_feedback
    )

    print("===== AI Prompt =====")
    print(prompt)
    print("\n===== Simulated AI Summary =====")
    print(generate_fake_ai_summary(prompt))
