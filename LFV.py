import os
import html
import webbrowser
import argparse
from collections import defaultdict

def find_log_files(search_path):
    log_files = []
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file.endswith('.log'):
                log_files.append(os.path.join(root, file))
    return log_files

def tail_file(file_path, lines=200):  # Increase default lines displayed to 200
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return ''.join(f.readlines()[-lines:])
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='ISO-8859-1') as f:
                return ''.join(f.readlines()[-lines:])
        except Exception as e:
            return f"Error reading file: {str(e)}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def categorize_log_files(log_files):
    categories = defaultdict(list)
    for log_file in log_files:
        category = os.path.dirname(log_file)
        category = category.replace(os.path.expanduser("~") + os.sep, '')
        categories[category].append(log_file)
    return categories

def analyze_log_file(file_path):
    error_count = 0
    event_counts = defaultdict(int)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if 'ERROR' in line:  # Adjust according to log format
                    error_count += 1
                # Example: Count occurrences of various log events
                event = line.split()[0]  # Assume first word is the event type
                event_counts[event] += 1

    except Exception as e:
        return {"error": f"Failed to analyze log: {str(e)}"}

    return {
        "total_lines": sum(event_counts.values()) + error_count,
        "error_count": error_count,
        "event_counts": event_counts
    }

def generate_html(log_files):
    categorized_logs = categorize_log_files(log_files)

    # Store log contents for searching
    log_contents = {}
    for log in log_files:
        log_contents[log] = tail_file(log)

    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Log File Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #121212; color: #e0e0e0; }
        h1 { text-align: center; color: #ffffff; }
        #searchContainer { text-align: center; margin: 20px; }
        #searchBar { width: 300px; padding: 10px; border: none; border-radius: 15px; background-color: #333333; color: #ffffff; }
        #searchButton { padding: 10px; border: none; border-radius: 15px; background-color: #bb86fc; color: #ffffff; cursor: pointer; }
        #searchButton:hover { background-color: #9b68e2; }
        table { width: 100%; margin-top: 20px; border-collapse: collapse; }
        td, th { padding: 10px; border: 1px solid #444444; }
        .log-title { color: #bb86fc; cursor: pointer; }
        .log-title:hover { text-decoration: underline; }
        .log-content { 
            display: none; 
            background-color: #202020; 
            padding: 10px; 
            width: 100%;
            max-width: 100%; 
            height: 400px; 
            overflow-y: scroll; 
            overflow-x: hidden; 
        }
        pre { white-space: pre-wrap; word-wrap: break-word; color: #e0e0e0; }
        .category-title { font-weight: bold; color: #ffffff; cursor: pointer; }

        /* Analysis box style */
        .analysis-box {
            display: inline-block;
            background-color: #333333;
            color: #e0e0e0;
            border-radius: 5px;
            border: 1px solid #444444;
            padding: 5px;
            height: 30px; /* Fixed height */
            width: 100%; /* Full width */
            overflow-x: auto; /* Enable horizontal scrolling */
            white-space: nowrap; /* Prevent text from wrapping */
            margin-top: 5px; /* Space above the analysis box */
        }
    </style>
</head>
<body>

<h1>Log File Viewer</h1>
<div id="searchContainer">
    <input type="text" id="searchBar" onkeyup="filterLogs()" placeholder="Search for log files..." />
    <button id="searchButton" onclick="filterLogs()">🔍</button>
</div>

<table id="logTable">
    <thead>
        <tr>
            <th>Log Files</th>
        </tr>
    </thead>
    <tbody id="logContent">'''

    for category, logs in categorized_logs.items():
        if logs:
            html_content += f'''
                <tr>
                    <td>
                        <div class="category-title" onclick="toggleCategory('{html.escape(category)}')">{html.escape(category)}</div>
                        <table class="sub-table" id="{html.escape(category)}" style="display:none; width:100%; background-color: #1a1a1a;">
                        {''.join(f'''
                            <tr>
                                <td class="log-title" onclick="toggleContent('{html.escape(os.path.basename(log))}')">{html.escape(os.path.basename(log))}</td>
                                <td class="log-content" id="{html.escape(os.path.basename(log))}">
                                    <pre>{html.escape(log_contents[log])}</pre>
                                </td>
                                <td>
                                    <div class="analysis-box" id="analysis-{html.escape(os.path.basename(log))}">
                                        {html.escape(str(analyze_log_file(log)))}
                                    </div>
                                </td>
                            </tr>''' for log in logs)}
                        </table>
                    </td>
                </tr>
            '''

    html_content += '''
    </tbody>
</table>

<script>
var currentlyOpenLog = null;

function filterLogs() {
    var input = document.getElementById('searchBar');
    var filter = input.value.toLowerCase();
    var logTitles = document.getElementsByClassName('log-title');
    var categoryTitles = document.getElementsByClassName('category-title');

    var categoryVisibility = {};

    for (var i = 0; i < logTitles.length; i++) {
        var logTitle = logTitles[i];
        var logRow = logTitle.parentElement.parentElement;
        var logFilePath = logTitle.innerHTML.toLowerCase();

        // Get the log content
        var logContent = logTitle.nextElementSibling.firstElementChild.innerText.toLowerCase();

        if (logFilePath.indexOf(filter) > -1 || logContent.indexOf(filter) > -1) {
            logRow.style.display = '';
            categoryVisibility[logTitle.closest('.sub-table').parentElement.querySelector('.category-title').innerText] = true;
        } else {
            logRow.style.display = 'none';
        }
    }

    for (var j = 0; j < categoryTitles.length; j++) {
        var categoryTitle = categoryTitles[j];
        var categoryShown = categoryVisibility[categoryTitle.innerText] === true;
        categoryTitle.parentElement.style.display = categoryShown ? '' : 'none';
    }
}

function toggleCategory(category) {
    var table = document.getElementById(category);
    if (table.style.display === "none" || table.style.display === "") {
        table.style.display = "block";
    } else {
        table.style.display = "none";
    }
}

function toggleContent(fileName) {
    var content = document.getElementById(fileName);
    
    // If the content is already visible, just toggle it
    if (currentlyOpenLog === fileName) {
        content.style.display = content.style.display === "none" || content.style.display === "" ? "block" : "none";
        toggleAnalysisBox(fileName);
        return; // Exit the function
    }

    // Hide currently open log content if it exists
    if (currentlyOpenLog) {
        document.getElementById(currentlyOpenLog).style.display = "none";
        toggleAnalysisBox(currentlyOpenLog);
    }

    // Show the new log content
    content.style.display = "block";
    toggleAnalysisBox(fileName);

    // Update the currently open log variable
    currentlyOpenLog = fileName;
}

function toggleAnalysisBox(logFile) {
    var analysisBox = document.getElementById('analysis-' + logFile);
    if (document.getElementById(logFile).style.display === "none" || document.getElementById(logFile).style.display === "") {
        analysisBox.style.display = "block"; // Show analysis box
    } else {
        analysisBox.style.display = "none"; // Hide analysis box
    }
}
</script>
</body>
</html>'''

    output_path = '/tmp/index.html'
    with open(output_path, 'w') as f:
        f.write(html_content)

    return output_path

# Entry point for the script
if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description='Log File Viewer')
    parser.add_argument('--path', type=str, default='/', help='Path to search for log files (default: /)')
    args = parser.parse_args()

    log_files = find_log_files(args.path)

    html_path = generate_html(log_files)
    webbrowser.open('file://' + html_path)  # Open the generated HTML file in a web browser
