"""
Streamlit UI for Daily Activity Recommendation System
"""
import fix_experta

import os
import streamlit as st
import pandas as pd
from datetime import datetime
from expert_system import run_expert_system

# Page configuration
st.set_page_config(
    page_title="Student Activity Advisor",
    page_icon="images/page_icon.jpg",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recommendation-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid;
        color: #000000;  /* Black text for readability */
    }
    .recommendation-box h3 {
        color: #000000;  /* Black headings */
        margin-top: 0;
    }
    .recommendation-box p {
        color: #1a1a1a;  /* Very dark gray for paragraphs */
        margin: 0.5rem 0;
    }
    .recommendation-box strong {
        color: #000000;  /* Black for bold text */
    }
    .priority-1 {
        background-color: #ffebee;  /* Light red background */
        border-left-color: #d32f2f;  /* Dark red border */
    }
    .priority-2 {
        background-color: #fff3e0;  /* Light orange background */
        border-left-color: #f57c00;  /* Dark orange border */
    }
    .priority-3 {
        background-color: #e3f2fd;  /* Light blue background */
        border-left-color: #1976d2;  /* Dark blue border */
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header"> Daily Activity Recommendation System for Students</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">An Expert System using Rule-Based Reasoning with Experta</p>', unsafe_allow_html=True)

st.markdown("---")

# CREATE TABS 
tab1, tab2 = st.tabs(["Structured Input (Widgets)", "Natural Language Input (Chat)"])

# ============== TAB 1: EXISTING WIDGET INTERFACE ==============
with tab1:
    st.markdown("### Traditional Expert System Interface")
    st.markdown("Answer structured questions using sliders and dropdowns")

    # Sidebar for inputs
    st.sidebar.header("Tell me about your current state")

    # Get current hour
    current_hour = datetime.now().hour

    # Input questions
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sleep & Energy")
    
        sleep_hours = st.slider(
            "How many hours did you sleep last night?",
            min_value=0.0,
            max_value=12.0,
            value=7.0,
            step=0.5,
            help="Include any naps from yesterday"
        )
    
        energy_level = st.select_slider(
            "What is your current energy level?",
            options=["Very Low", "Low", "Moderate", "High"],
            value="Moderate"
        )
        
        stress_level = st.select_slider(
            "How stressed do you feel?",
            options=["Low", "Moderate", "High", "Very High"],
            value="Moderate"
        )

    with col2:
        st.subheader("Study & Schedule")
        
        study_hours_today = st.slider(
            "How many hours have you studied today?",
            min_value=0.0,
            max_value=12.0,
            value=2.0,
            step=0.5
        )
        
        deadline_urgency = st.selectbox(
            "Do you have any urgent deadlines?",
            ["None", "This week", "Within 48 hours", "Urgent (within 24h)"],
            help="Select your most urgent deadline"
        )
        
        break_taken = st.checkbox(
            "Have you taken a substantial break today? (15+ minutes)",
            value=False
        )

    # Additional inputs in expandable section
    with st.expander("Additional Information (Optional)"):
        col3, col4 = st.columns(2)
        
        with col3:
            task_complexity = st.selectbox(
                "Complexity of your current/next task",
                ["Low", "Medium", "High"],
                index=1
            )
            
            passive_learning_hours = st.slider(
                "Hours of passive learning today (reading/watching)",
                min_value=0.0,
                max_value=8.0,
                value=1.0,
                step=0.5
            )
            
            social_isolation_days = st.slider(
                "Days since last social interaction",
                min_value=0,
                max_value=7,
                value=1
            )
        
        with col4:
            sedentary_hours = st.slider(
                "Hours sitting/sedentary today",
                min_value=0.0,
                max_value=12.0,
                value=4.0,
                step=0.5
            )
            
            cramming = st.checkbox(
                "Are you cramming (>6h on one subject today)?",
                value=False
            )
            
            current_time = st.slider(
                "Current time (hour)",
                min_value=0,
                max_value=23,
                value=current_hour,
                help="Automatically set to current time"
            )

    # Run button
    st.markdown("---")
    if st.button("Get Personalized Recommendations", type="primary", use_container_width=True):
        
        # Prepare inputs for expert system
        user_inputs = {
            'sleep_hours': sleep_hours,
            'energy_level': energy_level,
            'stress_level': stress_level,
            'study_hours_today': study_hours_today,
            'deadline_urgency': deadline_urgency,
            'break_taken': break_taken,
            'task_complexity': task_complexity,
            'passive_learning_hours': passive_learning_hours,
            'social_isolation_days': social_isolation_days,
            'sedentary_hours': sedentary_hours,
            'cramming': cramming,
            'current_time': current_time
        }
        
        # Run expert system
        with st.spinner("Analyzing your state and generating recommendations..."):
            recommendations, engine = run_expert_system(user_inputs)
        
        # Display results
        st.markdown("---")
        st.markdown("## Your Personalized Recommendations")
        
        if recommendations:
            # Show count of alternatives
            rec_count = len(recommendations)
            # Top recommendation highlighted
            st.success(f"**Top Recommendation:** {recommendations[0]['activity']}")
        
            # Show alternative solutions feature
            if rec_count > 1:
                st.info(f"**Alternative Solutions:** System generated {rec_count} ranked recommendations based on your situation.")
            
            # Analyze information completeness
            info_analysis = {
                'provided': [],
                'assumed': []
            }
        
            # Core information (always provided)
            info_analysis['provided'].extend([
                f"Sleep hours: {sleep_hours}h",
                f"Energy level: {energy_level}",
                f"Stress level: {stress_level}",
                f"Study hours today: {study_hours_today}h",
                f"Deadline urgency: {deadline_urgency}",
                f"Break taken: {'Yes' if break_taken else 'No'}"
            ])
        
            # Check optional fields
            if passive_learning_hours != 1.0:
                info_analysis['provided'].append(f"Passive learning: {passive_learning_hours}h")
            else:
                info_analysis['assumed'].append("Passive learning: 1h (default - moderate amount)")
        
            if task_complexity != "Medium":
                info_analysis['provided'].append(f"Task complexity: {task_complexity}")
            else:
                info_analysis['assumed'].append("Task complexity: Medium (default)")
        
            if sedentary_hours != 4.0:
                info_analysis['provided'].append(f"Sedentary hours: {sedentary_hours}h")
            else:
                info_analysis['assumed'].append("Sedentary hours: 4h (default - typical)")
        
            if social_isolation_days != 1:
                info_analysis['provided'].append(f"Social isolation: {social_isolation_days} days")
            else:
                info_analysis['assumed'].append("Social isolation: 1 day (default - recent contact)")
        
            if cramming:
                info_analysis['provided'].append("Cramming: Yes")
            else:
                info_analysis['assumed'].append("Cramming: No (default - normal pace)")
        
            # Display information completeness - COLLAPSED BY DEFAULT
            assumptions_count = len(info_analysis['assumed'])
        
            if assumptions_count > 0:
                # Show expander with count - user can click to expand
                with st.expander(f"View Information Completeness Analysis ({assumptions_count} assumptions made)", expanded=False):
                
                    col1, col2 = st.columns(2)
                
                    with col1:
                        st.markdown("### Information Provided")
                        for item in info_analysis['provided']:
                            st.markdown(f"- {item}")
                
                    with col2:
                        st.markdown("### Assumptions Made")
                        for item in info_analysis['assumed']:
                            st.markdown(f"- {item}")
                
                    st.markdown("---")
                
                    # Calculate completeness percentage
                    total_fields = len(info_analysis['provided']) + len(info_analysis['assumed'])
                    completeness = (len(info_analysis['provided']) / total_fields) * 100
                
                    st.metric("Information Completeness", f"{completeness:.0f}%")
                
                    st.markdown(f"""
                    **ES Feature: Incomplete Information Handling**
                
                    The expert system successfully processed your request with **{assumptions_count} missing optional fields** by:
                
                    1. ✅ **Making conservative assumptions** based on typical student patterns
                    2. ✅ **Reducing confidence levels** by ~10-15% for rules using assumed data
                    3. ✅ **Providing useful recommendations** despite incomplete information
                    """)
            else:
                # If all fields provided, show a small success badge
                with st.expander("✅ View Information Completeness Analysis (100% complete)", expanded=False):
                    st.success("""
                    **100% Information Completeness!**
                
                    All optional fields were provided. The expert system has maximum confidence in its recommendations.
                
                    **Information Provided:**
                    """)
                    for item in info_analysis['provided']:
                        st.markdown(f"- {item}")

            # ES Features in action - metrics
            metric_cols = st.columns(3)
            with metric_cols[0]:
                st.metric("Alternatives", rec_count, help="Different activity options provided")
            with metric_cols[1]:
                avg_conf = sum(r['confidence'] for r in recommendations) / len(recommendations)
                st.metric("Avg Confidence", f"{avg_conf:.0f}%", help="Average confidence level")
            with metric_cols[2]:
                rules = len(set(r['rule_fired'] for r in recommendations))
                st.metric("Rules Fired", rules, help="Number of expert rules applied")
        
            st.markdown("---")

            # Display all recommendations
            for idx, rec in enumerate(recommendations, 1):
                priority_class = f"priority-{rec['priority']}"
                
                confidence_bar = "🟢" * int(rec['confidence'] / 20)
                
                st.markdown(f"""
                <div class="recommendation-box {priority_class}">
                    <h3>#{idx}. {rec['activity']}</h3>
                    <p><strong>What to do:</strong> {rec['description']}</p>
                    <p><strong>Duration:</strong> {rec['duration']}</p>
                    <p><strong>Why:</strong> {rec['reason']}</p>
                    <p><strong>Confidence:</strong> {confidence_bar} {rec['confidence']}%</p>
                    <p style="font-size: 0.8rem; color: #888;">Rule: {rec['rule_fired']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show rules fired (Explainability)
            with st.expander("See Which Rules Were Fired (Explainability)"):
                rules_fired = [rec['rule_fired'] for rec in recommendations]
                st.write("**Rules that matched your situation:**")
                for rule in rules_fired:
                    st.write(f"- {rule}")
                
                st.info("**Explainability**: Each recommendation is based on specific rules derived from research. "
                    "You can trace exactly why each suggestion was made.")
            
            # Download recommendations
            df = pd.DataFrame(recommendations)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Recommendations as CSV",
                data=csv,
                file_name=f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
        else:
            st.warning("No specific recommendations matched your current state. You seem to be in a balanced condition!")
            st.info("General advice: Continue with your planned activities and maintain your current routine.")

# ============== TAB 2: NEW NATURAL LANGUAGE INTERFACE ==============
with tab2:
    st.markdown("### Natural Language Interface (LLM-Enhanced)")
    st.markdown("Describe your situation in your own words, and the AI will extract structured information for the Expert System.")
    
    # Import LLM parser
    from llm_parser import parse_natural_language, get_extraction_explanation
    
    # Example prompts
    with st.expander("Example Inputs"):
        st.markdown("""
        Try describing your situation naturally:
        
        - *"I only slept 4 hours last night, feeling exhausted, and I have a big exam tomorrow morning"*
        - *"Feeling pretty good today, got 8 hours of sleep, but I've been studying for 5 hours straight"*
        - *"I'm super stressed, haven't talked to anyone in 4 days, and I have three assignments due this week"*
        - *"Just woke up after a good night's sleep, it's 9 AM and I'm ready to tackle my hardest subject"*
        """)
    
    # Text input
    user_input = st.text_area(
        "Describe your current situation:",
        placeholder="E.g., I slept only 5 hours, feeling tired, have an exam in 2 days, and studied for 3 hours already...",
        height=100,
        key="nl_input"
    )
    
    # Process button
    if st.button("Get AI-Powered Recommendations", type="primary", use_container_width=True, key="nl_submit"):
        
        if not user_input.strip():
            st.warning("⚠️ Please describe your situation first!")
        else:
            with st.spinner("AI is analyzing your input and extracting information..."):
                # Parse with LLM
                result = parse_natural_language(user_input)
                
                if result['success']:
                    extracted_data = result['data']
                    
                    # Show what was extracted
                    st.success("✅ Successfully extracted information from your input!")
                    
                    with st.expander("View What AI Extracted from Your Input", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Your Input:**")
                            st.info(user_input)
                        
                        with col2:
                            st.markdown("**Extracted Information:**")
                            explanation = get_extraction_explanation(user_input, extracted_data)
                            for item in explanation:
                                st.markdown(f"- {item}")
                        
                        # Show full structured data
                        with st.expander("Full Structured Data (for Expert System)"):
                            st.json(extracted_data)
                    
                    st.markdown("---")
                    st.markdown("### Expert System Processing...")
                    
                    # Feed to expert system (same as widget interface!)
                    with st.spinner("Expert System is applying rules and generating recommendations..."):
                        recommendations, engine = run_expert_system(extracted_data)
                    
                    # Display results (SAME AS TAB 1)
                    st.markdown("## Your Personalized Recommendations")
                    
                    if recommendations:
                        rec_count = len(recommendations)
                        st.success(f"**Top Recommendation:** {recommendations[0]['activity']}")

                        # Analyze information completeness
                        info_analysis = {
                            'provided': [],
                            'assumed': []
                        }
                        
                        # Check what was extracted vs defaults
                        if extracted_data.get('sleep_hours', 7) != 7:
                            info_analysis['provided'].append(f"Sleep hours: {extracted_data['sleep_hours']}h")
                        else:
                            info_analysis['assumed'].append("Sleep hours: 7h (default)")
                        
                        if extracted_data.get('energy_level', 'Moderate') != 'Moderate':
                            info_analysis['provided'].append(f"Energy level: {extracted_data['energy_level']}")
                        else:
                            info_analysis['assumed'].append("Energy level: Moderate (default)")
                        
                        if extracted_data.get('stress_level', 'Moderate') != 'Moderate':
                            info_analysis['provided'].append(f"Stress level: {extracted_data['stress_level']}")
                        else:
                            info_analysis['assumed'].append("Stress level: Moderate (default)")
                        
                        if extracted_data.get('study_hours_today', 2) != 2:
                            info_analysis['provided'].append(f"Study hours: {extracted_data['study_hours_today']}h")
                        else:
                            info_analysis['assumed'].append("Study hours: 2h (default)")
                        
                        if extracted_data.get('deadline_urgency', 'None') != 'None':
                            info_analysis['provided'].append(f"Deadline: {extracted_data['deadline_urgency']}")
                        else:
                            info_analysis['assumed'].append("Deadline: None (default)")
                        
                        if extracted_data.get('break_taken', False):
                            info_analysis['provided'].append("Break taken: Yes")
                        else:
                            info_analysis['assumed'].append("Break taken: No (default)")
                        
                        if extracted_data.get('passive_learning_hours', 1) != 1:
                            info_analysis['provided'].append(f"Passive learning: {extracted_data['passive_learning_hours']}h")
                        else:
                            info_analysis['assumed'].append("Passive learning: 1h (default)")
                        
                        if extracted_data.get('task_complexity', 'Medium') != 'Medium':
                            info_analysis['provided'].append(f"Task complexity: {extracted_data['task_complexity']}")
                        else:
                            info_analysis['assumed'].append("Task complexity: Medium (default)")
                        
                        if extracted_data.get('sedentary_hours', 4) != 4:
                            info_analysis['provided'].append(f"Sedentary hours: {extracted_data['sedentary_hours']}h")
                        else:
                            info_analysis['assumed'].append("Sedentary hours: 4h (default)")
                        
                        if extracted_data.get('social_isolation_days', 1) != 1:
                            info_analysis['provided'].append(f"Social isolation: {extracted_data['social_isolation_days']} days")
                        else:
                            info_analysis['assumed'].append("Social isolation: 1 day (default)")
                        
                        if extracted_data.get('cramming', False):
                            info_analysis['provided'].append("Cramming: Yes")
                        else:
                            info_analysis['assumed'].append("Cramming: No (default)")
                        
                        # Display information completeness
                        assumptions_count = len(info_analysis['assumed'])
                        
                        if assumptions_count > 0:
                            with st.expander(f"View Information Completeness Analysis ({assumptions_count} assumptions made)", expanded=False):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("### Information Extracted")
                                    for item in info_analysis['provided']:
                                        st.markdown(f"- {item}")
                                
                                with col2:
                                    st.markdown("### Assumptions Made")
                                    for item in info_analysis['assumed']:
                                        st.markdown(f"- {item}")
                                
                                st.markdown("---")
                                
                                total_fields = len(info_analysis['provided']) + len(info_analysis['assumed'])
                                completeness = (len(info_analysis['provided']) / total_fields) * 100
                                
                                st.metric("Information Completeness", f"{completeness:.0f}%")
                                
                                st.markdown(f"""
                                **ES Feature: Incomplete Information Handling**
                                
                                The expert system processed your natural language with **{assumptions_count} missing/default fields** by:
                                
                                1. ✅ **AI extraction** - LLM extracted what it could
                                2. ✅ **Conservative assumptions** - Used defaults for missing info
                                3. ✅ **Confidence adjustment** - Reduced confidence appropriately
                                4. ✅ **Useful recommendations** - Still provides guidance
                                
                                *Tip: Mentioning more details increases accuracy!*
                                """)
                        else:
                            with st.expander("View Information Completeness Analysis (100% complete)", expanded=False):
                                st.success("""
                                **100% Information Completeness!**
                                
                                The AI extracted all necessary fields!
                                
                                **Information Extracted:**
                                """)
                                for item in info_analysis['provided']:
                                    st.markdown(f"- {item}")
                        
                        metric_cols = st.columns(3)
                        with metric_cols[0]:
                            st.metric("Alternatives", rec_count, help="Different activity options")
                        with metric_cols[1]:
                            avg_conf = sum(r['confidence'] for r in recommendations) / len(recommendations)
                            st.metric("Avg Confidence", f"{avg_conf:.0f}%", help="Average confidence level")
                        with metric_cols[2]:
                            rules = len(set(r['rule_fired'] for r in recommendations))
                            st.metric("Rules Fired", rules, help="Expert rules applied")
                        
                        st.markdown("---")

                        # Display recommendations (reuse your existing code)
                        for idx, rec in enumerate(recommendations, 1):
                            priority_class = f"priority-{rec['priority']}"
                            confidence_bar = "🟢" * int(rec['confidence'] / 20)
                            
                            st.markdown(f"""
                            <div class="recommendation-box {priority_class}">
                                <h3>#{idx}. {rec['activity']}</h3>
                                <p><strong>What to do:</strong> {rec['description']}</p>
                                <p><strong>Duration:</strong> {rec['duration']}</p>
                                <p><strong>Why:</strong> {rec['reason']}</p>
                                <p><strong>Confidence:</strong> {confidence_bar} {rec['confidence']}%</p>
                                <p style="font-size: 0.8rem; color: #888;">Rule: {rec['rule_fired']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Explainability section
                        with st.expander("See Which Rules Were Fired (Explainability)"):
                            rules_fired = [rec['rule_fired'] for rec in recommendations]
                            st.write("**Rules that matched your situation:**")
                            for rule in rules_fired:
                                st.write(f"- {rule}")
                            
                            st.info("**Full Explainability Maintained**: Even with AI input parsing, "
                                   "all recommendations trace back to explicit expert system rules. "
                                   "No black-box decisions!")
                    else:
                        st.info("No specific recommendations matched. You seem to be in good balance!")
                
                else:
                    st.error(f"Error processing input: {result['error']}")
                    st.info("Please check your API key is set correctly in .env file")



# Footer with ES features demonstration
st.markdown("---")
st.markdown("### Expert System Features Demonstrated")

st.markdown("""
This system demonstrates all 8 key characteristics of expert systems:
""")

# First row
feature_cols1 = st.columns(4)

with feature_cols1[0]:
    st.markdown("**Narrow Domain**")
    st.caption("Student daily activities only")

with feature_cols1[1]:
    st.markdown("**Question-Driven**")
    st.caption("Widgets OR natural language")

with feature_cols1[2]:
    st.markdown("**Incomplete Info**")
    st.caption("Works with missing data")

with feature_cols1[3]:
    st.markdown("**Alternative Solutions**")
    st.caption("Multiple ranked options")

# Second row
feature_cols2 = st.columns(4)

with feature_cols2[0]:
    st.markdown("**Confidence Levels**")
    st.caption("70-90% evidence-based")

with feature_cols2[1]:
    st.markdown("**Recommendations**")
    st.caption("Suggests, not commands")

with feature_cols2[2]:
    st.markdown("**Heuristics**")
    st.caption("Research + experience")

with feature_cols2[3]:
    st.markdown("**Explainability**")
    st.caption("Shows which rules fired")

# About section
with st.sidebar:
    st.markdown("---")
    st.markdown("### About This System")
    st.info("""
    **Daily Activity Recommendation System**
    
    An expert system that helps students make better daily decisions about:
    - Study timing
    - Rest and breaks
    - Exercise and wellness
    - Social activities
    
    **Built with:**
    - Experta (Rule-based reasoning)
    - Streamlit (User interface)
    - 25 research-backed rules
    """)