import argparse
import sys
from src.agent import MacroAgent

def main():
    parser = argparse.ArgumentParser(description="Macro News Agent CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: run
    parser_run = subparsers.add_parser("run", help="Run the agent loop once")

    # Command: list
    parser_list = subparsers.add_parser("list", help="List saved reports")
    parser_list.add_argument("--days", type=int, default=7, help="Number of days to look back")

    # Command: show
    parser_show = subparsers.add_parser("show", help="Show a specific report")
    parser_show.add_argument("report_id", type=str, help="Filename of the report (e.g., report_20240101.md)")

    args = parser.parse_args()
    
    agent = MacroAgent()

    if args.command == "run":
        agent.run_cycle()
    elif args.command == "list":
        agent.list_reports(days=args.days)
    elif args.command == "show":
        agent.show_report(args.report_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
