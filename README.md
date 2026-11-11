# SRTP Research Portfolio | 大模型学科题目合成与评测

这是我参与浙江大学大学生创新训练项目（SRTP）期间的个人科研实践展示。项目研究方向为**面向多模态大模型推理能力评测的学科竞赛题目合成**。

> 本仓库是面向奖学金申请和个人科研经历展示整理的脱敏版本，不是项目官方仓库，也不代表团队的完整研究成果。

## 项目背景

现有大模型在复杂学科推理中仍可能出现条件理解偏差、推导错误、答案不一致和机械拼接等问题。项目围绕数理化生及信息学竞赛题目的合成与评测，探索题目生成、结构化数据处理、质量检查以及人工评估流程。

项目目前仍在推进，相关投稿论文处于修改阶段。因此，本仓库**不包含论文 PDF、论文正文、未公开方法细节、完整实验结果、内部数据集或第三方文献**。

## 我的科研参与

### 1. 结构化数据处理与质量检查

- 使用 Python 处理 JSON/JSONL 格式的题目数据；
- 检查题目、解答、答案等关键字段是否缺失；
- 识别 JSON 解析错误、字段不一致及不符合要求的表述；
- 对批量处理结果进行格式规范化和人工复核。

### 2. 大模型工具与 API 实践

- 使用大模型 API 辅助生成、整理和检查结构化题目数据；
- 处理模型输出中代码块、额外文本和不规范 JSON 等问题；
- 通过重试、格式校验和异常处理提高批处理流程的稳定性；
- 使用 ChatGPT、通义千问等工具分析报错、理解代码逻辑并查找解决方案。

### 3. 人工质量评测

我参与了生成物理题的人工评测，对 **60 条去重样本**进行最终评分。评测采用四个维度：

| 维度 | 评估内容 |
| --- | --- |
| Problem Correctness | 题目设定是否符合物理规律、条件是否完整 |
| Solution Correctness | 推导过程和最终答案是否正确 |
| Language Quality | 题干与解答是否清晰、自然、规范 |
| Fusion Elegance | 不同物理机制的组合是否合理、自然 |

这项工作让我进一步理解了：大模型生成内容不能只依赖自动分数，还需要通过清晰的评价标准、人工复核和可追溯记录保证质量。

## 仓库内容

```text
.
├── README.md
├── CONTRIBUTIONS.md
├── PRIVACY.md
├── .env.example
├── requirements.txt
├── examples/
│   ├── demo_problems.jsonl
│   └── demo_reviews.jsonl
└── src/
    ├── jsonl_quality_audit.py
    ├── review_summary.py
    └── review_app.py
```

- `jsonl_quality_audit.py`：检查 JSONL 数据的格式与关键字段；
- `review_summary.py`：按样本保留最新正式评分并输出汇总结果；
- `review_app.py`：一个使用匿名示例数据构建的简化评分界面；
- `examples/`：为展示程序流程而重新编写的虚构样例，不来自未公开数据集。

## 快速体验

```bash
python src/jsonl_quality_audit.py examples/demo_problems.jsonl
python src/review_summary.py examples/demo_reviews.jsonl
```

运行匿名评分界面：

```bash
pip install -r requirements.txt
streamlit run src/review_app.py -- --data examples/demo_problems.jsonl
```

## 技术工具

`Python` · `JSON/JSONL` · `Streamlit` · `LLM API` · `Git/GitHub` · `人工评测`

## 凭据安全

仓库中涉及 API 凭据的展示统一使用 `********`，不会出现真实值。实际运行时应通过环境变量读取凭据，例如 `LLM_API_KEY`，不要把真实 Key 写进源码、截图、文档或 Git 历史。

## 说明

- 本仓库只展示我实际参与过的研究环节，不将团队成果表述为个人独立成果；
- 示例代码是对科研工作流的脱敏重构，不等同于项目生产代码；
- 如需了解项目的正式成果，请以项目组后续公开版本为准。

