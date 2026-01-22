
# ☁️ Deploying RSI Divergence Bot on PythonAnywhere

Follow these steps to deploy your bot on [PythonAnywhere](https://www.pythonanywhere.com/).

## 1. Open a Bash Console
1. Log in to your PythonAnywhere dashboard.
2. Click on **Consoles** → **Bash**.

## 2. Clone the Repository
Run the following command to download your code:
```bash
git clone https://github.com/ronadasakalesha/RSI-Divergence.git
cd RSI-Divergence
```

## 3. Create a Virtual Environment
It's best practice to use a virtual environment.
```bash
# Create a virtual environment named 'rsi_bot'
mkvirtualenv --python=/usr/bin/python3.10 rsi_bot

# If mkvirtualenv is not found (rare), use standard venv:
# python3 -m venv venv
# source venv/bin/activate
```
*Note: Your console will now show `(rsi_bot)` at the start of the line.*

## 4. Install Dependencies
Install the required libraries:
```bash
pip install -r requirements.txt
```

## 5. Configure Environment Variables
You need to create your `.env` file with your credentials.
```bash
# Copy the example file
cp .env.example .env

# Edit the file using nano or vim
nano .env
```
*   Paste your **Angel One API Key**, **Client ID**, **Password**, **TOTP Secret**, and **Telegram Keys**.
*   Press `Ctrl+X`, then `Y`, then `Enter` to save and exit.

## 6. Run the Bot
To verify everything is working, run the bot manually:
```bash
python src/main.py
```
If you see `[SUCCESS] Login successful!`, the bot is running. Press `Ctrl+C` to stop it.

## 7. Run Continuously (24/7)

### Option A: "Always On" Task (Paid Accounts - Recommended)
1. Go to the **Tasks** tab in your dashboard.
2. Scroll to **Always-on tasks**.
3. Enter the command:
   ```bash
   /home/yourusername/.virtualenvs/rsi_bot/bin/python /home/yourusername/RSI-Divergence/src/main.py
   ```
   *(Replace `yourusername` with your actual PythonAnywhere username)*.
4. Click **Create**.
5. The bot will now restart automatically if it crashes or the server reboots.

### Option B: Scheduled Task (Free Accounts)
Free accounts cannot use "Always On". You can use a daily scheduled task, but it has execution limits (usually 1 hour).
1. Go to **Tasks**.
2. Create a daily task with the same command as above.
3. *Note: This is not ideal for a continuous trading bot on a free account.*

### Option C: Manual Console (Free Accounts)
1. Keep the **Bash console open** running `python src/main.py`.
2. Note that PythonAnywhere may kill the process if the console is inactive for too long.
