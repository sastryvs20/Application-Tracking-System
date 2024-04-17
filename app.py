import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_repsonse(input, resume_text, job_description):
    formatted_prompt = input_prompt.format(text=resume_text, jd=job_description)
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(formatted_prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt ="""

Act like a very skilled and experienced ATS(Application Tracking System). You will be provided with the content of a resume in text and the job description(also in text). You must evaluate the resume and provide]
assistance to the user to improve their resume. Respond with the percentage match with the job description and the missing keywords. Perform the line by line anslysis and let the user know
in which line he has to make changes to make the resume better. Also give the resume summary.

resume : {text}
jd : {jd}
"""

## streamlit app

st.title("Rix")
jd=st.text_area("Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt,text,jd)
        st.subheader(response)
