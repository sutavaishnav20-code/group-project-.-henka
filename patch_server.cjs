const fs = require('fs');

let serverCode = fs.readFileSync('server.js', 'utf8');

const configRoute = `
app.get('/api/config', (req, res) => {
  res.json({ mapsApiKey: process.env.GOOGLE_MAPS_API_KEY || '' });
});
`;

serverCode = serverCode.replace(
  "app.get('/api/health', (req, res) => {\n  res.json({ status: 'ok', time: new Date().toISOString() });\n});",
  "app.get('/api/health', (req, res) => {\n  res.json({ status: 'ok', time: new Date().toISOString() });\n});\n" + configRoute
);

fs.writeFileSync('server.js', serverCode);
console.log("Patched server.js");
