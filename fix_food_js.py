import re

with open("index.html", "r") as f:
    content = f.read()

pattern = r"// --- Food Analysis Logic ---.*?window\.resetFoodUpload = function\(\) \{.*?\};"

new_js = """// --- Nutrition Tabs Logic ---
        window.switchNutritionTab = function(tabId, btn) {
            document.querySelectorAll('#view-diet .tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('#view-diet .tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            if (btn) btn.classList.add('active');
        };

        // --- Macro Calculator Logic ---
        const macroForm = document.getElementById('macroForm');
        if (macroForm) {
            macroForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const weight = parseFloat(document.getElementById('macroWeight').value);
                const goal = document.getElementById('macroGoal').value;
                
                if(!weight) return;
                
                let calories = weight * 22 * 1.5; // Basal roughly
                if (goal === 'lose') calories *= 0.8;
                if (goal === 'gain') calories *= 1.15;
                
                let protein = weight * 2.2; // High protein
                let fat = (calories * 0.25) / 9; // 25% fats
                let carbs = (calories - (protein * 4) - (fat * 9)) / 4;
                
                const res = document.getElementById('macroResult');
                res.innerHTML = `
                    <div style="text-align:center; margin-bottom:12px;"><strong>Your Daily Targets</strong></div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;"><span>Calories:</span> <strong>${Math.round(calories)} kcal</strong></div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;"><span>Protein:</span> <strong>${Math.round(protein)}g</strong></div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;"><span>Fats:</span> <strong>${Math.round(fat)}g</strong></div>
                    <div style="display:flex; justify-content:space-between;"><span>Carbs:</span> <strong>${Math.round(carbs)}g</strong></div>
                `;
                res.style.display = 'block';
            });
        }

        // --- Hydration Tracker Logic ---
        let dailyWater = parseFloat(localStorage.getItem('dailyWater') || '0');
        const waterDisplay = document.getElementById('waterCount');
        
        function updateWaterDisplay() {
            if (waterDisplay) waterDisplay.innerText = dailyWater.toFixed(2) + ' L';
        }
        updateWaterDisplay();
        
        window.addWater = function(amount) {
            dailyWater += amount;
            localStorage.setItem('dailyWater', dailyWater.toString());
            updateWaterDisplay();
        };
        window.resetWater = function() {
            dailyWater = 0;
            localStorage.setItem('dailyWater', dailyWater.toString());
            updateWaterDisplay();
        };

        // --- AI Food Scanner Logic ---
        const fileInput = document.getElementById('fileInput');
        const imagePreview = document.getElementById('imagePreview');
        const analyzeFoodBtn = document.getElementById('analyzeFoodBtn');
        const analysisResult = document.getElementById('analysisResult');
        const foodCameraContainer = document.getElementById('foodCameraContainer');
        const foodVideo = document.getElementById('foodVideo');
        
        let currentBase64Image = null;
        let foodStream = null;

        window.startFoodCamera = async function() {
            try {
                foodStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
                foodVideo.srcObject = foodStream;
                foodCameraContainer.style.display = 'block';
                imagePreview.style.display = 'none';
                if (analyzeFoodBtn) analyzeFoodBtn.style.display = 'none';
                if (analysisResult) analysisResult.style.display = 'none';
            } catch (err) {
                showToast('Camera access denied or unavailable.');
            }
        };

        window.captureFoodPhoto = function() {
            if (!foodStream) return;
            const canvas = document.createElement('canvas');
            canvas.width = foodVideo.videoWidth;
            canvas.height = foodVideo.videoHeight;
            canvas.getContext('2d').drawImage(foodVideo, 0, 0);
            currentBase64Image = canvas.toDataURL('image/jpeg', 0.8);
            
            // Stop camera
            foodStream.getTracks().forEach(t => t.stop());
            foodStream = null;
            foodCameraContainer.style.display = 'none';
            
            // Show preview
            imagePreview.src = currentBase64Image;
            imagePreview.style.display = 'block';
            if (analyzeFoodBtn) analyzeFoodBtn.style.display = 'flex';
        };

        if (fileInput) {
            fileInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        currentBase64Image = e.target.result;
                        imagePreview.src = currentBase64Image;
                        imagePreview.style.display = 'block';
                        if (analyzeFoodBtn) analyzeFoodBtn.style.display = 'flex';
                        if (analysisResult) analysisResult.style.display = 'none';
                        if (foodCameraContainer) foodCameraContainer.style.display = 'none';
                        if (foodStream) {
                            foodStream.getTracks().forEach(t => t.stop());
                            foodStream = null;
                        }
                    }
                    reader.readAsDataURL(this.files[0]);
                }
            });
        }

        if (analyzeFoodBtn) {
            analyzeFoodBtn.addEventListener('click', async () => {
                if (!currentBase64Image) return;
                
                showLoading(true, 'Analyzing nutritional content...');
                try {
                    const res = await fetch('/api/analyze-food', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ image: currentBase64Image })
                    });
                    
                    const data = await res.json();
                    if (!res.ok) throw new Error(data.error || 'Failed to analyze image');
                    
                    if (analysisResult) analysisResult.style.display = 'block';
                    
                    const isHealthy = data.healthScore >= 60;
                    const healthBadge = isHealthy 
                        ? `<span style="background:var(--moss); color:#fff; padding:4px 8px; border-radius:4px; font-size:12px;">✅ Healthy (${data.healthScore}/100)</span>`
                        : `<span style="background:var(--kaki); color:#fff; padding:4px 8px; border-radius:4px; font-size:12px;">⚠️ Unhealthy (${data.healthScore}/100)</span>`;

                    let html = `
                        <h4 style="font-family: 'Shippori Mincho', serif; font-size: 18px; color: var(--indigo-deep); margin-bottom: 12px; display: flex; justify-content: space-between; align-items:center;">
                            <span>Nutrition Profile</span>
                            ${healthBadge}
                        </h4>
                        <p style="font-size: 14px; margin-bottom: 16px;"><strong>Type:</strong> ${data.dietaryType}</p>
                        
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 20px; text-align: center;">
                            <div style="background: var(--paper-2); padding: 10px; border-radius: 6px; border: 1px solid var(--line);">
                                <div style="font-size: 11px; text-transform: uppercase; color: var(--ink-faint);">Calories</div>
                                <strong style="font-size: 16px; color: var(--indigo);">${data.totalCalories}</strong>
                            </div>
                            <div style="background: var(--paper-2); padding: 10px; border-radius: 6px; border: 1px solid var(--line);">
                                <div style="font-size: 11px; text-transform: uppercase; color: var(--ink-faint);">Protein</div>
                                <strong style="font-size: 16px; color: var(--moss);">${data.protein_g}g</strong>
                            </div>
                            <div style="background: var(--paper-2); padding: 10px; border-radius: 6px; border: 1px solid var(--line);">
                                <div style="font-size: 11px; text-transform: uppercase; color: var(--ink-faint);">Carbs</div>
                                <strong style="font-size: 16px; color: var(--gold);">${data.carbs_g}g</strong>
                            </div>
                            <div style="background: var(--paper-2); padding: 10px; border-radius: 6px; border: 1px solid var(--line);">
                                <div style="font-size: 11px; text-transform: uppercase; color: var(--ink-faint);">Fats</div>
                                <strong style="font-size: 16px; color: var(--kaki);">${data.fat_g}g</strong>
                            </div>
                        </div>
                        
                        <strong style="font-size: 13px; display: block; margin-bottom: 8px;">Detected Items:</strong>
                        <ul style="font-size: 13px; color: var(--ink-soft); padding-left: 20px; margin-bottom: 16px;">
                    `;
                    
                    if (data.items && data.items.length) {
                        data.items.forEach(item => {
                            html += `<li>${item.name} (${item.portion}) — ${item.calories} kcal</li>`;
                        });
                    } else {
                        html += `<li>No specific items detected.</li>`;
                    }
                    
                    html += `</ul>
                        <div style="background: rgba(161, 90, 46, 0.05); border-left: 3px solid var(--kaki); padding: 12px; border-radius: 0 6px 6px 0; font-size: 13px; font-style: italic; color: var(--ink);">
                            "${data.summary}"
                        </div>
                    `;
                    
                    if (analysisResult) analysisResult.innerHTML = html;
                } catch (err) {
                    showToast(err.message);
                } finally {
                    showLoading(false);
                }
            });
        }
"""

content = re.sub(pattern, new_js, content, flags=re.DOTALL)

# Let's also fix the HTML where switchNutritionTab is called so it passes 'this'
content = content.replace("onclick=\"switchNutritionTab('nutri-macro')\"", "onclick=\"switchNutritionTab('nutri-macro', this)\"")
content = content.replace("onclick=\"switchNutritionTab('nutri-scanner')\"", "onclick=\"switchNutritionTab('nutri-scanner', this)\"")
content = content.replace("onclick=\"switchNutritionTab('nutri-hydration')\"", "onclick=\"switchNutritionTab('nutri-hydration', this)\"")

with open("index.html", "w") as f:
    f.write(content)

print("Replaced JS")
