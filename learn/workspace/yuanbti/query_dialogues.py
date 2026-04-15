import subprocess, json, sys

characters = [
    ("满宠", 3), ("程昱", 3), ("简雍", 3), ("史子眇", 3), ("法正", 3), ("张角", 3), ("荀彧", 3),
    ("庞羲", 2), ("夏侯惇", 2), ("曹植", 2), ("刘繇", 2), ("甄宓", 2), ("曹丕", 2), ("卢植", 2),
    ("太史慈", 2), ("张昭", 2), ("葛洪", 2), ("朱然", 2), ("司马徽", 2), ("董白", 2), ("华佗", 2),
    ("严白虎", 2), ("刘璋", 2), ("张仲景", 2), ("夏侯渊", 2), ("程普", 2), ("刘豹", 2), ("安期", 2),
    ("小乔", 2), ("孙尚香", 2), ("吕蒙", 2), ("张鲁", 2), ("公孙珊", 2), ("王粲", 2), ("张修", 2),
    ("干吉", 2), ("庞统", 2), ("蒯良", 2), ("周群", 2), ("蔡琰", 2), ("虞翻", 2), ("陆逊", 2), ("钟繇", 2),
    ("袁绍", 1), ("马腾", 2), ("曹操", 1), ("伍丹", 1), ("耿公子", 2), ("孙坚", 1), ("陈宫", 2),
    ("李傕", 2), ("刘协", 2), ("郭汜", 2), ("伏寿", 1), ("刘表", 1), ("刘备", 1), ("吴夫人", 1),
    ("袁术", 1), ("公孙瓒", 1), ("陈昭", 1),
]

for char, quota in characters:
    speaker = char
    sql = f"SELECT story_title, text, emotion, dialogue_type FROM dialogues WHERE speaker = '{speaker}' AND text != '' ORDER BY story_title, line_order LIMIT 40"
    result = subprocess.run(["db9", "sql", "learn_test", "-q", sql], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    if len(lines) <= 1:
        print(f"=== {char} (quota:{quota}) === NO DIALOGUES")
        continue
    print(f"=== {char} (quota:{quota}) === {len(lines)-1} lines")
    for line in lines[1:41]:
        parts = line.split('\t')
        if len(parts) >= 4:
            story, text, emotion, dtype = parts[0], parts[1], parts[2], parts[3]
            text = text.replace('\n', ' ').replace('\r', ' ')[:150]
            print(f"  [{story}] ({emotion}/{dtype}) {text}")
    print()
