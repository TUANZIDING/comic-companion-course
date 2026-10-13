#!/usr/bin/env python3
"""教学示例，非原始制作记录。直接依赖仅reportlab；其余为Python标准库。

读取章节数据v1.1.json，生成五页布局示例。插画占位有明确标记。
"""
import argparse
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics

FONT = "Helvetica"
# 为满足仅reportlab、无外部字体的可移植运行，本简化PDF使用英文；中文说明保留在JSON和网页。
PAGE_W, PAGE_H = A4
INK = HexColor("#163c2d")
PAPER = HexColor("#fff8e7")
HONEY = HexColor("#efbd4e")


def wrapped(c, text, x, y, width, size=11, line_height=16):
    """按实际字体宽度换行；英文在空格处分行，中文可按字符分行。"""
    c.setFont(FONT, size)
    line = ""
    for ch in text:
        if ch == "\n":
            c.drawString(x, y, line); y -= line_height; line = ""; continue
        if pdfmetrics.stringWidth(line + ch, FONT, size) > width:
            if " " in line and ord(ch) < 128:
                previous, remaining = line.rsplit(" ", 1)
                c.drawString(x, y, previous); line = remaining + ch
            else:
                c.drawString(x, y, line); line = ch
            y -= line_height
        else:
            line += ch
    if line:
        c.drawString(x, y, line); y -= line_height
    return y


def page_base(c, data, number, title):
    c.setFillColor(PAPER); c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(FONT, 23); c.drawString(36, PAGE_H-55, title)
    wrapped(c, data["book"]["titleEn"], 36, PAGE_H-82, PAGE_W-72, 12)
    wrapped(c, "Teaching example, not the original production record. Artwork areas are placeholders.", 36, PAGE_H-105, PAGE_W-72, 9, 13)
    c.setStrokeColor(INK); c.line(36, PAGE_H-120, PAGE_W-36, PAGE_H-120)
    c.setFont(FONT, 8); c.drawString(36, 26, "Haixiang Ding, MD | AI-assisted with Codex | CC BY-NC 4.0")
    c.setFont(FONT, 7); c.drawString(36, 14, "Layout demo only - curriculum list pending review")
    c.drawRightString(PAGE_W-36, 26, f"{number} / 5")


def box(c, x, y, w, h, title):
    c.setFillColor(HONEY); c.setStrokeColor(INK)
    c.roundRect(x, y, w, h, 9, stroke=1, fill=1)
    c.setFillColor(INK); wrapped(c, title, x+10, y+h-20, w-20, 10, 14)


def comic_page(c, data, units):
    page_base(c, data, 1, "01 - Six comic panels")
    w=(PAGE_W-84)/2; h=180
    for i,panel in enumerate(data["chapter"]["panels"]):
        x=36+(i%2)*(w+12); y=PAGE_H-140-(i//2+1)*(h+12)
        box(c,x,y,w,h,f"{i+1}. Illustration placeholder")
        wrapped(c,panel["artBriefEn"],x+12,y+h-44,w-24,10,14)
        unit=units[panel["utteranceId"]]
        wrapped(c,f'{unit["speaker"]}: {unit["text"]}',x+12,y+62,w-24,12,17)
        wrapped(c,unit["id"],x+12,y+26,w-24,10,14)
    wrapped(c,data["chapter"]["summaryEn"],36,82,PAGE_W-72,10,14)


def panorama_page(c, data, units):
    page_base(c,data,2,"02 - Panorama and finding objects")
    box(c,36,350,PAGE_W-72,330,"Panorama placeholder: six labelled boxes, not finished illustration.")
    for i,word in enumerate(data["chapter"]["findObjects"]):
        x=55+(i%3)*165; y=410+(i//3)*100
        c.setFillColor(PAPER); c.roundRect(x,y,140,70,8,stroke=1,fill=1)
        c.setFillColor(INK); wrapped(c,word,x+8,y+44,124,12)
    wrapped(c,"Find it: point to the six labels. A real activity requires verified artwork.",36,310,PAGE_W-72,13,20)
    wrapped(c,"This example demonstrates layout only. Object count and visibility require image review.",36,240,PAGE_W-72,12,18)


def words_page(c,data,units):
    page_base(c,data,3,"03 - Five word cards")
    for i,word in enumerate(data["chapter"]["words"]):
        x=36+(i%2)*266; y=PAGE_H-145-(i//2+1)*185
        box(c,x,y,253,165,word["word"]+" - picture placeholder")
        wrapped(c,word["meaningEn"],x+12,y+119,229,12)
        wrapped(c,"Pronunciation source: pending",x+12,y+91,229,10)
        wrapped(c,units[word["exampleId"]]["text"],x+12,y+56,229,12,17)
        wrapped(c,word["exampleId"],x+12,y+22,229,10,14)


def lesson_page(c,data,units):
    page_base(c,data,4,"04 - Shared text for read-along")
    y=PAGE_H-162
    for uid in data["chapter"]["audioOrder"]:
        unit=units[uid]
        y=wrapped(c,f'{uid} · {unit["speaker"]}',36,y,PAGE_W-72,10,15)
        y=wrapped(c,unit["text"],36,y,PAGE_W-72,17,24)
        y-=25
    wrapped(c,"Read-along plan: leave 3 seconds after each line. No audio or measured timeline exists.",36,155,PAGE_W-72,12,18)
    wrapped(c,"Act it out: swap roles. Speaker labels are not part of the spoken English text.",36,106,PAGE_W-72,12,18)


def homework_page(c,data,units):
    page_base(c,data,5,"05 - Practice page")
    words=" / ".join(word["word"] for word in data["chapter"]["words"])
    wrapped(c,"Word box: "+words,36,PAGE_H-155,PAGE_W-72,13,20)
    y=PAGE_H-205
    for i,activity in enumerate(data["chapter"]["activities"]):
        original=units[activity["utteranceId"]]["text"]
        target=activity["answer"]
        sentence=original.replace(target,"________",1)
        box(c,36,y-90,PAGE_W-72,90,f"{i+1}. Picture hint: {activity['imageHintEn']}")
        wrapped(c,sentence,49,y-60,PAGE_W-98,16,23); y-=125
    wrapped(c,"Say it first, then fill in. Add a stamp after trying:",36,245,PAGE_W-72,13)
    for i in range(3): c.circle(285+i*60,229,17,stroke=1,fill=0)
    wrapped(c,"Parent answers are upside down. Artwork and text still need review.",36,168,PAGE_W-72,11)
    answers=" / ".join(a["answer"] for a in data["chapter"]["activities"])
    c.saveState(); c.translate(PAGE_W-36,74); c.rotate(180)
    wrapped(c,"Parent answers: "+answers,0,0,PAGE_W-72,9,13); c.restoreState()


def validate(data):
    chapter=data["chapter"]; ids=[u["id"] for u in chapter["utterances"]]
    if len(ids)!=len(set(ids)): raise ValueError("正文ID重复")
    units={u["id"]:u for u in chapter["utterances"]}
    if len(chapter["panels"])!=6 or len(chapter["words"])!=5 or len(chapter["findObjects"])!=6:
        raise ValueError("示例需要六格、五词卡和六个找物占位")
    for unit in units.values():
        if len(unit["text"].split())>8: raise ValueError("正文超过8词："+unit["id"])
    for row in chapter["panels"]+chapter["activities"]:
        if row["utteranceId"] not in units: raise ValueError("正文引用不存在")
    for row in chapter["words"]:
        if row["exampleId"] not in units: raise ValueError("词卡正文引用不存在")
    for uid in chapter["audioOrder"]:
        if uid not in units: raise ValueError("听读正文引用不存在")
    if len(set(chapter["findObjects"]))!=len(chapter["findObjects"]):
        raise ValueError("找物目标重复")
    for activity in chapter["activities"]:
        if units[activity["utteranceId"]]["text"].count(activity["answer"])!=1:
            raise ValueError("答案不能唯一对应原句")
    return units


def main():
    base=Path(__file__).resolve().parent
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data",type=Path,default=base/"章节数据v1.1.json")
    parser.add_argument("--output",type=Path,default=base/"输出/五页排版示例v1.1.pdf")
    args=parser.parse_args(); data=json.loads(args.data.read_text(encoding="utf-8")); units=validate(data)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(args.output),pagesize=A4,pageCompression=1)
    c.setTitle("五页排版教学示例，非原始制作记录")
    c.setAuthor("Haixiang Ding, MD")
    c.setSubject("AI-assisted teaching layout example with Codex; CC BY-NC 4.0")
    for render in (comic_page,panorama_page,words_page,lesson_page,homework_page):
        render(c,data,units); c.showPage()
    c.save(); print("生成5页教学示例："+str(args.output))


if __name__=="__main__": main()
