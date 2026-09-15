import re

with open("index.html", "r") as f:
    html = f.read()

# Fix for sleep chart width
sleep_chart_width_fix = """
            const clientWidth = container.clientWidth || 300; // Fallback width
            const width = Math.max(clientWidth - margin.left - margin.right, 200); // Minimum width
"""
html = re.sub(
    r"const width = container.clientWidth - margin.left - margin.right;",
    sleep_chart_width_fix,
    html
)

# Fix for fitness chart width (renderChart)
render_chart_width_fix = """
            const clientWidth = chartContainer.clientWidth || 300;
            const width = Math.max(clientWidth - margin.left - margin.right, 200);
"""
html = re.sub(
    r"const width = chartContainer.clientWidth - margin.left - margin.right;",
    render_chart_width_fix,
    html
)

# Trigger render on switchView
switch_view_trigger = """
            if (targetView) {
                targetView.classList.add('active');
                
                // Re-render charts when their container becomes visible
                if(viewId === 'view-mental' && typeof renderSleepChart === 'function') {
                    setTimeout(renderSleepChart, 50);
                }
                if(viewId === 'view-physical' && typeof window.renderChart === 'function') {
                    setTimeout(window.renderChart, 50);
                }
            }
"""
html = re.sub(
    r"if \(targetView\) \{\s*targetView\.classList\.add\('active'\);\s*\}",
    switch_view_trigger,
    html
)

# Trigger render on switchPhysicalTab
switch_physical_tab_trigger = """
            document.getElementById(tabId).classList.add('active');
            if (tabId === 'tab-tracker' && typeof window.renderChart === 'function') {
                setTimeout(window.renderChart, 50);
            }
"""
html = re.sub(
    r"document\.getElementById\(tabId\)\.classList\.add\('active'\);",
    switch_physical_tab_trigger,
    html
)

with open("index.html", "w") as f:
    f.write(html)
print("Done")
