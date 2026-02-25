# 💹 AI Investment Decision Assistant

A beginner-friendly, multi-turn financial chatbot built with **Google Gemini** and **Streamlit**.

---

## 📁 Project Structure

```
ai-investment-assistant/
│
├── app.py              # Main Streamlit app (UI + session memory)
├── gemini_client.py    # Gemini API integration
├── prompts.py          # System prompt / assistant instructions
├── requirements.txt    # Python dependencies
├── .env.example        # Template for your API key
└── README.md           # This file
```

---

## 🧠 How Multi-Turn Memory Works

Streamlit reruns the full Python script on every user interaction. Normally, this would reset all variables — making the chatbot forget everything.

**The solution: `st.session_state`**

We store the conversation history in `st.session_state`, which persists across reruns:

```
User types message
       ↓
Append to st.session_state.messages          ← for display in UI
Append to st.session_state.gemini_history    ← for sending to Gemini
       ↓
Call Gemini with FULL gemini_history         ← Gemini sees all past messages
       ↓
Get response → display → save to both lists
       ↓
Next message: repeat with full history
```

Gemini receives the entire conversation every time, so it always has context.

---

## ⚙️ Local Setup

### Step 1: Get a Gemini API Key

1. Go to [https://aistudio.google.com/](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click **"Get API Key"** → **"Create API Key"**
4. Copy your key

### Step 2: Clone / Download the Project

```bash
# If using git
git clone https://github.com/your-username/ai-investment-assistant.git
cd ai-investment-assistant

# Or just create the folder and copy the files manually
```

### Step 3: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Set Up Your API Key

```bash
# Copy the example file
cp .env.example .env

# Open .env and replace the placeholder with your real key
# .env should look like:
# GEMINI_API_KEY=AIza...your_actual_key...
```

> ⚠️ Never share your `.env` file or commit it to Git. Add `.env` to your `.gitignore`.

### Step 6: Run the App

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

## ☁️ Deploying to AWS EC2

### Step 1: Launch an EC2 Instance

1. Go to [AWS Console](https://console.aws.amazon.com/ec2/)
2. Click **"Launch Instance"**
3. Choose: **Ubuntu Server 22.04 LTS** (free tier eligible)
4. Instance type: `t2.micro` (free tier) or `t3.small` for better performance
5. Create or select a key pair (you'll need the `.pem` file to SSH in)
6. **Security Group settings — add these inbound rules:**
   - SSH: Port 22 (your IP)
   - Custom TCP: Port 8501 (anywhere / 0.0.0.0/0) ← Streamlit's default port
7. Launch the instance

### Step 2: Connect to Your EC2 Instance

```bash
# Replace with your actual .pem file path and EC2 public IP
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Step 3: Install Python & Dependencies on EC2

```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Verify
python3 --version
```

### Step 4: Upload Your Project to EC2

**Option A: Using SCP (from your local machine)**
```bash
scp -i your-key.pem -r ./ai-investment-assistant ubuntu@your-ec2-ip:~/
```

**Option B: Using Git**
```bash
# On EC2
sudo apt install git -y
git clone https://github.com/your-username/ai-investment-assistant.git
cd ai-investment-assistant
```

### Step 5: Set Up the App on EC2

```bash
cd ai-investment-assistant

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create your .env file with your API key
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

### Step 6: Run Streamlit on EC2

```bash
# Run on all network interfaces so it's publicly accessible
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Access your app at: `http://your-ec2-public-ip:8501`

### Step 7: Keep It Running After SSH Disconnect (Using screen)

```bash
# Install screen
sudo apt install screen -y

# Start a named screen session
screen -S chatbot

# Inside screen, run the app
source venv/bin/activate
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Detach from screen (app keeps running): Press Ctrl+A, then D

# To reattach later:
screen -r chatbot
```

### Optional: Use a Domain Name

1. Point your domain's A record to the EC2 public IP
2. Use Nginx as a reverse proxy on port 80 → 8501
3. Add SSL with Let's Encrypt (Certbot)

---

## 🔒 Security Tips

- Never hardcode your API key in Python files
- Use IAM roles on EC2 for AWS services instead of access keys
- Restrict SSH access (Port 22) to your IP only
- Rotate your Gemini API key periodically

---

## 🐛 Troubleshooting

| Problem | Solution |
|--------|----------|
| `GEMINI_API_KEY not found` | Make sure `.env` exists and has the correct key |
| Port 8501 not accessible | Check EC2 Security Group inbound rules |
| App crashes on EC2 | Check `python3 --version` is 3.9+ |
| Gemini quota exceeded | Free tier has limits; wait or upgrade plan |

---

## 📚 Resources

- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Streamlit Docs](https://docs.streamlit.io)
- [python-dotenv Docs](https://pypi.org/project/python-dotenv/)

---

> ⚠️ **Disclaimer:** This app is for educational purposes only. It does not constitute financial advice. Always consult a certified financial advisor before making investment decisions.
