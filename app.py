note = """APP HAS ISSUES WITH PYTHON 3.12, USE PYTHON 3.10 INSTEAD"""

import streamlit as st
from utils import text_from_pdf_file, read_docx, text_from_pdf_file_path, upload_file
import uuid


from philter import Philter # Source: https://github.com/BCHSI/philter-ucsf
import time
import os


def deidentify(uploaded_file_text, uploaded_file_name = "note_"):
    """
    Source of core functionality: https://github.com/BCHSI/philter-ucsf
    """
    if uploaded_file_text is not None:
        # Create a .txt version of the file in the input folder
        file_unique_name = str(uploaded_file_name) + str(uuid.uuid1())
        if not file_unique_name.endswith(".txt"):
            file_unique_name += ".txt"
        file_in_path = f"files/inputs/{file_unique_name}"
        with open(file_in_path, "w", encoding="utf-8") as f:
            f.write(uploaded_file_text)
        # Remove PHI from the file; store in output folder
        try:
            philter_config = {
                "verbose":True,
                "run_eval":False,
                "finpath":"./files/inputs/",
                "foutpath":"./files/outputs/",
                "outformat":"asterisk",
                "filters":"./configs/philter_delta.json",
                "cachepos":None
            }
            filterer = Philter(philter_config)
            filterer.map_coordinates()
            filterer.transform()
        except Exception as e:
            st.error("Error in deidentifying the file. ")
            st.error(str(e))
            os.remove(f"files/inputs/{file_unique_name}")
            os.remove(f"files/outputs/{file_unique_name}")
            st.stop()
        # Read the output file(s) into memory
        with open(f"files/outputs/{file_unique_name}", "r", encoding="utf-8") as f:
            output = f.read()
        os.remove(f"files/inputs/{file_unique_name}")
        os.remove(f"files/outputs/{file_unique_name}")

        return output
def initialize_session_state():
    if "input_choice" not in st.session_state:
        st.session_state["input_choice"] = None
    if "prev_uploaded_file" not in st.session_state:
        st.session_state["prev_uploaded_file"] = None
    if "downloaded_file" not in st.session_state:
        st.session_state["downloaded_file"] = False
    if "deidentified_note" not in st.session_state:
        st.session_state["deidentified_note"] = None

# This is a test report with fake PHI/PII to test the app.
EXAMPLE_REPORT = """Note: The PHI/PII in this note are not from a real patient. This note is for testing/demonstration purposes.

**Patient Name:** John Doe  
**Date of Birth:** 02/14/1983  
**Address:** 123 Main Street, Springfield, IL, 62704  
**Phone:** (555) 123-4567  
**Email:** johndoe@example.com  
**SSN:** 123-45-6789  
**Insurance ID:** 9876543210  
**Primary Physician:** Dr. Jane Smith  
**Date of Visit:** 01/20/2024  

**Medical History:**  
- Patient has a history of Type 2 Diabetes diagnosed in 2010.
- Previous surgery: Appendectomy in 2015.

**Medications:**  
- Metformin 500 mg twice daily.
- Lisinopril 10 mg once daily.

**Allergies:**  
- Penicillin
- Peanuts

**Chief Complaint:**  
Patient complains of intermittent chest pain for the past week, often occurring during physical activity.

**Examination Findings:**  
- Blood Pressure: 140/90 mmHg
- Heart Rate: 78 bpm
- Height: 5 feet 9 inches
- Weight: 200 lbs
- Physical exam unremarkable except for mild tenderness in the chest area upon palpation.

**Assessment and Plan:**  
- Suspected stable angina.
- Recommend cardiac stress test and echocardiogram.
- Increase physical activity, advise to follow a heart-healthy diet.
- Follow-up appointment scheduled for 02/01/2024 with Cardiology Specialist Dr. Emily Taylor at Springfield Cardiac Care, 456 Health Rd, Springfield, IL, 62704.

**Notes:**  
Patient expressed concerns about managing new symptoms with current work schedule. Discussed importance of lifestyle modification and regular monitoring of cardiovascular health.

"""
def main():
    initialize_session_state()
    st.title("Deidentify PHI in your file")
    st.markdown("This app uses the [Philter](https://github.com/BCHSI/philter-ucsf) library to deidentify PHI in your file.")
    st.markdown("""
    ### Instructions
    1. Paste the text of the clinical note/text, or upload a file in .txt, .pdf, or .docx format.  
    2. After a few seconds, the file will be deidentified and the output will be displayed.  
    """) 
    st.markdown("""
                ### Enter Text or Upload File Below
                """)
    input_choice = st.radio("Choose your input method:", ('Paste Text', 'Upload File'), horizontal=True)
    st.session_state["input_choice"] = input_choice
    if input_choice == 'Paste Text':
        text_container = st.empty()
        report_text = text_container.text_area("Paste your clinical note/text here. After pasting it, press ctrl + Enter and then press 'Deidentify clinical note':")
    else:
        _, report_text = upload_file()
    col1, col2, _ = st.columns([3, 4, 3])
    deidentify_report_button = col1.button("Deidentify clinical note", type="primary")
    try_example = col2.button("Try example clinical note")
    if try_example:
        if input_choice == 'Paste Text':
            report_text = text_container.text_area("Paste your clinical note/text here. After pasting it, press ctrl + Enter and then press 'Deidentify clinical note':", value=EXAMPLE_REPORT, key="text_area")
            st.session_state["deidentified_note"] = deidentify(report_text)
        else:
            report_text = EXAMPLE_REPORT
            st.session_state["deidentified_note"] = deidentify(report_text)
    if deidentify_report_button and report_text.strip():
        st.session_state["deidentified_note"] = deidentify(report_text)

    if st.session_state["deidentified_note"]:
        st.subheader("Deidentified clinical note:")
        st.text(st.session_state["deidentified_note"])
        st.download_button("Download file as .txt", data=st.session_state["deidentified_note"], file_name="deidentified_note.txt")
if __name__ == "__main__":
    main()