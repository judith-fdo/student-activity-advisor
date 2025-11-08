# Daily Activity Recommendation System for Students

An intelligent expert system that helps students make better daily decisions about study timing, rest, exercise, and social activities using rule-based reasoning.

## Overview

This expert system was developed as part of the **CM3610 - Expert Systems** course at the University of Moratuwa. It demonstrates all 8 key characteristics of expert systems while addressing the real-world problem of student time management and wellness.

## Features

The system demonstrates **all 8 expert system characteristics**:

1. **Narrow Domain** - Focuses exclusively on student daily activity decisions
2. **Question-Driven** - Asks 6-12 structured questions to assess student state
3. **Handles Incomplete Information** - Works even with missing data using conservative assumptions
4. **Provides Alternative Solutions** - Offers multiple ranked recommendations
5. **Confidence Levels** - Each recommendation includes 70-90% evidence-based confidence
6. **Recommendations Over Commands** - Suggests rather than prescribes actions
7. **Uses Heuristics** - Combines research findings with expert experience
8. **Explainable** - Shows which rules fired and why each recommendation was made

## Technology Stack

- **Expert System Engine**: Experta (Python rule-based reasoning library)
- **User Interface**: Streamlit (Interactive web application)
- **Knowledge Base**: 25 research-backed rules from cognitive psychology and student wellness studies
- **Python Version**: 3.10+

## Knowledge Base

The system's 25 rules are derived from peer-reviewed research including:

- Sleep-cognition studies (Pilcher & Huffcutt 1996, Mednick et al. 2003)
- Study effectiveness research (Ariga & Lleras 2011, Cepeda et al. 2006)
- Cognitive load theory (Sweller 1988)
- Professional guidelines (WHO, APA, National Sleep Foundation)

## Installation & Usage

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/judith-fdo/student-activity-advisor.git
cd student-activity-advisor
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open in browser**
The app will automatically open at `http://localhost:8501`

## 📁 Project Structure
```
student-activity-advisor/
│
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
├── REFERENCES.md           # Complete academic citations (33 sources)
├── requirements.txt        # Python dependencies
│
├── fix_experta.py          # Python 3.10+ compatibility patch
├── expert_system.py        # Core expert system logic (25 rules)
└── app.py                  # Streamlit user interface
```

## System Architecture
```
User Input → Streamlit UI → Expert System (Experta) → Rule Matching → Recommendations
                                      ↓
                              Knowledge Base (25 Rules)
                                      ↓
                              Evidence Sources (Research)
```

## Use Cases

The system helps students with:

- **Sleep-deprived exam preparation** - Recommends strategic rest over exhausted studying
- **Morning productivity planning** - Suggests challenging tasks during cognitive peak hours
- **Study break optimization** - Prevents burnout with evidence-based break recommendations
- **Deadline pressure management** - Balances urgency with physiological needs
- **Stress and wellness** - Detects social isolation and recommends connection


## Example Scenarios

### Scenario 1: Sleep-Deprived with Urgent Deadline
**Input:**
- Sleep: 4 hours
- Energy: Very Low
- Deadline: Within 24 hours

**Output:**
- Top Recommendation: 30-minute power nap (90% confidence)
- Reason: Even with deadline pressure, short rest improves efficiency more than tired studying
- Rules Fired: R1_CRITICAL_SLEEP_DEFICIT, R3_POWER_NAP

### Scenario 2: Well-Rested Morning Student
**Input:**
- Sleep: 8 hours
- Energy: High
- Time: 10 AM

**Output:**
- Top Recommendation: Tackle most challenging subjects (85% confidence)
- Reason: Peak cognitive performance with adequate rest
- Rules Fired: R4_ADEQUATE_SLEEP, R9_MORNING_PEAK

## Expert System Features Demonstration

| Feature | Implementation |
|---------|----------------|
| Narrow Domain | Only student daily activities (not career, finance, etc.) |
| Question-Driven | 6 core questions + 6 optional detailed questions |
| Incomplete Info | Uses defaults, reduces confidence appropriately |
| Alternatives | Provides 1-5 ranked recommendations per scenario |
| Confidence | 70-90% based on research strength and data completeness |
| Recommendations | "Consider...", "Recommended..." language (not commands) |
| Heuristics | Rules from research + counselor experience |
| Explainability | Shows all rules fired with reasoning trace |

## References

**[Complete reference list with 33 academic sources](REFERENCES.md)**

## Contributing

This is an academic project. Suggestions and feedback are welcome!

## License

This project is developed for academic purposes.

## Author

**Judith Fernando**  
University of Moratuwa

## Acknowledgments

- Research papers and professional guidelines that informed the knowledge base
- Course instructors for guidance on expert system principles
- Streamlit and Experta communities for excellent documentation

---

**Note**: This system provides educational guidance based on general research. Always consult academic advisors or healthcare professionals for personalized advice.