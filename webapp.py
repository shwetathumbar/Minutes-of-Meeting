import google.generativeai as genai
import os
import streamlit as st
from pdfextractor import text_extractor_pdf
from docxextractor import text_extracor_docx
from imageextractor import extract_text_image

# Configure the model
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key='AIzaSyCA2uu5GaTNoNUXeelsTv0G4rgzzjRL_Zs')
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# upload a file in sidebar
user_text = None
st.sidebar.title(':orange[Upload your MoM Notes here:]')
st.sidebar.subheader('Only Upload Images, PDFs and DOCX')
user_file = st.sidebar.file_uploader('Upload your file', type=['pdf','docx','jpg','jpeg'])
if user_file:
    if user_file.type == 'application/pdf':
        user_text = text_extractor_pdf(user_file)
    elif user_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        user_text = text_extracor_docx(user_file)
    elif user_file.type in ['image/jpg','image/jpeg','image/png']:
        user_text = extract_text_image(user_file)
    else:
        st.write("Upload Correct File Format")



# Main Page
st.title(':blue[Minutes of Meeting]: :green[AI Assisted MoM generator in standardized form]')
tips = ''' Tips to use this app:
* Upload your meeting in side bar (Image, PDF or DOCX)
* Click on generate MOM and get the standardized MOM's'''
st.write(tips)

if st.button('Generate MOM'):
    if user_text is None:
        st.error('Text is not generated')
    else:
        with st.spinner('Processing your data...'):


            prompt = f'''Assume you are expert in creating minutes of meeting. 
            User has provided notes in text format. Using this data you need to create a standardized
            minutes pf meeting for the user. 

            output must follow word/docx format, strictly in the following manner:
            title: Title of meeting
            Heading: Meeting agenda
            Subheading : Name of Attendees (If attendees name is not there keep it NA)
            subheading : date of meeting and place of meeting (place means name of the conference / meeting room)
            Body : The body must follow the following sequence of points:
            * Key points discussed
            * Highlight any decision that has been finalised.
            * Mention actionalble items.
            * Any Additional notes.
            * Any deadline that has been discused.
            * Any next meeting date that has been discused.
            * 2-3 line of summary.
            * Use bullet points and highlight or bold important keywords such the context is clear.
            * Generate the output in such a format that can download and edit.

            The data provided by user is as follows {user_text}

            '''
            response = model.generate_content(prompt)
            st.write(response.text)

            st.download_button(label='Click',
                               data=response.text,
                               file_name='MOM.txt',
                               mime='text/plain')

         

         

     


