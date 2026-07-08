# Shared

前后端共享的轻量类型包。当前只放不会绑定具体实现的领域枚举和响应结构：

- 导入状态：`uploaded`、`extracting`、`chunking`、`embedding`、`ready`、`failed`
- 回答类型：`direct_rule`、`related_inference`、`not_found`、`conflict`
- 来源类型：基础规则、扩展规则、FAQ、勘误和玩家备注

后续如果 API 使用 OpenAPI 生成类型，应优先让这里消费生成结果，而不是维护两套互相漂移的结构。
