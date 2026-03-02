# ChargeAutoTool（重构版）

目录重构为单总控 + 单文件聚合功能/服务：

- `run.py`：程序入口
- `app_controller.py`：唯一总控
- `app_state.py`：应用状态
- `features.py`：日志搜索/healthd/vbat/曲线/AI协议/寄存器分析
- `services.py`：AdbService/LogIO/RuleManager/TaskRunner
- `ui/`：主窗口、组件、样式、资源
- `rules/rules.json`：统一规则

## 运行

```bash
python -m ChargeAutoTool.run
```
