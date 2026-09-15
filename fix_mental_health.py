import re

with open("index.html", "r") as f:
    content = f.read()

# 1. Add Modal CSS
css_to_add = """
        /* ---- Tool Modal ---- */
        .tool-modal-overlay {
            display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); z-index: 1000; align-items: center; justify-content: center;
        }
        .tool-modal {
            background: var(--paper); border: 1px solid var(--line); border-radius: 12px; width: 90%; max-width: 500px; padding: 24px; position: relative; max-height: 90vh; overflow-y: auto;
        }
        .tool-modal-close {
            position: absolute; top: 16px; right: 16px; background: none; border: none; font-size: 24px; cursor: pointer; color: var(--ink-soft); line-height: 1;
        }
        .tool-modal-close:hover { color: var(--ink); }
        
        /* Breathing Tool */
        .breathe-circle {
            width: 200px; height: 200px; border-radius: 50%; background: var(--moss); opacity: 0.8; margin: 40px auto; transition: all 4s linear; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; font-weight: 500;
        }
    </style>
"""
content = content.replace("    </style>", css_to_add)

# 2. Add Modal HTML at the end of body before scripts
modal_html = """
    <!-- Tool Modal -->
    <div id="toolModalOverlay" class="tool-modal-overlay">
        <div class="tool-modal">
            <button class="tool-modal-close" onclick="closeToolModal()">×</button>
            <div id="toolModalContent"></div>
        </div>
    </div>
    
    <script>
"""
content = content.replace("    <script>", modal_html)


# 3. Add onclick handlers to the buttons
mental_health_html = """
                        <div class="option-list">
                            <button class="option-btn" onclick="openBoxBreathing()">Box Breathing (4-4-4-4)</button>
                            <button class="option-btn" onclick="showToast('Vagus Nerve Reset coming soon')">Vagus Nerve Reset</button>
                        </div>
                    </div>
                    <div class="pillar-card">
                        <div class="pillar-head">
                            <span class="pillar-icon">✍️</span>
                            <h3>Journaling</h3>
                        </div>
                        <p>Expressive writing and cognitive reframing.</p>
                        <div class="option-list">
                            <button class="option-btn" onclick="showToast('Gratitude Log coming soon')">Gratitude Log</button>
                            <button class="option-btn" onclick="openBrainDump()">Anxiety Brain Dump</button>
                        </div>
                    </div>
                    <div class="pillar-card">
                        <div class="pillar-head">
                            <span class="pillar-icon">🌙</span>
                            <h3>Sleep</h3>
                        </div>
                        <p>Optimize your circadian rhythm and sleep hygiene.</p>
                        <div class="option-list">
                            <button class="option-btn" onclick="showToast('Sleep Soundscapes coming soon')">Sleep Soundscapes</button>
                            <button class="option-btn" onclick="showToast('Wind-down Routine coming soon')">Wind-down Routine</button>
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
"""

# I need to find the old option list block and replace it carefully. Let's do it via regex or just exact replacements.
def repl(match):
    return mental_health_html

old_pattern = r"""                        <div class="option-list">
                            <button class="option-btn">Box Breathing \(4-4-4-4\)</button>
                            <button class="option-btn">Vagus Nerve Reset</button>
                        </div>
                    </div>
                    <div class="pillar-card">
                        <div class="pillar-head">
                            <span class="pillar-icon">✍️</span>
                            <h3>Journaling</h3>
                        </div>
                        <p>Expressive writing and cognitive reframing.</p>
                        <div class="option-list">
                            <button class="option-btn">Gratitude Log</button>
                            <button class="option-btn">Anxiety Brain Dump</button>
                        </div>
                    </div>
                    <div class="pillar-card">
                        <div class="pillar-head">
                            <span class="pillar-icon">🌙</span>
                            <h3>Sleep</h3>
                        </div>
                        <p>Optimize your circadian rhythm and sleep hygiene.</p>
                        <div class="option-list">
                            <button class="option-btn">Sleep Soundscapes</button>
                            <button class="option-btn">Wind-down Routine</button>
                        </div>
                    </div>
                    <div class="pillar-card">
                        <div class="pillar-head">
                            <span class="pillar-icon">📈</span>
                            <h3>Tracking</h3>
                        </div>
                        <p>Monitor your mood and stress levels over time.</p>
                        <div class="option-list">
                            <button class="option-btn">Daily Mood Check-in</button>
                        </div>"""

content = re.sub(old_pattern, mental_health_html, content, flags=re.MULTILINE)

# 4. Add JavaScript for the tools
js_logic = """
        // --- Mental Health Tools ---
        const modalOverlay = document.getElementById('toolModalOverlay');
        const modalContent = document.getElementById('toolModalContent');
        let breathingInterval = null;

        function closeToolModal() {
            modalOverlay.style.display = 'none';
            modalContent.innerHTML = '';
            if (breathingInterval) {
                clearInterval(breathingInterval);
                breathingInterval = null;
            }
        }

        window.closeToolModal = closeToolModal;

        window.openBoxBreathing = function() {
            modalContent.innerHTML = `
                <h3 style="margin-top:0;">Box Breathing</h3>
                <p>Follow the circle to regulate your nervous system.</p>
                <div id="breatheCircle" class="breathe-circle">Ready</div>
                <button class="primary-btn" id="startBreatheBtn" style="width:100%; justify-content:center;">Start Session</button>
            `;
            modalOverlay.style.display = 'flex';

            document.getElementById('startBreatheBtn').addEventListener('click', () => {
                document.getElementById('startBreatheBtn').style.display = 'none';
                const circle = document.getElementById('breatheCircle');
                const phases = [
                    { text: 'Inhale', scale: '1.5', color: 'var(--moss)' },
                    { text: 'Hold', scale: '1.5', color: 'var(--indigo)' },
                    { text: 'Exhale', scale: '1', color: 'var(--kaki)' },
                    { text: 'Hold', scale: '1', color: 'var(--ink-soft)' }
                ];
                let phaseIndex = 0;

                function nextPhase() {
                    if (!document.getElementById('breatheCircle')) return;
                    circle.innerText = phases[phaseIndex].text;
                    circle.style.transform = `scale(${phases[phaseIndex].scale})`;
                    circle.style.background = phases[phaseIndex].color;
                    phaseIndex = (phaseIndex + 1) % 4;
                }

                nextPhase(); // immediate start
                breathingInterval = setInterval(nextPhase, 4000);
            });
        };

        window.openBrainDump = function() {
            modalContent.innerHTML = `
                <h3 style="margin-top:0;">Anxiety Brain Dump</h3>
                <p>Write out what's bothering you. Our AI will help reframe it objectively.</p>
                <textarea id="brainDumpText" rows="5" style="width:100%; padding:12px; border-radius:4px; border:1px solid var(--line); margin-bottom:16px; background:var(--paper-2); color:var(--ink); font-family:inherit;" placeholder="I feel overwhelmed because..."></textarea>
                <button class="primary-btn" id="brainDumpBtn" style="width:100%; justify-content:center;">Reframe Perspective</button>
                <div id="brainDumpResult" style="margin-top:16px; display:none; padding:16px; background:rgba(31, 63, 88, 0.05); border-left:3px solid var(--indigo); border-radius:0 6px 6px 0; font-size:13.5px;"></div>
            `;
            modalOverlay.style.display = 'flex';

            document.getElementById('brainDumpBtn').addEventListener('click', async () => {
                const text = document.getElementById('brainDumpText').value;
                if (!text.trim()) return;

                document.getElementById('brainDumpBtn').innerText = "Analyzing...";
                document.getElementById('brainDumpBtn').disabled = true;

                try {
                    const res = await fetch('/api/reframe-anxiety', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ anxietyText: text })
                    });
                    const data = await res.json();
                    if (!res.ok) throw new Error(data.error);

                    const resDiv = document.getElementById('brainDumpResult');
                    resDiv.innerHTML = `<strong>Reframed Perspective:</strong><br><br>${data.reframed}`;
                    resDiv.style.display = 'block';
                } catch(err) {
                    showToast('Failed to reframe. ' + err.message);
                } finally {
                    document.getElementById('brainDumpBtn').innerText = "Reframe Perspective";
                    document.getElementById('brainDumpBtn').disabled = false;
                }
            });
        };

        window.openMoodTracker = function() {
            let logs = JSON.parse(localStorage.getItem('moodLogs') || '[]');
            let logsHtml = logs.slice(0, 5).map(l => `<div style="font-size:13px; padding:8px 0; border-bottom:1px solid var(--line);"><strong>${l.date}</strong>: ${l.mood} - ${l.note}</div>`).join('');
            
            modalContent.innerHTML = `
                <h3 style="margin-top:0;">Daily Mood Check-in</h3>
                <div style="display:flex; justify-content:space-between; font-size:32px; cursor:pointer; margin:20px 0;" id="moodEmojis">
                    <span data-mood="Terrible">😫</span>
                    <span data-mood="Bad">🙁</span>
                    <span data-mood="Neutral">😐</span>
                    <span data-mood="Good">🙂</span>
                    <span data-mood="Great">😁</span>
                </div>
                <input type="text" id="moodNote" placeholder="Brief note (optional)" style="width:100%; padding:12px; border-radius:4px; border:1px solid var(--line); margin-bottom:16px; background:var(--paper-2); color:var(--ink); font-family:inherit;">
                <button class="primary-btn" id="saveMoodBtn" style="width:100%; justify-content:center;">Save Log</button>
                
                <h4 style="margin-top:24px; margin-bottom:8px;">Recent Logs</h4>
                <div>${logsHtml || '<div style="font-size:13px; color:var(--ink-soft);">No logs yet.</div>'}</div>
            `;
            modalOverlay.style.display = 'flex';

            let selectedMood = "Neutral";
            document.querySelectorAll('#moodEmojis span').forEach(el => {
                el.addEventListener('click', (e) => {
                    document.querySelectorAll('#moodEmojis span').forEach(s => s.style.transform = 'scale(1)');
                    e.target.style.transform = 'scale(1.3)';
                    selectedMood = e.target.getAttribute('data-mood');
                });
            });

            document.getElementById('saveMoodBtn').addEventListener('click', () => {
                const note = document.getElementById('moodNote').value || "-";
                const log = { date: new Date().toLocaleDateString(), mood: selectedMood, note };
                logs.unshift(log);
                localStorage.setItem('moodLogs', JSON.stringify(logs));
                showToast('Mood logged successfully!');
                closeToolModal();
            });
        };

"""
content = content.replace("        // --- Physical Tabs & BMI ---", js_logic + "\n        // --- Physical Tabs & BMI ---")

with open("index.html", "w") as f:
    f.write(content)
print("Updated index.html")

