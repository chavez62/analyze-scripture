import os
from openai import OpenAI
import textwrap
from dotenv import load_dotenv
from colorama import init, Fore, Style, Back
import re

# Initialize colorama for cross-platform color support
init()

class BibleSymbolismAnalyzer:
    def __init__(self, api_key=None):
        # Load environment variables from .env file
        load_dotenv()
        
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set it in .env file or pass it directly.")
            
        self.client = OpenAI(api_key=self.api_key)

    def analyze_scripture(self, scripture_text):
        """
        Analyzes biblical scripture for symbolic meaning using OpenAI API.
        
        Args:
            scripture_text (str): The biblical text to analyze
        
        Returns:
            str: Detailed analysis of the scripture's symbolism
        """
        prompt = f"""
        Analyze the following biblical scripture and explain its symbolic meaning. 
        Format your response with these exact headers:
        HISTORICAL CONTEXT:
        KEY SYMBOLS:
        SPIRITUAL INTERPRETATION:
        BIBLICAL CONNECTIONS:
        
        Scripture:
        {scripture_text}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a biblical scholar specializing in Catholic scripture interpretation and symbolism."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            analysis = response.choices[0].message.content
            return self._format_analysis(analysis)
            
        except Exception as e:
            return f"{Fore.RED}Error analyzing scripture: {str(e)}{Style.RESET_ALL}"
    
    def _format_analysis(self, analysis):
        """Format the analysis with colors and improved readability"""
        # Color scheme for different sections
        sections = {
            "HISTORICAL CONTEXT:": Fore.YELLOW,
            "KEY SYMBOLS:": Fore.GREEN,
            "SPIRITUAL INTERPRETATION:": Fore.CYAN,
            "BIBLICAL CONNECTIONS:": Fore.MAGENTA
        }
        
        # Add colors to section headers and format content
        colored_analysis = analysis
        for header, color in sections.items():
            # Color the headers
            colored_analysis = colored_analysis.replace(
                header,
                f"\n{color}{Style.BRIGHT}{header}{Style.RESET_ALL}\n"
            )
            
            # Find the content between this header and the next
            pattern = f"{header}(.*?)(?={'|'.join(sections.keys())}|$)"
            matches = re.finditer(pattern, analysis, re.DOTALL)
            
            for match in matches:
                content = match.group(1).strip()
                # Wrap text while preserving paragraphs
                wrapped_content = "\n".join(
                    textwrap.fill(paragraph.strip(), width=80)
                    for paragraph in content.split("\n")
                )
                colored_analysis = colored_analysis.replace(
                    match.group(1),
                    f"\n{color}{wrapped_content}{Style.RESET_ALL}\n"
                )
        
        return colored_analysis

def main():
    try:
        analyzer = BibleSymbolismAnalyzer()
        
        print(f"{Back.BLUE}{Fore.WHITE}{Style.BRIGHT} Welcome to the Bible Symbolism Analyzer {Style.RESET_ALL}")
        print(f"{Fore.CYAN}Enter 'quit' to exit{Style.RESET_ALL}")
        
        while True:
            print(f"\n{Fore.GREEN}Paste your scripture text (press Enter twice when done):{Style.RESET_ALL}")
            lines = []
            while True:
                line = input()
                if line:
                    lines.append(line)
                else:
                    break
            
            scripture = ' '.join(lines)
            if scripture.lower() == 'quit':
                break
            
            if scripture:
                print(f"\n{Fore.YELLOW}Analyzing scripture...{Style.RESET_ALL}\n")
                analysis = analyzer.analyze_scripture(scripture)
                print(analysis)
            else:
                print(f"{Fore.RED}No text entered. Please try again.{Style.RESET_ALL}")
                
    except ValueError as e:
        print(f"{Fore.RED}Error: {e}")
        print(f"Please ensure your .env file is set up correctly.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()