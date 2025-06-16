import os
import re

# 仓库路径
base_dir = r"E:\github\xrayr"

# 替换目标：每个值是“完整 YAML 段落”的首行，注释会插入在它后面
# 格式：唯一标识的字符串 → 注释（#XY、#AB等）
block_tags = {
    'ApiHost: "https://xytx.85652312.xyz"': "#XY",
    # 继续添加更多...
}

# 排除 .git 目录
for root, dirs, files in os.walk(base_dir):
    if ".git" in root:
        continue

    for file in files:
        file_path = os.path.join(root, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            continue

        modified = False
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            new_lines.append(line)
            # 遍历目标项，看是否匹配
            for keyword, comment in block_tags.items():
                if keyword in line:
                    # 回溯找到包含 "-" 且缩进相同的起始行
                    for j in range(i - 1, max(i - 5, -1), -1):
                        if re.match(r"\s*-\s*$", lines[j]) or re.match(r"\s*-\s+#", lines[j]):
                            # 替换那一行，加注释
                            indent = re.match(r"^(\s*)-", lines[j]).group(1)
                            lines[j] = f"{indent}- {comment}\n"
                            modified = True
                            break
                    break
            i += 1

        if modified:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)
                print(f"✅ 加注释完成: {file_path}")
            except Exception as e:
                print(f"⚠️ 写入失败: {file_path}, 错误: {e}")
