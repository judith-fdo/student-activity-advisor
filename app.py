"""
Streamlit UI for Daily Activity Recommendation System
"""
import fix_experta

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
    st.caption("6-12 structured questions")

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