# 肖像视觉规范与提示词

## 默认依据与可选参考

本技能不附带参考图片。默认只输入用户当前人物照片，通过下列文字规范控制画风，不要求额外上传风格图。

照片决定身份特征；若用户另行提供画风图，只借鉴笔触、留白和配色，不复制其中人物的脸、配饰、服装或签名。默认提示词按单张目标照片编写，不能描述不存在的第二、第三张图片。

形体概括原则见 [portrait-abstraction.md](portrait-abstraction.md)，用于区分身份结构保留与绘画细节简化。

## 视觉要点

暖米白纤维纸底（约 `#F4F1E9`），近黑墨色（约 `#15130F`），不均匀赭金/黄土色（约 `#B8933A`）；色值是视觉锚点，并非校色结果。轻微毛边、干刷断笔与纸面颗粒；五官形体准确，但笔触简练。头发顺着发型用束状黑色刷痕和纸白飞白表现，而非描绘每根发丝。

表达密度应低于源照片：把细密发丝合并成少数宽弧形墨带，宽发束的整体方向先于其中纹理；不要用满头细碎裂纹模拟干刷。用较明确的墨线交代眼睑、鼻孔、鼻翼、唇缘、下颌和耳廓，其他面部体积留给纸白和金赭笔触。保留必要的年龄线索，可省略细碎皱纹；不把皮肤完全描成照片纹理，也不把人物美化年轻。

默认只使用纸白、黑墨、金赭，包括嘴唇；避免源照片的粉红唇色、彩色领带和连续肤色混入成图。面部大部分是未着色纸白，额头中央、鼻梁和双颊中心尤其要留白。金色以短弧线、窄带与少量不规则色块落在眼周、鼻侧、脸侧、唇部、下颌和颈部，不全脸涂金，不作柔光喷枪或大面积水彩晕染。色块内部相对完整，边缘才有适量干刷；不要用散点和斑驳皮肤替代块面。金色为哑光、有轻微刷痕的颜料，不作立体金属高光。虹膜可使用小面积金赭，搭配黑色瞳孔与纸白眼白；保留原有眼形、眼距和目光，不变成发光眼睛，不强行放大眼睛。用户指定原眼色时优先遵从。

唇部用正向形状指令：将上下唇概括成黑色轮廓内的平整哑光金赭形状，保留嘴形与微笑，露齿处留纸白。身份保真指五官结构与表情，不要求保留原照的肤色、唇色或局部照片质感；只写“不要红色”仍可能残留原唇色。

纸面纤维纹理应跨背景、脸部留白和衣服留白一致出现，不能仅集中在嘴周和脸颊制造毛孔或胡茬。金赭颜料内部的细微材质与皮肤颗粒不是同一种效果。

衣服保留源照片的服装类别与轮廓，用少数墨线交代领口、翻领和必要褶皱，内部大片纸白；通常省略繁复花纹，往下自然收笔。微笑与露齿是身份特征：保留嘴形和牙齿留白，不改成严肃闭嘴。

避免照片加滤镜、铅笔灰阶素描、密集排线铜版画、油画体积光、动漫美化、3D 金属皮肤、华丽背景和复制画家签名。

## 英文提示词

按真实输入次序替换编号，补充源照片可见特征；不把未提供的身份信息写进外貌要求。

```text
Use case: style-transfer / identity-preserving portrait edit.
Asset: one original illustrated laureate-style portrait; a profile-page asset only when requested.

INPUT ROLES:
Image 1 is the target person's photograph and the ONLY source of identity, facial structure, visible age, hairstyle, glasses (if present), clothing and expression. Preserve recognizable structural relationships, not pixel-for-pixel photographic detail.
By default, Image 1 is the only image input. The following written specification defines the drawing style.

PRIMARY REQUEST:
Transform the person in Image 1 into an original hand-drawn laureate-inspired black-ink and ochre-gold portrait following the written specification below. Keep the person clearly recognizable. Preserve face shape, eye spacing, nose, mouth, jaw, hairline and distinctive visible features.

ABSTRACTION STRATEGY:
Redraw from scratch as economical brush drawing rather than tracing a photograph and coloring it gold. Reduce the number of depicted marks: merge fine hair into a small set of broad sweeping ink ribbons; use selective confident contours for eyelids, nostrils, nose wings, lip edges, jaw and ears. Keep facial structural proportions, recognizable expression and age cues, allowing natural hand-drawn contour simplification. Do not enlarge eyes, reshape every jaw or force symmetry as a universal style rule.
The three materials have distinct jobs: ink describes structure; ochre shapes are deliberately chosen arcs, narrow ribbons and a few contiguous shadow masses; untouched paper carries most of the facial planes. Do not recreate every photographic light gradient, pore or wrinkle.

MEDIUM AND PALETTE:
Use only warm off-white paper, near-black brush ink and matte ochre-gold pigment unless the user explicitly requests another color. This includes lips and clothing: no pink/red lips or colored photographic skin tones. Expressive thin-to-thick contours with natural pauses and occasional broken bristle edges. Hair is broad directional brush ribbons and large black masses alternating with broad exposed-paper gaps; do not render individual photographic strands or thousands of tiny scratches.
Most facial planes are untouched paper white; keep the forehead center, nose bridge and central cheeks clear. Sparse ochre arcs and narrow bands around eyes, nose sides, cheek edges and lips, with a few larger contiguous ochre shapes under the jaw and on the neck. Relatively solid pigment interiors with restrained grain and hand-brushed edges, not all-over mottled skin. Paper grain stays subtle and consistent across background, face and clothing, never concentrated into stubble or pores. Small matte ochre irises with black pupils and white sclera are acceptable; preserve original eye shape and gaze, no glowing or enlarged eyes. If original iris color is requested, preserve it.
No continuous flesh-color gradients, soft airbrushing, broad watercolor washes or photographic skin modeling. Preserve facial anatomy and apparent age, not every skin-texture detail.
Keep source clothing category, collar and lapel silhouettes. Use sparse black outlines and broad unpainted paper; omit decorative fabric patterns unless requested. Preserve the original smile and exposed teeth as paper-white shapes.
Redraw the upper and lower lips as deliberate flat matte ochre shapes enclosed by economical black contours, keeping the source mouth shape and smile. Exposed teeth are untouched paper white. Identity preservation means structural likeness and expression, not retaining photographic skin or lip colors.

COMPOSITION:
Use the user's requested aspect ratio and background when specified. Otherwise vertical 2:3, centered head-and-shoulders to chest bust, complete hair silhouette and comfortable paper margins, opaque warm paper background. Follow source pose, gaze and expression. Aim for 1024 x 1536 pixels or higher if supported. Recognizable realistic facial proportions, economical hand-drawn marks. No unnecessary medals or ceremonial clothing.

CONSTRAINTS:
Exactly one person. Identity and apparent age first, ink/ochre/white-paper relationships second, framing and paper texture third. No text, captions, artist signature, watermarks, medal, seal or official logo. Do not add glasses, facial hair or different clothing unless requested. Do not mimic reference signatures.
Avoid photographic filters, smooth skin gradients, pores, pink lips, all-over yellow tint, metallic gold skin, vector-uniform outlines, dense engraving cross-hatching, cartoon exaggeration, fantasy eyes and ornate backgrounds.
```

该模板用于单张目标照片的初次生成。用户提供额外风格图时，按实际次序补充其角色，例如“Image 2 is STYLE ONLY; do not transfer this person's face or accessories.”；没有额外图片时不添加该句。修正时源照片为身份、当前成图为编辑目标，画风仍由文字规范或用户明确提供的可选风格图确定。检查与修正按 [review-and-repair.md](review-and-repair.md) 执行。

在 `portrait-prompt.txt` 记录最终提示词、输入角色、生成方式、实际像素；不包含源照片 base64 或个人文件系统路径。将工具返回的真实图像复制进交付目录再构建网页。
