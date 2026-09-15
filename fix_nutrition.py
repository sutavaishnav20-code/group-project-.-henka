import re

with open("index.html", "r") as f:
    content = f.read()

nutrition_view_old_pattern = r"            <!-- 3\. NUTRITION VIEW -->.*?<div id=\"analysisResult\"></div>\s*</div>\s*</div>"
nutrition_view_new = """            <!-- 3. NUTRITION VIEW -->
            <div id="view-diet" class="view">
                <div class="eyebrow">Pillar 03</div>
                <h2 class="section-title">Nutrition & Fuel</h2>
                <p class="section-sub">Analyze your meals and track your macronutrients for optimal energy.</p>

                <div class="physical-tabs" style="margin-bottom: 24px;">
                    <button class="tab-btn active" onclick="switchNutritionTab('nutri-macro')">Macro Calculator</button>
                    <button class="tab-btn" onclick="switchNutritionTab('nutri-scanner')">AI Food Scanner</button>
                    <button class="tab-btn" onclick="switchNutritionTab('nutri-hydration')">Hydration Tracker</button>
                </div>

                <div id="nutri-macro" class="tab-content active">
                    <div class="coach-panel">
                        <h3>Daily Macro Calculator</h3>
                        <p>Calculate your daily protein, fats, and carbs targets based on your body and goals.</p>
                        <form id="macroForm">
                            <div class="input-group">
                                <label>Weight (kg)</label>
                                <input type="number" id="macroWeight" placeholder="70" required step="1">
                            </div>
                            <div class="input-group">
                                <label>Goal</label>
                                <select id="macroGoal">
                                    <option value="maintain">Maintain Weight</option>
                                    <option value="lose">Lose Fat</option>
                                    <option value="gain">Build Muscle</option>
                                </select>
                            </div>
                            <button type="submit" class="primary-btn">Calculate Macros</button>
                        </form>
                        <div id="macroResult" style="display:none; margin-top:16px; padding:16px; background:var(--paper-2); border:1px solid var(--line); border-radius:6px; font-size:14px; line-height:1.6;"></div>
                    </div>
                </div>

                <div id="nutri-scanner" class="tab-content">
                    <div class="coach-panel">
                        <h3>AI Food Scanner</h3>
                        <p>Upload or snap a photo of your meal. Our AI will classify it as healthy/unhealthy, list exact nutrients, and provide a health score.</p>
                        
                        <div style="display:flex; gap:12px; margin-bottom: 16px;">
                            <button class="option-btn" onclick="document.getElementById('fileInput').click()" style="flex:1; justify-content:center;">📁 Upload Image</button>
                            <button class="option-btn" onclick="startFoodCamera()" style="flex:1; justify-content:center;">📷 Snap Photo</button>
                        </div>
                        <input type="file" id="fileInput" accept="image/jpeg, image/png" style="display:none;">

                        <div id="foodCameraContainer" style="display:none; position:relative; border-radius:8px; overflow:hidden; background:#000; margin-bottom:16px;">
                            <video id="foodVideo" style="width:100%; display:block;" autoplay playsinline></video>
                            <button class="primary-btn" onclick="captureFoodPhoto()" style="position:absolute; bottom:16px; left:50%; transform:translateX(-50%);">Capture & Analyze</button>
                        </div>
                        
                        <img id="imagePreview" class="preview-img" src="" alt="Meal Preview" style="display:none; width:100%; border-radius:8px; margin-bottom:16px; object-fit:cover; max-height:300px;">
                        
                        <button id="analyzeFoodBtn" class="primary-btn" style="display:none; width:100%; justify-content:center;">Analyze Meal</button>
                        
                        <div id="analysisResult" style="display:none; margin-top:24px;"></div>
                    </div>
                </div>

                <div id="nutri-hydration" class="tab-content">
                    <div class="coach-panel">
                        <h3>Hydration Tracker</h3>
                        <p>Track your daily water intake. Goal: 2.5 - 3.0 Liters.</p>
                        <div style="text-align:center; padding: 24px;">
                            <div style="font-size:48px; color:var(--ocean); font-weight:700;" id="waterCount">0 L</div>
                            <div style="font-size:14px; color:var(--ink-soft); margin-top:8px;">Consumed today</div>
                            
                            <div style="display:flex; gap:12px; justify-content:center; margin-top:24px;">
                                <button class="primary-btn" style="background:var(--ocean);" onclick="addWater(0.25)">+ 250ml</button>
                                <button class="primary-btn" style="background:var(--ocean);" onclick="addWater(0.50)">+ 500ml</button>
                                <button class="option-btn" onclick="resetWater()">Reset</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>"""

content = re.sub(nutrition_view_old_pattern, nutrition_view_new, content, flags=re.DOTALL)

with open("index.html", "w") as f:
    f.write(content)
print("done")
