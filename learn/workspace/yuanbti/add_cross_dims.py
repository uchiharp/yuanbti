#!/usr/bin/env python3
"""
为鸢BTI题目选项添加交叉维度分值。
规则：
- 主维度不变
- 每个选项最多加2个副维度
- 副维度分值 = 主维度分值 ± 0.5~1档
- 分值只能用 1/2/2.5/3/3.5/4/5
- 不是所有题都加，只给语义上明显涉及多个维度的加
"""

import json
import os
import sys

VALID_SCORES = [1, 2, 2.5, 3, 3.5, 4, 5]
ALL_DIMS = ['S1','S2','S3','S4','S5','S6','S7','S8','S9','S10']

# 维度关键词映射 - 用于判断选项文本涉及哪些维度
DIM_KEYWORDS = {
    'S1': ['谋','算','计','策','布局','设局','棋','暗','布局','算计','筹谋','策略','谋划','谋略','运筹','权谋','城府','深','腹','揣摩','心机','暗中','预判','棋局','棋子','谋划','利用','操控','操纵','算计','谋划'],
    'S2': ['爱','情','心','泪','哭','痛','悲','温暖','抱','拥抱','温柔','心疼','在乎','珍惜','喜欢','爱','深情','感情','情意','真情','深情','牵','挂念','思念','想念','依恋','眷恋','动心','心动','感动','泪','哭','悲伤','难过','伤心','心痛','爱意','情丝','缱绻','柔情','表白','告白','陪伴','守护','守护'],
    'S3': ['钱','财','利','益','富','贵','价','值','务实','现实','成本','收益','利益','报酬','银两','金银','买卖','交易','赚','实惠','划算','代价','物质','财富','贪','势力','好处','经营','盘算','精明','商','利润','盈亏'],
    'S4': ['面具','伪装','演','装','假','真','面具','隐藏','掩饰','伪装','假象','表象','角色','扮演','伪装','瞒','骗','谎','隐藏','藏','内敛','克制','沉默','不言','隐忍','不露','深藏','含蓄','伪装'],
    'S5': ['做','动','冲','果断','立刻','马上','快','急','冲','行动','执行','实干','动手','直接','行动','雷厉','果断','决断','冲在','冲','勇','猛','迅速','抢先','抢先','出击','进攻','动手','暴','怒','暴躁','急躁','莽','鲁莽','冲动','先发','主动'],
    'S6': ['底线','原则','规则','法','道德','正','义','善','恶','不','绝不','无论','任何','底线','原则','红线','禁忌','不可','不能','绝对','绝不','道德','良知','操守','界限','分寸','尺度','容忍','妥协','退让','纵容','默许','包庇','放纵','逾矩','越界','违规','违背','坚持'],
    'S7': ['锋','锐','刺','骂','怼','言','说','怼人','犀利','刻薄','尖锐','毒舌','讽刺','挖苦','直言','坦率','锋芒','刺','尖锐','犀利','尖锐','毒','怼','呛','呛声','反击','回击','强势','气场','压迫','气势','威压','不留情','不客气','针锋'],
    'S8': ['柔','软','暖','温','和','善','体贴','关心','照顾','安慰','安抚','包容','宽容','忍耐','忍让','温柔','和善','慈悲','仁慈','怜悯','同情','体谅','理解','善解','柔和','暖','细','细腻','细腻','温柔','善意','柔和','温暖','疼','呵护','珍惜'],
    'S9': ['权','势','位','地位','官','皇','王','上位','掌权','统治','控制','驾驭','命令','服从','臣服','权力','权威','尊卑','等级','阶层','地位','名分','正统','霸','领袖','掌控','制衡','势','权力欲','野心','统治','号令'],
    'S10': ['秩序','规则','法','制度','规范','条理','规划','计划','整齐','规律','秩序','法度','纲纪','章法','规矩','传统','礼','礼法','体制','程序','流程','框架','系统','制度','法则','约定','章程','条例','纪律','约束','组织','管理'],
}

# 副维度分值调整策略
def adjust_score(main_score, is_strong_match=False):
    """根据主分值和匹配强度计算副维度分值"""
    if is_strong_match:
        # 强匹配：副维度分值接近主维度
        offset = 0.5
    else:
        # 弱匹配：副维度分值比主维度低1档左右
        offset = 1.0
    
    secondary = main_score - offset
    # 对齐到合法分值
    best = min(VALID_SCORES, key=lambda x: abs(x - secondary))
    if best == main_score:
        # 避免和主维度相同
        candidates = [x for x in VALID_SCORES if x != main_score]
        best = min(candidates, key=lambda x: abs(x - secondary))
    return best

def find_cross_dimensions(text, main_dim):
    """分析选项文本，找出涉及的副维度"""
    text_lower = text
    candidates = []
    
    for dim, keywords in DIM_KEYWORDS.items():
        if dim == main_dim:
            continue
        match_count = 0
        for kw in keywords:
            if kw in text_lower:
                match_count += 1
        
        if match_count >= 2:
            candidates.append((dim, True))  # 强匹配
        elif match_count == 1:
            candidates.append((dim, False))  # 弱匹配
    
    # 按匹配强度排序，最多取2个
    candidates.sort(key=lambda x: (x[1], x[0]), reverse=True)
    return candidates[:2]

# 语义模式匹配 - 补充关键词匹配不够精确的情况
SEMANTIC_RULES = [
    # (关键词或短语, 副维度, 是否强匹配)
    # 涉及权谋+面具的组合
    ('暗中布局|不知不觉|陷阱|引诱|设套', 'S4', True),
    ('暗中布局|不知不觉|陷阱|引诱|设套', 'S5', False),
    ('暗算|背后|秘密行动', 'S4', True),
    # 涉及情感+温柔
    ('抱紧|拥抱|不要害怕|陪在你身边', 'S8', True),
    ('心疼|难过|流泪|舍不得', 'S2', True),
    ('安慰|温暖|温柔对待', 'S8', True),
    # 涉及底线+秩序
    ('绝不|无论|绝对不能|红线', 'S10', True),
    ('底线|原则|不可逾越', 'S6', True),
    # 涉及权力+权谋
    ('上位|掌权|夺权|夺位', 'S9', True),
    ('统治|驾驭|控制|掌控', 'S1', True),
    ('皇位|王位|天下', 'S9', True),
    # 涉及锋芒+表达
    ('直言|不讳|当面怼|针锋相对', 'S7', True),
    ('讽刺|挖苦|毒舌|刻薄', 'S7', True),
    ('不客气|不留情|毫不', 'S7', True),
    # 涉及行动+果断
    ('果断|立刻|马上|先下手', 'S5', True),
    ('冲在前面|抢先|主动出击', 'S5', True),
    ('动手|亲自|冲上去', 'S5', True),
    # 涉及务实+金钱
    ('成本|代价|收益|划算', 'S3', True),
    ('现实|利益|好处|势力', 'S3', True),
    # 涉及面具+温柔
    ('故作轻松|强颜欢笑|假装不在意', 'S4', True),
    ('不让他看到|默默承受|藏在心里', 'S4', True),
    # 涉及底线+情感
    ('宁愿你恨我|推开|推开你|为你好', 'S2', True),
    ('为你死|陪你死|不管前面', 'S6', False),
    # 涉及秩序+底线
    ('法度|纲纪|礼法|规矩', 'S6', True),
    ('制度|规范|条例|章程', 'S10', True),
    # 涉及权谋+底线
    ('牺牲|背叛|出卖', 'S6', True),
    ('不择手段|不惜代价', 'S6', True),
    # 温柔相关
    ('叫他的名字|叫他不要怕|陪着他', 'S8', True),
    ('记得他|记住他|不会忘记', 'S2', True),
]

import re

def find_semantic_cross_dims(text, main_dim):
    """通过语义规则找副维度"""
    candidates = {}
    for pattern, dim, strong in SEMANTIC_RULES:
        if dim == main_dim:
            continue
        if re.search(pattern, text):
            if dim not in candidates or (strong and not candidates[dim]):
                candidates[dim] = strong
    result = [(d, s) for d, s in candidates.items()]
    result.sort(key=lambda x: (x[1], x[0]), reverse=True)
    return result[:2]

def add_cross_dimensions(question):
    """为单个题目的选项添加交叉维度分值"""
    main_dim = question['dimension']
    modified = False
    total_added = 0
    
    for opt in question['options']:
        # 合并关键词和语义规则的结果
        kw_dims = find_cross_dimensions(opt['text'], main_dim)
        sem_dims = find_semantic_cross_dims(opt['text'], main_dim)
        
        # 合并去重
        all_candidates = {}
        for dim, strong in kw_dims + sem_dims:
            if dim not in all_candidates:
                all_candidates[dim] = strong
            elif strong and not all_candidates[dim]:
                all_candidates[dim] = strong
        
        # 排序：强匹配优先
        sorted_dims = sorted(all_candidates.items(), key=lambda x: (x[1], x[0]), reverse=True)[:2]
        
        if not sorted_dims:
            continue
        
        main_score = list(opt['scores'].values())[0]
        new_scores = dict(opt['scores'])
        
        for dim, strong in sorted_dims:
            score = adjust_score(main_score, strong)
            new_scores[dim] = score
            total_added += 1
            modified = True
        
        opt['scores'] = new_scores
    
    return modified, total_added

def process_file(filepath):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    file_modified = False
    file_added = 0
    modified_questions = 0
    
    for q in questions:
        modified, added = add_cross_dimensions(q)
        if modified:
            file_modified = True
            file_added += added
            modified_questions += 1
    
    if file_modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
    
    return modified_questions, file_added

def main():
    base_dir = '/Users/sunwenyong/.openclaw/agents/learn/workspace/yuanbti/questions'
    
    # 要处理的文件列表
    files = [
        # 男主
        'liubian.json', 'furong.json', 'yuanji.json', 'sunce.json', 'zuoci.json',
        # 热门密探
        'zhangmiao.json', 'guojia.json', 'zhouyu.json', 'zhugeliang.json', 
        'caocao.json', 'lvbu.json', 'sunquan.json', 'xiahoudun.json',
        'machao.json', 'zhangliao.json', 'zhangfei.json', 'luxun.json',
        'pangtong.json', 'xunyu.json', 'jiaxu.json', 'simahui.json',
        'caopi.json', 'liubei.json', 'zhaoyun.json' if os.path.exists(os.path.join(base_dir, 'zhaoyun.json')) else None,
    ]
    files = [f for f in files if f and os.path.exists(os.path.join(base_dir, f))]
    
    # 处理所有文件
    total_modified = 0
    total_added = 0
    
    for fname in files:
        filepath = os.path.join(base_dir, fname)
        modified, added = process_file(filepath)
        total_modified += modified
        total_added += added
        print(f'{fname}: 优化了 {modified} 道题, 新增 {added} 个维度评分点')
    
    print(f'\n=== 总计 ===')
    print(f'优化题目: {total_modified} 道')
    print(f'新增评分点: {total_added} 个')

if __name__ == '__main__':
    main()
