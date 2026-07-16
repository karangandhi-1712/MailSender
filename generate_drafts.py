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

api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set. Add it to .env or your environment.')
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-3.5-flash')

INPUT_CSV = 'contacts.csv'
OUTPUT_CSV = 'drafts.csv'

CLUB_NAME = os.environ.get('CLUB_NAME', 'CodeChef VIT Chennai')
SENDER_NAME = os.environ.get('SENDER_NAME', 'Karan Anand Gandhi')


def generate_email(name, email, notes):
    prompt = f"""
The sender is {SENDER_NAME}, leader of {CLUB_NAME}. Write a highly personalized, concise cold email pitching a sponsorship/collaboration opportunity.

Recipient Details:
- Name: {name}
- Email: {email}
- Raw Notes: {notes if notes else 'None'}

Instructions:
1. Deduction: Infer the recipient's Company, Position, and Industry/Domain strictly from the Email address domain and Raw Notes.
2. Perspective: Write in an impersonal third-person style instead of the first person (e.g., "{CLUB_NAME} is exploring partnerships" rather than "I am writing to you").
3. Hook: Acknowledge their inferred role and connect how the {CLUB_NAME} developer talent aligns with their company's work.
4. Customization: Strictly incorporate any specific requests or financial amounts mentioned in the Raw Notes.
5. Constraints: Maximum 150 words. Plain text only (no markdown, no emojis, no robotic tone).
6. Call to Action: End with a low-friction ask for a brief chat.

Format exactly:
SUBJECT: [subject]
BODY: [body]
"""
    try:
        response = model.generate_content(prompt)
        text = response.text or ""
        subject = text.split("SUBJECT:")[1].split("BODY:")[0].strip()
        body = text.split("BODY:")[1].strip()
        return subject, body
    except Exception as e:
        print(f"Error generating content: {e}")
        subject = f"Sponsorship Opportunity with {CLUB_NAME}"
        body = (
            f"Hello {name},\n\n"
            f"{CLUB_NAME} is reaching out to discuss a potential partnership.\n\n"
            f"Regards,\n{SENDER_NAME}"
        )
        return subject, body


with open(INPUT_CSV, mode='r', encoding='utf-8') as infile, \
     open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    writer.writerow(["Name", "Email", "Subject", "Body"])

    for row in reader:
        name = row.get("name", "")
        email = row.get("email", "")
        notes = row.get("notes", "")

        print(f"Generating draft for {name}...")
        # Now passing email to allow domain inference
        subject, body = generate_email(name, email, notes) 
        writer.writerow([name, email, subject, body])

print(f"\nDrafts saved to {OUTPUT_CSV}. Please review them before sending.")