note = """APP HAS ISSUES WITH PYTHON 3.12, USE PYTHON 3.10 INSTEAD"""

import streamlit as st
from utils import upload_file
import uuid


from philter import Philter # Source: https://github.com/BCHSI/philter-ucsf
import time
import os


def deidentify(uploaded_file_name, uploaded_file_text):
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

def main():
    st.title("Deidentify PHI in your file")
    st.markdown("This app uses the [Philter](https://github.com/BCHSI/philter-ucsf) library to deidentify PHI in your file.")
    st.markdown("""
    ## Instructions
    1. Upload a file in .txt, .pdf, or .docx format.  
    2. After a couple seconds, the file will be deidentified and the output will be displayed.  
    """)
    st.markdown("## Upload your file")
    uploaded_file_name, uploaded_file_text = upload_file()
    initial_time = time.time()
    output = deidentify(uploaded_file_name, uploaded_file_text)
    if output:
        st.markdown("## Output (Deidentified file)")
        st.text(output)
    end_time = time.time()
    time_taken = end_time - initial_time
    print(time_taken)
if __name__ == "__main__":
    main()