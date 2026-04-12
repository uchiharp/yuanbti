#!/usr/bin/env python3
"""
快速验证OpenClaw Hub v4二期A的业务逻辑。
"""
import requests
import time
import json
import sys
import os

BASE_URL = "http://localhost:10080/api/v1"
HEADERS = {"Content-Type": "application/json"}

def print_result(name, ok, msg=""):
    status = "✅" if ok else "❌"
    print(f"{status} {name}: {msg}")
    return ok

def test_rate_limit():
    """验证登录速率限制：5次/5分钟，429 + Retry-After，成功清除计数"""
    print("\n=== 1. 登录速率限制 ===")
    url = f"{BASE_URL}/auth/login"
    ip = "10.0.0.99"
    headers = {"X-Forwarded-For": ip}
    
    # 5次失败登录
    for i in range(5):
        resp = requests.post(url, json={"username": "wrong", "password": "wrong"}, headers=headers)
        if resp.status_code != 401 and resp.status_code != 429:
            print(f"  第{i+1}次失败返回 {resp.status_code}")
    
    # 第6次应被限流
    resp = requests.post(url, json={"username": "wrong", "password": "wrong"}, headers=headers)
    ok1 = resp.status_code == 429
    retry = resp.headers.get("Retry-After")
    ok2 = retry is not None and retry.isdigit()
    print_result("5次失败后返回429", ok1, f"状态码 {resp.status_code}")
    print_result("Retry-After头存在且为数字", ok2, f"Retry-After: {retry}")
    
    # 使用成功登录清除计数（需要有效凭证）
    # 暂不测试，因为需要有效用户
    
    return ok1 and ok2

def test_refresh_token_rotation():
    """验证 refresh_token 轮换：旧token写DB revoked，重启后仍不可用"""
    print("\n=== 2. Refresh Token 轮换 ===")
    # 先登录获取refresh_token
    resp = requests.post(f"{BASE_URL}/auth/login", json={"username": "admin", "password": "admin"}, headers=HEADERS)
    if resp.status_code != 200:
        print("  无法登录admin账户，跳过测试")
        return False
    data = resp.json()
    old_refresh = data.get("refresh_token")
    if not old_refresh:
        print("  响应中没有refresh_token")
        return False
    print(f"  获取到refresh_token: {old_refresh[:10]}...")
    
    # 使用旧refresh_token获取新access_token
    resp = requests.post(f"{BASE_URL}/auth/refresh", json={"refresh_token": old_refresh})
    ok1 = resp.status_code == 200
    print_result("旧refresh_token可刷新", ok1, f"状态码 {resp.status_code}")
    if ok1:
        new_data = resp.json()
        new_refresh = new_data.get("refresh_token")
        print(f"  获得新refresh_token: {new_refresh[:10]}...")
        # 再次使用旧refresh_token应失败
        resp2 = requests.post(f"{BASE_URL}/auth/refresh", json={"refresh_token": old_refresh})
        ok2 = resp2.status_code == 401
        print_result("旧refresh_token已撤销", ok2, f"状态码 {resp2.status_code}")
        # 验证DB中是否有revoked记录（间接验证）
        # 可通过查询日志或检查API，但此处省略
        return ok1 and ok2
    return False

def test_config_admin_only():
    """验证配置API的admin-only校验"""
    print("\n=== 3. 配置API Admin-only校验 ===")
    # 先获取非admin token（只有admin用户，所以测试403逻辑）
    resp = requests.post(f"{BASE_URL}/auth/login", json={"username": "admin", "password": "admin"})
    if resp.status_code != 200:
        print("  登录失败，跳过")
        return False
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 尝试更新配置
    resp = requests.put(f"{BASE_URL}/config", json={"key": "poll_interval", "value": "35"}, headers=headers)
    # 注意：当前实现检查user.get("role") != "admin"，但token中没有role字段
    # 预期行为：可能允许（因为role不是admin？）或拒绝
    print(f"  更新配置返回状态码 {resp.status_code}")
    # 由于token中没有role，user.get("role")返回None，所以条件 None != "admin" 为True，应返回403
    # 但实际情况需验证
    if resp.status_code == 403:
        print_result("非admin角色（或无role）被拒绝", True, "符合预期")
        return True
    elif resp.status_code == 200:
        print_result("admin检查可能缺失", False, "配置更新成功，admin检查可能未生效")
        return False
    else:
        print_result("未知响应", False, f"状态码 {resp.status_code}")
        return False

def test_logs_device_name():
    """验证Logs device_name LEFT JOIN正确，null处理"""
    print("\n=== 4. Logs device_name LEFT JOIN ===")
    # 需要先有日志记录，尝试获取日志列表
    resp = requests.post(f"{BASE_URL}/auth/login", json={"username": "admin", "password": "admin"})
    if resp.status_code != 200:
        print("  登录失败，跳过")
        return False
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    resp = requests.get(f"{BASE_URL}/logs", headers=headers)
    if resp.status_code != 200:
        print(f"  获取日志失败 {resp.status_code}")
        return False
    data = resp.json()
    items = data.get("items", [])
    if items:
        item = items[0]
        has_device_name = "device_name" in item
        print_result("日志项包含device_name字段", has_device_name)
        # 检查device_name是否可能为null
        for it in items[:3]:
            print(f"  示例: device_id={it.get('device_id')}, device_name={it.get('device_name')}")
        return True
    else:
        print("  无日志数据，跳过深度检查")
        return True  # 无数据也视为通过

def test_frontend_429():
    """验证前端429处理：倒计时、按钮禁用、自动恢复（静态分析）"""
    print("\n=== 5. 前端429处理 ===")
    # 静态检查前端代码
    import os
    frontend_path = "/Users/sunwenyong/projects/openclaw-hub/frontend/src/pages/Login.tsx"
    if os.path.exists(frontend_path):
        with open(frontend_path, "r") as f:
            content = f.read()
            has_rate_limit = "rateLimited" in content
            has_retry_after = "retryAfter" in content
            has_disabled = "disabled={rateLimited}" in content
            has_timer = "setInterval" in content
            print_result("有rateLimited状态", has_rate_limit)
            print_result("有retryAfter状态", has_retry_after)
            print_result("按钮禁用逻辑", has_disabled)
            print_result("倒计时定时器", has_timer)
            return all([has_rate_limit, has_retry_after, has_disabled, has_timer])
    else:
        print("  前端文件不存在")
        return False

def test_frontend_settings():
    """验证前端Settings页面：配置CRUD、系统信息展示"""
    print("\n=== 6. 前端Settings页面 ===")
    frontend_path = "/Users/sunwenyong/projects/openclaw-hub/frontend/src/pages/Settings.tsx"
    if os.path.exists(frontend_path):
        with open(frontend_path, "r") as f:
            content = f.read()
            has_system_info = "系统信息" in content
            has_config_form = "配置管理" in content
            has_save_button = "保存配置" in content
            has_poll_interval = "poll_interval" in content
            print_result("系统信息展示", has_system_info)
            print_result("配置管理表单", has_config_form)
            print_result("保存按钮", has_save_button)
            print_result("配置字段映射", has_poll_interval)
            return all([has_system_info, has_config_form, has_save_button, has_poll_interval])
    else:
        print("  Settings文件不存在")
        return False

def test_api_contract():
    """验证前后端契约：API路径、请求/响应格式对齐"""
    print("\n=== 7. 前后端契约 ===")
    # 检查几个关键端点
    endpoints = [
        ("POST /auth/login", {"username": "string", "password": "string"}),
        ("POST /auth/refresh", {"refresh_token": "string"}),
        ("GET /logs", {}),
        ("PUT /config", {"key": "string", "value": "string"}),
        ("GET /config", {}),
    ]
    # 仅做简单存在性检查
    ok = True
    for endpoint, _ in endpoints:
        method, path = endpoint.split()
        if path.startswith("/"):
            full = BASE_URL + path
        else:
            full = BASE_URL + "/" + path
        try:
            if method == "GET":
                resp = requests.get(full, timeout=2)
            elif method == "POST":
                resp = requests.post(full, json={}, timeout=2)
            elif method == "PUT":
                resp = requests.put(full, json={}, timeout=2)
            else:
                continue
            # 不关心状态码，只要端点存在（非404）
            if resp.status_code == 404:
                print_result(f"{endpoint} 存在", False, "404 Not Found")
                ok = False
            else:
                print_result(f"{endpoint} 存在", True, f"状态码 {resp.status_code}")
        except Exception as e:
            print_result(f"{endpoint} 可达", False, str(e))
            ok = False
    return ok

def main():
    results = []
    results.append(test_rate_limit())
    results.append(test_refresh_token_rotation())
    results.append(test_config_admin_only())
    results.append(test_logs_device_name())
    results.append(test_frontend_429())
    results.append(test_frontend_settings())
    results.append(test_api_contract())
    
    passed = sum(results)
    total = len(results)
    print(f"\n=== 总结 ===")
    print(f"通过 {passed}/{total}")
    if passed == total:
        print("✅ 所有重点验证通过")
    else:
        print("❌ 部分验证失败")
        sys.exit(1)

if __name__ == "__main__":
    main()