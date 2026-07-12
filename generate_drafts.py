import csv
import os
import google.generativeai as genai


def load_env_file(path='.env'):
    if not os.path.exists(path):
        return
    with open(path, mode='r', encoding='utf-8') as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())


load_env_file()

# Configure API key from environment
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set. Add it to .env or your environment.')
genai.configure(api_key=api_key)

# Use the recommended model for text generation
model = genai.GenerativeModel('gemini-2.5-flash')

INPUT_CSV = 'contacts.csv'
OUTPUT_CSV = 'drafts.csv'

# Optional personalization values
CLUB_NAME = os.environ.get('CLUB_NAME', 'CodeChef VIT Chennai')
SENDER_NAME = os.environ.get('SENDER_NAME', 'Karan Anand Gandhi')

def generate_email(company, notes):
    prompt = f"""
    Write a concise, professional sponsorship email from {SENDER_NAME}, leader of {CLUB_NAME}, to {company}.
    We are seeking sponsorship and promotion opportunities for our upcoming student club event.
    Additional context about the company: {notes if notes else 'None'}.
    
    Format the output exactly as follows:
    SUBJECT: [Proposed Subject Line]
    BODY: [Email Body]
    """
    response = model.generate_content(prompt)
    text = response.text
    
    try:
        # Parse the subject and body from the LLM output
        subject = text.split("SUBJECT:")[1].split("BODY:")[0].strip()
        body = text.split("BODY:")[1].strip()
        return subject, body
    except IndexError:
        # Fallback if the LLM formatting fails
        return "Sponsorship Opportunity", text.strip()

# Read the input and generate the drafts
with open(INPUT_CSV, mode='r', encoding='utf-8') as infile, \
     open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    # Write the header for the output CSV
    writer.writerow(["Company", "Email", "Subject", "Body"])
    
    for row in reader:
        company = row.get("Company", "")
        email = row.get("Email", "")
        notes = row.get("Notes", "")
        
        print(f"Generating draft for {company}...")
        subject, body = generate_email(company, notes)
        writer.writerow([company, email, subject, body])

print(f"\nDrafts saved to {OUTPUT_CSV}. Please review them before sending.")