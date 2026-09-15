import json

with open("metadata.json", "r") as f:
    data = json.load(f)

if "geolocation" not in data.get("requestFramePermissions", []):
    data.setdefault("requestFramePermissions", []).append("geolocation")

with open("metadata.json", "w") as f:
    json.dump(data, f, indent=2)

print("Updated metadata.json")
