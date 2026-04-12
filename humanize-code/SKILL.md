---
name: humanize-code
description: 去除代码AI味，让代码更自然、更像人类写的。在代码审核、写代码、修复代码时必须使用。识别AI代码特征（模板化注释、过度规范、机械命名、冗余导入）并应用人类风格（业务导向注释、个性化风格、针对性异常处理、防御性编程）。
---

## 元数据
- **type:** knowledge
- **triggers:** agent-need
- **requires:** read, write
- **auto-load:** true
- **priority:** high

---

# Humanize Code - 去除代码AI味

## 核心理念

**AI代码像"标准答案"，正确但缺乏灵魂；人类代码像"实战经验"，可能不够优雅但解决问题。**

去AI化的本质是注入业务理解、上下文判断和工程经验，让代码从"能跑"变成"能维护、能演进"。

---

## 识别AI代码特征

### 🚨 必须去除的AI特征

#### 1. 注释模板化
❌ **AI特征：**
```java
/**
 * 处理用户数据
 *
 * @param data 数据
 * @return 结果
 */
```
- 内容重复或泛泛而谈
- 缺乏业务上下文
- "处理数据"这种无意义注释

✅ **人类风格：**
```java
/**
 * 计算税费（为什么用redis？因为mysql扛不住高并发）
 */
```

#### 2. 结构过度规范
❌ **AI特征：**
- 函数拆分细致到原子级别
- 简单脚本也用argparse
- 即使2行代码也写完整的Shebang
- 仿佛在写教科书示例

✅ **人类风格：**
- 复杂的地方复杂，简单的地方简单
- 该长就长，该短就短
- 实用主义优先

#### 3. 变量命名机械
❌ **AI特征：**
```python
data1 = ...
result_list = ...
temp = ...
```

✅ **人类风格：**
```python
user_order_count = ...
pending_payments = ...
calculated_tax_for_resident = ...
```

#### 4. 冗余导入
❌ **AI特征：**
```python
import os
import sys
import subprocess  # 根本没用
```

✅ **人类风格：**
```python
import json  # 只导入真正用的
```

#### 5. 过度工程
❌ **AI特征：**
- 简单功能也引入重量级依赖
- 处处追求"完美"架构
- 3行代码也要抽象工厂模式

✅ **人类风格：**
- 够用就行，别过度设计
- YAGNI原则（You Aren't Gonna Need It）

---

## 应用人类代码特征

### ✅ 必须添加的人类特征

#### 1. 业务导向注释
✅ **说明为什么，不是做了什么：**
```java
// 这里用redis是因为mysql扛不住
// 之所以不用MQ，是因为量太小不值得
// TODO: 并发超过1000要重构
```

#### 2. 口语化表达
✅ **自然而不是教科书：**
```java
log.warn("用户{}今日AI调用已达上限", userId);
// 而非：
// log.warn("User {} has exceeded the daily AI call limit", userId);
```

#### 3. 留下"活着"的痕迹
✅ **有迭代历史感：**
```java
// 2026-04-04: 临时方案，等Redis集群好了要改
// FIXME: 这里有并发问题，生产环境会炸
// TODO: 加个缓存
// 注释掉的旧代码（舍不得删）
```

#### 4. 针对性异常处理
✅ **具体异常具体对待：**
```python
# ❌ AI风格：
try:
    ...
except Exception as e:
    log.error(e)

# ✅ 人类风格：
try:
    ...
except FileNotFoundError:
    # 文件不存在就创建
    create_file()
except PermissionError:
    # 没权限就告警
    alert_admin()
except Exception as e:
    # 真正的未知错误才记录
    log.error(f"意外的错误: {e}")
```

#### 5. 防御性编程
✅ **考虑边界情况：**
```java
// ❌ AI风格：
public String getUserName(User user) {
    return user.getName();
}

// ✅ 人类风格：
public String getUserName(User user) {
    // 防御性：user可能为null
    return user != null ? user.getName() : "未知用户";
}
```

#### 6. 性能意识
✅ **知道哪里重要：**
```java
// ❌ AI风格：每次都查数据库
public List<Item> getItems() {
    return itemRepository.findAll();
}

// ✅ 人类风格：热点路径加缓存
@Cacheable("items")
public List<Item> getItems() {
    return itemRepository.findAll();
}
```

---

## 实施步骤

### 第一步：识别AI特征

**检查清单：**
- [ ] 是否有模板化的JavaDoc/注释？
- [ ] 是否有过度规范的代码结构？
- [ ] 是否有机械的变量名（data1, result_list）？
- [ ] 是否有未使用的导入？
- [ ] 是否有过度的抽象/设计模式？
- [ ] 是否有宽泛的异常捕获（catch Exception）？

### 第二步：应用人类风格

**重构原则：**
1. **简化注释** - 只保留关键信息，去掉冗余
2. **有意义命名** - 变量名要有业务语义
3. **实用主义** - 够用就行，别过度设计
4. **业务上下文** - 解释为什么，不是做了什么
5. **针对性异常** - 具体异常具体处理
6. **防御性编程** - 考虑边界和空值
7. **留下痕迹** - TODO、FIXME、历史注释
8. **口语化** - 自然表达，不是教科书式

### 第三步：注入"不完美"

**人类特征：**
- 不是所有代码都完美
- 有些地方可以"偷懒"
- 有历史痕迹（注释、TODO）
- 有调试痕迹（偶尔的print）
- 有"临时方案"

---

## 代码对比示例

### 示例1：注释风格

❌ **AI风格：**
```java
/**
 * 用户服务 - 提供用户相关功能
 *
 * 🔒 安全增强：包含密码加密
 * 🚀 性能优化：使用Redis缓存
 *
 * @author AI Generated
 * @version 1.0
 */
@Service
public class UserService {
    /**
     * 根据用户ID获取用户信息
     *
     * @param userId 用户ID
     * @return 用户信息对象
     */
    public User getUserById(Long userId) {
        return userRepository.findById(userId);
    }
}
```

✅ **人类风格：**
```java
/**
 * 用户服务
 * 
 * 注意：缓存时间设了1小时，因为用户信息不常变
 * TODO: 后面要改成主动失效机制
 */
@Service
public class UserService {
    
    public User getUserById(Long userId) {
        // userId为null就返回null，别抛异常
        if (userId == null) {
            return null;
        }
        
        return userRepository.findById(userId);
    }
}
```

### 示例2：异常处理

❌ **AI风格：**
```java
try {
    processPayment(order);
} catch (Exception e) {
    log.error("Payment processing failed", e);
    throw new RuntimeException("支付失败");
}
```

✅ **人类风格：**
```java
try {
    processPayment(order);
} catch (InsufficientBalanceException e) {
    // 余额不足，提示充值
    return "余额不足，请充值后重试";
} catch (PaymentTimeoutException e) {
    // 超时就重试一次
    return retryPayment(order);
} catch (Exception e) {
    // 真正的错误才记录堆栈
    log.error("支付系统异常: orderId={}", order.getId(), e);
    throw new RuntimeException("支付系统异常，请联系客服");
}
```

### 示例3：变量命名

❌ **AI风格：**
```python
data = get_data()
result = process(data)
output_list = []
for item in result:
    output_list.append(transform(item))
return output_list
```

✅ **人类风格：**
```python
user_orders = get_user_orders()
validated_orders = validate_orders(user_orders)
paid_orders = []
for order in validated_orders:
    if order.status == 'paid':
        paid_orders.append(order)
return paid_orders
```

---

## 质量检查标准

### 代码完成后检查：

#### AI味道检查
- [ ] ❌ 无模板化注释
- [ ] ❌ 无过度规范的代码
- [ ] ❌ 无机械的变量名
- [ ] ❌ 无未使用的导入
- [ ] ❌ 无过度的抽象

#### 人类特征检查
- [ ] ✅ 有业务上下文注释
- [ ] ✅ 有有意义的命名
- [ ] ✅ 有针对性的异常处理
- [ ] ✅ 有防御性编程
- [ ] ✅ 有"活着"的痕迹（TODO/FIXME）

---

## 注意事项

### ⚠️ 不要过度

**不要为了"人性化"而：**
- ❌ 故意写烂代码
- ❌ 去掉所有注释
- ❌ 使用无意义的变量名
- ❌ 忽略最佳实践

**保持平衡：**
- ✅ 代码要能跑
- ✅ 代码要可维护
- ✅ 代码要可读
- ✅ 但不要"教科书式"

### 🎯 目标

**从"标准答案"到"实战代码"：**
- 能跑 → 能维护
- 完美 → 实用
- 规范 → 自然
- AI味 → 人味

---

## 使用场景

### 必须使用的场景：
1. ✅ **代码审查时** - 检查AI特征
2. ✅ **写代码时** - 应用人类风格
3. ✅ **修复代码时** - 去除AI味道
4. ✅ **重构代码时** - 注入人性特征

### 具体步骤：
1. 识别AI特征
2. 应用人类风格
3. 注入"不完美"
4. 质量检查

---

## 核心原则总结

1. **简洁胜过冗余** - 注释要精简
2. **实用胜过完美** - 够用就行
3. **业务胜过技术** - 解释为什么
4. **具体胜过宽泛** - 针对性处理
5. **自然胜过规范** - 口语化表达
6. **痕迹胜过干净** - 有历史感

---

**记住：代码是写给人看的，不是写给机器看的。让它有人的温度。**
