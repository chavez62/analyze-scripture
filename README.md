# Bible Symbolism Analyzer 📖✨
A Python-based tool that leverages OpenAI's GPT-4 to analyze Catholic biblical scriptures and provide detailed symbolic interpretations with color-coded output.

## Features 🌟

+ Analyzes biblical passages using OpenAI's GPT-4
+ Provides detailed analysis including:
  + Historical Context
  + Key Symbols
  + Spiritual Interpretation
  + Biblical Connections
+ Color-coded output for improved readability
+ Secure API key management using environment variables
+ Cross-platform color support
+ User-friendly command-line interface

## Prerequisites 📋
Before running the analyzer, make sure you have:
+ Python 3.6 or higher
+ An OpenAI API key

## Installation 🚀
1. Clone the repository:

```bash
Copygit clone https://github.com/yourusername/bible-symbolism-analyzer.git
cd bible-symbolism-analyzer
```
2. Install required packages:

```bash
Copypip install openai python-dotenv colorama
```
3. Create a .env file in the project root:

```bash
Copytouch .env
```
4. Add your OpenAI API key to the .env file:

```Copy
OPENAI_API_KEY=your-api-key-here
```
## Usage 💡

1. Run the script:

```bash
Copypython bible_analyzer.py
```

2. When prompted, paste your scripture text and press Enter twice to submit.
3. View the color-coded analysis:

+ 🟡 Historical Context (Yellow)
+ 🟢 Key Symbols (Green)
+ 🔵 Spiritual Interpretation (Cyan)
+ 🟣 Biblical Connections (Magenta)

4. Type 'quit' to exit the program.

## Example Output 📝
```Copy
Welcome to the Bible Symbolism Analyzer
Enter 'quit' to exit

Paste your scripture text (press Enter twice when done):
[Your scripture text here]

Analyzing scripture...

HISTORICAL CONTEXT:
[Historical analysis appears here in yellow]

KEY SYMBOLS:
[Symbol analysis appears here in green]

SPIRITUAL INTERPRETATION:
[Spiritual analysis appears here in cyan]

BIBLICAL CONNECTIONS:
[Biblical connections appear here in magenta]
```
## Configuration ⚙️
The script uses the following default settings:
+ GPT-4 model (can be modified to use GPT-3.5-turbo)
+ Temperature: 0.7 (controls response creativity)
+ Max tokens: 1000 (controls response length)

## Security Notes 🔒
+ Never commit your .env file to version control
+ Add .env to your .gitignore file
+ Keep your API key secure and rotate it regularly

## Error Handling 🚨
The script includes error handling for:
+ Missing API keys
+ Invalid API responses
+ Empty input validation
+ Connection issues

## License 📄
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏
+ OpenAI for providing the GPT-4 API
+ Colorama for cross-platform color support
+ Python-dotenv for environment management
