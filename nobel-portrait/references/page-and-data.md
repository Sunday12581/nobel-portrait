# 网页布局、资料字段与构建

模板为 `assets/page-template.html`。布局由模板和下面的文字规范确定，无需参考截图或抓取在线页面。

白底、金色姓名和奖项标题、居中页眉、细线；宽屏约 1000 px，左侧目录，右侧姓名、“人物资料 / Facts”、肖像和介绍。手机纵向排列，肖像不裁剪、不拉伸。仅一人一页。页眉写 `NOBEL PORTRAIT`，不复制官方标志、版权署名、画家签名或虚构官方个人页面 URL。顶部标“创作获奖情景”，页脚说明非官方记录；补写字段旁显示“创作设定”。导航使用本页锚点，下载对应真实图片，不访问 CDN 或字体服务器。

## profile.json

模型根据用户输入与创作补全生成；脚本不推断人物或编写理由。以下只是字段示例，不能当作下一位用户的资料：

```json
{
  "language": "zh",
  "name": "获奖者",
  "prize": "诺贝尔物理学奖",
  "year": 2026,
  "birth": "1988年6月",
  "birthplace": "杭州，中国",
  "affiliation": "星桥量子研究院",
  "affiliation_address": "上海，中国",
  "motivation": "因提出在常温条件下稳定操控量子信息的新方法，为可扩展量子网络奠定了基础。",
  "prize_share": "1/1",
  "portrait_credit": "AI 生成肖像 · 用户照片转绘",
  "invented_fields": ["year", "birth", "birthplace", "affiliation", "affiliation_address", "motivation", "prize_share"]
}
```

- `language` 为 `zh` 或 `en`，默认 `zh`；英文版资料也需模型写为英文，脚本仅翻译界面。
- `name`、`prize`、`birth`、`birthplace`、`affiliation`、`affiliation_address`、`motivation` 为必需非空字符串，保留用户用词，不接收 HTML。
- `year` 为 1–9999 的整数或数字字符串。用户未给时取当前用户时区年份并记为补写。
- `invented_fields` 必须为列表，逐字段列出实际补写内容；支持上述字段加 `year`、`prize_share`。单位名/地址和出生年月/出生地分别追踪。
- `prize_share` 可选，默认 `1/1` 并自动记为补写。`portrait_credit` 可选；AI 生成时用默认署名，参考图演示则写“用户提供的画风参考，非新生成肖像”，不能伪造官方署名。
- 支持用户明确提出的自创奖项，作为创作设定展示。

## 构建

使用现有 Python；转换依赖仅为 Pillow，没有框架或 API 依赖。

```text
python "<skill-dir>/scripts/build_page.py" --profile "<profile-path>" --portrait "<generated-image-path>" --out "<new-output-directory>"
```

生成 `index.html`（同目录资源）、`standalone.html`（图像及下载资源全部内嵌）、`portrait.png`、`portrait.jpg`（质量95）、规范化的 `profile.json`。不缩放像素，转换图不携带原始 EXIF。目录需不存在或为空，防止覆盖。

Pillow 不可用时可加 `--keep-original`，保留原格式并生成网页；如实报告未完成的格式转换，不通过改扩展名冒充 PNG/JPG。脚本不上传、不发布，不复制人物原照片。`portrait-prompt.txt` 由执行技能的模型另行保存。
