import json
from collections import Counter

data = json.load(open('/Users/sunwenyong/.openclaw/agents/learn/workspace/dhyy_features_活动剧情.json'))
results = []

for d in data:
    title = d['title']
    wl = d.get('worldline_keywords', [])
    tk = d.get('time_keywords', [])
    prefix = title.split('/')[0]
    sub = '/'.join(title.split('/')[1:]) if '/' in title else ''
    
    world_line = "World-0"
    year = "时间未知"
    year_sort = 0
    confidence = "medium"
    reasoning = ""
    summary = ""
    glw_state = "正常"

    # Cross-world activities
    if '仙殒' in title:
        world_line = "World-C"; confidence = "high"; glw_state = "穿越中"
        if '光和' in str(tk): year = "约189年"; year_sort = 189
        else: year = "架空时间"; year_sort = -1
        reasoning = f"仙殒活动涉及广陵王穿越到过去的世界，世界线关键词{wl}"
        summary = f"仙殒系列{sub}：广陵王穿越到昔日时空的经历"
    elif '梦入浮生' in title:
        world_line = "World-C"; confidence = "high"; glw_state = "梦境中"
        year = "架空时间"; year_sort = -1
        reasoning = f"梦入浮生活动明确涉及梦境/异世界体验，关键词{wl}"
        summary = f"梦入浮生{sub}：广陵王在梦境中经历IF线人生"
    elif '斧蝶梦' in title:
        world_line = "World-C"; confidence = "high"; glw_state = "梦境/穿越中"
        year = "架空时间"; year_sort = -1
        reasoning = f"斧蝶梦涉及梦境和天命相关元素，关键词{wl}"
        summary = f"斧蝶梦{sub}：广陵王在梦境/异世界中的经历"
    elif '燕歌行' in title:
        world_line = "World-C"; confidence = "high"; glw_state = "梦境中"
        year = "架空时间"; year_sort = -1
        reasoning = f"燕歌行活动涉及梦境、天命、魂魄等穿越元素，关键词{wl}"
        summary = f"燕歌行{sub}：广陵王在梦境世界中的冒险"
    elif '天下隐光' in title:
        world_line = "World-C"; confidence = "high"; glw_state = "穿越中"
        year = "架空时间"; year_sort = -1
        reasoning = f"天下隐光涉及宇宙、天命等跨世界线元素，关键词{wl}"
        summary = f"天下隐光{sub}：跨世界线的冒险故事"
    elif '剑剑剑来' in title:
        world_line = "World-C"; confidence = "high"; glw_state = "剑中世界中"
        year = "架空时间"; year_sort = -1
        reasoning = f"剑剑剑来涉及剑中世界、命数等异世界元素，关键词{wl}"
        summary = f"剑剑剑来{sub}：广陵王进入剑中世界的经历"
    elif '朝歌之战' in title:
        world_line = "World-C"; confidence = "high"; glw_state = "另一个世界线"
        year = "架空时间"; year_sort = -1
        reasoning = f"朝歌之战涉及另一个世界、梦等元素，关键词{wl}"
        summary = f"朝歌之战{sub}：在另一个世界线的战斗"
    elif '三千宇宙' in str(wl):
        world_line = "World-C"; confidence = "high"; glw_state = "穿越中"
        year = "架空时间"; year_sort = -1
        reasoning = "涉及三千宇宙元素，属于穿越世界线"
        summary = "涉及三千宇宙的穿越剧情"
    elif '恋念' in title:
        has_special = any(k in str(wl) for k in ['梦','魂','三千','命数','天命','真实','镜中'])
        if has_special:
            if '魂' in str(wl) or '魂魄' in str(wl):
                world_line = "World-C"; glw_state = "魂魄状态"; confidence = "high"
                reasoning = f"恋念剧情涉及魂魄/离魂元素，关键词{wl}"
            elif '梦' in str(wl) or '梦境' in str(wl):
                world_line = "World-C"; glw_state = "梦境中"; confidence = "high"
                reasoning = f"恋念剧情涉及梦境元素，关键词{wl}"
            elif '镜中' in str(wl):
                world_line = "World-C"; glw_state = "镜中世界"; confidence = "high"
                reasoning = f"恋念剧情涉及镜中世界元素，关键词{wl}"
            elif '三千' in str(wl):
                world_line = "World-C"; glw_state = "穿越中"; confidence = "high"
                reasoning = f"恋念剧情涉及三千宇宙元素，关键词{wl}"
            elif '天命' in str(wl) or '命数' in str(wl):
                world_line = "World-C"; glw_state = "命运交错"; confidence = "medium"
                reasoning = f"恋念剧情涉及天命/命数元素，可能涉及世界线变动，关键词{wl}"
            else:
                world_line = "World-C"; glw_state = "特殊状态"; confidence = "medium"
                reasoning = f"恋念剧情含特殊世界线关键词{wl}"
            year = "架空时间"; year_sort = -1
        else:
            world_line = "World-0"; confidence = "medium"; glw_state = "正常"
            year = "时间未知"; year_sort = 0
            reasoning = "恋念剧情，无明显穿越/梦境元素，归属主世界"
        summary = f"{prefix}{sub}：恋念剧情"
    elif '三国志绒绒版' in title:
        world_line = "World-P"; confidence = "high"; glw_state = "绒绒形态"
        year = "架空时间"; year_sort = -1
        reasoning = "三国志绒绒版是全员变成猫狗的平行世界IF线"
        summary = f"三国志绒绒版{sub}：猫狗平行世界的故事"
    elif '三国志魂魂版' in title:
        world_line = "World-P"; confidence = "high"; glw_state = "离魂状态"
        year = "架空时间"; year_sort = -1
        reasoning = "三国志魂魂版是全员变成魂魄的平行世界"
        summary = f"三国志魂魂版{sub}：离魂平行世界的故事"
    elif '寒夜厄境' in title:
        world_line = "World-0"; confidence = "medium"
        glw_state = "幻觉中" if '幻觉' in str(wl) else "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "寒夜厄境发生在主世界的暴风雪中，含幻觉元素"
        summary = f"寒夜厄境{sub}：广陵王在暴风雪中的遭遇"
    elif '约会' in title:
        world_line = "World-0"; confidence = "high"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "约会类活动属于主世界的日常剧情"
        summary = f"{prefix}{sub}：与{prefix.split('-')[0]}的约会日常"
    elif '幽州慨飒宫' in title:
        world_line = "Side-Story"; confidence = "high"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "幽州慨飒宫是温泉休闲活动，Q版角色，属于番外支线"
        summary = f"幽州慨飒宫{sub}：温泉度假番外"
    elif '东海海水浴场' in title:
        world_line = "Side-Story"; confidence = "high"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "东海海水浴场是海滩休闲活动，属于番外支线"
        summary = f"东海海水浴场{sub}：海滩度假番外"
    elif '桃源温泉山庄' in title:
        world_line = "Side-Story"; confidence = "high"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "桃源温泉山庄是温泉休闲活动，属于番外支线"
        summary = "桃源温泉山庄：温泉度假番外"
    elif '青丘戏坊' in title:
        world_line = "Side-Story"; confidence = "high"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "青丘戏坊是轻松的戏曲主题活动，属于番外"
        summary = f"青丘戏坊{sub}：戏曲主题番外"
    elif '咪教模拟器' in title:
        world_line = "Side-Story"; confidence = "high"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "咪教模拟器是趣味模拟游戏活动，属于番外"
        summary = f"咪教模拟器{sub}：趣味模拟番外"
    elif '地下遗迹' in title or prefix == '魇·地下遗迹':
        has_sp = any(k in str(wl) for k in ['梦','魂','穿越','世界'])
        if has_sp:
            world_line = "World-C"; confidence = "medium"; glw_state = "遗迹探索中"
            year = "架空时间"; year_sort = -1
            reasoning = f"地下遗迹含特殊世界线关键词{wl}，可能涉及穿越元素"
        else:
            world_line = "World-0"; confidence = "medium"; glw_state = "正常"
            year = "时间未知"; year_sort = 0
            reasoning = "地下遗迹系列，无明显穿越元素，归属主世界"
        summary = f"{prefix}{sub}：地下遗迹探索故事"
    elif '陶生' in title:
        world_line = "World-0"; confidence = "medium"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "陶生系列是独立小故事，归属主世界"
        summary = f"陶生{sub}：陶生的故事"
    elif '元夕灯如昼' in title:
        world_line = "Side-Story"; confidence = "high"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "元夕灯如昼是元宵节主题活动，属于节日番外"
        summary = f"元夕灯如昼{sub}：元宵节番外"
    elif '月海夜航船' in title:
        world_line = "Side-Story"; confidence = "high"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "月海夜航船是轻松的航海主题活动，属于番外"
        summary = f"月海夜航船{sub}：航海主题番外"
    elif '七载相逢之秋' in title:
        world_line = "World-C"; confidence = "high"; glw_state = "梦境中"
        year = "架空时间"; year_sort = -1
        reasoning = "七载相逢之秋含梦境关键词，属于穿越/梦境世界线"
        summary = "七载相逢之秋：梦境中的重逢"
    elif '七载重逢之秋' in title:
        world_line = "World-0"; confidence = "medium"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "七载重逢之秋周年活动，归属主世界"
        summary = "七载重逢之秋：周年纪念活动"
    elif '夕情欢馀牙轴' in title:
        world_line = "Side-Story"; confidence = "medium"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "夕情欢馀牙轴是主题活动，属于番外"
        summary = "夕情欢馀牙轴：主题活动番外"
    elif '广陵成长计划' in title:
        world_line = "World-0"; confidence = "high"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "广陵成长计划是新手引导剧情，归属主世界"
        summary = f"广陵成长计划{sub}：新手引导"
    elif '春节晚会' in title:
        world_line = "Side-Story"; confidence = "high"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "春节晚会是节日特别活动，属于番外"
        summary = "乙巳年春节晚会：春节特别番外"
    elif '团建' in title:
        world_line = "Side-Story"; confidence = "high"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "团建活动是纪念性质的轻松番外"
        summary = "绣衣楼半周年团建：纪念番外"
    elif '休沐日' in title:
        world_line = "Side-Story"; confidence = "high"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "休沐日是轻松日常番外"
        summary = "傅副官的休沐日：日常番外"
    elif '乘风破浪' in title:
        world_line = "Side-Story"; confidence = "medium"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "乘风破浪的公务是主题活动，属于轻松番外"
        summary = f"乘风破浪的公务{sub}：公务主题番外"
    elif '实习考核' in title:
        world_line = "Side-Story"; confidence = "medium"; glw_state = "正常"
        year = "时间未知"; year_sort = 0
        reasoning = "实习考核是主题活动，属于轻松番外"
        summary = f"披荆斩棘的实习考核{sub}：考核主题番外"
    else:
        has_cross = any(k in str(wl) for k in ['穿越','另一个','宇宙','平行','循环','重置'])
        side_kw = ['温泉','灯','浴场','山庄','竹露','阆苑','陶然','塞上','快意','惊甜','破浪','水村','江东万里','渺渺','狐虎','回乡偶书','躬耕南阳']
        is_side = any(s in title for s in side_kw)
        if has_cross:
            world_line = "World-C"; confidence = "medium"; glw_state = "穿越中"
            year = "架空时间"; year_sort = -1
            reasoning = f"含跨世界线关键词{wl}"
        elif is_side:
            world_line = "Side-Story"; confidence = "medium"; glw_state = "正常"
            year = "时间未知"; year_sort = 0
            reasoning = "轻松主题/日常向活动，归属番外"
        else:
            world_line = "World-0"; confidence = "medium"; glw_state = "正常"
            year = "时间未知"; year_sort = 0
            reasoning = "无明显跨世界线元素，默认归属主世界"
        summary = title

    results.append({
        "title": title,
        "world_line": world_line,
        "estimated_year": year,
        "year_sort": year_sort,
        "confidence": confidence,
        "reasoning": reasoning,
        "story_summary": summary,
        "guanglingwang_state": glw_state
    })

with open('/Users/sunwenyong/.openclaw/agents/learn/workspace/dhyy_classified_活动剧情.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

wc = Counter(r['world_line'] for r in results)
print("World line distribution:")
for k,v in wc.most_common(): print(f"  {k}: {v}")
print(f"\nTotal: {len(results)}")
