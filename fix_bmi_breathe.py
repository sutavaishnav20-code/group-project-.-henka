import re

with open("index.html", "r") as f:
    content = f.read()

# 1. Update CSS
css_breathe_old = """        .breathe-circle {
            width: 200px; height: 200px; border-radius: 50%; background: var(--moss); opacity: 0.8; margin: 40px auto; transition: all 4s linear; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; font-weight: 500;
        }"""
        
css_breathe_new = """        .breathe-circle {
            width: 200px; height: 200px; border-radius: 50%; background: var(--moss); margin: 40px auto; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; font-weight: 500; box-shadow: 0 8px 32px rgba(87,100,74,0.2); text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        @keyframes boxBreatheAnim {
            0%   { transform: scale(1); background: var(--moss); box-shadow: 0 8px 32px rgba(87,100,74,0.2); }
            25%  { transform: scale(1.6); background: var(--indigo); box-shadow: 0 16px 48px rgba(31,63,88,0.4); }
            50%  { transform: scale(1.6); background: var(--indigo); box-shadow: 0 16px 48px rgba(31,63,88,0.4); }
            75%  { transform: scale(1); background: var(--kaki); box-shadow: 0 8px 32px rgba(161,90,46,0.2); }
            100% { transform: scale(1); background: var(--moss); box-shadow: 0 8px 32px rgba(87,100,74,0.2); }
        }"""
content = content.replace(css_breathe_old, css_breathe_new)

# 2. Update Box Breathing JS
box_breathing_old_pattern = r"window\.openBoxBreathing = function\(\) \{.*?(?=window\.openVagusReset = function\(\) \{)"
box_breathing_new = """window.openBoxBreathing = function() {
            modalContent.innerHTML = `
                <h3 style="margin-top:0;">Box Breathing</h3>
                <p style="font-size:14px; color:var(--ink-soft); margin-bottom: 24px;">Follow the circle to regulate your nervous system.</p>
                <div id="breatheCircle" class="breathe-circle">Ready</div>
                <button class="primary-btn" id="startBreatheBtn" style="width:100%; justify-content:center;">Start Session</button>
            `;
            modalOverlay.style.display = 'flex';

            document.getElementById('startBreatheBtn').addEventListener('click', () => {
                document.getElementById('startBreatheBtn').style.display = 'none';
                const circle = document.getElementById('breatheCircle');
                
                // Use pure CSS animation for ultra-smooth scaling and color transitions
                circle.style.animation = 'boxBreatheAnim 16s linear infinite';
                
                const phases = ['Inhale', 'Hold', 'Exhale', 'Hold'];
                let phaseIndex = 0;

                function updateText() {
                    if (!document.getElementById('breatheCircle')) return;
                    circle.innerText = phases[phaseIndex];
                    
                    // Subtle CSS text-pop effect
                    circle.style.opacity = '0.7';
                    setTimeout(() => circle.style.opacity = '1', 100);
                    
                    phaseIndex = (phaseIndex + 1) % 4;
                }

                updateText();
                breathingInterval = setInterval(updateText, 4000);
            });
        };

        """
content = re.sub(box_breathing_old_pattern, box_breathing_new, content, flags=re.DOTALL)

# 3. Update BMI JS
bmi_old_pattern = r"const res = document\.getElementById\('bmiResult'\);\s*res\.innerHTML = `.*?`;\s*res\.style\.display = 'block';"
bmi_new = """const res = document.getElementById('bmiResult');
                
                const clampedBmi = Math.max(15, Math.min(bmi, 40));
                const percent = ((clampedBmi - 15) / 25) * 100;
                
                res.innerHTML = `
                    <div style="display:flex; justify-content: space-between; align-items:flex-end;">
                        <div>
                            <div style="font-size: 13px; color: var(--ink-soft);">Your BMI</div>
                            <strong style="font-size: 32px; color: ${color}; line-height: 1;">${bmi}</strong>
                        </div>
                        <div style="font-size: 16px; font-weight: 600; color: ${color};">${cat}</div>
                    </div>
                    
                    <div style="margin-top: 36px; position: relative;">
                        <!-- Pointer -->
                        <div style="position: absolute; left: ${percent}%; bottom: 100%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; transition: left 1s cubic-bezier(0.4, 0, 0.2, 1); margin-bottom: 4px;">
                            <div style="background: ${color}; color: #fff; padding: 4px 8px; border-radius: 6px; font-weight: bold; font-size: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); white-space: nowrap;">You: ${bmi}</div>
                            <div style="width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 6px solid ${color};"></div>
                        </div>
                        <!-- Bar -->
                        <div style="width: 100%; height: 16px; border-radius: 8px; overflow: hidden; display: flex; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);">
                            <div style="flex: 3.5; background: #60a5fa;" title="Underweight (< 18.5)"></div>
                            <div style="flex: 6.5; background: #4ade80;" title="Normal (18.5 - 24.9)"></div>
                            <div style="flex: 5; background: #facc15;" title="Overweight (25 - 29.9)"></div>
                            <div style="flex: 10; background: #f87171;" title="Obese (30+)"></div>
                        </div>
                        <!-- Labels -->
                        <div style="display:flex; justify-content: space-between; font-size: 11px; color: var(--ink-faint); margin-top: 8px; font-weight: 500;">
                            <span style="flex: 3.5;">15</span>
                            <span style="flex: 6.5; text-align: left;">18.5</span>
                            <span style="flex: 5; text-align: left;">25</span>
                            <span style="flex: 10; text-align: left;">30</span>
                            <span style="text-align: right; width: 0; overflow: visible; direction: rtl;">40+</span>
                        </div>
                    </div>
                `;
                res.style.display = 'block';"""

content = re.sub(bmi_old_pattern, bmi_new, content, flags=re.DOTALL)

with open("index.html", "w") as f:
    f.write(content)
print("done")
