import re
import csv
import subprocess
import argparse
from datetime import datetime


class NginxLogAnalyzer:
    LOG_PATTERN = (
        r'(?P<ip>[\d\.]+) - - \[(?P<datetime>[^\]]+)\] "(?P<method>\w+) (?P<path>[^ ]+) HTTP/[^"]+" '
        r'(?P<status>\d+) (?P<size>\d+) "[^"]*" "(?P<agent>[^"]+)"'
    )

    def __init__(self, log_file, output_file):
        self.log_file = log_file
        self.output_file = output_file

    def parse_log_line(self, line):
        match = re.match(self.LOG_PATTERN, line)
        return match.groupdict() if match else None

    def read_logs(self):
        """ Reads the log file and parses each line """
        with open(self.log_file, "r") as file:
            return [self.parse_log_line(line) for line in file if self.parse_log_line(line)]

    def filter_logs(self, logs, ip=None, status=None, method=None, start_date=None, end_date=None):
        """ Filters logs by the specified parameters """
        def log_filter(log):
            if ip and log['ip'] != ip:
                return False
            if status and log['status'] != status:
                return False
            if method and log['method'] != method:
                return False
            if start_date or end_date:
                log_date = datetime.strptime(log['datetime'].split(' ')[0], "%d/%b/%Y:%H:%M:%S")
                if start_date and log_date < start_date:
                    return False
                if end_date and log_date > end_date:
                    return False
            return True

        return list(filter(log_filter, logs))

    def sort_logs(self, logs, key, reverse=False):
        """ Sorts logs by the specified key """
        if key == "size":
            return sorted(logs, key=lambda log: int(log[key]) if log[key].isdigit() else 0, reverse=True)
        return sorted(logs, key=lambda log: log[key], reverse=reverse)

    def write_to_csv(self, logs):
        """ Saves the processed logs to a CSV file """
        fieldnames = ["ip", "datetime", "method", "path", "status", "size", "agent"]
        with open(self.output_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(logs)

    def ensure_git_repo(self):
        """ Checks if the directory is a Git repository and initializes it if necessary """
        try:
            subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print("Initializing Git repository in current directory...")
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True)
            print("Git repository initialized.")

    def commit_to_git(self):
        try:
            # Check if the directory is a Git repository
            subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print("Initializing Git repository in current directory...")
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True)
            print("Git repository initialized.")

        # Add the source CSV file to Git
        subprocess.run(["git", "add", self.output_file], check=True)

        # Check if there are changes before the committee
        status_output = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status_output.stdout.strip():  # Якщо є зміни
            try:
                subprocess.run(["git", "commit", "-m", "Added processed logs to CSV"], check=True)
                print("Changes committed to the local Git repository.")
            except subprocess.CalledProcessError as e:
                print(f"Git commit failed: {e}")
        else:
            print("No changes detected. Skipping commit.")

    def process_logs(self, filters, sort_key=None, reverse=False):
        """ The main process of log processing """
        logs = self.read_logs()
        logs = self.filter_logs(
            logs,
            ip=filters.get("ip"),
            status=filters.get("status"),
            method=filters.get("method"),
            start_date=filters.get("start_date"),
            end_date=filters.get("end_date"),
        )
        if sort_key:
            logs = self.sort_logs(logs, key=sort_key, reverse=reverse)
        self.write_to_csv(logs)
        self.commit_to_git()
        print(f"Logs successfully written to {self.output_file} and committed to Git.")


def parse_arguments():
    """ Processes command line arguments """
    parser = argparse.ArgumentParser(description="Nginx Log Analyzer")
    parser.add_argument("--log-file", type=str, required=True, help="Path to the Nginx log file")
    parser.add_argument("--output-file", type=str, required=True, help="Path to the output CSV file")
    parser.add_argument("--filter-ip", type=str, help="Filter logs by IP address")
    parser.add_argument("--filter-status", type=str, help="Filter logs by status code")
    parser.add_argument("--filter-method", type=str, help="Filter logs by HTTP method")
    parser.add_argument("--filter-start-date", type=str, help="Filter logs from a specific date (format: YYYY-MM-DD)")
    parser.add_argument("--filter-end-date", type=str, help="Filter logs up to a specific date (format: YYYY-MM-DD)")
    parser.add_argument("--sort-by", type=str, choices=["ip", "datetime", "status", "size"], help="Sort logs by a specific field")
    parser.add_argument("--reverse", action="store_true", help="Sort in descending order")
    return parser.parse_args()


def main():
    args = parse_arguments()

    filters = {
        "ip": args.filter_ip,
        "status": args.filter_status,
        "method": args.filter_method,
        "start_date": datetime.strptime(args.filter_start_date, "%Y-%m-%d") if args.filter_start_date else None,
        "end_date": datetime.strptime(args.filter_end_date, "%Y-%m-%d") if args.filter_end_date else None,
    }

    analyzer = NginxLogAnalyzer(log_file=args.log_file, output_file=args.output_file)
    analyzer.process_logs(filters, sort_key=args.sort_by, reverse=args.reverse)


if __name__ == "__main__":
    main()







