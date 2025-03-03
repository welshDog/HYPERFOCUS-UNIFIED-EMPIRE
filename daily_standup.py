import os
import json
from datetime import datetime
import argparse
import signal

class DailyStandup:
    """
    Tool to track daily progress and blockers for the BROski project
    Helps keep development on track and document progress
    """
    
    def __init__(self, standup_dir="standups"):
        self.standup_dir = standup_dir
        if not os.path.exists(standup_dir):
            os.makedirs(standup_dir)
    
    def _input_with_timeout(self, prompt, timeout):
        """Handle input with timeout"""
        def handler(signum, frame):
            raise TimeoutError

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout)
        try:
            return input(prompt)
        finally:
            signal.alarm(0)  # Cancel the alarm
    
    def create_standup(self, developer_name):
        """Create a new standup entry for today"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{self.standup_dir}/standup_{today}_{developer_name}.json"
        
        if os.path.exists(filename):
            print(f"Standup for {developer_name} on {today} already exists!")
            return False
        
        standup_data = {
            "date": today,
            "developer": developer_name,
            "completed_yesterday": [],
            "working_on_today": [],
            "blockers": [],
            "notes": "",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Interactive input
        print(f"\n--- Daily Standup: {developer_name} on {today} ---\n")
        
        # What did you complete yesterday?
        print("What did you complete yesterday? (Enter empty line when done)")
        while True:
            try:
                item = self._input_with_timeout("> ", timeout=30)
                if not item:
                    break
                standup_data["completed_yesterday"].append(item)
            except TimeoutError:
                print("\nInput timed out! Moving to the next section.")
                break
        
        # What will you work on today?
        print("\nWhat will you work on today? (Enter empty line when done)")
        while True:
            try:
                item = self._input_with_timeout("> ", timeout=30)
                if not item:
                    break
                standup_data["working_on_today"].append(item)
            except TimeoutError:
                print("\nInput timed out. Moving to the next section.")
                break
                
        # Any blockers?
        print("\nAny blockers for your work? (Enter empty line when done)")
        while True:
            try:
                item = self._input_with_timeout("> ", timeout=30)
                if not item:
                    break
                standup_data["blockers"].append(item)
            except TimeoutError:
                print("\nInput timed out. Moving to the next section.")
                break
        
        # Additional notes
        print("\nAdditional notes:")
        try:
            standup_data["notes"] = self._input_with_timeout("> ", timeout=30)
        except TimeoutError:
            print("\nInput timed out. No additional notes added.")
            standup_data["notes"] = ""
        
        # Save the standup
        with open(filename, 'w') as f:
            json.dump(standup_data, f, indent=4)
        
        print(f"\nStandup for {developer_name} on {today} saved!")
        return True
    
    def list_standups(self, days=7):
        """List recent standups"""
        standups = []
        for filename in os.listdir(self.standup_dir):
            if filename.startswith("standup_") and filename.endswith(".json"):
                with open(os.path.join(self.standup_dir, filename), 'r') as f:
                    standup = json.load(f)
                    standups.append(standup)
        
        import heapq

        # Use a heap to maintain the most recent standups
        recent_standups = heapq.nlargest(days, standups, key=lambda x: x["timestamp"])

        # Print the most recent standups
        for standup in recent_standups:
            print(f"\n=== {standup['date']} - {standup['developer']} ===")
            
            print("\nCompleted:")
            for item in standup["completed_yesterday"]:
                print(f"  ✓ {item}")
            
            print("\nWorking on:")
            for item in standup["working_on_today"]:
                print(f"  → {item}")
            
            print("\nBlockers:")
            if standup["blockers"]:
                for item in standup["blockers"]:
                    print(f"  ⚠ {item}")
            else:
                print("  (none)")
                
            if standup["notes"]:
                print(f"\nNotes: {standup['notes']}")
    
    def _generate_summary_report(self):
        """Generate a summary report of all active work and blockers"""
        today = datetime.now().strftime("%Y-%m-%d")
        standups = []
        
        # Initialize the report with a header
        report = f"# BROski Project Status Report - {today}\n\n"
        
        for filename in os.listdir(self.standup_dir):
            if filename.startswith("standup_") and filename.endswith(".json"):
                with open(os.path.join(self.standup_dir, filename), 'r') as f:
                    standup = json.load(f)
                    standups.append(standup)
        
        # Get the most recent standup for each developer
        developer_standups = {}
        for standup in standups:
            dev = standup["developer"]
            if dev not in developer_standups or standup["date"] > developer_standups[dev]["date"]:
                developer_standups[dev] = standup
        
        # Active work
        report += "## Current Work in Progress\n\n"
        for dev, standup in developer_standups.items():
            for item in standup["working_on_today"]:
                report += f"- {item} ({dev})\n"
        
        # Blockers
        report += "\n## Current Blockers\n\n"
        has_blockers = False
        for dev, standup in developer_standups.items():
            for item in standup["blockers"]:
                report += f"- ⚠ {item} ({dev})\n"
                has_blockers = True
        
        if not has_blockers:
            report += "- No current blockers reported\n"
        
        # Save the report
        with open("summary_report.txt", 'w') as f:
            f.write(report)
        
        print(f"Summary report generated: summary_report.txt")
        return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BROski Daily Standup Tool")
    parser.add_argument("action", choices=["create", "list", "report"], help="Action to perform: 'create' to create a new standup, 'list' to list recent standups, 'report' to generate a summary report")
    parser.add_argument("--dev", "-d", help="Developer name (required for 'create' action)")
    parser.add_argument("--days", type=int, default=7, help="Number of days to list recent standups (default: 7)")
    
    args = parser.parse_args()
    if not os.path.exists("standups"):
        os.makedirs("standups")
    standup = DailyStandup()
    
    if args.action == "create":
        if not args.dev:
            parser.error("Developer name is required for create action")
        standup.create_standup(args.dev)
    elif args.action == "list":
        standup.list_standups(args.days)
    elif args.action == "report":
        standup._generate_summary_report()
