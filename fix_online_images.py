import os

# البحث عن ملف online_games.html
online_files = []
for root, dirs, files in os.walk('templates'):
    for file in files:
        if 'online' in file.lower():
            online_files.append(os.path.join(root, file))

print(f" found files: {online_files}")

# إنشاء صور افتراضية احترافية باستخدام CSS/SVG بدلاً من الصور المفقودة
os.makedirs('static/images', exist_ok=True)

# إنشاء صورة Y8 Games (SVG)
with open('static/images/y8-games.svg', 'w') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100">
        <rect fill="#ef4444" width="200" height="100" rx="10"/>
        <text x="100" y="60" font-family="Arial" font-size="40" font-weight="bold" fill="white" text-anchor="middle">Y8</text>
    </svg>''')

# إنشاء صورة Poki (SVG)
with open('static/images/poki.svg', 'w') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100">
        <rect fill="#22c55e" width="200" height="100" rx="10"/>
        <text x="100" y="60" font-family="Arial" font-size="35" font-weight="bold" fill="white" text-anchor="middle">POKI</text>
    </svg>''')

# إنشاء صورة Crazy Games (SVG)
with open('static/images/crazy-games.svg', 'w') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100">
        <rect fill="#a855f7" width="200" height="100" rx="10"/>
        <text x="100" y="45" font-family="Arial" font-size="25" font-weight="bold" fill="white" text-anchor="middle">CRAZY</text>
        <text x="100" y="75" font-family="Arial" font-size="20" fill="white" text-anchor="middle">GAMES</text>
    </svg>''')

# إنشاء صورة Kizi (SVG)
with open('static/images/kizi.svg', 'w') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100">
        <rect fill="#3b82f6" width="200" height="100" rx="10"/>
        <text x="100" y="60" font-family="Arial" font-size="35" font-weight="bold" fill="white" text-anchor="middle">KIZI</text>
    </svg>''')

# إنشاء صورة Friv (SVG)
with open('static/images/friv.svg', 'w') as f:
    f.write('''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" viewBox="0 0 200 100">
        <rect fill="#f59e0b" width="200" height="100" rx="10"/>
        <text x="100" y="60" font-family="Arial" font-size="35" font-weight="bold" fill="white" text-anchor="middle">FRIV</text>
    </svg>''')

print("✅ تم إنشاء صور SVG احترافية")

# تحديث config.py لتستخدم SVG بدلاً من PNG
with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('.png', '.svg')
print("✅ تم تحديث المسارات في config.py")

with open('config.py', 'w', encoding='utf-8') as f:
    f.write(content)
