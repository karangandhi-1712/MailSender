# AI Cold Email Sender - Setup & Usage Guide

This guide will walk you through setting up your environment, getting the necessary API keys and passwords, preparing your data, and running the email automation scripts.

## Step 1: Prerequisites & Virtual Environment

1. **Python**: Ensure you have Python installed on your system.
2. **Create a Virtual Environment**: It is highly recommended to create a virtual environment to keep your project's packages isolated. Open your terminal in the project folder and run:
   ```bash
   # On Windows
   python -m venv venv
   
   # On Mac/Linux
   python3 -m venv venv
   ```
3. **Activate the Virtual Environment**:
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate
   ```
4. **Dependencies**: Now, install the Google Generative AI package needed to generate the email drafts:
   ```bash
   pip install google-generativeai
   ```

## Step 2: Get Your Gemini API Key

We use Google's Gemini AI to write personalized emails.

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Sign in with your Google account.
3. Click on **"Create API key"** (you may need to create a new project first).
4. Copy the generated API key and save it somewhere safe. You will need it for the `.env` file in Step 4.

## Step 3: Get Your Gmail App Password

To send emails automatically from your Gmail account, you cannot use your regular password. You need to create an "App Password".

1. Go to your [Google Account Manage Page](https://myaccount.google.com/).
2. On the left navigation panel, click on **Security**.
3. Under "How you sign in to Google", ensure **2-Step Verification** is turned **ON**.
4. Once 2-Step Verification is on, search for **"App passwords"** in the top search bar of your Google Account settings, or navigate to it under the 2-Step Verification menu.
5. Provide a name for the app (e.g., "Mail Sender Script") and click **Create**.
6. A 16-character password will appear in a yellow box. **Copy this password** (without the spaces). You will not be able to see it again.

## Step 4: Create the `.env` Configuration File

Your scripts need a `.env` file to securely load your keys and passwords without hardcoding them in the scripts.

1. In the same folder as the Python scripts (`generate_drafts.py` and `send_emails.py`), create a new text file and name it exactly `.env` (make sure it doesn't accidentally get named `.env.txt`).
2. Open the `.env` file in any text editor (like Notepad or VS Code).
3. Paste the following template and fill in your specific details:

```env
GEMINI_API_KEY=your_gemini_api_key_here
CLUB_NAME=Your Club Name
SENDER_NAME=Your Full Name
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_16_character_app_password_here
```
*(Note: Do not put quotes around the values)*

## Step 5: Convert Your Excel Data to CSV

The scripts read data from a CSV file. If you have your contacts in an Excel spreadsheet (`.xlsx`), you need to convert it.

1. Open your Excel spreadsheet.
2. Ensure your columns are named exactly like this in the first row: `name`, `email`, `notes`.
3. Go to **File** > **Save As**.
4. In the format dropdown, select **CSV (Comma delimited) (*.csv)** or **CSV UTF-8 (Comma delimited) (*.csv)**.
5. Save the file as **`contacts.csv`**.
6. **Important:** Move or copy this `contacts.csv` file into the same folder as your Python scripts.

## Step 6: Run the Scripts in Succession

Now you are ready to generate drafts and send emails. Open your terminal or command prompt, navigate to the folder containing your scripts, and follow these steps:

### 1. Generate the Email Drafts
Run the draft generation script:
```bash
python generate_drafts.py
```
*(Use `python3` instead of `python` if you are on Mac/Linux)*

- The script will read your `contacts.csv` file, use Gemini to deduce industry/position details from the email domain, and write personalized emails.
- Once finished, it will create a new file called **`drafts.csv`**.

### 2. Review the Drafts (CRUCIAL)
- **Do not skip this step!** Open `drafts.csv` in Excel or a text editor.
- Read through the generated `Subject` and `Body` for each contact.
- Make any manual edits if the AI made a mistake or if you want to tweak the wording.
- Save and close `drafts.csv` (ensure it stays in CSV format).

### 3. Send the Emails
Once you are happy with the drafts, run the sending script:
```bash
python send_emails.py
```
- This script will log into your Gmail using the App Password and send out every email listed in `drafts.csv`.
- You will see a success message in the terminal for each email sent.

## Step 7: Check Your Sent Mails

To confirm everything worked perfectly:
1. Open your browser and go to your Gmail account.
2. Click on the **Sent** folder on the left sidebar.
3. You should see all the emails the script just sent out. Click on a few to verify the formatting and content look correct!
