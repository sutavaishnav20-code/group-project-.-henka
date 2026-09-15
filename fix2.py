with open('index.html', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<div id="tab-walk"' in line:
        # Check lines before this
        print("Lines before tab-walk:")
        for j in range(i-5, i+1):
            print(repr(lines[j]))
        break
