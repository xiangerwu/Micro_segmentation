##
## 處理ACL 規則相關邏輯
##

from pyparsing import Word, Literal, nums, Group, Optional, Combine


# 定義 DSL 語法規則
action = Literal("allow") | Literal("deny")
protocol = Literal("ping")  # 僅支持 ping 協議（ICMP）

# 定義 IP 地址的每一部分，支持 0-255 範圍
ip_part = Word(nums, min=1, max=3)  # 每一部分應該是一個數字（支持 0-255）
ip = Combine(ip_part + "." + ip_part + "." + ip_part + "." + ip_part)  # 組合成 IP 地址格式

# 源 IP 和目標 IP
src_ip = ip("src_ip")
dst_ip = ip("dst_ip")

# DSL 語法規則
dsl_rule = Group(action("action") + protocol("protocol") + Literal("from") + src_ip("src_ip") + Literal("to") + dst_ip("dst_ip"))

# 解析 DSL 規則
def parse_acl(dsl):
    print(dsl)
    parsed_data = dsl_rule.parseString(dsl)
    return parsed_data

# 更新acl_rules 的規則
def update_acl_rules(data):   
    with open("config/acl_rules.txt", "w") as acl_file:
        for entry in data:
            # 獲取 egress_ip, ingress_ip, protocol 和 method
            egress_ip = entry['egress_ip'].strip(',')
            ingress_ip = entry['ingress_ip']
            protocol = entry['protocol']
            method = entry['method']
  
            # 根據 method（allow 或 deny）來生成規則
            rule = f"{method} {protocol} from {egress_ip} to {ingress_ip}\n"            
            # 將規則寫入 acl_rules.txt
            acl_file.write(rule)
            
            # 自動補 ICMP 雙向流（僅限 allow）
            if protocol.upper() == "ICMP" and method.lower() == "allow":
                reverse_rule = f"{method} {protocol} from {ingress_ip} to {egress_ip}\n"
                print(reverse_rule)
                acl_file.write(reverse_rule)
# 刪除ACL_rules 的規則
def delete_acl_rules_byip(ip):   
    with open("config/acl_rules.txt", "r") as acl_file:
        lines = acl_file.readlines()
    
     # 過濾出不包含該 IP 的規則
    new_lines = []
    for line in lines:
        # 忽略空白行或註解
        if line.strip() == "" or line.strip().startswith("#"):
            new_lines.append(line)
            continue

        # 若該行包含來源或目的 IP 為指定 IP，則跳過（刪除）
        if ip in line:
            continue
        new_lines.append(line)

    # 將過濾後的規則寫回原檔案
    with open("config/acl_rules.txt", "w") as acl_file:
        acl_file.writelines(new_lines)

    print(f"[INFO] 已刪除來源或目的為 {ip} 的 ACL 規則")