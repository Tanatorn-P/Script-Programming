# agentic-data-processor/main.py
import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from config_parser import ConfigParser
from data_agent import DataAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    config_path = os.path.join(os.path.dirname(__file__), 'configs', 'data_pipeline_config.json')
    try:
        parser = ConfigParser(config_path)
        config = parser.load_config()
        
        agent = DataAgent(config)
        agent.run()
    except Exception as e:
        logging.critical(f"Pipeline execution failed: {e}")

if __name__ == "__main__":
    main()