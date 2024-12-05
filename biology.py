import streamlit as st
import csv
from datetime import datetime

# Set page config for responsiveness
st.set_page_config(page_title="Biologie Quiz App", layout="centered")

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered_questions' not in st.session_state:
    st.session_state.answered_questions = set()
if 'submitted_answers' not in st.session_state:
    st.session_state.submitted_answers = {}
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'reset' not in st.session_state:
    st.session_state.reset = False

# Multiple-choice questions
mc_questions = [
    {
        "question": "Zu welcher Tiergruppe gehören Schnecken?",
        "choices": ["Wirbeltiere", "Gliederfüßer", "Weichtiere", "Säugetiere"],
        "correct": ["Weichtiere"],
        "hint": "Sie haben keine Knochen, aber oft ein Gehäuse.",
        "explanation": "Schnecken gehören zu den Weichtieren, da sie keinen festen Körperbau wie Wirbeltiere haben."
    },
    {
        "question": "Was ist die Hauptfunktion des Schneckenhauses?",
        "choices": [
            "Es dient der Tarnung.",
            "Es schützt die Schnecke vor Feinden.",
            "Es hilft der Schnecke, schneller zu kriechen.",
            "Es speichert Wasser."
        ],
        "correct": ["Es schützt die Schnecke vor Feinden."],
        "hint": "Denke an Feinde der Schnecke und Schutzmechanismen.",
        "explanation": "Das Schneckenhaus schützt die Schnecke vor Fressfeinden und Umwelteinflüssen."
    },
    {
        "question": "Wie viele Beine haben Insekten?",
        "choices": ["6", "8", "10", "12"],
        "correct": ["6"],
        "hint": "Zähle die Beine einer Ameise oder einer Biene.",
        "explanation": "Insekten haben immer 6 Beine."
    },
    {
        "question": "Warum sind Honigbienen für uns Menschen so wichtig?",
        "choices": [
            "Sie produzieren Honig.",
            "Sie bestäuben viele Pflanzen.",
            "Sie bekämpfen Schädlinge.",
            "Sie halten den Boden fruchtbar."
        ],
        "correct": ["Sie produzieren Honig.", "Sie bestäuben viele Pflanzen."],
        "hint": "Denke an ihre Rolle in der Natur und für den Menschen.",
        "explanation": "Honigbienen produzieren nicht nur Honig, sondern sind auch entscheidend für die Bestäubung von Pflanzen."
    },
    {
    "question": "Wie kommunizieren Honigbienen miteinander?",
    "choices": [
        "Durch Summen unterschiedlicher Frequenzen.",
        "Durch Tänze, die die Richtung und Entfernung von Futterquellen anzeigen.",
        "Durch das Versprühen von Düften.",
        "Durch das Klopfen mit den Beinen auf die Waben."
    ],
    "correct": [
        "Durch Tänze, die die Richtung und Entfernung von Futterquellen anzeigen.",
        "Durch das Versprühen von Düften."
    ],
    "hint": "Denke an ihren Schwänzeltanz und die Rolle von Pheromonen.",
    "explanation": "Honigbienen nutzen den Schwänzeltanz, um die Richtung und Entfernung von Futterquellen mitzuteilen, und Pheromone, um chemisch zu kommunizieren."
}, 
{
    "question": "Wie geben Honigbienen die Richtung zu einer Futterquelle weiter?",
    "choices": [
        "Durch Summen in unterschiedlichen Tönen.",
        "Durch einen Tanz, der die Richtung zeigt.",
        "Durch das Sprühen von Duftstoffen.",
        "Durch das Klopfen auf die Waben."
    ],
    "correct": ["Durch einen Tanz, der die Richtung zeigt."],
    "hint": "Überlege, wie der berühmte 'Schwänzeltanz' der Bienen funktioniert.",
    "explanation": "Honigbienen zeigen die Richtung einer Futterquelle durch ihren Schwänzeltanz. Die Richtung des Tanzes in Bezug auf die Sonne weist auf die Flugrichtung hin."
},
{
    "question": "Was sind die Hauptkörperteile von Insekten?",
    "choices": ["Kopf, Brust, Hinterleib", "Kopf, Flügel, Beine", "Kopf, Thorax, Abdomen", "Kopf, Panzer, Schwanz"],
    "correct": ["Kopf, Brust, Hinterleib", "Kopf, Thorax, Abdomen"],
    "hint": "Thorax und Brust sind synonym, ebenso Abdomen und Hinterleib.",
    "explanation": "Insekten haben drei Hauptkörperteile: Kopf, Brust (Thorax) und Hinterleib (Abdomen)."
},
{
    "question": "Welche Funktion haben die Mundwerkzeuge von Gliederfüßern?",
    "choices": [
        "Sie dienen zur Verteidigung.",
        "Sie werden zum Zerkleinern von Nahrung genutzt.",
        "Sie helfen bei der Fortbewegung.",
        "Sie werden zur Paarung verwendet."
    ],
    "correct": ["Sie dienen zur Verteidigung.", "Sie werden zum Zerkleinern von Nahrung genutzt."],
    "hint": "Überlege, wie Gliederfüßer ihre Nahrung aufnehmen und sich gegen Feinde schützen.",
    "explanation": "Die Mundwerkzeuge von Gliederfüßern dienen dazu, Nahrung zu zerkleinern und können auch zur Verteidigung eingesetzt werden."
},
{
    "question": "Wo bauen rote Waldameisen ihre Nester?",
    "choices": [
        "In hohlen Baumstämmen.",
        "In Erdhügeln aus Erde und Pflanzenteilen.",
        "In alten Vogelnestern.",
        "Unter Steinen."
    ],
    "correct": ["In Erdhügeln aus Erde und Pflanzenteilen."],
    "hint": "Achte auf typische Ameisenhügel in Wäldern.",
    "explanation": "Rote Waldameisen bauen ihre Nester aus Erde und Pflanzenteilen, die sie zu großen Hügeln formen."
},{
    "question": "Wie schützt sich die rote Waldameise vor Feinden?",
    "choices": [
        "Sie beißt mit ihren Mundwerkzeugen.",
        "Sie sprüht Ameisensäure.",
        "Sie versteckt sich im Ameisenhaufen.",
        "Sie flieht vor Angreifern."
    ],
    "correct": [
        "Sie beißt mit ihren Mundwerkzeugen.",
        "Sie sprüht Ameisensäure."
    ],
    "hint": "Denke daran, dass Ameisensäure ein bekanntes Verteidigungsmittel ist.",
    "explanation": "Rote Waldameisen verteidigen sich durch kräftige Bisse und das Sprühen von Ameisensäure, die Angreifer abwehren kann."
},{
    "question": "Was fressen rote Waldameisen hauptsächlich?",
    "choices": [
        "Blätter und Samen.",
        "Kleine Insekten und Aas.",
        "Honigtau von Blattläusen.",
        "Holz."
    ],
    "correct": [
        "Kleine Insekten und Aas.",
        "Honigtau von Blattläusen."
    ],
    "hint": "Überlege, warum Ameisen oft in der Nähe von Blattläusen sind.",
    "explanation": "Rote Waldameisen ernähren sich von kleinen Insekten, Aas und dem süßen Honigtau, den Blattläuse absondern."
},
{
    "question": "Welche Aufgabe hat die Königin in einem Ameisenstaat?",
    "choices": [
        "Sie legt Eier.",
        "Sie sucht Nahrung.",
        "Sie verteidigt den Bau.",
        "Sie baut den Ameisenhaufen."
    ],
    "correct": ["Sie legt Eier."],
    "hint": "Die Königin hat eine spezielle Rolle im Ameisenstaat.",
    "explanation": "Die Hauptaufgabe der Königin ist die Fortpflanzung, indem sie Eier legt."
}
]

# Open-ended questions
text_questions = [
    {
        "question": "Beschreibe, wie sich Schnecken fortbewegen.",
        "type": "text",
        "points": 3,
        "key_phrases": [
            "muskulöser fuß",
            "gleiten",
            "schleim",
            "wellenförmig"
        ],
        "hint": "Denke an die Bewegung ihres Fußes und die Rolle des Schleims.",
        "explanation": "Schnecken bewegen sich mit einem muskulösen Fuß, der wellenförmig arbeitet. Sie scheiden Schleim aus, der das Gleiten erleichtert."
    },
    {
        "question": "Warum bauen Honigbienen Waben, und wie nutzen sie diese?",
        "type": "text",
        "points": 3,
        "key_phrases": [
            "honig",
            "larven",
            "schutz",
            "struktur",
            "stabilität"
        ],
        "hint": "Überlege, wofür Honigbienen die Waben brauchen.",
        "explanation": "Honigbienen bauen Waben, um Honig zu lagern und ihre Larven zu schützen. Die Waben bieten Stabilität und Schutz im Bau."
    },
    {
    "question": "Beschreibe den Unterschied zwischen Wirbeltieren und Wirbellosen.",
    "type": "text",
    "points": 3,
    "key_phrases": ["skelett", "wirbelsäule", "organe", "komplex", "keine knochen"],
    "hint": "Denke an das Skelett und die Organstrukturen.",
    "explanation": "Wirbeltiere haben ein Skelett mit einer Wirbelsäule, während Wirbellose keine Wirbelsäule haben. Sie besitzen oft komplexere Organe."
},
{
    "question": "Wie hilft die rote Waldameise dem Wald?",
    "type": "text",
    "points": 3,
    "key_phrases": ["säubern", "aas", "pﬂanzensamen", "schädlinge", "wald"],
    "hint": "Denke an die Aufgaben der Ameisen im Wald.",
    "explanation": "Rote Waldameisen säubern den Wald von Aas, verteilen Pflanzensamen und bekämpfen Schädlinge, wodurch sie das Ökosystem stabilisieren."
}
]

# Logging functionality
def log_performance(student_name, score, total_questions):
    log_file = "bio_quiz_performance.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, student_name, score, total_questions])

# Function to check text-based answers
def check_text_answer(answer, key_phrases, min_matches=2):
    answer = answer.lower()
    matches = [phrase for phrase in key_phrases if phrase in answer]
    score = len(matches) >= min_matches
    
    if score:
        feedback = "Sehr gut! Deine Antwort enthält wichtige Schlüsselbegriffe."
    else:
        feedback = f"Deine Antwort könnte vollständiger sein. Wichtige Begriffe wären z.B.: {', '.join(key_phrases[:3])}..."
    
    return score, feedback

# Reset quiz
def reset_quiz():
    st.session_state.score = 0
    st.session_state.answered_questions = set()
    st.session_state.submitted_answers = {}
    st.session_state.reset = True

# Streamlit App
st.title("Biologie Quiz App")
st.write("Teste dein Wissen über Weichtiere, Insekten, Ameisen und Honigbienen!")

# Name input
student_name = st.text_input("Dein Name:", value=st.session_state.name)
st.session_state.name = student_name

if not student_name:
    st.warning("Bitte gib deinen Namen ein, bevor du fortfährst.")
else:
    # Multiple-choice questions
    for i, q in enumerate(mc_questions):
        st.subheader(f"Frage {i+1}: {q['question']}")
        selected = st.multiselect("Wähle die richtige(n) Antwort(en):", q['choices'], key=f"q{i}")
        if st.button(f"Antwort bestätigen für Frage {i+1}", key=f"confirm_{i}"):
            if set(selected) == set(q['correct']):
                st.success("Richtig!")
                st.session_state.score += 2
            else:
                st.error(f"Falsch! Hinweis: {q['hint']}")
                st.info(f"Richtige Antwort(en): {', '.join(q['correct'])}")
                st.write(f"**Erklärung:** {q['explanation']}")

    # Open-ended questions
    for i, q in enumerate(text_questions):
        st.subheader(f"Frage {len(mc_questions) + i + 1}: {q['question']}")
        answer = st.text_area("Deine Antwort:", key=f"text_{i}")
        if st.button(f"Antwort überprüfen für Frage {len(mc_questions) + i + 1}", key=f"text_confirm_{i}"):
            if answer:
                score, feedback = check_text_answer(answer, q['key_phrases'])
                if score:
                    st.success(feedback)
                    st.session_state.score += q['points']
                else:
                    st.error(feedback)
                    st.info(f"Tipp: {q['hint']}")
                    st.write(f"**Erklärung:** {q['explanation']}")
            else:
                st.warning("Bitte gib eine Antwort ein.")

    # Results
    if st.button("Ergebnis anzeigen"):
        total_points = len(mc_questions) * 2 + sum(q['points'] for q in text_questions)
        st.write(f"**Dein Gesamtergebnis: {st.session_state.score} von {total_points} Punkten**")
        log_performance(student_name, st.session_state.score, total_points)
        if st.session_state.score == total_points:
            st.balloons()
            st.success("Hervorragend! Du hast alle Fragen richtig beantwortet!")
        elif st.session_state.score > total_points // 2:
            st.info("Gut gemacht, aber du kannst noch besser werden!")
        else:
            st.warning("Übe noch ein wenig weiter!")

    # Reset
    if st.button("Quiz zurücksetzen"):
        reset_quiz()
