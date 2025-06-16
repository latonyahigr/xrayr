import os

# 仓库路径
base_dir = r"E:\github\xrayr"

# 替换内容：原字符串 → 新字符串
replacements = {
    'ApiHost: "https://sytx.3651250.xyz"': 'ApiHost: "https://sytx.3651250.xyz"',
}

# 遍历所有文件，排除 .git 目录
for root, dirs, files in os.walk(base_dir):
    if ".git" in root:
        continue

    for file in files:
        file_path = os.path.join(root, file)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue  # 忽略无法读取的文件

        original_content = content
        for old, new in replacements.items():
            content = content.replace(old, new)

        if content != original_content:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ 已修改: {file_path}")
            except Exception as e:
                print(f"⚠️ 写入失败: {file_path}, 错误: {e}")
