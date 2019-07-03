# Twitter Sentiment Analysis Tool
Hello! Welcome to my project. In this tool, we'll take your input (either a Username or Hashtag), run it through my script, and output an easy-to-read analysis of the Twitter content, word usage, and general sentiment (i.e. "Positive" or "Negative"). Let's get started!

## Installation

 1. Fork this GitHub repository.
 2. Open the repository and then open within your command prompt of choice (e.g. Git Bash, Terminal).
 3. Create the Twitter environment: **conda create -n env-twitterfree python=3.7 #**
 4. Activate the Twitter environment: **conda activate env-twitterfree**
 5. Install the required packages: **pip install -r requirements.txt** *(Note: if you encounter any issues of missing packages, please review list of imports at top of twitterfree.py script and ensure all are installed.)*
 6. Create a .env file with your Twitter API credentials (if you do not yet have one, apply at https://developer.twitter.com/). Variables are: CONSUMER_KEY, CONSUMER_SECRET, API_TOKEN, API_SECRET. 
 7. Run the script: **python twitterfree.py** (that's it, you're done!)
 
 
## Requirements

Other than a connection to the Internet, Python (Anaconda package in order to follow above directions), and a terminal/command prompt tool, none!

## Data Directory
Upon running this script, a folder in your installation directory will be created called ".../data/," in which script exports will be stored (.PDF file of charts and .XLSX file of pulled data [5 tabs]). You may freely delete its contents without affecting the script. 

*Note: The charts/data will be automatically exported after each run. To disable, simply comment out all code beginning on line 495 ("CHARTS & EXPORTS"). That will have no adverse impact on the script, but will prevent any data being saved locally.*
