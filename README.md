# ACL2

当前仓库为 `ChargeAutoTool` 规则驱动重构版本：

- 六大能力（日志搜索 / healthd / vbat / 曲线 / AI 协议 / 寄存器）全部由 `ChargeAutoTool/rules/rules.json` 配置驱动。
- 主程序采用单总控结构：`app_controller.py + app_state.py + features.py + services.py`。

运行：

```bash
python -m ChargeAutoTool.run
```
