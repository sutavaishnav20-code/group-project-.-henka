import re

with open("index.html", "r") as f:
    content = f.read()

# 1. Insert Tab Logic and BMI before // --- Fitness Plan Generation ---
bmi_logic = """
        // --- Physical Tabs & BMI ---
        window.switchPhysicalTab = function(tabId) {
            document.querySelectorAll('.physical-tabs .tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
            
            document.querySelector(`[onclick="switchPhysicalTab('${tabId}')"]`).classList.add('active');
            document.getElementById(tabId).classList.add('active');
        };

        document.getElementById('bmiForm').addEventListener('submit', (e) => {
            e.preventDefault();
            const w = parseFloat(document.getElementById('bmiWeight').value);
            const h = parseFloat(document.getElementById('bmiHeight').value) / 100;
            if (w && h) {
                const bmi = (w / (h * h)).toFixed(1);
                let cat = "Normal weight";
                let color = "var(--moss)";
                if (bmi < 18.5) { cat = "Underweight"; color = "var(--kaki)"; }
                else if (bmi >= 25 && bmi < 30) { cat = "Overweight"; color = "var(--gold)"; }
                else if (bmi >= 30) { cat = "Obese"; color = "var(--kaki)"; }
                
                const res = document.getElementById('bmiResult');
                res.innerHTML = `
                    <div style="font-size: 13px; color: var(--ink-soft);">Your BMI</div>
                    <strong style="font-size: 32px; color: ${color};">${bmi}</strong>
                    <div style="font-size: 14px; font-weight: 600; margin-top: 4px;">${cat}</div>
                `;
                res.style.display = 'block';
                
                // Pre-fill plan form
                document.getElementById('planWeight').value = w;
                document.getElementById('planHeight').value = (h*100).toFixed(0);
            }
        });

"""
content = content.replace("// --- Fitness Plan Generation ---", bmi_logic + "// --- Fitness Plan Generation ---")


# 2. Update startCameraBtn event listener
old_camera_code = """        document.getElementById('startCameraBtn').addEventListener('click', async () => {
            const container = document.getElementById('cameraContainer');
            const startBtn = document.getElementById('startCameraBtn');
            const stopBtn = document.getElementById('stopCameraBtn');
            
            container.style.display = 'block';
            startBtn.style.display = 'none';
            stopBtn.style.display = 'flex';
            feedbackEl.style.display = 'block';
            feedbackEl.innerText = 'Initializing AI Model...';

            if (!trackerPose) {
                trackerPose = new window.Pose({locateFile: (file) => {
                    return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
                }});
                trackerPose.setOptions({
                    modelComplexity: 1,
                    smoothLandmarks: true,
                    enableSegmentation: false,
                    smoothSegmentation: false,
                    minDetectionConfidence: 0.5,
                    minTrackingConfidence: 0.5
                });
                trackerPose.onResults(onResults);
            }

            if (!trackerCamera) {
                trackerCamera = new window.Camera(videoElement, {
                    onFrame: async () => {
                        await trackerPose.send({image: videoElement});
                    },
                    width: 640,
                    height: 480
                });
            }
            
            trackerCamera.start();
        });"""


new_camera_code = """        document.getElementById('startCameraBtn').addEventListener('click', async () => {
            const container = document.getElementById('cameraContainer');
            const startBtn = document.getElementById('startCameraBtn');
            const stopBtn = document.getElementById('stopCameraBtn');
            
            try {
                // Explicitly ask for camera permission first
                await navigator.mediaDevices.getUserMedia({ video: true });
            } catch (err) {
                showToast("Camera access denied or unavailable.");
                return;
            }
            
            container.style.display = 'block';
            startBtn.style.display = 'none';
            stopBtn.style.display = 'flex';
            feedbackEl.style.display = 'block';
            feedbackEl.innerText = 'Downloading AI Model (Faster Lite Version)... Please wait.';
            feedbackEl.style.background = 'rgba(31, 63, 88, 0.9)';

            if (!trackerPose) {
                trackerPose = new window.Pose({locateFile: (file) => {
                    return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
                }});
                trackerPose.setOptions({
                    modelComplexity: 0, // 0 for faster load
                    smoothLandmarks: true,
                    enableSegmentation: false,
                    smoothSegmentation: false,
                    minDetectionConfidence: 0.5,
                    minTrackingConfidence: 0.5
                });
                trackerPose.onResults(onResults);
            }

            if (!trackerCamera) {
                trackerCamera = new window.Camera(videoElement, {
                    onFrame: async () => {
                        await trackerPose.send({image: videoElement});
                    },
                    width: 640,
                    height: 480
                });
            }
            
            trackerCamera.start();
        });"""

content = content.replace(old_camera_code, new_camera_code)

with open("index.html", "w") as f:
    f.write(content)
print("done")
