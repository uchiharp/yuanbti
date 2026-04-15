# 鸢BTI — 代号鸢角色性格测试题库

基于《代号鸢》(Ashes of the Kingdom) 真实剧情台词生成的角色性格测试题库。

## 题库规模

- **总计**: 544 题
- **男主** (5人): 各30题 — 袁基、刘辩、傅融、孙策、左慈
- **密探** (42人): 3~20题不等
- **维度**: S1-S10（权谋/情感/金钱/面具/行动/底线/锋芒/温柔/权力/秩序）
- **题型**: sweet / funny / angst / scheme / daily / classic

## 文件结构

```
├── README.md                  # 本文件
├── QUESTION_GUIDE.md          # 出题指南 v4.2
├── character-centroids.md     # 12维质心评分体系
├── questions/
│   ├── pool_all.json          # 大题池（全部题目合并）
│   ├── yuanji.json            # 袁基（30题）
│   ├── liubian.json           # 刘辩（30题）
│   ├── furong.json            # 傅融（30题）
│   ├── sunce.json             # 孙策（30题）
│   ├── zuoci.json             # 左慈（30题）
│   └── ...                    # 其他密探题库
└── questions_v2/              # 情商优化版（待生成）
```

## 题目格式

每道题包含：
- `source_character`: 角色名
- `text`: 题干（基于真实台词）
- `type`: 题型
- `dimension`: 测量维度（单维度）
- `scores`: 选项分值映射
- `options`: 3个选项，每个含 text/score/tendency/reasoning

## 数据来源

台词来自 PostgreSQL 数据库 `learn_test.dialogues`（99,544条台词，1,518个故事），原始数据来源于 BWiki。

## License

本项目仅供学习交流使用。角色和台词版权归《代号鸢》/ 游族网络所有。
