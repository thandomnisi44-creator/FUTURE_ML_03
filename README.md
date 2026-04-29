# Resume Screening System

This Python script provides a robust system for screening resumes against a given job description. It automates the process of matching candidate skills and experience with job requirements, ranking applicants based on their relevance.

## Features

*   **Text Cleaning**: Preprocesses raw resume text by converting to lowercase, removing URLs, special characters, and common stopwords.
*   **Skill Extraction**: Identifies key technical and soft skills from resumes and job descriptions using a pre-defined skill database.
*   **Missing Skills Identification**: Highlights skills mentioned in the job description that are absent from a candidate's resume.
*   **Similarity Scoring**: Calculates a match score between a cleaned resume and job description using TF-IDF vectorization and cosine similarity.
*   **Candidate Ranking**: Ranks candidates based on their match score, providing an ordered list of most suitable applicants.
*   **Excel Integration**: Reads resume data from an Excel file and outputs results back to a CSV file.

## How to Use

1.  **Prepare Your Data**: Ensure your resumes are compiled in an Excel file (`.xlsx`). The script will attempt to auto-detect the column containing the resume text. If it fails, you may need to adjust the `possible_text_cols` list within the `screen_resumes` function or ensure a clear 'Resume' or 'ResumeText' column exists.

2.  **Set `EXCEL_FILE`**: Update the `EXCEL_FILE` variable in the `if __name__ == "__main__":` block to point to your Excel file (e.g., `"resume.xlsx"`).

3.  **Define `JOB_DESCRIPTION`**: Modify the `JOB_DESCRIPTION` variable with the specific requirements for the role you are screening for.

4.  **Run the Script**: Execute the cell containing the `screen_resumes` function and the example usage.

5.  **Review Results**: The script will print the top 10 ranked candidates to the console and save the full results to a CSV file named `resume_screening_results.csv`.

## Dependencies

This script requires the following Python libraries:

*   `pandas`
*   `re`
*   `nltk`
*   `numpy`
*   `scikit-learn`

NLTK data (`punkt` and `stopwords`) will be downloaded automatically if not already present.

## Example Usage

```python
# ---- USER INPUTS ----
EXCEL_FILE = "resume.xlsx" # Your Excel file containing resumes
JOB_DESCRIPTION = """
We are looking for a Data Scientist with strong Python, SQL, and machine learning skills.
Experience with TensorFlow, Pandas, and cloud platforms (AWS/Azure) is a plus.
Excellent communication and teamwork are required.
"""

# Run screening
ranked_candidates = screen_resumes(EXCEL_FILE, JOB_DESCRIPTION)

# Display top 10 results
print(ranked_candidates.head(10).to_string(index=True))

# Save full results to CSV
output_file = "resume_screening_results.csv"
ranked_candidates.to_csv(output_file, index=True)
```

## Output

The script generates a pandas DataFrame (`ranked_candidates`) and a CSV file (`resume_screening_results.csv`) with the following columns:

*   `Candidate_ID`: Unique identifier for each candidate.
*   `Resume_Label`: Label for the resume (e.g., `Candidate_1`).
*   `Match_Score_%`: The percentage match score against the job description.
*   `Skills_Found`: A comma-separated list of relevant skills found in the resume.
*   `Missing_Key_Skills`: A comma-separated list of important skills from the job description not found in the resume.