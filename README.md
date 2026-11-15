# indie game assets combo for free

一个用于独立游戏制作的 Codex skill。按需求在十个资源站中寻找免费素材，核对具体文件的许可与兼容性，并给出获取路径。遇到搜索游戏素材、导入资源或替换占位素材的任务时，已安装的技能可由 Codex 自动选择。

| 网站 | 主要资源 |
| --- | --- |
| Kenney | 2D 瓦片、UI、低多边形 3D、游戏音效 |
| OpenGameArt | 2D/3D、概念图、纹理、音效、音乐 |
| itch.io | 像素美术、瓦片、UI、字体、动画、音频 |
| Unity Asset Store | Unity 插件、模板、模型、特效、音频 |
| Fab | 3D 模型、环境、材质、动画、引擎插件 |
| Godot Asset Store / Asset Library | Godot 插件、脚本、工具、模板、演示项目 |
| Poly Haven | CC0 PBR 材质、HDRI、3D 模型 |
| Mixamo | 人形角色、自动绑骨、动捕动画 |
| Freesound | 音效、环境声、拟音 |
| Pixabay | 音乐、音效、图片、插画、视频 |

## 安装到 Codex

在 Codex 中发送以下指令。

```text
用 $skill-installer 安装 https://github.com/vincentcrc/indie-game-assets-combo-for-free/tree/main/skills/indie-game-assets-combo-for-free
```

手动安装可将 [技能目录](skills/indie-game-assets-combo-for-free) 连同其子目录复制到用户技能目录。若当前会话未列出新技能，重启 Codex 后再试。可显式调用。

```text
用 $indie-game-assets-combo-for-free 给 Godot 4.4 项目找可商用的像素草地瓦片和 UI 点击音。
```

## 脚本

在仓库根目录运行。使用 Python 3.8+ 标准库。

```sh
python3 skills/indie-game-assets-combo-for-free/scripts/find_assets.py route 2d "pixel grass tiles"
python3 skills/indie-game-assets-combo-for-free/scripts/find_assets.py poly-search materials "weathered brick"
python3 skills/indie-game-assets-combo-for-free/scripts/find_assets.py godot-search "inventory" --version 4.7
```

`route` 生成搜索入口。Poly Haven 和 Godot 的新旧资源库使用公开 API 实时返回 JSON。Unity Asset Store 提供手动路径。其他来源通过官方页面查找或获取，部分下载需要平台账号。素材随各自原始许可发布，本仓库仅包含技能与脚本。详见[站点与许可指南](skills/indie-game-assets-combo-for-free/references/sources.md)。
