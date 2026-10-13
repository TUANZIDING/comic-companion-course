<p align="center"><img src="course/assets/%E8%AF%BE%E7%A8%8B%E5%B0%81%E9%9D%A2v1.0.svg" width="100%" alt="原创概念封面：五页纸卡与一本书，不是原著插画"></p>
<h1 align="center">从一本书到漫画伴读<br>Comic Companion Course</h1>
<p align="center">真实页面、可复制的教学提示词、可运行的五页排版示例。</p>
<p align="center"><a href="README.md">简体中文</a> · <a href="docs/%E8%8B%B1%E6%96%87%E8%AF%B4%E6%98%8Ev1.0.md">English</a></p>
<p align="center"><code>本地课程v1.0</code> · <code>12课</code> · <code>尚未发布</code></p>

这是纯静态HTML课程。适合医学科研人员和AI应用学习者；全站使用虚构读者与虚构医学场景。提示词及代码均标为“教学示例，非原始制作记录”。

## 本地开始

在仓库目录运行以下命令，保留服务器进程，再用Chrome打开本地地址：

```sh
python3 -m http.server 8875 --bind 127.0.0.1
```

本地入口为 `http://127.0.0.1:8875/`。不要仅以file方式评估复制按钮。网页、样式、图片、PDF和字体没有外部CDN依赖；本地服务器运行时，断开互联网仍可浏览内容。外部依据链接需要联网。直接双击HTML可阅读基本内容，复制采用兼容回退，但正式检查使用HTTP。

[课程入口](index.html) · [全部大纲](index.html#curriculum) · [PDF下载区](index.html#books) · [本地交付检查](docs/%E4%BA%A4%E4%BB%98%E6%A3%80%E6%9F%A5v1.0.md)

## 运行五页排版教学示例

只直接依赖reportlab；Pillow等由reportlab的安装依赖自动处理。脚本只导入Python标准库与reportlab，不读取私人制作脚本，也无需图片或系统字体文件。PDF使用内置Helvetica完成英文布局示范，中文教学说明保留在JSON与网页；插画为明确的版式占位。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r examples/示例依赖v1.0.txt
.venv/bin/python examples/排版示例v1.0.py
```

默认读取examples/章节数据v1.0.json，生成examples/输出/五页排版示例v1.0.pdf。Windows使用虚拟环境Scripts目录中的python执行同一脚本。可选参数：`--data PATH`、`--output PATH`。

[查看已生成的五页示例](examples/%E8%BE%93%E5%87%BA/%E4%BA%94%E9%A1%B5%E6%8E%92%E7%89%88%E7%A4%BA%E4%BE%8Bv1.0.pdf) · [脚本](examples/%E6%8E%92%E7%89%88%E7%A4%BA%E4%BE%8Bv1.0.py) · [章节数据](examples/%E7%AB%A0%E8%8A%82%E6%95%B0%E6%8D%AEv1.0.json)

> **现有改编样例，未完成全书逐页审核。** 已知问题见[第08课](course/08-%E8%B4%A8%E6%A3%80%E6%B8%85%E5%8D%95v1.0.html)；仅作本地案例展示。

## 已有作品与当前范围

| 作品 | 页数 | 原版副本 | 压缩预览 |
| --- | --- | --- | --- |
| Winnie-the-Pooh漫画伴读 | 50页／10章 | 29.6MB | 8.65MB |
| Peter Rabbit漫画伴读 | 20页／4个教学单元 | 12.9MB | 3.89MB |

原始PDF保持原名和原路径。books中是带版本副本；两本各6张实际页面截图小于300KB。压缩预览保留文字层和页数，插画精度降低。现有作品的局部问题仍有记录，不作全书质量结论。

## 课程路径

从读者设定、选书与版权开始，依次学习拆章、角色、生成图像、五页版式、自动排版、质检、亲子使用、医学迁移，最后提交一章。每课结构一致：目标、讲解、实际PDF案例、提示词、检查清单、小作业。

## 素材、许可与未知项

课程新写文字与代码采用CC BY-NC 4.0。原著文字、原著插画、第三方材料与AI生成图像单列，不被该许可覆盖。Gutenberg书目标注美国公版；中国大陆及其他地区：待核查。维尼仅讨论1926年原著，与迪士尼形象无关，不使用迪士尼版造型作参考。

[素材与版权说明](docs/%E7%B4%A0%E6%9D%90%E4%B8%8E%E7%89%88%E6%9D%83%E8%AF%B4%E6%98%8Ev1.0.md) · [完整许可](LICENSE) · [所有待补充项与证据](docs/%E4%BA%A4%E4%BB%98%E6%A3%80%E6%9F%A5v1.0.md)

讲者介绍仅为：Haixiang Ding, MD，急诊创伤外科医生，苏州大学临床医学博士在读。

## 当前状态与发布计划

当前仅本地制作与检查；没有创建远端仓库、推送或启用Pages。本地自检完成后停下，等待用户确认发布。建议仓库TUANZIDING/comic-companion-course；未来Pages来源main分支根目录，预计网址 `https://TUANZIDING.github.io/comic-companion-course/`。这是计划地址，不是已上线站点。

[课程与设计说明](docs/%E8%AF%BE%E7%A8%8B%E4%B8%8E%E8%AE%BE%E8%AE%A1%E8%AF%B4%E6%98%8Ev1.0.md) · [文件清单与大小](docs/%E6%96%87%E4%BB%B6%E6%B8%85%E5%8D%95v1.0.md)
