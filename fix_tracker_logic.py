import re

with open("index.html", "r") as f:
    content = f.read()

# Make sure we add Planks to the select and the new UI
if "trackerChartContainer" not in content:
    print("Tracker Chart not found, re-adding it.")
    tracker_pattern = r"(<div id=\"tab-tracker\" class=\"tab-content\">.*?<div class=\"coach-panel\">)(.*?)(<button id=\"startCameraBtn\" class=\"primary-btn\" style=\"margin-bottom: 16px;\">)"

    def replacer(match):
        prefix = match.group(1)
        middle = match.group(2)
        suffix = match.group(3)
        middle = middle.replace("</select>", "    <option value=\"planks\">Planks (Timed)</option>\n                                </select>")
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

    content = re.sub(tracker_pattern, replacer, content, flags=re.DOTALL)

# Find the tracker variables
tracker_vars_pattern = r"let repCount = 0;\s*let trackerPose = null;\s*let trackerCamera = null;"
tracker_vars_new = """let repCount = 0;
        let trackerPose = null;
        let trackerCamera = null;
        let timerStart = 0;
        let currentDuration = 0;
        let isHolding = false;
        let weeklyData = JSON.parse(localStorage.getItem('henkaWeeklyData') || '[]');
        
        // Ensure some mock data if empty for the chart
        if (weeklyData.length === 0) {
            const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            weeklyData = days.map(d => ({ day: d, value: Math.floor(Math.random() * 20) + 5 }));
            localStorage.setItem('henkaWeeklyData', JSON.stringify(weeklyData));
        }

        function renderChart() {
            if (typeof d3 === 'undefined') return;
            d3.select('#d3Chart').selectAll('*').remove();
            
            const margin = {top: 10, right: 10, bottom: 20, left: 30};
            const width = document.getElementById('d3Chart').clientWidth - margin.left - margin.right;
            const height = 200 - margin.top - margin.bottom;

            const svg = d3.select('#d3Chart')
              .append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
              .append('g')
                .attr('transform', `translate(${margin.left},${margin.top})`);

            const x = d3.scalePoint()
              .domain(weeklyData.map(d => d.day))
              .range([0, width])
              .padding(0.5);

            const y = d3.scaleLinear()
              .domain([0, d3.max(weeklyData, d => d.value) * 1.2 || 10])
              .range([height, 0]);

            svg.append('g')
              .attr('transform', `translate(0,${height})`)
              .call(d3.axisBottom(x).tickSize(0).tickPadding(8))
              .call(g => g.select('.domain').attr('stroke', 'var(--line)'))
              .selectAll('text').attr('fill', 'var(--ink-faint)');

            svg.append('g')
              .call(d3.axisLeft(y).ticks(4).tickSize(-width))
              .call(g => g.select('.domain').remove())
              .call(g => g.selectAll('.tick line').attr('stroke', 'var(--line)').attr('stroke-dasharray', '2,2'))
              .selectAll('text').attr('fill', 'var(--ink-faint)');

            const line = d3.line()
              .x(d => x(d.day))
              .y(d => y(d.value))
              .curve(d3.curveMonotoneX);

            svg.append('path')
              .datum(weeklyData)
              .attr('fill', 'none')
              .attr('stroke', 'var(--indigo)')
              .attr('stroke-width', 3)
              .attr('d', line);

            svg.selectAll('.dot')
              .data(weeklyData)
              .enter().append('circle')
              .attr('cx', d => x(d.day))
              .attr('cy', d => y(d.value))
              .attr('r', 4)
              .attr('fill', 'var(--indigo)')
              .attr('stroke', 'var(--paper)')
              .attr('stroke-width', 2);
        }

        setTimeout(renderChart, 500);
        window.addEventListener('resize', renderChart);
        
        function updateWeeklyData(newValue) {
            const today = new Date().toLocaleDateString('en-US', {weekday: 'short'});
            let found = weeklyData.find(d => d.day === today);
            if (found) {
                found.value += newValue;
            } else {
                weeklyData.push({ day: today, value: newValue });
                if (weeklyData.length > 7) weeklyData.shift();
            }
            localStorage.setItem('henkaWeeklyData', JSON.stringify(weeklyData));
            renderChart();
        }
"""
content = re.sub(tracker_vars_pattern, tracker_vars_new, content)

# Now find onResults and inject the timer logic
onResults_pattern = r"function onResults\(results\) \{.*?ctx\.restore\(\);\s*\}"

def onResults_replacer(match):
    original = match.group(0)
    
    # We will rewrite onResults entirely since we need to inject the timer and the exercise modes
    new_func = """function onResults(results) {
            ctx.save();
            ctx.clearRect(0, 0, canvasElement.width, canvasElement.height);
            ctx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

            const ex = document.getElementById('exerciseSelect').value;
            const repLabel = document.querySelector('#repCountDisplay').previousElementSibling;

            if (ex === 'planks') {
                repLabel.innerText = 'SECONDS';
                if (results.poseLandmarks) {
                    window.drawConnectors(ctx, results.poseLandmarks, window.POSE_CONNECTIONS, {color: '#A15A2E', lineWidth: 4});
                    window.drawLandmarks(ctx, results.poseLandmarks, {color: '#FF0000', lineWidth: 2});
                    
                    const leftShoulder = results.poseLandmarks[11];
                    const leftHip = results.poseLandmarks[23];
                    const leftAnkle = results.poseLandmarks[27];

                    // Simple check for horizontal alignment (plank)
                    if (leftShoulder && leftHip && leftAnkle) {
                        const yDiffShoulderHip = Math.abs(leftShoulder.y - leftHip.y);
                        const yDiffHipAnkle = Math.abs(leftHip.y - leftAnkle.y);

                        // If body is relatively flat
                        if (yDiffShoulderHip < 0.15 && yDiffHipAnkle < 0.15) {
                            if (!isHolding) {
                                isHolding = true;
                                timerStart = Date.now() - (currentDuration * 1000);
                                feedbackEl.innerText = 'Hold it...';
                                feedbackEl.style.background = 'rgba(74, 111, 100, 0.9)'; // moss
                            } else {
                                currentDuration = Math.floor((Date.now() - timerStart) / 1000);
                                repCountDisplay.innerText = currentDuration;
                            }
                        } else {
                            if (isHolding) {
                                isHolding = false;
                                feedbackEl.innerText = 'Form broken. Resume plank.';
                                feedbackEl.style.background = 'rgba(161, 90, 46, 0.9)';
                            }
                        }
                    }
                } else {
                    isHolding = false;
                    feedbackEl.innerText = 'Align your body horizontally to start.';
                }
            } else {
                repLabel.innerText = 'REPS';
                repCountDisplay.innerText = repCount;
                if (results.poseLandmarks) {
                    window.drawConnectors(ctx, results.poseLandmarks, window.POSE_CONNECTIONS, {color: '#A15A2E', lineWidth: 4});
                    window.drawLandmarks(ctx, results.poseLandmarks, {color: '#FF0000', lineWidth: 2});

                    if (ex === 'squats') {
                        const hip = results.poseLandmarks[23];
                        const knee = results.poseLandmarks[25];
                        const ankle = results.poseLandmarks[27];
                        if (hip && knee && ankle) {
                            const angle = calculateAngle(hip, knee, ankle);
                            if (angle > 160) {
                                if (stage === 'down') {
                                    repCount++;
                                    repCountDisplay.innerText = repCount;
                                    feedbackEl.innerText = 'Good Rep!';
                                    feedbackEl.style.background = 'rgba(74, 111, 100, 0.9)';
                                }
                                stage = 'up';
                            }
                            if (angle < 100) {
                                stage = 'down';
                                feedbackEl.innerText = 'Go up!';
                                feedbackEl.style.background = 'rgba(31, 63, 88, 0.9)';
                            }
                            if (stage === 'up' && angle < 160 && angle > 100) {
                                feedbackEl.innerText = 'Go lower...';
                                feedbackEl.style.background = 'rgba(161, 90, 46, 0.9)';
                            }
                        }
                    } else if (ex === 'pushups') {
                        const shoulder = results.poseLandmarks[11];
                        const elbow = results.poseLandmarks[13];
                        const wrist = results.poseLandmarks[15];
                        if (shoulder && elbow && wrist) {
                            const angle = calculateAngle(shoulder, elbow, wrist);
                            if (angle > 160) {
                                if (stage === 'down') {
                                    repCount++;
                                    repCountDisplay.innerText = repCount;
                                    feedbackEl.innerText = 'Good Rep!';
                                    feedbackEl.style.background = 'rgba(74, 111, 100, 0.9)';
                                }
                                stage = 'up';
                            }
                            if (angle < 90) {
                                stage = 'down';
                                feedbackEl.innerText = 'Push up!';
                                feedbackEl.style.background = 'rgba(31, 63, 88, 0.9)';
                            }
                        }
                    } else if (ex === 'bicep_curls') {
                        const shoulder = results.poseLandmarks[12];
                        const elbow = results.poseLandmarks[14];
                        const wrist = results.poseLandmarks[16];
                        if (shoulder && elbow && wrist) {
                            const angle = calculateAngle(shoulder, elbow, wrist);
                            if (angle > 160) {
                                if (stage === 'up') {
                                    repCount++;
                                    repCountDisplay.innerText = repCount;
                                    feedbackEl.innerText = 'Good Rep!';
                                    feedbackEl.style.background = 'rgba(74, 111, 100, 0.9)';
                                }
                                stage = 'down';
                            }
                            if (angle < 45) {
                                stage = 'up';
                                feedbackEl.innerText = 'Squeeze & lower...';
                                feedbackEl.style.background = 'rgba(31, 63, 88, 0.9)';
                            }
                        }
                    }
                } else {
                    feedbackEl.innerText = 'Align your body to start.';
                }
            }
            ctx.restore();
        }"""
    
    return new_func

content = re.sub(onResults_pattern, onResults_replacer, content, flags=re.DOTALL)

# Add Download report button logic
download_report_logic = """
        const downloadBtn = document.getElementById('downloadReportBtn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => {
                let data = JSON.parse(localStorage.getItem('henkaWeeklyData') || '[]');
                if (data.length === 0) {
                    showToast('No progress data to download yet.');
                    return;
                }
                let reportText = "=== Henka Weekly Progress Report ===\\n\\n";
                data.forEach(d => {
                    reportText += `${d.day}: ${d.value} Reps/Secs\\n`;
                });
                reportText += "\\nKeep up the great work!";
                
                const blob = new Blob([reportText], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'Henka_Progress_Report.txt';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            });
        }
"""
if "downloadReportBtn" in content and "Henka_Progress_Report.txt" not in content:
    content = content.replace("document.addEventListener('DOMContentLoaded', () => {", download_report_logic + "\n        document.addEventListener('DOMContentLoaded', () => {")

# Modify Stop Tracker to save data
stop_logic_pattern = r"if \(trackerCamera\) \{\s*trackerCamera\.stop\(\);\s*\}"
stop_logic_new = """if (trackerCamera) {
                trackerCamera.stop();
            }
            
            const ex = document.getElementById('exerciseSelect').value;
            let val = ex === 'planks' ? currentDuration : repCount;
            if (val > 0) {
                updateWeeklyData(val);
                repCount = 0;
                currentDuration = 0;
                isHolding = false;
                timerStart = 0;
                repCountDisplay.innerText = 0;
            }"""
content = re.sub(stop_logic_pattern, stop_logic_new, content)

with open("index.html", "w") as f:
    f.write(content)
print("Done")
