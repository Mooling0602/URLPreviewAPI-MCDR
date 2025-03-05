# URLPreviewAPI-MCDR
Preview the text or image content of the URLs in game chat.

This plugin need Minecraft: Java Edition client, click link to open browser is impossible to support Geyser!

## Usage
Execute `!!url <url>` in the game, and a formatted URL text will be sent to the game chat.
> All players can see it in the game client. If http prefix not added, 'https://' will be added as a prefix.

## Docs
If you want to use this plugin as an API to format url in chat messages, just do this: 
```python
from mcdreforged.api.all import *
from url_preview import RTextURL 

def main(server: PluginServerInterface):
    url = "https://example.com"
    rtext_url = RTextURL()
    url_text = rtext_url(url) # is a RText obj with formatted URL with previewed info.
    server.say("..." + url_text + "...") # just an example.
```
> Remember to add `url_preview` as a dependency in your plugin's meta file(mcdreforged.plugin.json).