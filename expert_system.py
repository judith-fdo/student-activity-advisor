"""
Daily Activity Recommendation Expert System
Using Experta for rule-based reasoning
"""
import fix_experta

from experta import *
from datetime import datetime

# Define Facts
class StudentState(Fact):
    """Represents the current state of the student"""
    pass

class Recommendation(Fact):
    """Represents a recommendation with confidence"""
    pass

# Main Expert System
class ActivityAdvisorES(KnowledgeEngine):
    
    def __init__(self):
        super().__init__()
        self.recommendations = []
        
    @DefFacts()
    def initial_facts(self):
        """Initialize with timestamp"""
        yield Fact(system_start=True)
    
    # ==================== CATEGORY 1: SLEEP RULES ====================
    
    @Rule(
        StudentState(sleep_hours=MATCH.sleep),
        TEST(lambda sleep: sleep < 5),
        StudentState(deadline_urgency=MATCH.deadline)
    )
    def critical_sleep_deficit(self, sleep, deadline):
        """
        Rule 1: Critical Sleep Deficit
        Source: Pilcher & Huffcutt (1996), Curcio et al. (2006)
        """
        self.declare(Recommendation(
            activity="Rest Priority",
            description=f"Take a 30-90 minute rest/nap before studying",
            confidence=90,
            reason=f"Critical sleep deficit detected ({sleep}h). Research shows severe "
                   f"cognitive impairment below 5 hours. Rest will improve study efficiency "
                   f"even with deadline pressure.",
            priority=1,
            duration="30-90 minutes",
            category="rest",
            rule_fired="R1_CRITICAL_SLEEP_DEFICIT"
        ))
    
    @Rule(
        StudentState(sleep_hours=MATCH.sleep),
        TEST(lambda sleep: 5 <= sleep < 6.5),
        StudentState(energy_level=L("Low") | L("Very Low"))
    )
    def moderate_sleep_deficit(self, sleep):
        """
        Rule 2: Moderate Sleep Deficit
        Source: Lim & Dinges (2010)
        """
        self.declare(Recommendation(
            activity="Short Rest",
            description="Take a 30-60 minute rest before demanding tasks",
            confidence=75,
            reason=f"Moderate sleep deficit ({sleep}h) with low energy. "
                   f"Short rest can help recover cognitive capacity.",
            priority=2,
            duration="30-60 minutes",
            category="rest",
            rule_fired="R2_MODERATE_SLEEP_DEFICIT"
        ))
    
    @Rule(
        StudentState(sleep_hours=MATCH.sleep),
        TEST(lambda sleep: sleep < 6.5),
        StudentState(current_time=MATCH.time),
        TEST(lambda time: 13 <= time < 16)
    )
    def power_nap_recommendation(self, sleep, time):
        """
        Rule 3: Power Nap Effectiveness
        Source: Mednick et al. (2003)
        """
        self.declare(Recommendation(
            activity="Power Nap",
            description="Take a 20-30 minute power nap",
            confidence=85,
            reason=f"Sleep deficit with afternoon timing (current time: {time}:00). "
                   f"Short naps improve alertness for 2-3 hours without disrupting night sleep.",
            priority=1,
            duration="20-30 minutes",
            category="rest",
            rule_fired="R3_POWER_NAP"
        ))
    
    @Rule(
        StudentState(sleep_hours=MATCH.sleep),
        TEST(lambda sleep: sleep >= 7),
        StudentState(energy_level=L("High") | L("Moderate"))
    )
    def adequate_sleep_state(self, sleep):
        """
        Rule 4: Adequate Sleep - Optimal for Challenging Tasks
        Source: National Sleep Foundation (2015)
        """
        self.declare(Recommendation(
            activity="Challenging Study",
            description="Tackle your most difficult subjects/topics now",
            confidence=85,
            reason=f"Well-rested state ({sleep}h sleep) with good energy. "
                   f"Optimal conditions for cognitively demanding tasks.",
            priority=1,
            duration="60-90 minutes",
            category="study",
            rule_fired="R4_ADEQUATE_SLEEP"
        ))
    
    # ==================== CATEGORY 2: STUDY DURATION & BREAKS ====================
    
    @Rule(
        StudentState(study_hours_today=MATCH.hours),
        TEST(lambda hours: hours >= 4),
        StudentState(break_taken=False)
    )
    def mandatory_break_rule(self, hours):
        """
        Rule 5: Maximum Continuous Study
        Source: Ariga & Lleras (2011), Ericsson et al. (1993)
        """
        self.declare(Recommendation(
            activity="Mandatory Break",
            description="Take a 15-30 minute break immediately",
            confidence=80,
            reason=f"You've studied {hours} hours today without a substantial break. "
                   f"Attention and cognitive performance decline after 4 hours continuous work.",
            priority=1,
            duration="15-30 minutes",
            category="break",
            rule_fired="R5_MANDATORY_BREAK"
        ))
    
    @Rule(
        StudentState(study_hours_today=MATCH.hours),
        TEST(lambda hours: hours > 6),
        StudentState(stress_level=L("High") | L("Very High"))
    )
    def study_overload_detection(self, hours):
        """
        Rule 15: High Stress with Excessive Study
        Source: Schneiderman et al. (2005)
        """
        self.declare(Recommendation(
            activity="Stress Reduction",
            description="Stop studying and do a stress-reduction activity",
            confidence=80,
            reason=f"Very high study hours ({hours}h) combined with high stress. "
                   f"Continuing will be counterproductive. Take a real break.",
            priority=1,
            duration="30-60 minutes",
            category="wellness",
            rule_fired="R15_HIGH_STRESS"
        ))
    
    @Rule(
        StudentState(cramming=True)
    )
    def anti_cramming_rule(self):
        """
        Rule 7: Discourage Cramming
        Source: Cepeda et al. (2006), Kelley & Whatson (2013)
        """
        self.declare(Recommendation(
            activity="Distributed Practice",
            description="Break your study into multiple shorter sessions over time",
            confidence=90,
            reason="Cramming (massed practice) is significantly less effective than "
                   "distributed practice. Plan to study in spaced intervals.",
            priority=2,
            duration="Multiple sessions",
            category="study_strategy",
            rule_fired="R7_ANTI_CRAMMING"
        ))
    
    # ==================== CATEGORY 3: TIME OF DAY ====================
    
    @Rule(
        StudentState(current_time=MATCH.time),
        TEST(lambda time: 9 <= time < 12),
        StudentState(energy_level=L("Moderate") | L("High")),
        StudentState(sleep_hours=MATCH.sleep),
        TEST(lambda sleep: sleep >= 6)
    )
    def morning_peak_rule(self, time):
        """
        Rule 9: Morning Cognitive Peak
        Source: Schmidt et al. (2007)
        """
        self.declare(Recommendation(
            activity="Challenging Study",
            description="Focus on your most difficult subjects during morning hours",
            confidence=75,
            reason=f"Morning time ({time}:00) with adequate rest and energy. "
                   f"Most people show peak cognitive performance in late morning.",
            priority=1,
            duration="90-120 minutes",
            category="study",
            rule_fired="R9_MORNING_PEAK"
        ))
    
    @Rule(
        StudentState(current_time=MATCH.time),
        TEST(lambda time: time >= 22),
        StudentState(sleep_hours=MATCH.sleep),
        TEST(lambda sleep: sleep < 7)
    )
    def late_evening_stop_rule(self, time, sleep):
        """
        Rule 11: Evening Study Caution
        Source: Czeisler et al. (1999), NSF guidelines
        """
        self.declare(Recommendation(
            activity="Prepare for Sleep",
            description="Stop studying and prepare for bed",
            confidence=80,
            reason=f"Late evening ({time}:00) with existing sleep debt ({sleep}h previous night). "
                   f"Sleep should be prioritized over late-night studying.",
            priority=1,
            duration="Begin sleep routine",
            category="rest",
            rule_fired="R11_EVENING_STOP"
        ))
    
    # ==================== CATEGORY 4: ENERGY & COGNITIVE LOAD ====================
    
    @Rule(
        StudentState(energy_level="Very Low"),
        StudentState(task_complexity="High")
    )
    def low_energy_complex_task_rule(self):
        """
        Rule 12: Low Energy + Complex Task Mismatch
        Source: Sweller (1988), Kahneman (2011)
        """
        self.declare(Recommendation(
            activity="Rest or Switch Task",
            description="Either rest, or switch to simpler tasks (review notes, organize)",
            confidence=85,
            reason="Very low energy with high complexity task. Cognitive load theory "
                   "indicates this will be ineffective. Rest or simplify tasks.",
            priority=1,
            duration="20-30 min rest OR switch tasks",
            category="rest",
            rule_fired="R12_ENERGY_TASK_MISMATCH"
        ))
    
    @Rule(
        StudentState(energy_level="High"),
        StudentState(sleep_hours=MATCH.sleep),
        TEST(lambda sleep: sleep >= 7)
    )
    def high_energy_utilization_rule(self):
        """
        Rule 14: High Energy Utilization
        Source: Baumeister et al. (1998)
        """
        self.declare(Recommendation(
            activity="Tackle Hardest Tasks",
            description="Use this high-energy state for your most challenging work",
            confidence=80,
            reason="High energy with good sleep. Cognitive resources are at peak. "
                   "Tackle the most demanding tasks before resources deplete.",
            priority=1,
            duration="90-120 minutes",
            category="study",
            rule_fired="R14_HIGH_ENERGY_USE"
        ))
    
    # ==================== CATEGORY 5: STRESS & MENTAL HEALTH ====================
    
    @Rule(
        StudentState(social_isolation_days=MATCH.days),
        TEST(lambda days: days > 3),
        StudentState(stress_level=L("Moderate") | L("High") | L("Very High"))
    )
    def social_isolation_rule(self, days):
        """
        Rule 16: Social Isolation Red Flag
        Source: Cacioppo & Patrick (2008)
        """
        self.declare(Recommendation(
            activity="Social Activity",
            description="Connect with friends - study group, meal together, or casual hangout",
            confidence=75,
            reason=f"You haven't had social interaction in {days} days with elevated stress. "
                   f"Social connection buffers stress and improves well-being.",
            priority=2,
            duration="1-2 hours",
            category="social",
            rule_fired="R16_SOCIAL_ISOLATION"
        ))
    
    # ==================== CATEGORY 6: PHYSICAL ACTIVITY ====================
    
    @Rule(
        StudentState(energy_level="Low"),
        StudentState(sleep_hours=MATCH.sleep),
        TEST(lambda sleep: sleep >= 6),
        StudentState(sedentary_hours=MATCH.sed),
        TEST(lambda sed: sed > 4)
    )
    def exercise_for_energy_rule(self, sed):
        """
        Rule 18: Exercise for Focus
        Source: Hillman et al. (2008)
        """
        self.declare(Recommendation(
            activity="Light Exercise",
            description="Take a 10-20 minute walk or do light stretching",
            confidence=80,
            reason=f"Low energy but adequate sleep with {sed}h sedentary time. "
                   f"Light physical activity can boost alertness and focus.",
            priority=2,
            duration="10-20 minutes",
            category="exercise",
            rule_fired="R18_EXERCISE_BOOST"
        ))
    
    # ==================== CATEGORY 7: DEADLINE MANAGEMENT ====================
    
    @Rule(
        StudentState(deadline_urgency="Urgent"),  # Within 24h
        StudentState(sleep_hours=MATCH.sleep),
        TEST(lambda sleep: sleep >= 6),
        StudentState(energy_level=L("Moderate") | L("High"))
    )
    def urgent_deadline_good_state_rule(self):
        """
        Rule 20: Urgent Deadline + Good State
        Source: Steel (2007), Cirillo (2006)
        """
        self.declare(Recommendation(
            activity="Focused Study Session",
            description="Use Pomodoro technique: 25 min focused work + 5 min breaks",
            confidence=80,
            reason="Urgent deadline with adequate rest and energy. "
                   "You're in good condition for productive focused work.",
            priority=1,
            duration="Multiple 25-min sessions",
            category="study",
            rule_fired="R20_URGENT_GOOD_STATE"
        ))
    
    @Rule(
        StudentState(deadline_urgency="Urgent"),  # Within 24h
        StudentState(sleep_hours=MATCH.sleep),
        TEST(lambda sleep: sleep < 5)
    )
    def urgent_deadline_poor_state_rule(self, sleep):
        """
        Rule 21: Urgent Deadline + Poor State
        Source: Pilcher & Huffcutt (1996), Mednick et al. (2003)
        """
        self.declare(Recommendation(
            activity="Strategic Rest Then Study",
            description="Take 20-30 min power nap, THEN study",
            confidence=75,
            reason=f"Urgent deadline but severe sleep deficit ({sleep}h). "
                   f"Even with time pressure, short rest will improve efficiency more than tired studying.",
            priority=1,
            duration="20-30 min nap + focused study",
            category="rest",
            rule_fired="R21_URGENT_POOR_STATE"
        ))
    
    # ==================== CATEGORY 8: TASK VARIETY ====================
    
    @Rule(
        StudentState(passive_learning_hours=MATCH.hours),
        TEST(lambda hours: hours > 2)
    )
    def active_learning_rule(self, hours):
        """
        Rule 24: Active vs Passive Learning
        Source: Freeman et al. (2014), Chi & Wylie (2014)
        """
        self.declare(Recommendation(
            activity="Active Learning",
            description="Switch to active learning: practice problems, teach concept, or write summary",
            confidence=85,
            reason=f"You've done {hours}h of passive learning (reading/watching). "
                   f"Research shows active learning is significantly more effective.",
            priority=2,
            duration="30-60 minutes",
            category="study_strategy",
            rule_fired="R24_ACTIVE_LEARNING"
        ))
    
    # ==================== GET RECOMMENDATIONS ====================
    
    def get_recommendations(self):
        """Extract all recommendations sorted by priority and confidence"""
        recommendations = []
        for fact in self.facts.values():
            if isinstance(fact, Recommendation):
                recommendations.append({
                    'activity': fact.get('activity'),
                    'description': fact.get('description'),
                    'confidence': fact.get('confidence'),
                    'reason': fact.get('reason'),
                    'priority': fact.get('priority'),
                    'duration': fact.get('duration'),
                    'category': fact.get('category'),
                    'rule_fired': fact.get('rule_fired')
                })
        
        # Sort by priority (lower number = higher priority), then by confidence
        recommendations.sort(key=lambda x: (x['priority'], -x['confidence']))
        
        return recommendations


def run_expert_system(user_inputs):
    """
    Run the expert system with user inputs
    
    Args:
        user_inputs: Dictionary containing student state information
    
    Returns:
        List of recommendations sorted by priority
    """
    # Create and reset the engine
    engine = ActivityAdvisorES()
    engine.reset()
    
    # Declare the student state facts
    engine.declare(StudentState(**user_inputs))
    
    # Run the inference engine
    engine.run()
    
    # Get recommendations
    recommendations = engine.get_recommendations()
    
    return recommendations, engine