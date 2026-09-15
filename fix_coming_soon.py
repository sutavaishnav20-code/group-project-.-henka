import re

with open("index.html", "r") as f:
    content = f.read()

# 1. Replace onclick handlers
content = content.replace("onclick=\"showToast('Vagus Nerve Reset coming soon')\"", "onclick=\"openVagusReset()\"")
content = content.replace("onclick=\"showToast('Gratitude Log coming soon')\"", "onclick=\"openGratitudeLog()\"")
content = content.replace("onclick=\"showToast('Sleep Soundscapes coming soon')\"", "onclick=\"openSoundscapes()\"")
content = content.replace("onclick=\"showToast('Wind-down Routine coming soon')\"", "onclick=\"openWindDown()\"")

# 2. Update closeToolModal
old_close = """        function closeToolModal() {
            modalOverlay.style.display = 'none';
            modalContent.innerHTML = '';
            if (breathingInterval) {
                clearInterval(breathingInterval);
                breathingInterval = null;
            }
        }"""

new_close = """        let globalAudioCtx = null;
        let globalNoiseNode = null;
        
        function closeToolModal() {
            modalOverlay.style.display = 'none';
            modalContent.innerHTML = '';
            if (breathingInterval) {
                clearInterval(breathingInterval);
                breathingInterval = null;
            }
            if (globalNoiseNode) { globalNoiseNode.stop(); globalNoiseNode.disconnect(); globalNoiseNode = null; }
            if (globalAudioCtx && globalAudioCtx.state !== 'closed') { globalAudioCtx.close(); globalAudioCtx = null; }
        }"""
content = content.replace(old_close, new_close)

# 3. Append the new JS functions
js_to_append = """

        window.openVagusReset = function() {
            modalContent.innerHTML = `
                <h3 style="margin-top:0;">Vagus Nerve Reset</h3>
                <p style="font-size:14px; color:var(--ink-soft); margin-bottom: 16px;">This exercise shifts your nervous system into a parasympathetic (rest and digest) state.</p>
                <div style="background:var(--paper-2); padding:16px; border-radius:8px; border:1px solid var(--line);">
                    <ol style="padding-left:16px; margin:0; line-height:1.6; font-size: 14.5px;">
                        <li>Interlock your fingers and place them behind your head.</li>
                        <li>Keep your head facing straight forward.</li>
                        <li>Look as far to the <strong>RIGHT</strong> as you comfortably can, using only your eyes.</li>
                        <li>Hold until you yawn, sigh, or swallow (typically 30-60 seconds).</li>
                        <li>Bring your eyes back to center.</li>
                        <li>Repeat looking to the <strong>LEFT</strong>.</li>
                    </ol>
                </div>
                <button class="primary-btn" style="width:100%; justify-content:center; margin-top:20px;" onclick="closeToolModal()">I've Completed This</button>
            `;
            modalOverlay.style.display = 'flex';
        };

        window.openGratitudeLog = function() {
            let logs = JSON.parse(localStorage.getItem('gratitudeLogs') || '[]');
            let logsHtml = logs.slice(0, 5).map(l => `<div style="font-size:13px; padding:8px 0; border-bottom:1px solid var(--line);"><strong>${l.date}</strong>: ${l.text}</div>`).join('');
            
            modalContent.innerHTML = `
                <h3 style="margin-top:0;">Gratitude Log</h3>
                <p style="font-size:14px; color:var(--ink-soft); margin-bottom: 16px;">Writing down things you are grateful for rewires your brain to spot the positive.</p>
                <input type="text" id="gratitudeInput" placeholder="Today I am grateful for..." style="width:100%; padding:12px; border-radius:4px; border:1px solid var(--line); margin-bottom:16px; background:var(--paper-2); color:var(--ink); font-family:inherit;">
                <button class="primary-btn" id="saveGratitudeBtn" style="width:100%; justify-content:center;">Save Entry</button>
                
                <h4 style="margin-top:24px; margin-bottom:8px;">Recent Entries</h4>
                <div>${logsHtml || '<div style="font-size:13px; color:var(--ink-soft);">No entries yet.</div>'}</div>
            `;
            modalOverlay.style.display = 'flex';

            document.getElementById('saveGratitudeBtn').addEventListener('click', () => {
                const text = document.getElementById('gratitudeInput').value.trim();
                if(!text) return;
                const log = { date: new Date().toLocaleDateString(), text };
                logs.unshift(log);
                localStorage.setItem('gratitudeLogs', JSON.stringify(logs));
                showToast('Gratitude logged!');
                closeToolModal();
            });
        };

        window.openSoundscapes = function() {
            modalContent.innerHTML = `
                <h3 style="margin-top:0;">Sleep Soundscapes</h3>
                <p style="font-size:14px; color:var(--ink-soft); margin-bottom: 16px;">Deep synthetic noise to mask background sounds and aid deep sleep.</p>
                <div style="display:flex; gap:12px; flex-direction:column;">
                    <button class="option-btn" id="btnBrownNoise" style="justify-content:center;">▶ Play Brown Noise (Deep & Warm)</button>
                    <button class="option-btn" id="btnPinkNoise" style="justify-content:center;">▶ Play Pink Noise (Balanced)</button>
                    <button class="option-btn" id="btnStopNoise" style="justify-content:center; display:none; color:var(--kaki);">⏹ Stop Audio</button>
                </div>
            `;
            modalOverlay.style.display = 'flex';

            function stopAudio() {
                if (globalNoiseNode) { globalNoiseNode.stop(); globalNoiseNode.disconnect(); globalNoiseNode = null; }
                if (globalAudioCtx && globalAudioCtx.state !== 'closed') { globalAudioCtx.close(); globalAudioCtx = null; }
                document.getElementById('btnStopNoise').style.display = 'none';
            }
            
            function playNoise(type) {
                stopAudio();
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                globalAudioCtx = new AudioContext();
                const bufferSize = globalAudioCtx.sampleRate * 2; // 2 seconds buffer
                const buffer = globalAudioCtx.createBuffer(1, bufferSize, globalAudioCtx.sampleRate);
                const output = buffer.getChannelData(0);
                
                if (type === 'brown') {
                    let lastOut = 0;
                    for (let i = 0; i < bufferSize; i++) {
                        let white = Math.random() * 2 - 1;
                        output[i] = (lastOut + (0.02 * white)) / 1.02;
                        lastOut = output[i];
                        output[i] *= 3.5; // Compensate for volume drop
                    }
                } else if (type === 'pink') {
                    let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
                    for (let i = 0; i < bufferSize; i++) {
                        let white = Math.random() * 2 - 1;
                        b0 = 0.99886 * b0 + white * 0.0555179;
                        b1 = 0.99332 * b1 + white * 0.0750759;
                        b2 = 0.96900 * b2 + white * 0.1538520;
                        b3 = 0.86650 * b3 + white * 0.3104856;
                        b4 = 0.55000 * b4 + white * 0.5329522;
                        b5 = -0.7616 * b5 - white * 0.0168980;
                        output[i] = b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362;
                        output[i] *= 0.11; // Compensate
                        b6 = white * 0.115926;
                    }
                }
                
                globalNoiseNode = globalAudioCtx.createBufferSource();
                globalNoiseNode.buffer = buffer;
                globalNoiseNode.loop = true;
                
                // Add soft gain node so it's not too loud
                const gainNode = globalAudioCtx.createGain();
                gainNode.gain.value = 0.5;
                
                globalNoiseNode.connect(gainNode);
                gainNode.connect(globalAudioCtx.destination);
                globalNoiseNode.start();
                document.getElementById('btnStopNoise').style.display = 'flex';
            }

            document.getElementById('btnBrownNoise').addEventListener('click', () => playNoise('brown'));
            document.getElementById('btnPinkNoise').addEventListener('click', () => playNoise('pink'));
            document.getElementById('btnStopNoise').addEventListener('click', stopAudio);
        };

        window.openWindDown = function() {
            let tasks = JSON.parse(localStorage.getItem('windDownTasks') || '[]');
            if (tasks.length === 0) {
                tasks = [
                    { id: 1, text: 'Dim overhead lights & screens', done: false },
                    { id: 2, text: 'Set room temperature to cool (18°C/65°F)', done: false },
                    { id: 3, text: 'Prepare clothes for tomorrow', done: false },
                    { id: 4, text: 'Read a physical book or listen to audio', done: false }
                ];
            }

            const renderTasks = () => {
                return tasks.map(t => `
                    <div style="display:flex; align-items:center; gap:12px; padding:12px; border-bottom:1px solid var(--line); background:${t.done ? 'var(--paper-2)' : 'transparent'};">
                        <input type="checkbox" id="wd-${t.id}" ${t.done ? 'checked' : ''} style="width:20px; height:20px; cursor:pointer;" onchange="toggleWindDown(${t.id}, this.checked)">
                        <label for="wd-${t.id}" style="cursor:pointer; flex:1; text-decoration:${t.done ? 'line-through' : 'none'}; color:${t.done ? 'var(--ink-soft)' : 'var(--ink)'}; font-size: 14.5px;">${t.text}</label>
                    </div>
                `).join('');
            };

            modalContent.innerHTML = `
                <h3 style="margin-top:0;">Evening Wind-down Routine</h3>
                <p style="font-size:14px; color:var(--ink-soft); margin-bottom: 16px;">Check off these habits to signal to your brain that it's time to rest.</p>
                <div id="windDownList" style="border:1px solid var(--line); border-radius:8px; overflow:hidden;">
                    ${renderTasks()}
                </div>
                <button class="option-btn" style="width:100%; justify-content:center; margin-top:16px;" onclick="resetWindDown()">Reset Routine for Today</button>
            `;
            modalOverlay.style.display = 'flex';

            window.toggleWindDown = function(id, checked) {
                const task = tasks.find(t => t.id === id);
                if(task) task.done = checked;
                localStorage.setItem('windDownTasks', JSON.stringify(tasks));
                document.getElementById('windDownList').innerHTML = renderTasks();
            };

            window.resetWindDown = function() {
                tasks.forEach(t => t.done = false);
                localStorage.setItem('windDownTasks', JSON.stringify(tasks));
                document.getElementById('windDownList').innerHTML = renderTasks();
            };
        };

        // --- End of New Mental Health Tools ---
"""
# Insert before "window.openBoxBreathing =" so it stays grouped, or just before physical tabs
content = content.replace("        window.openBoxBreathing =", js_to_append + "\n        window.openBoxBreathing =")

with open("index.html", "w") as f:
    f.write(content)
print("done")
