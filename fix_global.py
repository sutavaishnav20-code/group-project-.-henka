import re
with open('index.html', 'r') as f:
    html = f.read()
html = html.replace("function renderSleepChart() {", "window.renderSleepChart = function() {")
html = html.replace("typeof renderSleepChart === 'function'", "typeof window.renderSleepChart === 'function'")
html = html.replace("setTimeout(renderSleepChart, 50)", "setTimeout(window.renderSleepChart, 50)")
html = html.replace("setTimeout(renderSleepChart, 600)", "setTimeout(window.renderSleepChart, 600)")
html = html.replace("window.addEventListener('resize', renderSleepChart)", "window.addEventListener('resize', window.renderSleepChart)")
with open('index.html', 'w') as f:
    f.write(html)
print("Done")
