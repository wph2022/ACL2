# ChargeAutoTool（规则驱动版）

目录采用“单总控 + 规则驱动”设计：

- `run.py`：程序入口
- `app_controller.py`：唯一总控（UI <-> 功能 <-> 规则）
- `app_state.py`：应用状态（dataclass）
- `features.py`：功能执行器（日志搜索 / healthd / vbat / 曲线 / AI协议 / 寄存器）
- `services.py`：服务层（AdbService / LogIO / RuleManager / TaskRunner）
- `rules/rules.json`：全部功能规则配置
- `rules/presets/*.json`：器件预置规则覆盖示例

## 核心优化

本版本将六类分析能力全部抽离为配置规则：

1. 日志搜索：关键字、大小写、输出条数
2. healthd：多正则匹配模板
3. vbat：电压提取正则与分组
4. 曲线：x/y 抽取分组规则
5. AI协议：协议 token 计数配置
6. 寄存器：地址-名称映射配置

后续器件切换只需改 `rules.json` 或替换 `presets/*.json`，无需改 Python 业务逻辑。

## 运行

```bash
python -m ChargeAutoTool.run
```
