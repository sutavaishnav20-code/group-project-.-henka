import re

with open("index.html", "r") as f:
    html = f.read()

sleep_quality_block = """
                    <div class="pillar-card" style="grid-column: 1 / -1;">
                        <div class="pillar-head">
                            <span class="pillar-icon">📊</span>
                            <h3>Sleep Quality Trend</h3>
                        </div>
                        <p style="margin-bottom: 16px;">Track your deep sleep cycles and restfulness.</p>
                        <div style="background: var(--paper-2); padding: 16px; border-radius: 8px; border: 1px solid var(--line);">
                            <div id="sleepChart" style="width: 100%; height: 160px;"></div>
                        </div>
                    </div>
"""

tracking_block = """
                    <div class="pillar-card">
                        <div class="pillar-head">
                            <span class="pillar-icon">📈</span>
                            <h3>Tracking</h3>
                        </div>
                        <p>Monitor your mood and stress levels over time.</p>
                        <div class="option-list">
                            <button class="option-btn" onclick="openMoodTracker()">Daily Mood Check-in</button>
                        </div>

                    </div>
"""

# Let's locate the exact substring we want to replace
target_html = """
                    <div class="pillar-card" style="grid-column: 1 / -1;">
                        <div class="pillar-head">
                            <span class="pillar-icon">📊</span>
                            <h3>Sleep Quality Trend</h3>
                        </div>
                        <p style="margin-bottom: 16px;">Track your deep sleep cycles and restfulness.</p>
                        <div style="background: var(--paper-2); padding: 16px; border-radius: 8px; border: 1px solid var(--line);">
                            <div id="sleepChart" style="width: 100%; height: 160px;"></div>
                        </div>
                    </div>

                    <div class="pillar-card">
                        <div class="pillar-head">
                            <span class="pillar-icon">📈</span>
                            <h3>Tracking</h3>
                        </div>
                        <p>Monitor your mood and stress levels over time.</p>
                        <div class="option-list">
                            <button class="option-btn" onclick="openMoodTracker()">Daily Mood Check-in</button>
                        </div>

                    </div>
"""

replacement_html = """
                    <div class="pillar-card">
                        <div class="pillar-head">
                            <span class="pillar-icon">📈</span>
                            <h3>Tracking</h3>
                        </div>
                        <p>Monitor your mood and stress levels over time.</p>
                        <div class="option-list">
                            <button class="option-btn" onclick="openMoodTracker()">Daily Mood Check-in</button>
                        </div>
                    </div>

                    <div class="pillar-card" style="grid-column: 1 / -1;">
                        <div class="pillar-head">
                            <span class="pillar-icon">📊</span>
                            <h3>Sleep Quality Trend</h3>
                        </div>
                        <p style="margin-bottom: 16px;">Track your deep sleep cycles and restfulness.</p>
                        <div style="background: var(--paper-2); padding: 16px; border-radius: 8px; border: 1px solid var(--line);">
                            <div id="sleepChart" style="width: 100%; height: 160px;"></div>
                        </div>
                    </div>
"""

# Clean the whitespace to do a more robust regex or direct replace
# Because whitespace might differ, we can just cut out the sleep block and put it after tracking.

pattern = r'(<div class="pillar-card" style="grid-column: 1 / -1;">\s*<div class="pillar-head">\s*<span class="pillar-icon">📊</span>\s*<h3>Sleep Quality Trend</h3>.*?</div>\s*</div>)(\s*)(<div class="pillar-card">\s*<div class="pillar-head">\s*<span class="pillar-icon">📈</span>\s*<h3>Tracking</h3>.*?</div>\s*</div>)'

def replacer(match):
    sleep_block = match.group(1)
    space = match.group(2)
    tracking = match.group(3)
    return tracking + space + sleep_block

new_html = re.sub(pattern, replacer, html, flags=re.DOTALL)

with open("index.html", "w") as f:
    f.write(new_html)

print("Done")
