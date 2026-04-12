# TOOLS.md - 创业助手·评审官

## 代码审查

```bash
mvn clean compile              # 验证编译通过
mvn test                       # 运行单元测试
```

## 环境检查

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080
```

## 项目信息（由协调者传入）

- **被审查agent：** 创业助手
- **产出路径：** {协调者指定}
