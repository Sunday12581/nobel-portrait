# 成图检查与一次性修正

以实际看到的图像为准，不把提示词出现了某个词当作质量已经达标。

| 检查项 | 可观察的条件 | 有偏差时的修正方向 |
|---|---|---|
| 人物身份 | 脸型、眼距、鼻形、发际线、眼镜形状、表情和年龄可辨认 | 重新附源照片，指出变化的部位，明确参考不提供长相 |
| 面部纸白 | 额头中央、鼻梁、双颊主要是纸底，而非连续肤色 | 删除大范围渲染，只留下必要墨线及少量金赭结构面 |
| 三色关系 | 纸白、墨黑和哑光金赭为主；默认无粉红嘴唇和彩色服装 | 对残留唇色明确改画成黑轮廓内的平整金赭形状，牙齿留纸白；不全图加黄色滤镜 |
| 墨线与头发 | 墨线有粗细、断笔；头发首先能读成几束宽弧形墨带与飞白 | 合并过密发丝、小裂纹和细碎刷痕，保留发型整体方向 |
| 金赭塑形 | 色块有选择性，边缘有刷痕；没有金属反射 | 减少水彩晕染或高光，保留局部不规则平面 |
| 纸纹与皮肤 | 纸纹跨背景和留白区连续，脸上没有额外的毛孔、胡茬和碎斑 | 移除局部皮肤散点，保留少量颜料材质和全画面细纸纹 |
| 表达密度 | 眼睑、鼻翼、唇缘等关键结构明确，脸部有大块连续留白 | 删除非必要细节，并加强关键轮廓；不要通过增添纹理模拟手绘 |
| 衣服简化 | 领口、翻领可辨，内部留白，不抢过面部 | 去除花纹、面料颗粒和密集褶皱，保留类别与轮廓 |
| 构图与附件 | 完整发顶、自然肩部、无额外字、签名、配饰 | 按原始要求修构图和删除多余元素，不更改身份 |

发现明显偏差后只做一次有依据的修正；保留初稿和修正版，不必把所有检查项都塞入修正提示。输入应明确分工：原照片=身份，初稿=本次编辑目标，文字规范=默认画风依据。仅在用户提供额外参考画时将其标为笔法来源。重复需要保留的脸型、年龄、现有配饰和表情，再指出要改的实际偏差。

例如初稿像水彩滤镜、嘴唇残留粉红时：

```text
Keep the source person's likeness, age, existing accessories and expression unchanged. The source photo defines identity; the written ink/ochre/paper specification defines style; the generated portrait is the edit target. Reduce soft skin modeling and continuous watercolor shading into a few deliberate matte ochre shadow planes and expressive black contours, leaving forehead center, nose bridge and central cheeks paper white. Remove pink/red from lips: use only ink, ochre and paper white. Keep exposed teeth, if present, paper white. Preserve clothing silhouette, simplify decorative patterns. No new accessories or text.
```

修正版仍不达标时具体说明剩余差异，不宣称完全复刻，不继续自动生图。对比两个技能时使用同一目标照片、同一工具、同一画幅和相同其他要求；记录各自参考图选择以及调用/修正次数。不同参考图与生成随机性会影响结果，一次样例不足以证明技能普遍更好。
