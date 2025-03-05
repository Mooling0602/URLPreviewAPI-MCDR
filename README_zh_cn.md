# URLPreviewAPI-MCDR
在游戏聊天中预览 URL 的文本或图片内容。

一些特性无法支持通过Geyser连接的基岩版客户端，请使用Minecraft Java版游戏客户端以获得最佳体验！

## 使用方法
在游戏中执行 `!!url <url>`，格式化后的 URL 文本将发送到游戏聊天中。
> 所有玩家都可以在游戏客户端中看到它。如果没有添加 http 前缀，将自动添加 'https://' 作为前缀。

## 文档
如果你想使用此插件作为 API 在聊天消息中格式化 URL，只需这样做：
```python
from mcdreforged.api.all import *
from url_preview import RTextURL 

def main(server: PluginServerInterface):
    url = "https://example.com"
    rtext_url = RTextURL()
    url_text = rtext_url(url) # 是一个带有预览信息的格式化 URL 的 RText 对象。
    server.say("..." + url_text + "...") # 只是一个例子。
```
> 请记得在你的插件元数据(mcdreforged.plugin.json)中添加 `url_preview` 作为依赖项。