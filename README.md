# Log File Viewer

Log File Viewer is a Python script designed to search for and display log files on your system in a categorized and user-friendly HTML format. The script scans your root directory (and its subdirectories) for `.log` files, extracts the last 200 lines from each log file, and generates an HTML page that allows for easy navigation and searching among logs.

## Features

- **Find Log Files**: Recursively traverses directories to find all log files.
- **Log Tail**: Extracts the last 200 lines of each log file for quick viewing.
- **Categorization**: Organizes log files based on their directories.
- **Search Functionality**: Includes a search bar to filter log file results dynamically.
- **Interactive HTML UI**: Users can click to expand/collapse log categories and view logs without needing terminal access.

## Requirements

- Python 3.x

## Usage
1. Run the script. 
2. It will search the specified directory for `.log` files.
3. An HTML file (`index.html`) will be generated in the `/tmp` directory.
4. The script will automatically open the HTML file in your default web browser.
5. Use the search box to filter the log entries, and click on category titles to expand or collapse the list of logs.

## Customization
- You can customize the `search_path` variable in the script to point to any directory on your system where you want to search for log files.
- HTML and CSS styles can be modified within the script to better fit your preferences.

## Error Handling
The script includes basic error handling capabilities:
- It handles Unicode decode errors when reading log files to prevent crashes.
- It captures general exceptions during the file reading process and informs the user of any problems encountered.

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements or fixes.

