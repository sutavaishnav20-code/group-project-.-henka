import re

with open("index.html", "r") as f:
    content = f.read()

# Add CSS for image selector
css_to_add = """
        /* ---- Image Selector ---- */
        .physique-grid {
            display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 8px;
        }
        .physique-card {
            border: 2px solid transparent; border-radius: 8px; overflow: hidden; cursor: pointer; transition: all 0.2s ease; position: relative;
        }
        .physique-card img {
            width: 100%; height: 140px; object-fit: cover; display: block;
        }
        .physique-card .label {
            position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.7); color: #fff; padding: 6px; font-size: 11px; text-align: center; font-weight: 500;
        }
        .physique-card.selected {
            border-color: var(--indigo); box-shadow: 0 4px 12px rgba(31, 63, 88, 0.2);
        }
        .physique-card.selected::after {
            content: '✓'; position: absolute; top: 8px; right: 8px; background: var(--indigo); color: #fff; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold;
        }
    </style>
"""

content = content.replace("    </style>", css_to_add)

# Replace the select box
select_code = """<div class="input-group">
                                <label>Dream Physique Goal</label>
                                <select id="planGoal">
                                    <option value="lean_athletic">Lean & Athletic (Fat loss + Tone)</option>
                                    <option value="strength_power">Strength & Power (Muscle Mass)</option>
                                    <option value="v_taper_muscle">V-Taper (Upper Body Focus)</option>
                                    <option value="fat_shred">Maximum Fat Shred</option>
                                </select>
                            </div>"""

new_select_code = """<div class="input-group">
                                <label>Dream Physique Goal</label>
                                <input type="hidden" id="planGoal" value="lean_athletic">
                                <div class="physique-grid">
                                    <div class="physique-card selected" onclick="selectPhysique('lean_athletic', this)">
                                        <img src="./src/assets/images/lean_athletic_1789393743192.jpg" alt="Lean & Athletic">
                                        <div class="label">Lean & Athletic</div>
                                    </div>
                                    <div class="physique-card" onclick="selectPhysique('strength_power', this)">
                                        <img src="./src/assets/images/strength_power_1789393760070.jpg" alt="Strength & Power">
                                        <div class="label">Strength & Power</div>
                                    </div>
                                    <div class="physique-card" onclick="selectPhysique('v_taper_muscle', this)">
                                        <img src="./src/assets/images/v_taper_1789393774631.jpg" alt="V-Taper">
                                        <div class="label">V-Taper</div>
                                    </div>
                                    <div class="physique-card" onclick="selectPhysique('fat_shred', this)">
                                        <img src="./src/assets/images/fat_shred_1789393794500.jpg" alt="Fat Shred">
                                        <div class="label">Fat Shred</div>
                                    </div>
                                </div>
                            </div>"""

content = content.replace(select_code, new_select_code)

# Add selectPhysique logic
js_to_add = """
        // --- Physical Tabs & BMI ---
        window.selectPhysique = function(value, element) {
            document.querySelectorAll('.physique-card').forEach(c => c.classList.remove('selected'));
            element.classList.add('selected');
            document.getElementById('planGoal').value = value;
        };
"""

content = content.replace("// --- Physical Tabs & BMI ---", js_to_add)

with open("index.html", "w") as f:
    f.write(content)
print("Updated index.html")
