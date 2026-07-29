# -*- coding: utf-8 -*-
"""
里里工作台 · 数据扫描 + 图标生成
运行：python gen_workbench.py
产物：workbench/data.js  (供 index.html 读取)
       workbench/icons/icon-192.png, icon-512.png
只读取业务数据 + 记忆，排除 .workbuddy 配置与凭据。
"""
import os, re, json, datetime
from PIL import Image, ImageDraw, ImageFont

WS = r'C:\Users\叶磊\WorkBuddy\Claw'
OUT = os.environ.get('WB_OUT', os.path.join(WS, 'workbench'))
PUBLIC = os.environ.get('WB_PUBLIC') == '1'
ICONS = os.path.join(OUT, 'icons')
os.makedirs(ICONS, exist_ok=True)

def md_files(d):
    if not os.path.isdir(d):
        return []
    return [f for f in os.listdir(d) if f.endswith('.md')]

# ---------- work / 客户台账 ----------
clients_dir = os.path.join(WS, 'work', 'clients')
client_files = [f for f in md_files(clients_dir) if not f.startswith('_')]
client_count = len(client_files)

status_breakdown = {}
recent_clients = []
overview_path = os.path.join(clients_dir, '_总览_活跃管线.md')
if os.path.isfile(overview_path):
    txt = open(overview_path, encoding='utf-8').read()
    rows = []
    for line in txt.splitlines():
        m = re.match(r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|', line)
        if m:
            name = m.group(2).strip()
            st = m.group(3).strip()
            rows.append(name)
            status_breakdown[st] = status_breakdown.get(st, 0) + 1
    recent_clients = [] if PUBLIC else rows[:12]

# ---------- fatloss / 减脂 ----------
fl_dir = os.path.join(WS, 'fatloss', 'daily')
fl_files = sorted([f for f in md_files(fl_dir) if not f.startswith('_')], reverse=True)
latest_fl = None
if fl_files:
    t = open(os.path.join(fl_dir, fl_files[0]), encoding='utf-8').read()
    weight = re.search(r'(\d+)\s*斤', t)
    water = re.search(r'饮水', t)
    binge = re.search(r'未发生暴食|是否发生[：:].*?否|抗住.*?暴食', t)
    latest_fl = {
        'file': fl_files[0].replace('.md', ''),
        'weight': weight.group(1) if weight else None,
        'water': ('已饮水' if water else None),
        'no_binge': bool(binge),
    }
fatloss_streak = len(fl_files)

# ---------- study / 学习 ----------
study_dir = os.path.join(WS, 'study')
study_cats = {}
if os.path.isdir(study_dir):
    for cat in os.listdir(study_dir):
        cpath = os.path.join(study_dir, cat)
        if os.path.isdir(cpath) and not cat.startswith('_') and not cat.startswith('.'):
            study_cats[cat] = len([f for f in os.listdir(cpath) if f.endswith('.md')])
study_total = sum(study_cats.values())

# ---------- review / 复盘 ----------
rev_dir = os.path.join(WS, 'review')
rev = {}
for sub in ['daily', 'weekly', 'monthly']:
    sd = os.path.join(rev_dir, sub)
    fs = sorted([f for f in md_files(sd) if not f.startswith('_')], reverse=True)
    rev[sub] = fs[0].replace('.md', '') if fs else None

# ---------- life / 生活 ----------
life_daily = os.path.join(WS, 'life', 'daily')
life_files = sorted([f for f in md_files(life_daily) if not f.startswith('_')], reverse=True) if os.path.isdir(life_daily) else []
life_has = len(life_files) > 0

# ---------- memory / 记忆 ----------
mem_dir = os.path.join(WS, '.workbuddy', 'memory')
today = datetime.date.today().strftime('%Y-%m-%d')
mem_today = os.path.join(mem_dir, today + '.md')
mem_today_exists = os.path.isfile(mem_today)

data = {
    'generated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    'date': today,
    'spaces': {
        'work': {'clientCount': client_count, 'statusBreakdown': status_breakdown,
                 'recentClients': recent_clients},
        'fatloss': {'streak': fatloss_streak, 'latest': latest_fl},
        'study': {'total': study_total, 'byCat': study_cats},
        'review': rev,
        'life': {'hasData': life_has, 'recent': [f.replace('.md', '') for f in life_files[:5]]},
    },
    'memory': {'todayExists': mem_today_exists},
}

with open(os.path.join(OUT, 'data.js'), 'w', encoding='utf-8') as f:
    f.write('window.WB_DATA = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n')

# ---------- 图标 ----------
def make_icon(size):
    img = Image.new('RGB', (size, size), (15, 20, 25))
    d = ImageDraw.Draw(img)
    margin = int(size * 0.16)
    d.ellipse([margin, margin, size - margin, size - margin], fill=(240, 180, 60))
    try:
        font = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', int(size * 0.46))
    except Exception:
        font = ImageFont.load_default()
    txt = '里'
    bbox = d.textbbox((0, 0), txt, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((size - tw) / 2, (size - th) / 2 - bbox[1]), txt, font=font, fill=(15, 20, 25))
    img.save(os.path.join(ICONS, 'icon-%d.png' % size))

make_icon(192)
make_icon(512)

print('workbench 数据+图标生成完成')
print('  clients:', client_count, '| status:', status_breakdown)
print('  fatloss streak:', fatloss_streak, '| latest:', latest_fl)
print('  study:', study_cats)
print('  review:', rev)
print('  life hasData:', life_has, '| mem today:', mem_today_exists)
