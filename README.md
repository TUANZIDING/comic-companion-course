<p align="center"><img src="course/assets/%E8%AF%BE%E7%A8%8B%E5%B0%81%E9%9D%A2v1.0.svg" width="100%" alt="Codex辅助编写的原创SVG概念封面：一本书与五页纸卡，非原著插画"></p>
<h1 align="center">从一本书到漫画伴读<br>Comic Companion Course</h1>
<p align="center">把故事整理为看、读、演的五页小课堂。<br>Turn a story into a five-page comic reading workshop.</p>
<p align="center"><a href="README.md">简体中文</a> · <a href="docs/%E8%8B%B1%E6%96%87%E8%AF%B4%E6%98%8Ev1.1.md">English</a></p>
<p align="center"><code>免费非商业 v1.1</code> · <code>12课</code> · <a href="LICENSE">CC BY-NC 4.0：课程文字与代码</a></p>
<p align="center"><a href="https://tuanziding.github.io/comic-companion-course/">在线课程</a> · <a href="#showcase">两本案例</a> · <a href="#start">快速开始</a> · <a href="#workflow">工作流</a> · <a href="#status">能力状态</a> · <a href="#contact">共创与联系</a></p>

这是面向医学科研人员和AI应用学习者的纯静态HTML课程。读者及医学场景均为虚构示例。项目策划、改编组织与维护者：**Haixiang Ding, MD**，急诊创伤外科医生，苏州大学临床医学博士在读。

**AI参与声明：**两本历史漫画伴读借助Hark组织制作；课程文字、提示词、网页和示例代码由Codex辅助编写。新提示词和代码均是“教学示例，非原始制作记录”。具体生图模型、参考图、原始cast sheet及提示词记录仍【待补充】。本轮Codex实际内容审阅与本地自检不等于独立人工、法律或医学专家验收；Hark此前失败的审阅不计为通过。

<a id="scenarios"></a>
## 适合怎样使用

| 你想做什么 | 从哪里开始 |
| --- | --- |
| 根据孩子兴趣设置难度 | 第01课：虚构读者卡、句长与词表 |
| 把一段故事整理成漫画 | 第03–06课：分镜、角色、图文和五页结构 |
| 运行可修改的排版示例 | 第07课与examples目录 |
| 迁移到医学教学 | 第10课：虚构场景、来源与专业审核 |

<a id="showcase"></a>
## 两本实际案例

<table><tr><td width="50%"><img src="course/assets/pages/%E7%BB%B4%E5%B0%BC%E7%AC%AC01%E9%A1%B5v1.0.webp" width="100%" alt="AI辅助改编样例：维尼PDF内容第1页实际截图"><br>Winnie-the-Pooh · 50内容页 / 10章</td><td width="50%"><img src="course/assets/pages/%E5%BD%BC%E5%BE%97%E5%85%94%E7%AC%AC01%E9%A1%B5v1.0.webp" width="100%" alt="AI辅助改编样例：彼得兔PDF内容第1页实际截图"><br>The Tale of Peter Rabbit · 20内容页 / 4个教学单元</td></tr></table>

截图来自创作者提供的两本实际PDF，改编组织者Haixiang Ding, MD，AI辅助平台Hark；不是原著书页，也不是新生成的展示图。原著文字分别来自Gutenberg #67098 / #14838，原著与生成图像的权利分别记录。

[查看PDF与预览下载入口](index.html#books)。公开v1.1副本每页加注作者、AI辅助和来源声明，保持50/20个内容页；页面下方增加声明栏，原内容未改写。预览版均小于10MB，降低插画精度；原版副本保留细节。原始文件及v1.0副本在本地保持不动、不进入本次Git提交。

> **历史改编样例仍有已知问题。**气球颜色、主观判断题等在[第08课](course/08-%E8%B4%A8%E6%A3%80%E6%B8%85%E5%8D%95v1.0.html)按“问题→可能原因→修正方法”讨论，不冒充书稿已修订或全书已签收。

<a id="start"></a>
## 快速开始

直接访问[在线课程](https://tuanziding.github.io/comic-companion-course/)，或下载本仓库后运行：

```sh
python3 -m http.server 8875 --bind 127.0.0.1
```

保持服务器运行，在Chrome打开 `http://127.0.0.1:8875/`。无需构建工具、API账号或密钥。资源无CDN、统计脚本或外部字体；完整下载后可在本地服务器上离线浏览，外部依据及GitHub联系入口需要联网。

运行五页排版示例（直接依赖仅reportlab；中文说明保留在JSON/网页，PDF用内置Helvetica展示英文版式）：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r examples/示例依赖v1.0.txt
.venv/bin/python examples/排版示例v1.1.py
```

Windows使用虚拟环境Scripts目录内的python。默认读取examples/章节数据v1.1.json，生成examples/输出/五页排版示例v1.1.pdf；可用 `--data PATH --output PATH` 指定文件。插画为明确占位，不是完成的漫画。

[脚本](examples/%E6%8E%92%E7%89%88%E7%A4%BA%E4%BE%8Bv1.1.py) · [数据](examples/%E7%AB%A0%E8%8A%82%E6%95%B0%E6%8D%AEv1.1.json) · [五页示例](examples/%E8%BE%93%E5%87%BA/%E4%BA%94%E9%A1%B5%E6%8E%92%E7%89%88%E7%A4%BA%E4%BE%8Bv1.1.pdf)

<a id="workflow"></a>
## 一套可重复的工作流

合法来源 → 虚构读者设置 → 事件边界与六格 → 角色状态 → 无字插画 → 同源正文与五页排版 → 实际预览与质检。

每课包含目标、讲解、实际PDF案例、可复制教学提示词、检查清单和小作业。12课依次覆盖导览、读者、选书与版权、改编、角色、AI生图、版式、排版、质检、亲子使用、医学迁移和作业。

<a id="status"></a>
## 能力与证据

| 项目 | 当前边界 |
| --- | --- |
| 12课、主题、复制、画廊、进度 | 纯静态已实现；本轮实际内容阅读及浏览器自检记录见文档 |
| 五页排版代码 | 干净环境可运行；使用占位图，直接依赖reportlab |
| 音频 | 只提供跟读脚本设计方法与3秒空档建议；未生成音频或实际时间轴 |
| 教材匹配、试读效果 | 原始资料未提供，保留【待补充】，不宣称效果 |
| 版权与来源 | 四类分别说明；美国公版不等于全球公版，非美国地区待核查 |
| Hark审阅 | 历史失败保持为未完成，不作验收证据 |

<details><summary>维护者检查工具</summary>

`scripts/本地检查v1.1.py`需要html5lib、pypdf和Pillow；`scripts/浏览器检查v1.1.js`需要Playwright与本地Chrome。它们是维护者质检工具，不是课程运行依赖。

`scripts/公开副本加注v1.0.py`需要reportlab与pypdf，仅读取本地v1.0副本生成v1.1公开副本；源文件不覆盖。

</details>

<a id="contact"></a>
## 共创与公开联系

欢迎提出可复现的问题、改编流程建议、无身份信息的教学反馈。[创作者GitHub主页](https://github.com/TUANZIDING)是已核实的公开入口；发布后可通过[仓库Issues](https://github.com/TUANZIDING/comic-companion-course/issues)联系。不要在公开反馈中上传儿童或患者身份资料。

**后续商业合作可联系创作者；商业使用须另行核查授权。**本版免费、非商业，无付款入口或商业授权承诺。Hark对商业输出另有书面授权条件；联系创作者不替代原著、插画、参考素材或服务方的授权。

[素材与版权](docs/%E7%B4%A0%E6%9D%90%E4%B8%8E%E7%89%88%E6%9D%83%E8%AF%B4%E6%98%8Ev1.2.md) · [内容审阅与发布记录](docs/%E5%86%85%E5%AE%B9%E5%AE%A1%E9%98%85%E4%B8%8E%E5%8F%91%E5%B8%83%E8%AE%B0%E5%BD%95v1.1.md) · [待补充与自检](docs/%E4%BA%A4%E4%BB%98%E6%A3%80%E6%9F%A5v1.1.md) · [文件清单](docs/%E6%96%87%E4%BB%B6%E6%B8%85%E5%8D%95v1.1.md)

<p align="center">Haixiang Ding, MD · Codex辅助课程编写 / Hark辅助历史改编<br>CC BY-NC 4.0仅覆盖本课程新写文字与代码；第三方、原著插画、AI图像、PDF及截图单列，不被该许可覆盖。</p>

维尼仅涉及1926年Milne文字 / Shepard插画，与迪士尼形象无关，不使用迪士尼版造型作参考。中国大陆及其他地区版权状态：待核查。医学迁移仅用虚构案例，不构成医疗建议，真实材料须经专业审核并去标识化。
