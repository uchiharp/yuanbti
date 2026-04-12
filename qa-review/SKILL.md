---
name: qa-review
type: methodology
trigger: user-request
description: QA测试评审方法论。以"测试艺术家"视角评审测试质量，含覆盖度评估、用例质量、断言有效性、边界覆盖。
priority: high
auto-load: true
---

# QA 测试质量审查

> 💡 本 skill 可在 agent-pipeline 流程中使用，也可独立用于任何评审场景。

## 评审者思维模式：测试艺术家

测试不是证明代码能工作，是证明在什么情况下代码不能工作。

"所有测试通过但用户还遇到bug，说明测试方向错了。"

我是个侦探。每个bug都是一桩悬案，每行代码都有嫌疑。我不信任代码，不信任注释，不信任"应该没问题"。

### 死亡场景设计
先问：这段代码能怎么死？
- 空输入、超长输入、特殊字符、负数、零、最大值+1
- 并发访问、网络中断、超时、重试风暴
- 数据不一致：删除后查询、更新中读取、脏数据回滚
- 边界条件：分页第一页最后一页、时区切换、闰秒

### 断言精准度
- `assertTrue(result)` — 废话断言，告诉我它为什么true
- `assertEquals(expected, actual)` — 好一点，但expected对吗？
- 好断言要回答：值是什么？范围在哪？副作用是什么？状态变了吗？

### 测试意义检查
每个测试case必须回答：
1. **这个测试发现了哪种bug？** — 如果回答不了，删掉
2. **如果这个测试挂了，能快速定位问题吗？** — 如果不能，重写
3. **这个测试和哪个生产bug对应？** — 如果没有，它只是自嗨

### 审查清单

#### 测试覆盖率 ≠ 质量覆盖
- 覆盖率80%但全测getter/setter = 自欺欺人
- 关键路径没测 = 裸奔
- 边界条件没测 = 地雷阵
- 异常流程没测 = 等着出事

#### 测试坏味道
- 测试之间有依赖顺序 → 脆弱
- 测试里写死了时间/日期 → 定时炸弹
- Mock了被测函数本身 → 你在测什么？
- 一个测试跑了5分钟 → 没人会跑
- 测试名字是test1/test2 → 失去可读性

### 输出格式

对每个发现：
- **故障模式：** 怎么触发的
- **影响：** 用户会看到什么
- **复现步骤：** 一步步来
- **修复建议：** 具体到代码级别
- **回归测试：** 修完之后加什么测试防止复发

---

## 评估标准

# QA 评审官评估标准 v1.0

## 总则

| 规则 | 说明 |
|------|------|
| 评分范围 | 1-10，默认起点7分，扣分制 |
| 8分 | 无任何🟡/🔴项 |
| 9分 | 8分基础上至少2个维度有亮点 |
| 10分 | 几乎不可能，需要行业标杆级水准 |
| 一票否决 | 核心业务逻辑零覆盖；测试全绿但功能有bug |

## 权重分配

| 维度 | 权重 | 说明 |
|------|------|------|
| 测试覆盖度 | 15% | 分支、语句、业务路径覆盖 |
| 用例质量 | 15% | 用例是否测了真实业务逻辑 |
| 断言有效性 | 15% | 断言是否具体、有意义 |
| 边界覆盖 | 10% | 边界值、极端输入 |
| 异常场景覆盖 | 10% | 错误路径、异常分支 |
| 测试可维护性 | 10% | 可读性、DRY、结构清晰 |
| 测试独立性 | 10% | 测试间无依赖、可并行 |
| Mock合理性 | 10% | Mock范围适当、不Mock业务逻辑 |
| 去AI味评估 | 5% | 自然度、非模板化（详见末尾） |

---

## 1. 测试覆盖度（15%）

### 检查项

| # | 检查项 | 严重程度 | 扣分 |
|---|--------|----------|------|
| 1.1 | 核心业务逻辑有无测试覆盖 | 🔴阻断 | -3 |
| 1.2 | 所有public方法是否被测试 | 🔴阻断 | -2 |
| 1.3 | if/else 分支是否全覆盖 | 🟡重要 | -1/缺一个 |
| 1.4 | switch/case 每个分支是否覆盖 | 🟡重要 | -1/缺一个 |
| 1.5 | 循环边界（0次、1次、N次）是否覆盖 | 🟡重要 | -1 |
| 1.6 | 业务状态机/状态流转是否覆盖 | 🟡重要 | -2 |
| 1.7 | 空值/null 输入是否有测试 | 🟡重要 | -1 |
| 1.8 | protected/private 方法是否通过public方法间接覆盖 | 🟢建议 | -0.5 |
| 1.9 | 新增代码是否对应新增测试 | 🟡重要 | -1 |

### 判定条件

| 等级 | 条件 |
|------|------|
| 🟢 绿 | 核心逻辑100%覆盖，分支覆盖≥90% |
| 🟡 黄 | 核心逻辑有覆盖但存在≥2个未测分支 |
| 🔴 红 | 核心业务逻辑无测试，或分支覆盖<60% |

### 好测试 vs 坏测试

**❌ 坏：只测happy path，跳过条件分支**
```java
@Test
void testCalculatePrice() {
    int price = service.calculatePrice(order);
    assertTrue(price > 0);
}
```

**✅ 好：每个分支都有独立用例**
```java
@Test
void shouldReturnZero_whenOrderIsEmpty() {
    assertEquals(0, service.calculatePrice(emptyOrder));
}

@Test
void shouldApplyDiscount_whenOrderTotalExceedsThreshold() {
    assertEquals(85, service.calculatePrice(bigOrder));
}

@Test
void shouldThrow_whenOrderContainsInvalidItem() {
    assertThrows(InvalidOrderException.class,
        () -> service.calculatePrice(invalidOrder));
}
```

---

## 2. 用例质量（15%）

### 检查项

| # | 检查项 | 严重程度 | 扣分 |
|---|--------|----------|------|
| 2.1 | 用例是否真的验证了业务行为（而非实现细节） | 🔴阻断 | -3 |
| 2.2 | 测试方法名是否描述预期行为 | 🟡重要 | -0.5/个 |
| 2.3 | 是否存在"测通过"而非"测正确"的用例 | 🟡重要 | -2 |
| 2.4 | 是否有正向+反向对照用例 | 🟡重要 | -1 |
| 2.5 | Arrange-Act-Assert结构是否清晰 | 🟢建议 | -0.5 |
| 2.6 | 是否包含无意义的参数遍历测试 | 🟡重要 | -1 |
| 2.7 | 每个用例是否只验证一个行为 | 🟢建议 | -0.5 |

### 判定条件

| 等级 | 条件 |
|------|------|
| 🟢 绿 | 每个用例验证明确的业务规则，有正向+反向对照 |
| 🟡 黄 | 存在"验证能跑通"型用例，或部分用例描述模糊 |
| 🔴 红 | 用例只验证方法能被调用不报错，不验证任何业务规则 |

### 好测试 vs 坏测试

**❌ 坏：测"能跑通"不测"对不对"**
```java
@Test
void testProcessOrder() {
    Order order = new Order("item1", 10);
    service.processOrder(order);
    assertNotNull(order); // 废话断言
}
```

**✅ 好：验证具体业务行为**
```java
@Test
void shouldSetStatusToShipped_whenPaymentConfirmed() {
    service.processOrder(paidOrder);
    assertEquals(OrderStatus.SHIPPED, paidOrder.getStatus());
    verify(notificationService).sendShipmentEmail(paidOrder.getUserId());
}
```

---

## 3. 断言有效性（15%）

### 检查项

| # | 检查项 | 严重程度 | 扣分 |
|---|--------|----------|------|
| 3.1 | 是否存在只 assertNotNull/assertTrue 的低效断言 | 🔴阻断 | -2/处 |
| 3.2 | 断言是否验证了预期的具体值 | 🟡重要 | -1/处 |
| 3.3 | 字符串/集合比较是否使用了精确匹配 | 🟡重要 | -1 |
| 3.4 | 浮点数断言是否使用了delta参数 | 🟡重要 | -1 |
| 3.5 | 异常测试是否验证了异常信息内容 | 🟡重要 | -1 |
| 3.6 | 是否存在冗余断言（重复验证同一事实） | 🟢建议 | -0.5 |
| 3.7 | 断言失败时错误信息是否有助于定位问题 | 🟢建议 | -0.5 |

### 判定条件

| 等级 | 条件 |
|------|------|
| 🟢 绿 | 断言具体、精确，失败时可直接定位问题 |
| 🟡 黄 | 部分断言过于宽泛（notNull但没验具体值） |
| 🔴 红 | 全局仅 assertNotNull，无任何业务值验证 |

### 好测试 vs 坏测试

**❌ 坏：机械断言**
```java
@Test
void testGetUser() {
    User user = userService.getById(1L);
    assertNotNull(user);        // user不是null又怎样？名字对吗？
    assertTrue(user.getAge() > 0); // 废话
}
```

**✅ 好：精确断言**
```java
@Test
void shouldReturnUserWithCorrectProfile_whenIdExists() {
    User user = userService.getById(1L);
    assertEquals("张三", user.getName());
    assertEquals(28, user.getAge());
    assertEquals(Role.ADMIN, user.getRole());
    assertEquals(1L, user.getDepartmentId());
}
```

---

## 4. 边界覆盖（10%）

### 检查项

| # | 检查项 | 严重程度 | 扣分 |
|---|--------|----------|------|
| 4.1 | 数值边界（MIN, MAX, 0, -1, MAX+1） | 🟡重要 | -1/缺一类 |
| 4.2 | 集合边界（空集合、单元素、超大量） | 🟡重要 | -1 |
| 4.3 | 字符串边界（空串、超长串、特殊字符、SQL注入/XSS） | 🟡重要 | -1 |
| 4.4 | 分页边界（第1页、最后一页、超出范围页） | 🟡重要 | -1 |
| 4.5 | 时间边界（闰年、时区、夏令时、跨日） | 🟢建议 | -0.5 |
| 4.6 | 并发边界（并发访问同一资源） | 🟢建议 | -0.5 |
| 4.7 | ID/主键边界（0、负数、Long.MAX_VALUE） | 🟡重要 | -1 |

### 判定条件

| 等级 | 条件 |
|------|------|
| 🟢 绿 | 核心边界值全覆盖，含0/空/溢出场景 |
| 🟡 黄 | 覆盖了基本边界但遗漏极端值 |
| 🔴 红 | 无任何边界值测试 |

---

## 5. 异常场景覆盖（10%）

### 检查项

| # | 检查项 | 严重程度 | 扣分 |
|---|--------|----------|------|
| 5.1 | 网络超时/连接失败是否覆盖 | 🟡重要 | -1 |
| 5.2 | 外部服务返回错误码是否覆盖 | 🟡重要 | -1 |
| 5.3 | 数据库操作失败是否覆盖 | 🟡重要 | -1 |
| 5.4 | 数据格式不合法是否覆盖 | 🟡重要 | -1 |
| 5.5 | 权限不足/未授权是否覆盖 | 🟡重要 | -1 |
| 5.6 | 资源不存在（404）是否覆盖 | 🟡重要 | -1 |
| 5.7 | 并发冲突（乐观锁失败等）是否覆盖 | 🟢建议 | -0.5 |
| 5.8 | 磁盘/内存不足等系统级异常是否覆盖 | 🟢建议 | -0.5 |
| 5.9 | 异常后系统是否恢复到正确状态（无脏数据） | 🔴阻断 | -2 |

### 判定条件

| 等级 | 条件 |
|------|------|
| 🟢 绿 | 每个外部依赖至少覆盖1个失败场景，且验证了恢复状态 |
| 🟡 黄 | 有异常测试但覆盖不全或未验证恢复状态 |
| 🔴 红 | 无任何异常场景测试 |

---

## 6. 测试可维护性（10%）

### 检查项

| # | 检查项 | 严重程度 | 扣分 |
|---|--------|----------|------|
| 6.1 | 测试数据构建是否使用了Builder/工厂模式 | 🟢建议 | -0.5 |
| 6.2 | 是否存在测试间共享可变状态 | 🔴阻断 | -2 |
| 6.3 | 硬编码的魔数是否有常量/注释说明 | 🟡重要 | -0.5/处 |
| 6.4 | 测试方法长度是否≤30行 | 🟢建议 | -0.5 |
| 6.5 | 是否有重复的setup代码未提取 | 🟢建议 | -0.5 |
| 6.6 | 测试类/方法的组织是否与被测代码结构一致 | 🟢建议 | -0.5 |
| 6.7 | @BeforeEach/@BeforeAll使用是否合理 | 🟢建议 | -0.5 |
| 6.8 | 测试是否使用了有意义的测试数据（非 "test123"） | 🟡重要 | -1 |

### 判定条件

| 等级 | 条件 |
|------|------|
| 🟢 绿 | 结构清晰，有测试数据工厂，无不合理共享状态 |
| 🟡 黄 | 存在少量重复代码或魔数 |
| 🔴 红 | 测试间共享可变状态导致顺序依赖 |

---

## 7. 测试独立性（10%）

### 检查项

| # | 检查项 | 严重程度 | 扣分 |
|---|--------|----------|------|
| 7.1 | 测试是否可任意顺序执行 | 🔴阻断 | -2 |
| 7.2 | 是否依赖外部环境（数据库、文件系统、网络） | 🟡重要 | -1/处 |
| 7.3 | 单个测试失败是否影响其他测试 | 🔴阻断 | -2 |
| 7.4 | 是否使用了 @DirtiesContext 等补救手段（说明设计有问题） | 🟡重要 | -1 |
| 7.5 | 测试是否依赖时间/日期（非mock） | 🟡重要 | -1 |
| 7.6 | 测试是否依赖文件系统路径 | 🟡重要 | -1 |
| 7.7 | 并行执行是否稳定（无flaky test） | 🟡重要 | -2 |

### 判定条件

| 等级 | 条件 |
|------|------|
| 🟢 绿 | 完全独立，可并行，无flaky |
| 🟡 黄 | 顺序依赖但不严重，偶有flaky |
| 🔴 红 | 存在强制顺序依赖或高度不稳定的测试 |

---

## 8. Mock合理性（10%）

### 检查项

| # | 检查项 | 严重程度 | 扣分 |
|---|--------|----------|------|
| 8.1 | 是否Mock了被测对象自身 | 🔴阻断 | -3 |
| 8.2 | 是否Mock了简单POJO/DTO（不该mock） | 🟡重要 | -1 |
| 8.3 | Mock返回值是否固定不变（不管输入是什么） | 🟡重要 | -1/处 |
| 8.4 | 是否过度Mock导致测试什么都不验证 | 🔴阻断 | -2 |
| 8.5 | 外部服务Mock是否覆盖了正常+异常响应 | 🟡重要 | -1 |
| 8.6 | 是否使用了 spy 而非 mock 来保留部分真实行为 | 🟢建议 | -0.5 |
| 8.7 | verify 调用是否验证了参数（非 any()） | 🟡重要 | -1/处 |
| 8.8 | 是否有不必要的 reset() / clearInvocations() | 🟢建议 | -0.5 |
| 8.9 | 集成测试中是否错误使用了Mock | 🟡重要 | -2 |

### 判定条件

| 等级 | 条件 |
|------|------|
| 🟢 绿 | Mock范围精确，只mock外部依赖，返回值与输入相关 |
| 🟡 黄 | 存在不必要的mock或verify(any()) |
| 🔴 红 | Mock了被测对象或过度mock导致测试空转 |

### 好测试 vs 坏测试

**❌ 坏：过度Mock，什么都不验证**
```java
@Test
void testProcessOrder() {
    when(orderRepo.save(any())).thenReturn(order);
    when(paymentService.pay(any())).thenReturn(true);
    when(inventoryService.deduct(any())).thenReturn(true);
    
    orderService.processOrder(order);
    
    verify(orderRepo).save(any()); // any() = 没验证参数
    // 业务逻辑被mock掉了，测试形同虚设
}
```

**✅ 好：Mock外部依赖，验证业务编排**
```java
@Test
void shouldChargeAndShip_whenOrderPlaced() {
    orderService.processOrder(order);
    
    verify(paymentService).charge(order.getTotalAmount());
    verify(shippingService).scheduleDelivery(eq(order.getId()), any(LocalDateTime.class));
    verify(orderRepo).save(argThat(o -> 
        o.getStatus() == OrderStatus.PROCESSED 
        && o.getProcessedAt() != null));
}
```

---

## 9. 去AI味评估（5%）

> 此维度独立评分，检测测试代码是否由AI机械生成，缺乏人类工程师的判断力。

### 检查项

| # | AI特征 | 严重程度 | 扣分 |
|---|--------|----------|------|
| 9.1 | 模板化命名：`testMethod_normalCase`, `testMethod_edgeCase`, `testMethod_errorCase` | 🟡重要 | -1 |
| 9.2 | 机械断言模式：每个用例固定只有 `assertNotNull` 或 `assertTrue` | 🔴阻断 | -2 |
| 9.3 | 重复测试结构：N个用例结构完全相同只换参数，未用参数化 | 🟡重要 | -1 |
| 9.4 | 无意义注释：`// 测试正常情况`, `// 验证结果`, `// 测试边界条件` | 🟡重要 | -0.5/处 |
| 9.5 | 过度使用 `@DisplayName` 写中文大白话但方法名是英文模板 | 🟢建议 | -0.5 |
| 9.6 | 每个测试类都有完全相同的setup模板 | 🟡重要 | -1 |
| 9.7 | Mock配置冗余：`when(x).thenReturn(y)` 但 y 从未在断言中引用 | 🟡重要 | -1/处 |
| 9.8 | 测试数据使用无意义填充：`"testUser1"`, `"mockData"`, `"example"` | 🟡重要 | -0.5/处 |
| 9.9 | 缺乏业务语境：看不出这个测试在防什么bug | 🔴阻断 | -2 |

### AI味判定

| 等级 | 条件 |
|------|------|
| 🟢 绿 | 命名自然有业务含义，断言精确，结构有变化，有工程师判断痕迹 |
| 🟡 黄 | 存在1-2个AI特征但不严重 |
| 🔴 红 | ≥3个AI特征，或存在阻断级AI特征 |

### 好测试 vs 坏测试

**❌ 坏：AI味浓厚**
```java
// 测试正常情况
@Test
@DisplayName("测试用户注册 - 正常情况")
void testRegisterUser_normalCase() {
    // Arrange
    UserDTO userDTO = new UserDTO("testUser1", "password123");
    when(userRepo.save(any())).thenReturn(new User(1L, "testUser1"));
    
    // Act
    User result = userService.register(userDTO);
    
    // Assert
    assertNotNull(result);           // 又来了
    assertEquals("testUser1", result.getName());
}

// 测试边界条件
@Test
@DisplayName("测试用户注册 - 边界条件")
void testRegisterUser_edgeCase() {
    UserDTO userDTO = new UserDTO("testUser2", "password123");
    when(userRepo.save(any())).thenReturn(new User(2L, "testUser2"));
    
    User result = userService.register(userDTO);
    
    assertNotNull(result);
}
```

**✅ 好：像人写的**
```java
@Test
void shouldRejectRegistration_whenEmailAlreadyExists() {
    when(userRepo.findByEmail("zhang@example.com"))
        .thenReturn(Optional.of(existingUser));
    
    assertThrows(DuplicateEmailException.class,
        () -> userService.register(zhangRequest));
}

@Test
void shouldHashPasswordBeforeSaving() {
    userService.register(newRequest);
    
    verify(userRepo).save(argThat(user ->
        !user.getPassword().equals(rawPassword)
        && passwordEncoder.matches(rawPassword, user.getPassword())));
}
```

---

## 评分汇总模板

```
=== 测试质量评审报告 ===

1. 测试覆盖度    : __/10  [🟢🟡🔴]
2. 用例质量      : __/10  [🟢🟡🔴]
3. 断言有效性    : __/10  [🟢🟡🔴]
4. 边界覆盖      : __/10  [🟢🟡🔴]
5. 异常场景覆盖  : __/10  [🟢🟡🔴]
6. 测试可维护性  : __/10  [🟢🟡🔴]
7. 测试独立性    : __/10  [🟢🟡🔴]
8. Mock合理性    : __/10  [🟢🟡🔴]
9. 去AI味评估    : __/10  [🟢🟡🔴]

加权总分: __/10

一票否决: [ ] 无  [ ] 触发（原因：______）

必须修复（🔴）:
- ...

建议修复（🟡）:
- ...

可选改进（🟢）:
- ...
```

## 扣分速查

| 行为 | 扣分 |
|------|------|
| 核心逻辑零覆盖 | 一票否决 |
| 测全绿但功能有bug | 一票否决 |
| Mock了被测对象 | -3 |
| 断言全是assertNotNull | -2/处 |
| 过度mock致测试空转 | -2 |
| 测试间共享可变状态 | -2 |
| 未验证异常后恢复状态 | -2 |
| 每缺一个分支覆盖 | -1 |
| verify使用any()不验参数 | -1/处 |
| AI味≥3个特征 | 该维度按红处理 |

## 十、一眼AI套路识别（额外扣分项）

> **原则：AI写代码像做标准答案，人类写代码像打实战。一眼AI的东西必须严惩。**

### 🔴 一眼AI套路（每个-3分，叠加不封顶）

| 编号 | 一眼AI套路 | 典型特征 | 扣分 |
|------|-----------|---------|------|
| EYE-01 | **八股文注释** | `@param data 数据` / `@return 返回结果` / `这个方法用于处理...` — 注释100%废话 | -3 |
| EYE-02 | **万能try-catch** | 每个方法都套 `try { ... } catch (Exception e) { log.error(e); }`，就像AI有个代码模板 | -3 |
| EYE-03 | **教科书式代码结构** | Controller→Service→ServiceImpl→Repository→DTO→Converter，6层拆开，实际业务一句话能说完 | -3 |
| EYE-04 | **Emoji装饰风** | 注释或日志里大量使用 🚀💡⚠️✅❌ 等emoji，一看就是AI的"美观强迫症" | -3 |
| EYE-05 | **过度完整性** | 每个功能都写注册/登录/登出/CRUD/导出/导入/搜索/分页，看似完整实际没有核心亮点 | -3 |
| EYE-06 | **安全套话三件套** | "输入校验→参数化查询→输出编码" 或 "最小权限原则→加密传输→不暴露堆栈"，背概念不落地 | -3 |
| EYE-07 | **JSON假数据** | 接口返回的数据明显是编的，如用户名全是"张三李四王五"、地址全是"北京市朝阳区" | -3 |
| EYE-08 | **===分隔线强迫症** | 日志或输出里大量使用 `===` `---` `━━━` 分隔线，排版过于工整 | -3 |
| EYE-09 | **千篇一律的CSS** | 所有页面长一个样：白色背景+圆角卡片+蓝色按钮+灰色边框，毫无个性 | -3 |
| EYE-10 | **所有变量都是英文全拼** | `userAuthenticationTokenRepository` 而不是 `userTokenRepo`，过于"标准" | -3 |

### 🟡 高度可疑（每个-2分）

| 编号 | 特征 | 说明 |
|------|------|------|
| SUS-01 | 每个方法都有完整JavaDoc | 包括简单到不能再简单的getter |
| SUS-02 | 错误提示过于友好 | "抱歉，操作失败了，请稍后重试" — 真实产品不会这么温柔 |
| SUS-03 | TODO全是英文 | "TODO: add validation" "FIXME: handle edge case" — 中国开发者会写中文TODO |
| SUS-04 | 没有任何遗留代码 | 生产代码过于干净，没有注释掉的旧代码、没有调试痕迹 |
| SUS-05 | 所有import都精准使用 | 没有任何多余的import，也没有忘记的import — 真实开发总有遗漏 |
| SUS-06 | commit message完美 | "feat: add user authentication" "fix: resolve null pointer" — 太规范了 |
| SUS-07 | 测试用例命名过于统一 | `testCreateUser_success()` `testCreateUser_fail()` — 格式太整齐 |

### 🎯 AI文档/PRD 一眼识别（每个-3分）

| 编号 | 特征 | 示例 |
|------|------|------|
| DOC-01 | **"本文档旨在..."开头** | "本文档旨在介绍系统的设计理念和实现方案" |
| DOC-02 | **"值得注意的是"** | 每段都用"值得注意的是""需要指出的是""值得一提的是"过渡 |
| DOC-03 | **"综上所述"结尾** | 最后一句话永远是"综上所述，本方案..." |
| DOC-04 | **两面话不敢下结论** | "该方案在性能和可维护性之间取得了平衡" — 什么都没说 |
| DOC-05 | **过度使用排比** | "首先...其次...最后..." "一方面...另一方面..." |
| DOC-06 | **每点都面面俱到** | 10个需求每个都写2页，但没有一个深入到细节 |
| DOC-07 | **进度条/表格强迫症** | 报告里大量使用进度条、表格、emoji，排版过度精致 |

### 一眼AI的终极判断标准

问自己一个问题：**"如果这是我同事写的，我会信吗？"**

- 如果答案是"不太可能" → 这就是一眼AI
- 如果答案是"说不准" → 可疑，需要进一步检查
- 如果答案是"像他的风格" → 通过

### 惩罚规则

```
一眼AI扣分 = Σ(🔴项 × 3) + Σ(🟡项 × 2) + Σ(文档项 × 3)

最终去AI味得分 = 之前去AI味维度的得分 - 一眼AI扣分
（最低0分，不倒扣）
```

### 特别条款：三眼识别

**以下任一情况出现，直接判定去AI味为0分，总评自动降一档：**

1. 🔴 代码中出现 `@author AI` 相关标识
2. 🔴 ≥3个 一眼AI🔴套路同时出现
3. 🔴 文档中出现 ≥3个 DOC-01~DOC-07 的特征
4. 🔴 整个文件读下来没有任何"人味"——没有TODO、没有FIXME、没有历史痕迹、没有临时方案、没有个人风格

**记住：宁可写得粗糙有个性，也不要写得完美像AI。代码是人写的，它应该有人的温度。**


> **评审报告路径：** 由调用方（协调者/用户）在任务消息中指定。未指定时默认 `/tmp/agent-skills-output/`。本skill不硬编码产出位置，可独立使用于任何项目。