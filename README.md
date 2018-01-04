# 微信跳一跳

* jump_alg_top_edge 仅使用 opencv 边缘检测
  * canny后, 找下一个落点最高处坐标, 向下偏移一定量
  
* jump_alg_pattern_match 全部使用 opencv 模板匹配
