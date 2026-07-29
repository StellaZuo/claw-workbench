# 里里工作台 (PWA)

左星的个人工作台，可在手机主屏当作 app 使用（PWA：添加到主屏幕即全屏离线可用）。

## 结构
- `index.html` 仪表盘（手机优先，深色主题）
- `manifest.json` PWA 配置（名称 / 图标 / 全屏）
- `sw.js` Service Worker（离线缓存）
- `data.js` 由各空间扫描生成（**由脚本产出，勿手改**）
- `icons/` 应用图标
- `gen_workbench.py` 数据扫描 + 图标生成脚本

## 重生成
数据更新后，在 workbench 目录运行：
```
python gen_workbench.py
```
会刷新 `data.js` 与图标。

## 部署
见主工作区说明：需部署到可公网访问的静态托管（GitHub Pages / CloudStudio / OneDrive 等），
手机才能外网打开。本地可用 `python -m http.server` 或 `npx serve` 预览。
