# Windows

Copy your API key from wherever you got it.

Open Environment Variables:

Press Win + R, type sysdm.cpl, hit Enter.

Go to the Advanced tab → Environment Variables.

Create a new variable:

Under User variables (or System variables if you want it globally), click New.

Name it: GEMINI_API_KEY.

Paste your key as the value.

Save → OK your way out of the dialogs.

Restart your terminal/IDE because Windows doesn’t believe in instant updates.

Test in terminal:

echo %GEMINI_API_KEY%

# Linux / macOS

Open your shell config file (.bashrc, .zshrc, or whatever flavor you’ve cursed yourself with).

Add this line:

export GEMINI_API_KEY="your_api_key_here"


Save the file.

Reload it:

source ~/.bashrc   # or ~/.zshrc


Test:

echo $GEMINI_API_KEY
