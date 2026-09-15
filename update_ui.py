import re

with open("index.html", "r") as f:
    html = f.read()

# 1. Add Login/Register UI Auth Overlay
auth_ui = """
    <!-- AUTH OVERLAY -->
    <div id="authOverlay" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: var(--paper); z-index: 9999; display: flex; align-items: center; justify-content: center;">
        <div style="background: var(--paper-2); padding: 32px; border-radius: 12px; border: 1px solid var(--line); width: 90%; max-width: 400px; box-shadow: 0 12px 48px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 24px;">
                <div class="seal" style="margin: 0 auto 16px;">H</div>
                <h2 style="font-family: 'Shippori Mincho', serif; color: var(--indigo-deep);">Welcome to Henka</h2>
                <p style="color: var(--ink-soft); font-size: 14px;">Sign in or create an account to personalize your journey.</p>
            </div>
            <form id="authForm">
                <div class="input-group" style="margin-bottom: 16px;">
                    <label style="display: block; margin-bottom: 8px; font-size: 12px; font-weight: 600; color: var(--ink-soft); text-transform: uppercase;">Full Name</label>
                    <input type="text" id="authName" placeholder="Your Name" required style="width: 100%; padding: 12px; border-radius: 6px; border: 1px solid var(--line); background: var(--paper); color: var(--ink); font-family: inherit;">
                </div>
                <div class="input-group" style="margin-bottom: 24px;">
                    <label style="display: block; margin-bottom: 8px; font-size: 12px; font-weight: 600; color: var(--ink-soft); text-transform: uppercase;">Email Address</label>
                    <input type="email" id="authEmail" placeholder="you@example.com" required style="width: 100%; padding: 12px; border-radius: 6px; border: 1px solid var(--line); background: var(--paper); color: var(--ink); font-family: inherit;">
                </div>
                <button type="submit" class="primary-btn" style="width: 100%; justify-content: center; font-size: 16px;">Enter Henka</button>
            </form>
        </div>
    </div>
"""

# Insert right after <div class="toast"...
html = html.replace('<div class="toast" id="toastMsg">Action completed</div>', '<div class="toast" id="toastMsg">Action completed</div>\n' + auth_ui)

# Add logic to hide auth overlay if logged in, and update header.
header_html = """<header class="top">
            <button class="menu-trigger" id="menuBtn" aria-label="Menu" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
            <div class="brand-row">
                <div class="seal">H</div>
                <div class="brand-text">
                    <h1 class="logo">Henka</h1>
                    <div class="tagline" id="headerGreeting">Be The Change You Want</div>
                </div>
            </div>"""

html = html.replace("""<header class="top">
            <button class="menu-trigger" id="menuBtn" aria-label="Menu" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
            <div class="brand-row">
                <div class="seal">H</div>
                <div class="brand-text">
                    <h1 class="logo">Henka</h1>
                    <div class="tagline">Be The Change You Want</div>
                </div>
            </div>""", header_html)


# JS for Auth
auth_js = """
        // Auth Logic
        document.addEventListener('DOMContentLoaded', () => {
            const authOverlay = document.getElementById('authOverlay');
            const authForm = document.getElementById('authForm');
            const greeting = document.getElementById('headerGreeting');
            
            const savedUser = localStorage.getItem('henkaUser');
            if (savedUser) {
                if (authOverlay) authOverlay.style.display = 'none';
                try {
                    const user = JSON.parse(savedUser);
                    if(greeting) greeting.innerText = `Welcome back, ${user.name}`;
                } catch(e){}
            }
            
            if(authForm) {
                authForm.addEventListener('submit', (e) => {
                    e.preventDefault();
                    const name = document.getElementById('authName').value;
                    const email = document.getElementById('authEmail').value;
                    if(name && email) {
                        localStorage.setItem('henkaUser', JSON.stringify({name, email}));
                        authOverlay.style.opacity = '0';
                        authOverlay.style.transition = 'opacity 0.4s ease';
                        setTimeout(() => authOverlay.style.display = 'none', 400);
                        if(greeting) greeting.innerText = `Welcome, ${name}`;
                        showToast('Successfully logged in');
                    }
                });
            }
        });
"""
html = html.replace("// --- Init ---", auth_js + "\n        // --- Init ---")

# 2. Improve camera loading visual
old_loading_text = "feedbackEl.innerText = 'Downloading AI Model (Faster Lite Version)... Please wait.';"
new_loading_text = "feedbackEl.innerHTML = '<span style=\"display:inline-block; animation: spin 1s linear infinite;\">⏳</span> Downloading AI Model... Please wait.';"
html = html.replace(old_loading_text, new_loading_text)
if "animation: spin" not in html:
    html = html.replace("</style>", "    @keyframes spin { 100% { transform: rotate(360deg); } }\n    </style>")

# 3. Enhance body type visual
html = html.replace('alt="Lean & Athletic">\\n                                        <div class="label">Lean & Athletic</div>', 'alt="Lean & Athletic">\\n                                        <div class="label" style="background: linear-gradient(transparent, rgba(0,0,0,0.9)); height: 50%; display: flex; flex-direction: column; justify-content: flex-end; padding: 10px; font-size: 13px;">⚡ Lean & Athletic</div>')
html = html.replace('alt="Strength & Power">\\n                                        <div class="label">Strength & Power</div>', 'alt="Strength & Power">\\n                                        <div class="label" style="background: linear-gradient(transparent, rgba(0,0,0,0.9)); height: 50%; display: flex; flex-direction: column; justify-content: flex-end; padding: 10px; font-size: 13px;">🛡️ Strength & Power</div>')
html = html.replace('alt="V-Taper">\\n                                        <div class="label">V-Taper</div>', 'alt="V-Taper">\\n                                        <div class="label" style="background: linear-gradient(transparent, rgba(0,0,0,0.9)); height: 50%; display: flex; flex-direction: column; justify-content: flex-end; padding: 10px; font-size: 13px;">🏆 V-Taper</div>')
html = html.replace('alt="Fat Shred">\\n                                        <div class="label">Fat Shred</div>', 'alt="Fat Shred">\\n                                        <div class="label" style="background: linear-gradient(transparent, rgba(0,0,0,0.9)); height: 50%; display: flex; flex-direction: column; justify-content: flex-end; padding: 10px; font-size: 13px;">🔥 Fat Shred</div>')
html = html.replace('alt="Hourglass">\\n                                        <div class="label">Hourglass Tone</div>', 'alt="Hourglass">\\n                                        <div class="label" style="background: linear-gradient(transparent, rgba(0,0,0,0.9)); height: 50%; display: flex; flex-direction: column; justify-content: flex-end; padding: 10px; font-size: 13px;">⏳ Hourglass Tone</div>')
html = html.replace('alt="Longevity">\\n                                        <div class="label">Longevity</div>', 'alt="Longevity">\\n                                        <div class="label" style="background: linear-gradient(transparent, rgba(0,0,0,0.9)); height: 50%; display: flex; flex-direction: column; justify-content: flex-end; padding: 10px; font-size: 13px;">🌿 Longevity</div>')


# 4. Add progress insights
chart_html = """
                        <div id="trackerChartContainer" style="margin-bottom: 24px; padding: 16px; background: var(--paper-2); border-radius: 8px; border: 1px solid var(--line);">
                            <h4 style="margin-bottom: 12px; font-size: 14px; color: var(--ink-soft);">Weekly Progress (Reps/Secs)</h4>
                            <div id="d3Chart" style="width: 100%; height: 200px;"></div>
                            <div id="progressInsights" style="margin-top: 16px; padding: 12px; background: var(--paper); border-left: 4px solid var(--moss); border-radius: 4px; font-size: 13px; color: var(--ink); line-height: 1.5;">
                                Complete a workout to see insights here.
                            </div>
                        </div>
"""
html = html.replace("""
                        <div id="trackerChartContainer" style="margin-bottom: 24px; padding: 16px; background: var(--paper-2); border-radius: 8px; border: 1px solid var(--line);">
                            <h4 style="margin-bottom: 12px; font-size: 14px; color: var(--ink-soft);">Weekly Progress (Reps/Secs)</h4>
                            <div id="d3Chart" style="width: 100%; height: 200px;"></div>
                        </div>
""", chart_html)

# Update renderChart to fill insights
render_chart_js = """
            svg.selectAll('.dot')
              .data(weeklyData)
              .enter().append('circle')
              .attr('cx', d => x(d.day))
              .attr('cy', d => y(d.value))
              .attr('r', 4)
              .attr('fill', 'var(--indigo)')
              .attr('stroke', 'var(--paper)')
              .attr('stroke-width', 2);
              
            // Progress Insights logic
            const total = weeklyData.reduce((sum, d) => sum + d.value, 0);
            const insightsEl = document.getElementById('progressInsights');
            if(insightsEl) {
                if(total === 0) {
                    insightsEl.innerHTML = "You haven't tracked any exercises this week. Time to start!";
                } else if(total < 50) {
                    insightsEl.innerHTML = `<strong>Total this week: ${total}</strong>. Great start! Consistency is the key to building the habit. Keep going!`;
                } else {
                    insightsEl.innerHTML = `<strong>Total this week: ${total}</strong>. You are crushing it! Excellent consistency across the board. Your body is adapting and getting stronger.`;
                }
            }
"""
html = html.replace("""
            svg.selectAll('.dot')
              .data(weeklyData)
              .enter().append('circle')
              .attr('cx', d => x(d.day))
              .attr('cy', d => y(d.value))
              .attr('r', 4)
              .attr('fill', 'var(--indigo)')
              .attr('stroke', 'var(--paper)')
              .attr('stroke-width', 2);
""", render_chart_js)

with open("index.html", "w") as f:
    f.write(html)
print("Done")
