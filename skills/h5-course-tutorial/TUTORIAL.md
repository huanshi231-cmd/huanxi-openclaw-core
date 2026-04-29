# 【从零开始学做H5课件 · 完整教程】
> 作者：太阳
> 日期：2026-04-19
> 基于：wealth吸引_v4_滑动翻页.html 实战复盘

---

## 一、先看效果

这份教程会教你做出这样的H5课件：

✅ 全屏播放，像PPT一样一页一页翻
✅ 支持触摸滑动（手机/平板）
✅ 支持键盘翻页（电脑）
✅ 支持鼠标滑动翻页
✅ 底部进度条，点击跳转
✅ 深色高级感设计
✅ 直接浏览器打开，无需任何软件

**文件越小越好**（本教程产出约18KB，比PowerPoint轻100倍）

---

## 二、整体流程（3步搞定）

```
第1步：告诉我你要做什么主题
     ↓
第2步：我生成HTML文件（30秒）
     ↓
第3步：双击浏览器打开，完事
```

---

## 三、准备工作（只需做一次）

### 3.1 确认Mac有这些（一般都有）

- 浏览器：Chrome/Safari/Edge 任意一个
- 文本编辑器：VS Code（推荐，免费）或者备忘录也行

### 3.2 安装VS Code（没有才装）

```
1. 打开 https://code.visualstudio.com
2. 点 Download Mac
3. 拖到应用程序文件夹
4. 打开
```

---

## 四、核心代码讲解

### 4.1 整体结构（必须背下来）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>你的标题</title>
<!-- 字体（自动从Google加载） -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
/* 样式写这里 */
</style>
</head>
<body>

<!-- 幻灯片容器 -->
<div class="slides-container">
    
    <!-- 第1页 -->
    <div class="slide active" style="background:渐变背景">
        <div class="page-tag">01</div>
        <!-- 这一页的内容 -->
        <div style="text-align:center">
            <h1>标题</h1>
            <p>副标题</p>
        </div>
    </div>
    
    <!-- 第2页 -->
    <div class="slide" style="background:渐变背景">
        <div class="page-tag">02</div>
        <!-- 这一页的内容 -->
    </div>

</div>

<script>
// 交互逻辑写这里
</script>
</body>
</html>
```

### 4.2 样式（CSS）核心代码

```css
/* 重置默认样式 */
* { margin: 0; padding: 0; box-sizing: border-box; }

/* body：深色背景，字体 */
body { 
    font-family: 'Noto Sans SC', sans-serif; 
    background: #0a0a0f; /* 深黑底色 */
    color: #fff; 
    overflow: hidden; /* 禁止滚动 */
}

/* 幻灯片容器：占满全屏 */
.slides-container { 
    width: 100vw;  /* 100%视口宽度 */
    height: 100vh; /* 100%视口高度 */
    position: relative; 
    overflow: hidden; 
}

/* 每一页：绝对定位，叠在一起 */
.slide { 
    width: 100%; height: 100%; 
    position: absolute; top: 0; left: 0;
    display: flex; /* 弹性布局 */
    flex-direction: column; /* 垂直排列 */
    align-items: center; /* 水平居中 */
    justify-content: center; /* 垂直居中 */
    transform: translateX(100%); /* 默认在右边 */
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1); /* 动画 */
}

/* 当前页：移到中间 */
.slide.active { transform: translateX(0); }

/* 上一页：稍微露出来一点 */
.slide.prev { transform: translateX(-30%); }

/* 页码标签：固定在左上角 */
.page-tag { 
    position: fixed; top: 20px; left: 28px; 
    background: rgba(139,92,246,0.2); 
    border: 1px solid rgba(139,92,246,0.4); 
    color: #c084fc; 
    padding: 6px 16px; 
    border-radius: 20px; 
    font-size: 0.85rem; 
    font-weight: 700; 
    z-index: 200; 
}

/* 底部进度条容器 */
.progress-bar { 
    position: fixed; bottom: 24px; left: 50%; 
    transform: translateX(-50%); 
    display: flex; 
    gap: 10px; 
    z-index: 200; 
}

/* 进度点：圆形 */
.progress-dot { 
    width: 10px; height: 10px; 
    border-radius: 50%; 
    background: rgba(255,255,255,0.2); 
    cursor: pointer; 
    transition: all 0.3s; 
}

/* 当前进度点：高亮放大 */
.progress-dot.active { 
    background: #c084fc; 
    transform: scale(1.4); 
}
```

### 4.3 交互逻辑（JavaScript）核心代码

```javascript
<script>
var slides = document.querySelectorAll('.slide');       // 所有幻灯片
var dots = document.querySelectorAll('.progress-dot');  // 所有进度点
var currentSlide = 0;  // 当前是第几页（从0开始）

// 更新页面状态
function update() {
    // 遍历所有幻灯片
    for (var i = 0; i < slides.length; i++) {
        slides[i].classList.remove('active', 'prev');
        dots[i].classList.remove('active');
        if (i === currentSlide) {
            slides[i].classList.add('active');
            dots[i].classList.add('active');
        } else if (i < currentSlide) {
            slides[i].classList.add('prev');
        }
    }
    // 更新页码显示
    document.getElementById('pageTag').textContent = 
        String(currentSlide + 1).padStart(2, '0');
}

// 下一页
function next() { 
    if (currentSlide < slides.length - 1) { 
        currentSlide++; 
        update(); 
    } 
}

// 上一页
function prev() { 
    if (currentSlide > 0) { 
        currentSlide--; 
        update(); 
    } 
}

// 跳转到指定页
function go(i) { 
    currentSlide = i; 
    update(); 
}

// 键盘翻页
document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') next();
    if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') prev();
});

// 触摸滑动翻页（手机）
document.addEventListener('touchstart', function(e) {
    window._tx = e.touches[0].clientX;
});
document.addEventListener('touchend', function(e) {
    var dx = e.changedTouches[0].clientX - window._tx;
    if (dx < -50) next();
    if (dx > 50) prev();
});
</script>
```

### 4.4 进度条HTML（放在最后）

```html
<!-- 进度条：动态生成 -->
<div class="progress-bar" id="progressBar"></div>
<script>
// 动态生成进度点
var html = '';
for (var i = 0; i < slides.length; i++) {
    html += '<div class="progress-dot' + (i === 0 ? ' active' : '') + '" onclick="go(' + i + ')"></div>';
}
document.getElementById('progressBar').innerHTML = html;
</script>
```

### 4.5 页码HTML

```html
<!-- 页码标签：固定左上角 -->
<div class="page-tag" id="pageTag">01</div>
```

---

## 五、渐变背景配方（直接复制用）

### 紫色系（最常用）
```html
style="background:linear-gradient(135deg,#1a0a2e 0%,#0f0a1e 100%)"
```

### 深蓝系
```html
style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%)"
```

### 深红暗色
```html
style="background:linear-gradient(135deg,#1a0a0a 0%,#2e1a1a 100%)"
```

### 纯黑+光效
```html
style="background:#0a0a0f"
```
（配合 div 叠加渐变光效）

### 光效叠加代码（放内容 div 里面）
```html
<div style="position:absolute;inset:0;
    background:radial-gradient(ellipse at 70% 30%,rgba(139,92,246,0.25) 0%,transparent 60%),
               radial-gradient(ellipse at 30% 80%,rgba(236,72,153,0.2) 0%,transparent 50%)">
</div>
```

---

## 六、常用内容样式

### 大标题
```html
<h1 style="font-size:4rem;font-weight:900;color:#fff;margin-bottom:1rem">
    标题文字
</h1>
```

### 副标题
```html
<p style="font-size:1.4rem;color:rgba(255,255,255,0.6)">
    副标题文字
</p>
```

### 关键词高亮
```html
<span style="color:#c084fc;font-weight:700">高亮词</span>
```

### 渐变分隔线
```html
<div style="width:80px;height:2px;
    background:linear-gradient(90deg,transparent,#c084fc,transparent);
    margin:0 auto 1.5rem">
</div>
```

### 卡片容器
```html
<div style="background:rgba(139,92,246,0.1);
    border:1px solid rgba(139,92,246,0.3);
    border-radius:16px;padding:2rem">
    卡片内容
</div>
```

### 双栏对比
```html
<div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem">
    <div>左栏</div>
    <div>右栏</div>
</div>
```

### 引用文字
```html
<div style="font-size:10rem;color:rgba(192,132,252,0.1);line-height:0.5">"</div>
<h2 style="font-size:3rem;font-weight:900;color:#fff">引用内容</h2>
```

### Emoji装饰
```html
<div style="font-size:5rem">💎</div>
<div style="font-size:8rem">✨</div>
<div style="font-size:6rem">🔮</div>
```

### 标签/徽章
```html
<div style="display:inline-block;
    background:rgba(139,92,246,0.2);
    border:1px solid rgba(139,92,246,0.4);
    color:#c084fc;padding:6px 16px;
    border-radius:20px;font-size:0.85rem">
    标签文字
</div>
```

---

## 七、完整示例：3页课件

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>财富吸引 · 欢喜</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Noto Sans SC', sans-serif; background: #0a0a0f; color: #fff; overflow: hidden; }
.slides-container { width: 100vw; height: 100vh; position: relative; overflow: hidden; }
.slide { width: 100%; height: 100%; position: absolute; top: 0; left: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; transform: translateX(100%); transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
.slide.active { transform: translateX(0); }
.slide.prev { transform: translateX(-30%); }
.page-tag { position: fixed; top: 20px; left: 28px; background: rgba(139,92,246,0.2); border: 1px solid rgba(139,92,246,0.4); color: #c084fc; padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; z-index: 200; }
.progress-bar { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; z-index: 200; }
.progress-dot { width: 10px; height: 10px; border-radius: 50%; background: rgba(255,255,255,0.2); cursor: pointer; transition: all 0.3s; }
.progress-dot.active { background: #c084fc; transform: scale(1.4); }
</style>
</head>
<body>

<div class="page-tag" id="pageTag">01</div>
<div class="slides-container">

    <!-- 第1页：标题页 -->
    <div class="slide active" style="background:linear-gradient(135deg,#1a0a2e 0%,#0f0a1e 100%);">
        <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 70% 30%,rgba(139,92,246,0.25) 0%,transparent 60%);"></div>
        <div style="position:relative;text-align:center;z-index:1;">
            <div style="font-size:5rem">💎</div>
            <h1 style="font-size:5rem;font-weight:900;margin-bottom:1rem">财富吸引</h1>
            <p style="font-size:1.4rem;color:rgba(255,255,255,0.6)">从恐惧频率 → 爱的频率</p>
        </div>
    </div>

    <!-- 第2页：核心观点 -->
    <div class="slide" style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);">
        <div style="position:relative;text-align:center;z-index:1;">
            <h1 style="font-size:4rem;font-weight:900;margin-bottom:2rem">你不是缺钱<br><span style="color:#60a5fa">你是缺频率</span></h1>
            <p style="font-size:1.3rem;color:rgba(255,255,255,0.55)">钱不是追来的，是调频调出来的</p>
        </div>
    </div>

    <!-- 第3页：对比 -->
    <div class="slide" style="background:#0a0a0f;">
        <div style="position:relative;width:90%;max-width:1000px;z-index:1;">
            <h1 style="font-size:3rem;font-weight:900;margin-bottom:3rem;text-align:center">两种频率 · 两种结局</h1>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem">
                <div style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:20px;padding:2rem">
                    <div style="color:#f87171;font-weight:700;margin-bottom:1rem">恐惧频率</div>
                    <div style="font-size:1.5rem;font-weight:700;margin-bottom:1rem">盯着余额</div>
                    <p style="color:rgba(255,255,255,0.5);line-height:2">焦虑 · 收缩 · 匮乏<br>财富管道关闭</p>
                </div>
                <div style="background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.3);border-radius:20px;padding:2rem">
                    <div style="color:#c084fc;font-weight:700;margin-bottom:1rem">爱的频率</div>
                    <div style="font-size:1.5rem;font-weight:700;margin-bottom:1rem">盯着价值</div>
                    <p style="color:rgba(255,255,255,0.5);line-height:2">扩张 · 喜悦 · 本自具足<br>财富主动靠近</p>
                </div>
            </div>
        </div>
    </div>

</div>

<div class="progress-bar" id="progressBar"></div>

<script>
var slides = document.querySelectorAll('.slide');
var dots = document.querySelectorAll('.progress-dot');
var currentSlide = 0;

function update() {
    for (var i = 0; i < slides.length; i++) {
        slides[i].classList.remove('active', 'prev');
        dots[i].classList.remove('active');
        if (i === currentSlide) {
            slides[i].classList.add('active');
            dots[i].classList.add('active');
        } else if (i < currentSlide) {
            slides[i].classList.add('prev');
        }
    }
    document.getElementById('pageTag').textContent = String(currentSlide + 1).padStart(2, '0');
}

function next() { if (currentSlide < slides.length - 1) { currentSlide++; update(); } }
function prev() { if (currentSlide > 0) { currentSlide--; update(); } }
function go(i) { currentSlide = i; update(); }

document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') next();
    if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') prev();
});

document.addEventListener('touchstart', function(e) { window._tx = e.touches[0].clientX; });
document.addEventListener('touchend', function(e) {
    var dx = e.changedTouches[0].clientX - window._tx;
    if (dx < -50) next();
    if (dx > 50) prev();
});

var html = '';
for (var i = 0; i < slides.length; i++) {
    html += '<div class="progress-dot' + (i === 0 ? ' active' : '') + '" onclick="go(' + i + ')"></div>';
}
document.getElementById('progressBar').innerHTML = html;
</script>

</body>
</html>
```

---

## 八、Q&A 常见问题

### Q：为什么字体显示不出来？
A：检查网络，字体从 Google Fonts 加载。离线环境需要先把字体下载到本地。

### Q：怎么加新的一页？
A：在 `</div>` 之前加：
```html
<div class="slide" style="background:渐变">
    <div class="page-tag">页码</div>
    内容...
</div>
```

### Q：怎么改颜色风格？
A：改 `background:linear-gradient(...)` 里的颜色代码。

### Q：支持视频吗？
A：支持，直接用 `<video>` 标签插入。

### Q：能加音乐吗？
A：能，加这个：
```html
<audio src="音乐.mp3" autoplay loop></audio>
```

---

## 九、注意事项

1. **文件编码**：保存时选 UTF-8，不然中文乱码
2. **图片路径**：用相对路径或绝对URL，不要用本地绝对路径（如 /Users/xxx）
3. **文件位置**：建议放桌面或 iCloud 同步文件夹，方便分享
4. **分享方式**：上传到网盘/微信/邮件，对方直接浏览器打开即可

---

## 十、快速开始清单

- [ ] 打开文本编辑器（VS Code）
- [ ] 复制上面的完整示例代码
- [ ] 保存为 `course.html` 到桌面
- [ ] 用 Chrome 打开
- [ ] 测试翻页（键盘/触摸/鼠标）
- [ ] 开始改内容
- [ ] 完成，文件名改为 `h5-[主题]_[日期].html`

---

*教程完成 | 2026-04-19*
*产出位置：~/.openclaw/workspace-main/skills/h5-course-tutorial/*
