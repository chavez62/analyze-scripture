import os
from openai import OpenAI
import textwrap
from dotenv import load_dotenv
from colorama import init, Fore, Style, Back
import re
from typing import Optional, Dict, List
import json
from datetime import datetime
import sqlite3
from pathlib import Path

# Initialize colorama for cross-platform color support
init()


class DatabaseManager:
    def __init__(self, db_path: str = "bible_analysis.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the database with necessary tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scripture TEXT NOT NULL,
                    analysis TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def save_analysis(self, scripture: str, analysis: str):
        """Save analysis results to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT INTO analysis_history (scripture, analysis) VALUES (?, ?)',
                (scripture, analysis)
            )

    def get_recent_analyses(self, limit: int = 5) -> List[Dict]:
        """Retrieve recent analyses"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                'SELECT * FROM analysis_history ORDER BY timestamp DESC LIMIT ?',
                (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]


class BibleSymbolismAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        # Load environment variables from .env file
        load_dotenv()

        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please set it in .env file or pass it directly.")

        self.client = OpenAI(api_key=self.api_key)
        self.db_manager = DatabaseManager()

        # Create output directory for saving analyses
        self.output_dir = Path("analysis_outputs")
        self.output_dir.mkdir(exist_ok=True)

    def analyze_scripture(self, scripture_text: str, include_references: bool = True) -> str:
        """
        Analyzes biblical scripture for symbolic meaning using OpenAI API.

        Args:
            scripture_text (str): The biblical text to analyze
            include_references (bool): Whether to include biblical cross-references

        Returns:
            str: Detailed analysis of the scripture's symbolism
        """
        prompt = self._build_analysis_prompt(
            scripture_text, include_references)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a biblical scholar specializing in Catholic scripture interpretation and symbolism, with expertise in both Old and New Testament analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )

            analysis = response.choices[0].message.content
            formatted_analysis = self._format_analysis(analysis)

            # Save analysis to database
            self.db_manager.save_analysis(scripture_text, analysis)

            # Save analysis to file
            self._save_analysis_to_file(scripture_text, analysis)

            return formatted_analysis

        except Exception as e:
            return f"{Fore.RED}Error analyzing scripture: {str(e)}{Style.RESET_ALL}"

    def _build_analysis_prompt(self, scripture_text: str, include_references: bool) -> str:
        """Build the analysis prompt with optional sections"""
        base_sections = [
            "HISTORICAL CONTEXT:",
            "KEY SYMBOLS:",
            "SPIRITUAL INTERPRETATION:"
        ]

        if include_references:
            base_sections.append("BIBLICAL CONNECTIONS:")
            base_sections.append("RELATED PASSAGES:")

        prompt = f"""
        Analyze the following biblical scripture and provide a detailed interpretation.
        Format your response with these exact headers:
        {chr(10).join(base_sections)}
        
        Scripture:
        {scripture_text}
        
        Please provide specific details and examples for each section.
        For symbols, include their traditional interpretations and cultural significance.
        """
        return prompt

    def _format_analysis(self, analysis: str) -> str:
        """Format the analysis with colors and improved readability"""
        sections = {
            "HISTORICAL CONTEXT:": (Fore.YELLOW, "📚"),
            "KEY SYMBOLS:": (Fore.GREEN, "🔍"),
            "SPIRITUAL INTERPRETATION:": (Fore.CYAN, "✨"),
            "BIBLICAL CONNECTIONS:": (Fore.MAGENTA, "🔗"),
            "RELATED PASSAGES:": (Fore.BLUE, "📖")
        }

        colored_analysis = analysis
        for header, (color, emoji) in sections.items():
            # Color the headers with emoji
            colored_analysis = colored_analysis.replace(
                header,
                f"\n{color}{Style.BRIGHT}{emoji} {header}{Style.RESET_ALL}\n"
            )

            # Format section content
            pattern = f"{header}(.*?)(?={'|'.join(sections.keys())}|$)"
            matches = re.finditer(pattern, analysis, re.DOTALL)

            for match in matches:
                content = match.group(1).strip()
                wrapped_content = "\n".join(
                    textwrap.fill(paragraph.strip(), width=80)
                    for paragraph in content.split("\n")
                )
                colored_analysis = colored_analysis.replace(
                    match.group(1),
                    f"\n{color}{wrapped_content}{Style.RESET_ALL}\n"
                )

        return colored_analysis

    def _save_analysis_to_file(self, scripture: str, analysis: str):
        """Save the analysis to a JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"analysis_{timestamp}.json"

        data = {
            "timestamp": timestamp,
            "scripture": scripture,
            "analysis": analysis
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_analysis_history(self, limit: int = 5) -> List[Dict]:
        """Retrieve recent analysis history"""
        return self.db_manager.get_recent_analyses(limit)


def display_menu():
    """Display the main menu options"""
    menu = f"""
{Back.BLUE}{Fore.WHITE}{Style.BRIGHT} Bible Symbolism Analyzer Menu {Style.RESET_ALL}

1. Analyze New Scripture
2. View Recent Analyses
3. Help
4. Quit

{Fore.CYAN}Select an option (1-4):{Style.RESET_ALL} """
    return input(menu)


def main():
    try:
        analyzer = BibleSymbolismAnalyzer()

        while True:
            choice = display_menu()

            if choice == '1':
                print(
                    f"\n{Fore.GREEN}Enter your scripture text (press Enter twice when done):{Style.RESET_ALL}")
                lines = []
                while True:
                    line = input()
                    if line:
                        lines.append(line)
                    else:
                        break

                scripture = ' '.join(lines)
                if scripture:
                    print(
                        f"\n{Fore.YELLOW}Analyzing scripture...{Style.RESET_ALL}\n")
                    analysis = analyzer.analyze_scripture(scripture)
                    print(analysis)
                else:
                    print(
                        f"{Fore.RED}No text entered. Please try again.{Style.RESET_ALL}")

            elif choice == '2':
                recent_analyses = analyzer.get_analysis_history()
                if recent_analyses:
                    print(f"\n{Fore.CYAN}Recent Analyses:{Style.RESET_ALL}")
                    for idx, analysis in enumerate(recent_analyses, 1):
                        print(
                            f"\n{Fore.YELLOW}Analysis {idx} - {analysis['timestamp']}{Style.RESET_ALL}")
                        print(f"Scripture: {analysis['scripture'][:100]}...")
                else:
                    print(
                        f"{Fore.YELLOW}No previous analyses found.{Style.RESET_ALL}")

            elif choice == '3':
                print(f"""
{Fore.CYAN}Help Information:{Style.RESET_ALL}
• To analyze scripture: Choose option 1 and paste your text
• Each analysis is saved automatically
• View previous analyses using option 2
• Results are saved both to database and JSON files
• Press Enter twice after entering scripture text
                """)

            elif choice == '4':
                print(
                    f"{Fore.GREEN}Thank you for using Bible Symbolism Analyzer!{Style.RESET_ALL}")
                break

            else:
                print(
                    f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")

    except ValueError as e:
        print(f"{Fore.RED}Error: {e}")
        print(
            f"Please ensure your .env file is set up correctly.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
