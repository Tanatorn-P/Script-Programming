# agentic-spreadsheet-processor/main.py
import sys
import os

# Add 'src' directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils import setup_logging
from config_parser import ConfigParser
from spreadsheet_agent import SpreadsheetAgent

logger = setup_logging(__name__)

def main():
    """Main execution function."""
    config_file_path = os.path.join(os.path.dirname(__file__), 'configs', 'example_spreadsheet_config.json')

    try:
        os.makedirs('data', exist_ok=True)
        logger.info(f"Loading config from: {config_file_path}")

        parser = ConfigParser(config_file_path)
        config = parser.load_config()

        input_file = config.get("input_file")
        if not os.path.exists(input_file):
            logger.critical(f"Input file '{input_file}' not found. Please run 'python create_input_data.py' first.")
            return

        agent = SpreadsheetAgent(config)
        agent.run()

    except Exception as e:
        logger.critical(f"Execution failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()