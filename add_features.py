import re

with open("index.html", "r") as f:
    html = f.read()

# 1. Posture Correction Sound
sound_js = """
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        let lastWarningTime = 0;
        function playFormWarningSound() {
            if (!audioCtx) return;
            if (Date.now() - lastWarningTime < 2000) return; // debounce 2s
            lastWarningTime = Date.now();
            
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            
            oscillator.type = 'triangle';
            oscillator.frequency.setValueAtTime(440, audioCtx.currentTime); 
            oscillator.frequency.exponentialRampToValueAtTime(220, audioCtx.currentTime + 0.3); 
            
            gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
            
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            oscillator.start();
            oscillator.stop(audioCtx.currentTime + 0.3);
        }
"""
html = html.replace("// --- Init ---", sound_js + "\n        // --- Init ---")

# Replace form broken logic with sound trigger
html = html.replace("feedbackEl.innerText = 'Form broken. Resume plank.';", "feedbackEl.innerText = 'Form broken. Resume plank.'; playFormWarningSound();")
html = html.replace("feedbackEl.innerText = 'Go lower...';", "feedbackEl.innerText = 'Go lower...'; playFormWarningSound();")
html = html.replace("feedbackEl.innerText = 'Go up!';", "feedbackEl.innerText = 'Go up!'; playFormWarningSound();")
html = html.replace("feedbackEl.innerText = 'Push up!';", "feedbackEl.innerText = 'Push up!'; playFormWarningSound();")
html = html.replace("feedbackEl.innerText = 'Squeeze & lower...';", "feedbackEl.innerText = 'Squeeze & lower...'; playFormWarningSound();")

# 2. Nutrition Alerts
nutri_alerts_html = """
                    <div id="nutritionAlertContainer" style="margin-bottom: 24px; padding: 16px; background: var(--paper-2); border-radius: 8px; border: 1px solid var(--line);">
                        <h4 style="margin-bottom: 12px; font-size: 14px; color: var(--ink-soft); display: flex; align-items: center; gap: 8px;">
                            <span>⚠️</span> Nutrition Alerts & Reminders
                        </h4>
                        <div style="display: flex; flex-direction: column; gap: 12px;">
                            <div style="padding: 12px; background: var(--paper); border-left: 4px solid var(--moss); border-radius: 4px; font-size: 13px;">
                                <strong>Hydration:</strong> You are 3 glasses behind your daily water goal.
                            </div>
                            <div style="padding: 12px; background: var(--paper); border-left: 4px solid #A15A2E; border-radius: 4px; font-size: 13px;">
                                <strong>Protein Target:</strong> Make sure your next meal is protein-rich to hit your daily macro goal.
                            </div>
                        </div>
                    </div>
"""
# Insert above macro calculator in nutrition tab
html = html.replace('<div id="nutri-macro" class="tab-content active">', '<div id="nutri-macro" class="tab-content active">\n' + nutri_alerts_html)


# 3. Sleep Quality Chart
sleep_chart_html = """
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
# Insert after sleep card
html = html.replace("""<button class="option-btn" onclick="openWindDown()">Wind-down Routine</button>
                        </div>
                    </div>""", """<button class="option-btn" onclick="openWindDown()">Wind-down Routine</button>
                        </div>
                    </div>""" + "\n" + sleep_chart_html)

# Add sleep chart JS
sleep_chart_js = """
        function renderSleepChart() {
            if (typeof d3 === 'undefined') return;
            const container = document.getElementById('sleepChart');
            if (!container) return;
            
            d3.select('#sleepChart').selectAll('*').remove();
            
            const sleepData = [
                { day: 'Mon', score: 65 },
                { day: 'Tue', score: 72 },
                { day: 'Wed', score: 58 },
                { day: 'Thu', score: 85 },
                { day: 'Fri', score: 90 },
                { day: 'Sat', score: 78 },
                { day: 'Sun', score: 88 }
            ];
            
            const margin = {top: 10, right: 10, bottom: 20, left: 30};
            const width = container.clientWidth - margin.left - margin.right;
            const height = 160 - margin.top - margin.bottom;

            const svg = d3.select('#sleepChart')
              .append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
              .append('g')
                .attr('transform', `translate(${margin.left},${margin.top})`);

            const x = d3.scalePoint()
              .domain(sleepData.map(d => d.day))
              .range([0, width])
              .padding(0.5);

            const y = d3.scaleLinear()
              .domain([0, 100])
              .range([height, 0]);

            svg.append('g')
              .attr('transform', `translate(0,${height})`)
              .call(d3.axisBottom(x).tickSize(0).tickPadding(8))
              .call(g => g.select('.domain').attr('stroke', 'var(--line)'))
              .selectAll('text').attr('fill', 'var(--ink-faint)');

            svg.append('g')
              .call(d3.axisLeft(y).ticks(3).tickSize(-width))
              .call(g => g.select('.domain').remove())
              .call(g => g.selectAll('.tick line').attr('stroke', 'var(--line)').attr('stroke-dasharray', '2,2'))
              .selectAll('text').attr('fill', 'var(--ink-faint)');

            const line = d3.line()
              .x(d => x(d.day))
              .y(d => y(d.score))
              .curve(d3.curveBasis);

            svg.append('path')
              .datum(sleepData)
              .attr('fill', 'none')
              .attr('stroke', 'var(--moss)')
              .attr('stroke-width', 3)
              .attr('d', line);
              
            // Area fill
            const area = d3.area()
              .x(d => x(d.day))
              .y0(height)
              .y1(d => y(d.score))
              .curve(d3.curveBasis);
              
            svg.append('path')
              .datum(sleepData)
              .attr('fill', 'var(--moss)')
              .attr('opacity', 0.1)
              .attr('d', area);
        }
        setTimeout(renderSleepChart, 600);
        window.addEventListener('resize', renderSleepChart);
"""
html = html.replace("// --- Init ---", sleep_chart_js + "\n        // --- Init ---")


# 4. Daily Habit Streak
streak_html = """
                    <div style="margin-top: 16px; display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 20px; font-size: 13px; backdrop-filter: blur(4px);">
                        <span style="font-size: 16px;">🔥</span>
                        <span><strong>12 Day Streak</strong> — You're building a powerful habit!</span>
                    </div>
"""
html = html.replace("<p>A holistic space for your mind, body, and spirit. Choose a path below to begin tracking and improving your well-being.</p>", "<p>A holistic space for your mind, body, and spirit. Choose a path below to begin tracking and improving your well-being.</p>\n" + streak_html)


with open("index.html", "w") as f:
    f.write(html)
print("Done")
