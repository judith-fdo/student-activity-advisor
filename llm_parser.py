"""
LLM-based Natural Language Parser using Groq (FREE!)
Converts user's natural language input into structured facts for the Expert System
"""

from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()

def parse_natural_language(user_message):
    """
    Parse natural language input using Groq API (FREE)
    Returns structured data for the expert system
    """
    
    try:
        client = Groq(
            api_key=os.environ.get("GROQ_API_KEY")
        )
        
        # Prompt for LLM to extract structured information
        extraction_prompt = f"""You are helping extract structured information from a student's description of their current state.

The student said: "{user_message}"

Extract the following information and return ONLY a valid JSON object with these exact fields:

{{
    "sleep_hours": <number between 0-12, default 7>,
    "energy_level": <"Very Low" | "Low" | "Moderate" | "High", default "Moderate">,
    "stress_level": <"Low" | "Moderate" | "High" | "Very High", default "Moderate">,
    "study_hours_today": <number between 0-12, default 2>,
    "deadline_urgency": <"None" | "This week" | "Within 48 hours" | "Urgent (within 24h)", default "None">,
    "break_taken": <true | false, default false>,
    "task_complexity": <"Low" | "Medium" | "High", default "Medium">,
    "passive_learning_hours": <number between 0-8, default 1>,
    "social_isolation_days": <number between 0-7, default 1>,
    "sedentary_hours": <number between 0-12, default 4>,
    "cramming": <true | false, default false>,
    "current_time": <number between 0-23 for hour of day, use 14 if not mentioned>
}}

Rules for extraction:
- If information is not mentioned, use the default value
- Be conservative with estimates
- "tired", "exhausted", "drained" → energy_level: "Low" or "Very Low"
- "stressed", "anxious", "overwhelmed" → stress_level: "High" or "Very High"
- "exam tomorrow", "assignment due" → deadline_urgency: "Urgent (within 24h)"
- "haven't slept much", "barely slept" → sleep_hours: 3-5
- "all-nighter", "didn't sleep" → sleep_hours: 0-2
- "been studying all day", "studied for hours" → study_hours_today: 6-8
- "cramming", "studying non-stop" → cramming: true
- "haven't talked to anyone", "isolated" → social_isolation_days: 3-7

Return ONLY the JSON object, no explanation or markdown formatting."""
        
        # Call Groq API - using Llama 3.1
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": extraction_prompt,
                }
            ],
            model="llama-3.3-70b-versatile",  # Fast and good at structured output
            temperature=0.1,  # Low temperature for consistent extraction
            max_tokens=1024,
        )
        
        # Extract response
        response_text = chat_completion.choices[0].message.content.strip()
        
        # Sometimes LLM wraps in ```json, remove that
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()
        
        # Parse JSON
        extracted_data = json.loads(response_text)
        
        return {
            'success': True,
            'data': extracted_data,
            'raw_response': response_text,
            'model_used': 'Llama 3.3 70B (via Groq)'
        }
        
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'error': f'Failed to parse JSON: {str(e)}. Response was: {response_text[:200]}',
            'data': None
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': None
        }


def get_extraction_explanation(user_message, extracted_data):
    """
    Generate a human-readable explanation of what was extracted
    """
    explanation = []
    
    if extracted_data.get('sleep_hours', 7) != 7:
        explanation.append(f"Sleep: {extracted_data['sleep_hours']} hours")
    
    if extracted_data.get('energy_level') != "Moderate":
        explanation.append(f"Energy: {extracted_data['energy_level']}")
    
    if extracted_data.get('stress_level') != "Moderate":
        explanation.append(f"Stress: {extracted_data['stress_level']}")
    
    if extracted_data.get('study_hours_today', 0) > 0:
        explanation.append(f"Studied: {extracted_data['study_hours_today']} hours today")
    
    if extracted_data.get('deadline_urgency') != "None":
        explanation.append(f"Deadline: {extracted_data['deadline_urgency']}")
    
    if extracted_data.get('break_taken'):
        explanation.append(f"Break taken")
    
    if extracted_data.get('cramming'):
        explanation.append(f"Cramming detected")
    
    if extracted_data.get('task_complexity') != "Medium":
        explanation.append(f"Task complexity: {extracted_data['task_complexity']}")
    
    if extracted_data.get('social_isolation_days', 1) > 2:
        explanation.append(f"No social contact: {extracted_data['social_isolation_days']} days")
    
    return explanation if explanation else ["Using default values for most fields"]


def test_parser():
    """
    Test the parser with example inputs
    """
    test_cases = [
        "I slept 4 hours, feeling exhausted, have exam tomorrow",
        "Got 8 hours sleep, feeling great, ready to study my hardest subject",
        "Super stressed, been studying for 7 hours straight, haven't talked to anyone in 5 days"
    ]
    
    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"Input: {test}")
        print(f"{'='*60}")
        result = parse_natural_language(test)
        if result['success']:
            print(json.dumps(result['data'], indent=2))
            print("\nExplanation:")
            for item in get_extraction_explanation(test, result['data']):
                print(f"  {item}")
        else:
            print(f"Error: {result['error']}")


if __name__ == "__main__":
    # Test the parser
    test_parser()