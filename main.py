from cli.interface import CLIInterface
from managers.data_manager import DataManager
from managers.export_manager import ExportManager
import logging

def main():
    """Main function to run the EduPlatform CLI"""
    try:
        # Initialize core components
        data_manager = DataManager()
        export_manager = ExportManager(data_manager)
        cli = CLIInterface(data_manager, export_manager)

        # Run the application
        cli.run()

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        logging.error(f"Application error: {e}")
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()