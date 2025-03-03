import json
import os
from datetime import datetime

class TaskTracker:
    """
    Simple task tracking system for BROski development
    Helps team members stay updated on progress
    """
    
    def __init__(self, task_file="tasks.json"):
        self.task_file = task_file
        self.tasks = self._load_tasks()
        
    def _load_tasks(self):
        """Load tasks from JSON file or create if doesn't exist"""
        if os.path.exists(self.task_file):
            with open(self.task_file, 'r') as f:
                return json.load(f)
        else:
            # Initialize with default task structure
            return {
                "components": {
                    "configuration": {
                        "status": "in_progress",
                        "tasks": [
                            {"name": "Create config file structure", "status": "completed", "assigned_to": "team"},
                            {"name": "Add config validation", "status": "pending", "assigned_to": "unassigned"}
                        ]
                    },
                    "exchange_connector": {
                        "status": "in_progress",
                        "tasks": [
                            {"name": "Implement price fetching", "status": "completed", "assigned_to": "team"},
                            {"name": "Complete order placement", "status": "pending", "assigned_to": "unassigned"}
                        ]
                    },
                    "strategy_engine": {
                        "status": "in_progress",
                        "tasks": [
                            {"name": "Create signal generation framework", "status": "completed", "assigned_to": "team"},
                            {"name": "Implement RSI strategy", "status": "pending", "assigned_to": "unassigned"}
                        ]
                    },
                    "user_interface": {
                        "status": "in_progress",
                        "tasks": [
                            {"name": "Develop CLI menu", "status": "completed", "assigned_to": "team"},
                            {"name": "Add strategy selection UI", "status": "pending", "assigned_to": "unassigned"}
                        ]
                    }
                },
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.task_file, 'w') as f:
            tasks_copy = self.tasks.copy()
            tasks_copy["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            json.dump(tasks_copy, f, indent=4)
            
    def add_task(self, component, task_name, assigned_to="unassigned"):
        """Add a new task to a component"""
        if component not in self.tasks["components"]:
            self.tasks["components"][component] = {
                "status": "not_started",
                "tasks": []
            }
            
        self.tasks["components"][component]["tasks"].append({
            "name": task_name,
            "status": "pending",
            "assigned_to": assigned_to,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_tasks()
        
    def update_task_status(self, component, task_name, new_status):
        """Update the status of a specific task"""
        if component in self.tasks["components"]:
            for task in self.tasks["components"][component]["tasks"]:
                if task["name"] == task_name:
                    task["status"] = new_status
                    task["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
            # Update component status based on tasks
            tasks = self.tasks["components"][component]["tasks"]
            if all(task["status"] == "completed" for task in tasks):
                self.tasks["components"][component]["status"] = "completed"
            elif any(task["status"] == "completed" for task in tasks):
                self.tasks["components"][component]["status"] = "in_progress"
            else:
                self.tasks["components"][component]["status"] = "not_started"
                
            self.save_tasks()
    
    def generate_report(self):
        """Generate a readable progress report"""
        report = "# BROski Development Progress Report\n\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        total_tasks = 0
        completed_tasks = 0
        
        for component, details in self.tasks["components"].items():
            component_completed = sum(1 for t in details["tasks"] if t["status"] == "completed")
            component_total = len(details["tasks"])
            
            total_tasks += component_total
            completed_tasks += component_completed
            
            report += f"## {component.replace('_', ' ').title()} ({component_completed}/{component_total})\n"
            
            for task in details["tasks"]:
                status_symbol = "✅" if task["status"] == "completed" else "⏳"
                report += f"- {status_symbol} {task['name']} ({task['assigned_to']})\n"
            
            report += "\n"
            
        # Overall progress
        progress_pct = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        report += f"## Overall Progress: {completed_tasks}/{total_tasks} tasks completed ({progress_pct:.1f}%)\n"
        
        return report

if __name__ == "__main__":
    # Example usage
    tracker = TaskTracker()
    
    # Add some tasks
    tracker.add_task("documentation", "Create user guide", "dev_team")
    
    # Update task status
    tracker.update_task_status("configuration", "Create config file structure", "completed")
    
    # Print report
    print(tracker.generate_report())
