import os
import re
from pathlib import Path

# 配置区 ================================================
REPO_DIR = r"E:\github\xrayr"  # 你的仓库路径

# 需要删除的独立配置块（NodeID可能变化）
BLOCKS_TO_DELETE = [
    # XY节点配置块
    r'-\s*#XY\s*\n\s*PanelType:\s*"V2board"\s*\n\s*ApiConfig:\s*\n\s*ApiHost:\s*"https://xytx\.85652312\.xyz"\s*\n\s*ApiKey:\s*".*?"\s*\n\s*NodeID:\s*\d+\s*\n\s*NodeType:\s*V2ray\s*\n\s*ControllerConfig:\s*\n\s*CertConfig:\s*\n\s*CertMode:\s*none\s*\n?',
    
    # FF节点配置块
    r'-\s*#FF\s*\n\s*PanelType:\s*"V2board"\s*\n\s*ApiConfig:\s*\n\s*ApiHost:\s*"https://fftx\.385158\.xyz"\s*\n\s*ApiKey:\s*".*?"\s*\n\s*NodeID:\s*\d+\s*\n\s*NodeType:\s*V2ray\s*\n\s*ControllerConfig:\s*\n\s*CertConfig:\s*\n\s*CertMode:\s*none\s*\n?'
]

# 主逻辑 ================================================
def clean_blocks():
    changed_files = set()  # 使用集合避免重复记录
    
    for root, _, files in os.walk(REPO_DIR):
        if ".git" in root:
            continue
            
        for file in files:
            file_path = Path(root) / file
            try:
                # 读取文件（自动处理BOM和编码）
                content = file_path.read_text(encoding='utf-8-sig')
                original = content
                
                # 删除所有目标块
                for pattern in BLOCKS_TO_DELETE:
                    content = re.sub(pattern, '', content, flags=re.MULTILINE)
                
                # 清理多余空行（连续2个以上换行变1个）
                content = re.sub(r'\n{3,}', '\n\n', content)
                
                if content != original:
                    # 备份原文件（可选）
                    backup_path = file_path.with_suffix(file_path.suffix + '.bak')
                    file_path.replace(backup_path)
                    
                    # 写入新内容
                    file_path.write_text(content, encoding='utf-8')
                    changed_files.add(str(file_path))
                    print(f"✅ 已清理: {file_path}")
                    
            except Exception as e:
                print(f"❌ 处理失败 [{file_path}]: {str(e)}")
    
    return sorted(changed_files)  # 返回排序后的列表

if __name__ == "__main__":
    print("🔍 开始深度扫描所有文件...")
    modified_files = clean_blocks()
    
    print("\n=== 操作结果 ===")
    if modified_files:
        print(f"🎉 共修改了 {len(modified_files)} 个文件:")
        for f in modified_files:
            print(f"  → {f}")
        
        print("\n💡 后续操作建议:")
        print(f"cd {REPO_DIR}")
        print("git add .")
        print("git commit -m '移除XY和FF配置块'")
        print("git push")
    else:
        print("⚠️ 未找到需要删除的配置块")

    print("\n提示：原文件已自动备份为.bak后缀（如需还原）")
