import re

with open("server.js", "r") as f:
    content = f.read()

api_route = """
app.post('/api/reframe-anxiety', async (req, res) => {
    try {
        const { anxietyText } = req.body;
        if (!anxietyText) return res.status(400).json({ error: 'Text is required' });

        const prompt = `You are a cognitive behavioral therapy assistant. The user is experiencing this anxious thought: "${anxietyText}".
Provide a concise, objective, and empathetic "reframed perspective" (3-4 sentences maximum) that helps ground them and challenge any cognitive distortions. Keep it practical and calm.`;

        const result = await genAI.getGenerativeModel({ model: "gemini-2.5-flash" }).generateContent(prompt);
        const reframed = result.response.text();
        
        res.json({ reframed });
    } catch (error) {
        console.error('Reframe Error:', error);
        res.status(500).json({ error: 'Failed to reframe anxiety.' });
    }
});
"""

if "/api/reframe-anxiety" not in content:
    content = content.replace("app.post('/api/inquiries', async (req, res) => {", api_route + "\napp.post('/api/inquiries', async (req, res) => {")

with open("server.js", "w") as f:
    f.write(content)
print("Updated server.js")
