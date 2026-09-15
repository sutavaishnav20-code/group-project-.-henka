import re

with open("index.html", "r") as f:
    content = f.read()

onResults_pattern = r"function onResults\(results\) \{[\s\S]*?canvasCtx\.restore\(\);\s*\}"

def onResults_replacer(match):
    return """function onResults(results) {
            canvasCtx.save();
            canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
            canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

            const ex = document.getElementById('exerciseSelect').value;
            const repLabel = document.querySelector('#repCountDisplay').previousElementSibling;

            if (ex === 'planks') {
                repLabel.innerText = 'SECONDS';
                if (results.poseLandmarks) {
                    window.drawConnectors(canvasCtx, results.poseLandmarks, window.POSE_CONNECTIONS, {color: '#A15A2E', lineWidth: 4});
                    window.drawLandmarks(canvasCtx, results.poseLandmarks, {color: '#FF0000', lineWidth: 2});
                    
                    const leftShoulder = results.poseLandmarks[11];
                    const leftHip = results.poseLandmarks[23];
                    const leftAnkle = results.poseLandmarks[27];

                    if (leftShoulder && leftHip && leftAnkle && leftShoulder.visibility > 0.5) {
                        const yDiffShoulderHip = Math.abs(leftShoulder.y - leftHip.y);
                        const yDiffHipAnkle = Math.abs(leftHip.y - leftAnkle.y);

                        // If body is relatively flat
                        if (yDiffShoulderHip < 0.2 && yDiffHipAnkle < 0.2) {
                            if (!isHolding) {
                                isHolding = true;
                                timerStart = Date.now() - (currentDuration * 1000);
                                feedbackEl.innerText = 'Hold it...';
                                feedbackEl.style.background = 'rgba(74, 111, 100, 0.9)';
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
                    window.drawConnectors(canvasCtx, results.poseLandmarks, window.POSE_CONNECTIONS, {color: '#A15A2E', lineWidth: 4});
                    window.drawLandmarks(canvasCtx, results.poseLandmarks, {color: '#FF0000', lineWidth: 2});

                    if (ex === 'squats') {
                        const hip = results.poseLandmarks[23];
                        const knee = results.poseLandmarks[25];
                        const ankle = results.poseLandmarks[27];
                        if (hip && knee && ankle && hip.visibility > 0.5) {
                            const angle = calculateAngle(hip, knee, ankle);
                            if (angle > 160) {
                                if (exerciseStage === 'down') {
                                    repCount++;
                                    repCountDisplay.innerText = repCount;
                                    feedbackEl.innerText = 'Good Rep!';
                                    feedbackEl.style.background = 'rgba(74, 111, 100, 0.9)';
                                }
                                exerciseStage = 'up';
                            }
                            if (angle < 100) {
                                exerciseStage = 'down';
                                feedbackEl.innerText = 'Go up!';
                                feedbackEl.style.background = 'rgba(31, 63, 88, 0.9)';
                            }
                            if (exerciseStage === 'up' && angle < 160 && angle > 100) {
                                feedbackEl.innerText = 'Go lower...';
                                feedbackEl.style.background = 'rgba(161, 90, 46, 0.9)';
                            }
                        }
                    } else if (ex === 'pushups') {
                        const shoulder = results.poseLandmarks[11];
                        const elbow = results.poseLandmarks[13];
                        const wrist = results.poseLandmarks[15];
                        if (shoulder && elbow && wrist && shoulder.visibility > 0.5) {
                            const angle = calculateAngle(shoulder, elbow, wrist);
                            if (angle > 160) {
                                if (exerciseStage === 'down') {
                                    repCount++;
                                    repCountDisplay.innerText = repCount;
                                    feedbackEl.innerText = 'Good Rep!';
                                    feedbackEl.style.background = 'rgba(74, 111, 100, 0.9)';
                                }
                                exerciseStage = 'up';
                            }
                            if (angle < 90) {
                                exerciseStage = 'down';
                                feedbackEl.innerText = 'Push up!';
                                feedbackEl.style.background = 'rgba(31, 63, 88, 0.9)';
                            }
                        }
                    } else if (ex === 'bicep_curls') {
                        const shoulder = results.poseLandmarks[12];
                        const elbow = results.poseLandmarks[14];
                        const wrist = results.poseLandmarks[16];
                        if (shoulder && elbow && wrist && shoulder.visibility > 0.5) {
                            const angle = calculateAngle(shoulder, elbow, wrist);
                            if (angle > 160) {
                                if (exerciseStage === 'up') {
                                    repCount++;
                                    repCountDisplay.innerText = repCount;
                                    feedbackEl.innerText = 'Good Rep!';
                                    feedbackEl.style.background = 'rgba(74, 111, 100, 0.9)';
                                }
                                exerciseStage = 'down';
                            }
                            if (angle < 45) {
                                exerciseStage = 'up';
                                feedbackEl.innerText = 'Squeeze & lower...';
                                feedbackEl.style.background = 'rgba(31, 63, 88, 0.9)';
                            }
                        }
                    }
                } else {
                    feedbackEl.innerText = 'Align your body to start.';
                }
            }
            canvasCtx.restore();
        }"""

content = re.sub(onResults_pattern, onResults_replacer, content, flags=re.DOTALL)

with open("index.html", "w") as f:
    f.write(content)
print("Done onResults")
