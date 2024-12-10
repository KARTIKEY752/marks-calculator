import streamlit as st
import speech_recognition as sr
import pandas as pd

# Data storage
students_data = []
current_student_id = 1

def parse_voice_input_for_marks(paper_name):
    """Capture voice input for marks and return as a list of floats."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Set a short pause threshold (e.g., 2 seconds)
        recognizer.pause_threshold = 2
        st.info(f"Listening for marks for {paper_name}. Speak marks with 'plus' or '+' and 'point' for decimals (e.g., '3 point 5 plus 2').")
        try:
            audio = recognizer.listen(source, timeout=15)
            text = recognizer.recognize_google(audio)
            st.success(f"You said for {paper_name}: {text}")
            
            # Normalize input: Replace "point" with "." and handle "+" symbols
            formatted_text = text.replace("point", ".").replace("plus", " + ").replace("+", " + ")
            
            # Split text into tokens and evaluate expression
            marks = [float(mark.strip()) for mark in formatted_text.split("+")]
            return marks
        except ValueError:
            st.error(f"Invalid input for {paper_name}. Please speak numbers separated by 'plus' or '+' and use 'point' for decimals.")
        except sr.UnknownValueError:
            st.error(f"Could not understand your speech for {paper_name}. Please try again.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.WaitTimeoutError:
            st.error("Listening timed out. Please speak within 15 seconds.")
    return []

def add_student_marks(paper1_marks, paper2_marks):
    """Add the marks for Paper 1 and Paper 2 for a new student and update the table."""
    global current_student_id
    total_marks = sum(paper1_marks) + sum(paper2_marks)
    students_data.append({
        "Student ID": current_student_id, 
        "Paper 1 Marks": paper1_marks,
        "Paper 2 Marks": paper2_marks,
        "Total": total_marks
    })
    current_student_id += 1

def display_student_table():
    """Display the student marks table."""
    if students_data:
        df = pd.DataFrame(students_data)
        st.table(df)
    else:
        st.info("No student data available.")

# Streamlit app UI
st.title("Student Marks Recorder for Paper 1 and Paper 2")

# Record voice input
if st.button("Start Speaking for Paper 1"):
    paper1_marks = parse_voice_input_for_marks("Paper 1")
    if paper1_marks:
        st.session_state.paper1_marks = paper1_marks
        st.success("Marks for Paper 1 recorded successfully!")

if 'paper1_marks' in st.session_state:
    # Ask for Paper 2 marks after Paper 1 marks are recorded
    if st.button("Start Speaking for Paper 2"):
        paper2_marks = parse_voice_input_for_marks("Paper 2")
        if paper2_marks:
            st.session_state.paper2_marks = paper2_marks
            add_student_marks(st.session_state.paper1_marks, paper2_marks)
            st.success("Marks for Paper 2 recorded successfully!")
            st.session_state.paper1_marks = []  # Clear Paper 1 marks for next student

# Display the table of students and marks
st.header("Student Marks Table")
display_student_table()
