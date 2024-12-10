import streamlit as st
import pandas as pd

# Initialize a session state variable for the student data
if 'student_data' not in st.session_state:
    st.session_state.student_data = []

# Function to calculate total marks for each paper and the overall total
def calculate_marks(paper1_marks, paper2_marks):
    try:
        # Convert string input to list of floats for paper marks
        paper1_marks = list(map(float, paper1_marks.split()))
        paper2_marks = list(map(float, paper2_marks.split()))

        # Calculate the sum of marks for each paper
        paper1_total = sum(paper1_marks)
        paper2_total = sum(paper2_marks)

        # Calculate total marks secured by the student
        total_marks = paper1_total + paper2_total

        return paper1_total, paper2_total, total_marks

    except ValueError:
        # Handle the case where conversion to float fails (invalid input)
        st.error("Please enter valid space-separated decimal or integer values for marks.")
        return None, None, None

# Function to add a new student's data
def add_student():
    student_name = f"Student {len(st.session_state.student_data) + 1}"
    paper1_marks = st.text_input(f"Enter marks for Paper 1 for {student_name} (space-separated):")
    paper2_marks = st.text_input(f"Enter marks for Paper 2 for {student_name} (space-separated):")

    if st.button(f"Add Marks for {student_name}"):
        if paper1_marks and paper2_marks:
            paper1_total, paper2_total, total_marks = calculate_marks(paper1_marks, paper2_marks)
            
            if paper1_total is not None and paper2_total is not None:
                # Store the student's data
                st.session_state.student_data.append({
                    'name': student_name,
                    'paper1_marks': paper1_marks,
                    'paper2_marks': paper2_marks,
                    'paper1_total': paper1_total,
                    'paper2_total': paper2_total,
                    'total_marks': total_marks
                })

                # Display the results for the student
                st.success(f"Marks added for {student_name}")
                st.write(f"Total Marks for Paper 1: {paper1_total}")
                st.write(f"Total Marks for Paper 2: {paper2_total}")
                st.write(f"Total Marks Secured by {student_name}: {total_marks}")
        else:
            st.error("Both Paper 1 and Paper 2 marks must be entered.")

# Function to display all students in a table
def display_students():
    if st.session_state.student_data:
        st.subheader("Student Marks Data")

        # Convert the student data to a DataFrame for better table formatting
        data = []
        for student in st.session_state.student_data:
            data.append({
                "Student Name": student["name"],
                "Paper 1 Marks": student["paper1_marks"],
                "Paper 2 Marks": student["paper2_marks"],
                "Total Marks for Paper 1": student["paper1_total"],
                "Total Marks for Paper 2": student["paper2_total"],
                "Total Marks Secured": student["total_marks"]
            })

        # Create a pandas DataFrame to display as a table
        df = pd.DataFrame(data)

        # Display the DataFrame as a table in Streamlit
        st.table(df)

# Main function to run the Streamlit app
def main():
    st.title("Student Marks Calculator")
    add_student()  # Allow users to add marks for new students
    display_students()  # Display all the added student data

if __name__ == "__main__":
    main()
