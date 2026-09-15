import re

with open('index.html', 'r') as f:
    html = f.read()

# 2. Add tab content
tab_content = """
                <div id="tab-walk" class="tab-content">
                    <div class="coach-panel">
                        <h3>Walk & Run Tracker</h3>
                        <p>Track your real-world movement using GPS. Maps will render if a Google Maps API Key is provided.</p>
                        
                        <div style="display: flex; gap: 12px; margin-bottom: 24px;">
                            <button id="startWalkBtn" class="primary-btn" style="flex: 1; justify-content: center;">Start Walk</button>
                            <button id="stopWalkBtn" class="option-btn" style="flex: 1; justify-content: center; display: none; background: rgba(220, 38, 38, 0.1); color: #dc2626; border: 1px solid #dc2626;">End Walk</button>
                        </div>
                        
                        <div class="pillar-grid" style="margin-bottom: 24px;">
                            <div class="pillar-card" style="padding: 16px; text-align: center;">
                                <div style="font-size: 24px; font-weight: 600; color: var(--indigo);" id="walkDistance">0.00</div>
                                <div style="font-size: 12px; color: var(--ink-soft); text-transform: uppercase;">Kilometers</div>
                            </div>
                            <div class="pillar-card" style="padding: 16px; text-align: center;">
                                <div style="font-size: 24px; font-weight: 600; color: var(--moss);" id="walkSteps">0</div>
                                <div style="font-size: 12px; color: var(--ink-soft); text-transform: uppercase;">Est. Steps</div>
                            </div>
                            <div class="pillar-card" style="padding: 16px; text-align: center;">
                                <div style="font-size: 24px; font-weight: 600; color: #A15A2E;" id="walkCals">0</div>
                                <div style="font-size: 12px; color: var(--ink-soft); text-transform: uppercase;">Calories (kcal)</div>
                            </div>
                            <div class="pillar-card" style="padding: 16px; text-align: center;">
                                <div style="font-size: 24px; font-weight: 600; color: var(--ink);" id="walkTime">00:00</div>
                                <div style="font-size: 12px; color: var(--ink-soft); text-transform: uppercase;">Duration</div>
                            </div>
                        </div>

                        <div id="mapContainer" style="width: 100%; height: 300px; background: var(--paper-2); border-radius: 8px; border: 1px solid var(--line); display: flex; align-items: center; justify-content: center; overflow: hidden; position: relative;">
                            <span style="color: var(--ink-soft); font-size: 14px; text-align: center; padding: 16px;" id="mapPlaceholder">Loading GPS... (Configure Google Maps API Key in Secrets to render actual map)</span>
                        </div>
                    </div>
                </div>
"""

html = html.replace("<!-- 3. NUTRITION VIEW -->", tab_content + "\n            <!-- 3. NUTRITION VIEW -->")

with open('index.html', 'w') as f:
    f.write(html)
print("Done inserting tab content")
