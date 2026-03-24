import streamlit as st
import PyPDF2
import google.generativeai as genai

# --- 1. CONFIGURATION ---
# Streamlit will securely read this from its cloud servers
API_KEY = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. LOGIC: PDF EXTRACTION ---
def extract_text_from_pdf(file_object):
    pdf_reader = PyPDF2.PdfReader(file_object)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + " "
    return text

# --- 3. LOGIC: AI ANALYSIS ---
def evaluate_resume(resume_text, job_description):
    prompt = f"""
    You are an expert Applicant Tracking System (ATS) and Senior Technical Recruiter.
    Evaluate the following resume against the provided job description.
    
    Job Description: {job_description}
    Resume Text: {resume_text}
    
    Provide your output strictly in the following Markdown format:
    
    ### 📊 ATS Match Score: [Insert Score]%
    
    ### 🔍 Missing Keywords:
    - [Keyword 1]
    - [Keyword 2]
    
    ### 💡 Profile Summary & Actionable Advice:
    [Write 2-3 sentences explaining why this candidate is or isn't a strong fit, and exactly how they should update their resume summary or project descriptions for this specific role.]
    """
    response = model.generate_content(prompt)
    return response.text

# --- 4. STREAMLIT FRONTEND UI ---
st.set_page_config(page_title="AI Resume Analyzer", layout="wide", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.write("Bypass the ATS. Upload your resume and paste the target job description to get instant, AI-driven feedback.")

# Create two columns for a clean layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Your Resume")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

with col2:
    st.subheader("2. Target Role")
    job_desc = st.text_area("Paste Job Description", placeholder="e.g., Looking for a pre-final year Computer Science student for an AI/ML Internship. Must have strong Python skills...", height=200)

# The Execution Button
st.markdown("---")
if st.button("🚀 Analyze Fit", use_container_width=True):
    if uploaded_file is not None and job_desc:
        # Shows a loading spinner while the AI thinks
        with st.spinner("Extracting text and analyzing match..."):
            try:
                # Run the functions
                resume_text = extract_text_from_pdf(uploaded_file)
                analysis = evaluate_resume(resume_text, job_desc)
                
                # Print the result
                st.success("Analysis Complete!")
                st.markdown(analysis)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("⚠️ Please upload a resume and paste a job description first.")