import streamlit as st
import csv
from datetime import datetime

# Set page config for responsiveness
st.set_page_config(page_title="Physik Quiz App", layout="centered")

# Initialize session state for all variables we need to track
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

# Questions remain the same
questions = [
    {
        "question": "Wie funktioniert die menschliche Stimme?",
        "choices": [
            "Die Stimmbänder schwingen durch Luftstrom und erzeugen Töne.",
            "Der Herzschlag erzeugt die Stimme.",
            "Die Lunge schwingt und produziert den Ton."
        ],
        "correct": ["Die Stimmbänder schwingen durch Luftstrom und erzeugen Töne."],
        "hint": "Denke an die Zusammenarbeit zwischen Lunge und Stimmbändern.",
        "explanation": "Die Stimmbänder schwingen durch Luftstrom und erzeugen Töne. Dies ist der Hauptmechanismus der Stimme."
    },
    {
        "question": "Wie breitet sich Schall aus?",
        "choices": [
            "Schall benötigt ein Medium, weil er durch Teilchenbewegung übertragen wird.",
            "Schall kann sich im Vakuum ausbreiten.",
            "Schall ist eine elektromagnetische Welle."
        ],
        "correct": ["Schall benötigt ein Medium, weil er durch Teilchenbewegung übertragen wird."],
        "hint": "Überlege, warum Schall ohne Luft nicht funktioniert.",
        "explanation": "Schall benötigt ein Medium, weil er durch Teilchenbewegung übertragen wird. Dies ist der Grund, warum Schall im Vakuum nicht ausbreiten kann."
    },
    {
        "question": "Wie funktioniert ein Echolot?",
        "choices": [
            "Ein Schallimpuls wird ausgesendet, reflektiert und die Zeit bis zur Rückkehr gemessen.",
            "Es nutzt elektromagnetische Wellen, um Entfernungen zu messen.",
            "Es sendet Lichtsignale aus, die Objekte reflektieren."
        ],
        "correct": ["Ein Schallimpuls wird ausgesendet, reflektiert und die Zeit bis zur Rückkehr gemessen."],
        "hint": "Es hat mit Schallwellen und Reflexion zu tun.",
        "explanation": "Ein Schallimpuls wird ausgesendet, reflektiert und die Zeit bis zur Rückkehr gemessen. Dies ist der Standardmechanismus für die Entfernungsmessung mit Schall."
    },
    {
        "question": "Welche Teilbereiche der Physik gibt es? (Mehrere Antworten möglich)",
        "choices": ["Mechanik", "Akustik", "Optik", "Thermodynamik"],
        "correct": ["Mechanik", "Akustik", "Optik", "Thermodynamik"],
        "hint": "Alle diese Bereiche sind Teil der Physik.",
        "explanation": "Mechanik, Akustik, Optik und Thermodynamik sind alle Teilbereiche der Physik."
    },
    {
        "question": "Was ist Hertz?",
        "choices": [
            "Die Einheit für Frequenz.",
            "Eine elektromagnetische Welle.",
            "Eine elektrochemische Reaktion."
        ],
        "correct": ["Die Einheit für Frequenz."],
        "hint": "Denke daran, dass Frequenz die Anzahl der Schwingungen pro Sekunde ist.",
        "explanation": "Hertz ist die Einheit für Frequenz. Sie gibt an, wie viele Schwingungen pro Sekunde stattfinden."
    },
    {
        "question": "Was ist eine elektromagnetische Welle?",
        "choices": ["Eine Welle, die sich durch elektromagnetische Felder ausbreitet.", 
                    "Eine Welle, die sich durch elektrochemische Reaktionen ausbreitet.", 
                    "Eine Welle, die sich durch Luft ausbreitet."],
        "correct": ["Eine Welle, die sich durch elektromagnetische Felder ausbreitet."],
        "hint": "Denke daran, dass elektromagnetische Wellen durch elektromagnetische Felder ausbreitet werden.",
        "explanation": "Elektromagnetische Wellen breiten sich durch elektromagnetische Felder aus. Dies sind Wellen, die sich sowohl in elektrischen als auch in magnetischen Feldern ausbreiten."
    },
        {
        "question": "Was passiert, wenn die Frequenz einer Welle steigt?",
        "choices": [
            "Die Wellenlänge wird kürzer.",
            "Die Tonhöhe steigt.",
            "Der Ton wird lauter.",
            "Die Wellenlänge wird länger."
        ],
        "correct": ["Die Wellenlänge wird kürzer.", "Die Tonhöhe steigt."],
        "hint": "Denke an den Zusammenhang zwischen Frequenz, Wellenlänge und Tonhöhe.",
        "explanation": "Wenn die Frequenz steigt, wird die Wellenlänge kürzer und die Tonhöhe steigt."
    },
    {
        "question": "Welche Aussage über die Amplitude einer Welle ist richtig?",
        "choices": [
            "Sie beeinflusst die Tonhöhe.",
            "Sie beeinflusst die Lautstärke.",
            "Sie beschreibt die Ausbreitungsgeschwindigkeit des Schalls.",
            "Sie ist die maximale Auslenkung einer Welle."
        ],
        "correct": ["Sie beeinflusst die Lautstärke.", "Sie ist die maximale Auslenkung einer Welle."],
        "hint": "Die Amplitude hat etwas mit der Stärke der Schwingung zu tun.",
        "explanation": "Die Amplitude beeinflusst die Lautstärke und ist die maximale Auslenkung einer Welle."
    },
    {
        "question": "Welche der folgenden Materialien lässt Schall am besten leiten?",
        "choices": [
            "Luft",
            "Wasser",
            "Holz",
            "Metall"
        ],
        "correct": ["Metall"],
        "hint": "Denke an die Dichte des Materials.",
        "explanation": "Metall ist das beste Material für das Leiten von Schall, da es eine hohe Dichte und eine gute Schallleitung hat."
    },
    {
        "question": "Warum hört man in einem leeren Raum einen Hall?",
        "choices": [
            "Schallwellen werden von den Wänden reflektiert.",
            "Die Frequenz des Schalls wird verstärkt.",
            "Es gibt keine weichen Oberflächen, die den Schall absorbieren.",
            "Der Schall wird durch den Boden verstärkt."
        ],
        "correct": ["Schallwellen werden von den Wänden reflektiert.", 
                   "Es gibt keine weichen Oberflächen, die den Schall absorbieren."],
        "hint": "Überlege, was mit den Schallwellen passiert und was sie absorbieren könnte.",
        "explanation": "Schallwellen werden von den Wänden reflektiert und es gibt keine weichen Oberflächen, die den Schall absorbieren. Dies führt zu einem Echo, das man in einem leeren Raum hört."
    },
    {
        "question": "Was ist eine Resonanz?",
        "choices": [
            "Eine Verstärkung der Schwingung, wenn die Frequenzen übereinstimmen.",
            "Die Dämpfung einer Schwingung durch Reibung.",
            "Die Umwandlung von Schallwellen in Lichtwellen.",
            "Eine Eigenschaft von Vakuumwellen."
        ],
        "correct": ["Eine Verstärkung der Schwingung, wenn die Frequenzen übereinstimmen."],
        "hint": "Denke an das Mitschwingen bei gleichen Frequenzen.",
        "explanation": "Eine Resonanz tritt auf, wenn die Frequenzen von zwei Schwingungssystemen übereinstimmen. Dies führt zu einer Verstärkung der Schwingung."
    }
]

# Add new text-based questions with expected key phrases
text_questions = [
    {
        "question": "Warum nehmen wir bei lauter Musik zuerst die tiefen Töne wahr, bevor wir die hohen wahrnehmen?",
        "type": "text",
        "points": 3,
        "key_phrases": [
            "tiefe frequenzen",
            "bass",
            "durchdringen",
            "besser",
            "stärker",
            "energie",
            "wände"
        ],
        "hint": "Denke an die unterschiedliche Durchdringungskraft von tiefen und hohen Frequenzen.",
        "explanation": "Tiefe Frequenzen haben mehr Energie und können besser durch Wände dringen, weshalb sie zuerst wahrgenommen werden."
    },
    {
        "question": "Warum können Hunde Töne hören, die für Menschen nicht wahrnehmbar sind?",
        "type": "text",
        "points": 3,
        "key_phrases": [
            "höhere frequenzen",
            "ultraschall",
            "empfindlicher",
            "besser",
            "höher",
            "20000 hz",
            "20 khz"
        ],
        "hint": "Vergleiche den hörbaren Frequenzbereich von Menschen und Hunden.",
        "explanation": "Hunde können Töne hören, die für Menschen nicht wahrnehmbar sind. Dies liegt an ihrer besseren Hörschärfe für höhere Frequenzen."
    },
    {
        "question": "Ein Echo ist eine reflektierte Schallwelle. Warum dauert es bei einem sehr großen Berg länger, bis man das Echo hört?",
        "type": "text",
        "points": 3,
        "key_phrases": [
            "weg",
            "länger",
            "distanz",
            "entfernung",
            "zurücklegen",
            "zeit",
            "geschwindigkeit"
        ],
        "hint": "Denke an die Strecke, die der Schall zurücklegen muss.",
        "explanation": "Der Schall muss eine größere Strecke zurücklegen, um das Echo zu hören, da der Berg die Schallwellen reflektiert und sie zurückkehren müssen."
    },
    {
        "question": "Du klatschst in einem leeren Raum und hörst ein Echo. Wie könntest du mithilfe des Echos den Abstand zur nächsten Wand messen, ohne eine Formel zu kennen?",
        "type": "text",
        "points": 5,
        "key_phrases": [
            "zeit",
            "stoppen",
            "messen",
            "uhr",
            "stoppuhr",
            "sekunden",
            "hälfte"
        ],
        "hint": "Überlege, was du messen könntest und wie du daraus die Entfernung bestimmen kannst.",
        "explanation": "Du könntest die Zeit messen, die das Echo braucht, um zurückzukehren, und dann die Geschwindigkeit des Schalls verwenden, um die Entfernung zu bestimmen."
    },
    {
        "question": "In einem Wasserbehälter erzeugst du mit einem Stein Wellen. Was passiert, wenn zwei Wellen gleichzeitig von gegenüberliegenden Seiten aufeinandertreffen? Beschreibe den Effekt und erkläre, was mit der Amplitude passiert.",
        "type": "text",
        "points": 5,
        "key_phrases": [
            "interferenz",
            "überlagerung",
            "verstärken",
            "auslöschen",
            "amplitude",
            "doppelt",
            "null"
        ],
        "hint": "Denke an die Überlagerung von Wellen und was mit ihrer Amplitude passiert.",
        "explanation": "Wenn zwei Wellen gleichzeitig von gegenüberliegenden Seiten aufeinandertreffen, können sie sich überlagern oder auslöschen. Dies hängt von der Phasenverschiebung und der Amplitude der Wellen ab."
    }
]

def log_performance(student_name, score, total_questions):
    log_file = "student_performance.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, student_name, score, total_questions])

def check_text_answer(answer, key_phrases, min_matches=2):
    """
    Check if the answer contains enough key phrases.
    Returns (score, feedback)
    """
    answer = answer.lower()
    matches = [phrase for phrase in key_phrases if phrase in answer]
    score = len(matches) >= min_matches
    
    if score:
        feedback = "Sehr gut! Deine Antwort enthält wichtige Schlüsselbegriffe."
    else:
        feedback = f"Deine Antwort könnte vollständiger sein. Wichtige Begriffe wären z.B.: {', '.join(key_phrases[:3])}..."
    
    return score, feedback

def reset_quiz():
    st.session_state.score = 0
    st.session_state.answered_questions = set()
    st.session_state.submitted_answers = {}
    st.session_state.reset = True
    for i, q in enumerate(questions):
        for choice in q['choices']:
            checkbox_key = f"q{i}_{choice}"
            if checkbox_key in st.session_state:
                del st.session_state[checkbox_key]
    for i in range(len(text_questions)):
        answer_key = f"text_answer_{i}"
        if answer_key in st.session_state:
            del st.session_state[answer_key]

# Streamlit App
st.title("Physik Quiz App")
st.write("Teste dein Wissen zu den Themen Schall, Stimme, Echolot und Physikbereiche!")

# Name input
student_name = st.text_input("Dein Name:", value=st.session_state.name)
st.session_state.name = student_name

if not student_name:
    st.warning("Bitte gib deinen Namen ein, bevor du fortfährst.")
else:
    for i, q in enumerate(questions):
        st.subheader(f"Frage {i+1}: {q['question']}")
        
        # Create a unique key for each question's answers
        answer_key = f"answers_{i}"
        if answer_key not in st.session_state:
            st.session_state[answer_key] = []
        
        # Create checkboxes and store selections
        selected = []
        for choice in q['choices']:
            if st.checkbox(choice, key=f"q{i}_{choice}"):
                selected.append(choice)
        st.session_state[answer_key] = selected
        
        # Check answer button
        if st.button(f"Antwort bestätigen für Frage {i+1}", key=f"confirm_{i}"):
            if i not in st.session_state.answered_questions:
                if set(selected) == set(q['correct']):
                    st.success("Richtig! 😊")
                    st.session_state.score += 1
                else:
                    st.error(f"Falsch. Tipp: {q['hint']}")
                    st.info(f"Richtige Antwort(en): {', '.join(q['correct'])}")
                    st.write(f"**Erklärung:** {q['explanation']}")
                st.session_state.answered_questions.add(i)
                st.session_state.submitted_answers[i] = selected

    # Show results button for multiple choice questions
    if st.button("Ergebnis anzeigen", key="show_mc_results"):
        st.write(f"**Dein Ergebnis: {st.session_state.score} von {len(questions)}**")
        log_performance(student_name, st.session_state.score, len(questions))
        
        if st.session_state.score == len(questions):
            st.balloons()
            st.success("Perfekt! Du hast alle Fragen richtig beantwortet!")
        elif st.session_state.score > len(questions) // 2:
            st.info("Gut gemacht, aber du kannst noch besser werden!")
        else:
            st.warning("Nicht schlecht, aber übe noch ein wenig!")
        
        st.write("Deine Ergebnisse wurden gespeichert.")

    st.header("Offene Fragen")
    for i, q in enumerate(text_questions):
        st.subheader(f"Frage {len(questions) + i + 1}: {q['question']}")
        
        # Create unique keys for each text input
        answer_key = f"text_answer_{i}"
        if answer_key not in st.session_state:
            st.session_state[answer_key] = ""
        
        # Text input for answer
        user_answer = st.text_area(
            "Deine Antwort:",
            value=st.session_state[answer_key],
            key=f"text_input_{i}",
            height=100
        )
        st.session_state[answer_key] = user_answer
        
        # Check answer button with unique key
        if st.button(f"Antwort überprüfen für Frage {len(questions) + i + 1}", key=f"check_text_{i}"):
            if user_answer:
                score, feedback = check_text_answer(user_answer, q['key_phrases'])
                if score:
                    st.success(feedback)
                    if i not in st.session_state.answered_questions:
                        st.session_state.score += q['points']
                        st.session_state.answered_questions.add(i + len(questions))
                else:
                    st.error(feedback)
                    st.info(f"Tipp: {q['hint']}")
                    st.write(f"**Erklärung:** {q['explanation']}")
            else:
                st.warning("Bitte gib eine Antwort ein.")

    # Final results button
    if st.button("Gesamtergebnis anzeigen", key="show_final_results"):
        total_points = (len(questions) * 3) + sum(q['points'] for q in text_questions)
        st.write(f"**Dein Gesamtergebnis: {st.session_state.score} von {total_points} Punkten**")
        
        percentage = (st.session_state.score / total_points) * 100
        
        if percentage >= 90:
            st.balloons()
            st.success("Hervorragend! Du hast die Aufgaben sehr gut gemeistert!")
        elif percentage >= 75:
            st.success("Sehr gut gemacht!")
        elif percentage >= 50:
            st.info("Gut gemacht, aber da ist noch Raum für Verbesserung!")
        else:
            st.warning("Übe noch ein bisschen weiter!")
        
        log_performance(student_name, st.session_state.score, total_points)
        st.write("Deine Ergebnisse wurden gespeichert.")

    # Reset button
    if st.button("Quiz zurücksetzen", key="reset_quiz"):
        reset_quiz()

