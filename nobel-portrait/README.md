# 诺贝尔肖像馆 · Nobel Portrait

将人物照片转绘为黑墨、金赭与暖白纸底的手绘肖像，并按需生成配套的单人物介绍网页。

技能 ID：`nobel-portrait`。界面名称：**诺贝尔肖像馆**。

本项目的原创代码、技能说明与网页模板采用 MIT 许可证。当前发布版本不附带第三方参考图片或截图，画风与页面布局由文字规范和原创模板确定；素材政策见 [第三方素材说明](THIRD_PARTY_ASSETS.md)。本项目是个人创作工具，与诺贝尔奖官方机构无隶属关系。

## 功能

| 模式 | 输入 | 输出 |
| --- | --- | --- |
| 肖像转绘 | 清晰单人照片 | 手绘肖像及实际生成提示词 |
| 肖像与介绍网页 | 照片、希望获得的奖项；可选人物资料 | 肖像、单人物网页、结构化资料及提示词 |
| 转换提示词 | 风格要求；可选照片 | 可用于图像工具的文字提示词 |

画风以有粗细变化的黑墨线、宽弧形发束、局部哑光金赭阴影和大面积纸白构成。人物照片负责长相、表情、发型与服装，文字规范负责笔法与配色。默认只需目标人物照片；用户也可另行提供可选风格图。默认目标为竖向 2:3、1024 × 1536 像素或更高，实际分辨率以生成结果为准。

网页采用白底、金色标题、居中页眉、细分隔线、左侧目录和右侧人物资料，支持窄屏纵向排列、页内导航及肖像下载。

## 环境要求

- 能加载技能、查看图片和操作本地文件的 Codex 环境。
- 图像转绘需要宿主环境提供图像生成或编辑工具，优先使用内置 `image_gen`。本仓库不附带图像模型，也不包含独立生图 API 客户端。
- 网页构建需要 Python 3；当前构建器已使用 Python 3.12 验证。
- PNG/JPG 导出需要 Pillow。仅保留输入图片原格式时可使用 `--keep-original`，无需 Pillow。

在执行网页构建的同一 Python 环境安装依赖：

```bash
python -m pip install Pillow
```

内置图像工具不可用时，技能会说明限制；安装 Python 或 Pillow 本身不能提供 AI 图像生成能力。

## 安装

### 从 GitHub 安装到本地 Codex

将本仓库的实际 GitHub 地址交给内置安装技能，例如：

```text
$skill-installer 从 https://github.com/Sunday12581/nobel-portrait
安装技能。技能位于仓库根目录，包含 SKILL.md，安装名称为 nobel-portrait。
```

把 `<Sunday12581>` 替换为仓库所有者。安装后若未出现在技能列表中，可重启 Codex。

### 手动安装到项目

下载仓库并将含有 `SKILL.md` 的完整目录命名为 `nobel-portrait`，放入目标项目的 `.agents/skills/`：

```text
your-project/
└── .agents/
    └── skills/
        └── nobel-portrait/
            ├── SKILL.md
            ├── agents/
            ├── assets/
            ├── references/
            └── scripts/
```

保留全部相对目录关系。技能发现与安装方式参见 [OpenAI 官方文档](https://learn.chatgpt.com/docs/build-skills)。该仓库提供独立技能源码；如需通过插件目录分发，可另行封装为插件。

## 调用示例

先附上人物照片，再输入请求。

**只生成肖像：**

```text
$nobel-portrait 将这张照片转换为黑墨金赭手绘肖像，
保留人物长相、表情、发型和姿势。
```

**生成肖像与介绍网页：**

```text
$nobel-portrait 将这张照片转换为诺贝尔风格肖像，并制作介绍网页。
我希望获得诺贝尔化学奖。
姓名：示例人物；出生：2000年；出生地：安徽，中国。
工作单位：示例能源材料研究院。
未提供的介绍信息请按创作情景补全。
```

**为已有肖像制作网页：**

```text
$nobel-portrait 使用这张已经生成的肖像制作人物介绍网页，
奖项设为诺贝尔物理学奖。
```

**只提供提示词：**

```text
$nobel-portrait 只提供黑墨金赭肖像转换提示词，不生成图片或网页。
```

## 人物资料与创作说明

制作网页时，照片或已有肖像、奖项为必需输入。姓名、年份、出生信息、单位、地址及获奖理由可由用户提供；缺失资料按创作需求补全，并记录在 `profile.json` 的 `invented_fields` 中。

技能默认在补写字段旁标注“创作设定”，并显示非官方记录说明。用户可以明确要求调整这些标记、肖像署名或页面布局，例如只保留一行“个人创作展示，非官方获奖记录。”；当前脚本没有独立的隐藏标记命令行开关，这类展示调整由执行技能的助手完成。真实人物档案应采用核实的信息。

## 网页输出与修改

```text
output-directory/
├── index.html            普通静态网页，与图片放在同一目录
├── standalone.html       图像及下载链接全部内嵌，可独立离线打开
├── portrait.png
├── portrait.jpg
├── profile.json          人物资料与补写字段记录
└── portrait-prompt.txt   由执行技能的助手保存的实际生成提示词
```

网页默认保存为本地文件。公网发布需另行指定，技能不会因生成网页而自动上传人物照片。

可以直接编辑 HTML 修改展示；编辑 `profile.json` 后则需要重新构建网页。构建器不监控 JSON，也不会自动刷新现有页面。

从仓库根目录运行：

```bash
python scripts/build_page.py --profile profile.json --portrait portrait.png --out output-v1
```

输入 JSON 的字段说明见 [references/page-and-data.md](references/page-and-data.md)。上述路径为示例，需要指向实际已准备好的资料和肖像。构建器只负责网页与格式导出，不推断人物信息、不生成肖像。输出目录必须不存在或为空；修改后使用新的目录名，例如 `output-v2`。转换会保留实际像素尺寸，不额外放大。

## 项目结构

```text
nobel-portrait/
├── README.md
├── LICENSE
├── THIRD_PARTY_ASSETS.md
├── .gitignore
├── SKILL.md
├── agents/openai.yaml
├── assets/page-template.html
├── references/
│   ├── portrait-style.md
│   ├── portrait-abstraction.md
│   ├── review-and-repair.md
│   └── page-and-data.md
└── scripts/build_page.py
```

## 示例与素材

本版本已移除三张肖像参考、一张示范原照和一张页面截图，不需要寻找或补齐这些图片。文字画风规范见 [references/portrait-style.md](references/portrait-style.md)，形体简化原则见 [references/portrait-abstraction.md](references/portrait-abstraction.md)，网页由 `assets/page-template.html` 构建。

去除图片参考后的画风控制依赖文字提示词，生成细节可能与有图参考的结果不同；保留人物辨识度与黑墨、金赭、纸白关系仍是验收重点。图像生成有随机性，本次资料清理不代表已重新生成或比较成图。

本开源准备包不包含使用者的个人证件照、个人介绍网页或实际任务输出。若为仓库增加效果示例，可使用自有或允许展示的输入图，并同时提供输入、生成结果、提示词及实际尺寸。

## 贡献

欢迎通过 Issue 描述问题或通过 Pull Request 改进技能说明、画风控制和网页模板。修改构建器时请验证资料字段、资源路径和离线网页；添加素材时请同时填写来源、权利人及许可依据。避免提交个人照片、本地绝对路径、密钥、生成缓存和任务输出。

## 许可证

[MIT License](LICENSE) 适用于本项目原创的技能说明、参考分析文本、UI 配置、Python 脚本和 HTML/CSS 模板。贡献者保留各自贡献的权利。

[THIRD_PARTY_ASSETS.md](THIRD_PARTY_ASSETS.md) 记录当前无随附第三方图片及后续素材政策。用户运行时提供的照片或风格图不因使用本技能而获得 MIT 授权。生成肖像的使用范围取决于输入素材、宿主图像服务及实际使用情景，软件许可证不等同于每张生成图片的许可。

后续增加公开示例或第三方素材时，请记录其来源及许可范围。许可证基础说明参见 [GitHub 官方文档](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)。
