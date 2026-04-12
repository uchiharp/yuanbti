# TOOLS.md - 架构师·评审官

## 架构审查

- 使用 architecture-review skill 进行架构评审
- 产出审查报告到协调者指定的路径

## 构建验证

```bash
mvn clean compile              # 验证编译通过
mvn test                       # 运行单元测试
```

## 项目信息（由协调者传入）

- **被审查agent：** 架构师
- **产出路径：** {协调者指定}

## 审查标准

详见 code-review-standard skill（templates/REVIEW-STANDARDS.md）
