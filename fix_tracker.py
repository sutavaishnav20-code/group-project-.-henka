import re

with open("index.html", "r") as f:
    content = f.read()

# Add d3.js script
if "d3.v7.min.js" not in content:
    content = content.replace("</head>", "    <script src=\"https://d3js.org/d3.v7.min.js\"></script>\n</head>")

# Find tab-tracker
tracker_pattern = r"(<div id=\"tab-tracker\" class=\"tab-content\">.*?<div class=\"coach-panel\">)(.*?)(<button id=\"startCameraBtn\" class=\"primary-btn\" style=\"margin-bottom: 16px;\">)"

def replacer(match):
    prefix = match.group(1)
    middle = match.group(2)
    suffix = match.group(3)
    
    # Add new options to select
    middle = middle.replace("</select>", "    <option value=\"planks\">Planks (Timed)</option>\n                                </select>")
    
    # Add the Chart and Download button above the camera btn
    new_ui = """
                        <div style="display: flex; gap: 12px; margin-bottom: 16px; margin-top: 16px;">
                            <button id="downloadReportBtn" class="option-btn" style="flex: 1; justify-content: center;">📄 Download Report</button>
                        </div>
                        
                        <div id="trackerChartContainer" style="margin-bottom: 24px; padding: 16px; background: var(--paper-2); border-radius: 8px; border: 1px solid var(--line);">
                            <h4 style="margin-bottom: 12px; font-size: 14px; color: var(--ink-soft);">Weekly Progress (Reps/Secs)</h4>
                            <div id="d3Chart" style="width: 100%; height: 200px;"></div>
                        </div>
                        """
    return prefix + middle + new_ui + suffix

new_content = re.sub(tracker_pattern, replacer, content, flags=re.DOTALL)

with open("index.html", "w") as f:
    f.write(new_content)
