#!/usr/bin/env python3
"""鸢BTI批量出题 - 11位密探各20-25道题"""
import json,os,sys
B="/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions"
os.makedirs(B,exist_ok=True)
def q(i,d,t,sc,sr,r,c,tx,op,rv):
 return{"id":i,"dimension":d,"cross_dimension":None,"type":t,"source_character":sc,"source_story":sr,"route_hint":r,"city_hint":c,"text":tx,"options":[{"label":l,"text":t2,"scores":s,"tendency":g}for l,t2,s,g in op],"reveal":rv}
def save(name,data):
 with open(f"{B}/{name}.json","w",encoding="utf-8")as f:json.dump(data,f,ensure_ascii=False,indent=2)
 print(f"{name}: {len(data)}题")

# Load each character's questions from separate files
chars = ["zhangmiao","achan","xushu","chendeng","guojia","zhouyu","miheng","xixue","zhangliao","dongfeng","wangyi"]
for ch in chars:
    fp = f"{B}/_{ch}.json"
    if os.path.exists(fp):
        with open(fp,"r",encoding="utf-8") as f:
            data = json.load(f)
        save(ch, data)
        os.remove(fp)
    else:
        print(f"{ch}: 文件不存在")

print("全部完成！")
