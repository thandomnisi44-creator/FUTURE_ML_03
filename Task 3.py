import pandas as pd
import re
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data (run once)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# -------------------------------
# 1. TEXT CLEANING FUNCTION
# -------------------------------
def clean_text(text):
    """Clean and preprocess raw resume text."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    # Tokenize and remove stopwords
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    # Add custom stopwords (common but uninformative words)
    custom_stops = {'experience', 'skills', 'year', 'work', 'job', 'role',
                    'position', 'candidate', 'company', 'team', 'project', 'skill'}
    stop_words.update(custom_stops)
    tokens = [t for t in tokens if t not in stop_words]
    return ' '.join(tokens)

# -------------------------------
# 2. SKILL EXTRACTION (Pre-defined skill set)
# -------------------------------
def get_skill_list():
    """Return a list of common technical & soft skills."""
    return [
        'python', 'java', 'sql', 'javascript', 'html', 'css', 'react', 'angular',
        'vue', 'nodejs', 'express', 'django', 'flask', 'spring', 'hibernate',
        'mongodb', 'mysql', 'postgresql', 'oracle', 'sqlite', 'aws', 'azure',
        'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
        'machine learning', 'artificial intelligence', 'deep learning', 'nlp',
        'computer vision', 'data science', 'analytics', 'tensorflow', 'keras',
        'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
        'tableau', 'power bi', 'excel', 'communication', 'leadership',
        'project management', 'agile', 'scrum', 'kanban', 'linux', 'unix',
        'windows', 'bash', 'powershell', 'c++', 'c#', 'ruby', 'php', 'swift',
        'kotlin', 'go', 'rust', 'hadoop', 'spark', 'kafka', 'tensorflow'
    ]

def extract_skills(text, skills_db):
    """Return list of skills found in the text."""
    text_low = text.lower()
    return [skill for skill in skills_db if skill in text_low]

def get_missing_skills(job_desc, resume_text, skills_db):
    """Return skills mentioned in job description but missing from resume."""
    job_skills = extract_skills(job_desc, skills_db)
    resume_skills = extract_skills(resume_text, skills_db)
    return list(set(job_skills) - set(resume_skills))

# -------------------------------
# 3. SIMILARITY SCORING
# -------------------------------
def calculate_match_score(job_desc_clean, resume_clean):
    """Cosine similarity between cleaned job description and resume."""
    if not resume_clean or not job_desc_clean:
        return 0.0
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([job_desc_clean, resume_clean])
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return similarity[0][0] * 100

# -------------------------------
# 4. MAIN SCREENING PIPELINE
# -------------------------------
def screen_resumes(excel_path, job_description):
    """
    Load resumes from Excel, score & rank them against the job description.
    Returns a DataFrame with ranking, scores, skills, and missing skills.
    """
    # Read Excel file
    df = pd.read_excel(excel_path)
    print(f"Loaded {len(df)} resumes from {excel_path}")
    print(f"Columns found: {df.columns.tolist()}")

    # Find the column that contains resume text (heuristic)
    possible_text_cols = ['Resume', 'Resume_str', 'ResumeText', 'Text', 'resume', 'description']
    text_col = None
    for col in possible_text_cols:
        if col in df.columns:
            text_col = col
            break
    if text_col is None:
        # If no standard name, pick the first string column with average length > 100
        for col in df.columns:
            if df[col].dtype == object and df[col].astype(str).str.len().mean() > 100:
                text_col = col
                break
    if text_col is None:
        raise ValueError("Could not identify resume text column. Please check your Excel file.")

    print(f"Using column '{text_col}' as resume text.")

    # Clean job description once
    job_desc_clean = clean_text(job_description)
    skills_db = get_skill_list()

    results = []
    for idx, row in df.iterrows():
        raw_resume = str(row[text_col])
        cleaned_resume = clean_text(raw_resume)
        score = calculate_match_score(job_desc_clean, cleaned_resume)
        skills_found = extract_skills(raw_resume, skills_db)
        missing = get_missing_skills(job_description, raw_resume, skills_db)

        results.append({
            'Candidate_ID': idx + 1,
            'Resume_Label': row.get('Category', f'Candidate_{idx+1}'),  # if Category column exists
            'Match_Score_%': round(score, 2),
            'Skills_Found': ', '.join(skills_found[:15]),   # limit to 15 for readability
            'Missing_Key_Skills': ', '.join(missing[:10])
        })

    # Convert to DataFrame and sort by score descending
    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values('Match_Score_%', ascending=False).reset_index(drop=True)
    result_df.index = result_df.index + 1  # start ranking at 1
    return result_df

# -------------------------------
# 5. EXAMPLE USAGE (MODIFY HERE)
# -------------------------------
if __name__ == "__main__":
    # ---- USER INPUTS ----
    EXCEL_FILE = "resume.xlsx"   # <-- change to your file path
    JOB_DESCRIPTION = """
    We are looking for a Data Scientist with strong Python, SQL, and machine learning skills.
    Experience with TensorFlow, Pandas, and cloud platforms (AWS/Azure) is a plus.
    Excellent communication and teamwork are required.
    """

    # Run screening
    ranked_candidates = screen_resumes(EXCEL_FILE, JOB_DESCRIPTION)

    # Display top 10 results
    print("\n" + "="*80)
    print("TOP RANKED CANDIDATES")
    print("="*80)
    print(ranked_candidates.head(10).to_string(index=True))

    # Save full results to CSV
    output_file = "resume_screening_results.csv"
    ranked_candidates.to_csv(output_file, index=True)
    print(f"\nFull results saved to {output_file}")