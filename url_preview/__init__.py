from typing import Optional
from mcdreforged.api.all import *
from url_preview.paser import parse_url_info


builder = SimpleCommandBuilder()
psi = ServerInterface.psi()


class RTextURL:
    def __init__(self, preference: Optional[dict] = None):
        """
        :param url: The URL to be previewed.
        :param preference: A dictionary that contains the preference of the URL preview, if not provided, the default style will be applied to the rtext result.

        NOTE: about how to set preference, see this link.
        """
        self.preference = preference  # will  implement in the future.

    def __call__(self, url):
        if not url.startswith("http"):
            url = "https://" + url
        parsed_info = (
            parse_url_info(url, locale="zh-CN,zh;q=0.9")
            if psi.get_mcdr_language() == "zh_cn"
            else parse_url_info(url)
        )
        parsed_error = parsed_info.get("error")
        if parsed_error is not None:
            psi.logger.error(f"Error parsing URL: {parsed_error}")
            return None
        url_title = parsed_info.get("title")
        url_summary = parsed_info.get("summary")
        # url_image = Not implemented yet, will also support ChatImage in the future.
        for i in [url_title, url_summary]:
            if i is None:
                return None
        # url_title_format = f'[§b{url_title}§r]'
        # url_link_format = f'(§a{url}§r)'
        prefix = "Description"
        if psi.get_mcdr_language() == "zh_cn":
            prefix = "摘要"
        url_title_rtext = (
            "["
            + RText(text=url_title, color=RColor.aqua).h(f"{prefix}: {url_summary}")
            + "]"
        )
        url_link_rtext = (
            "("
            + RText(text=url, color=RColor.green).set_click_event(RAction.open_url, url)
            + ")"
        )
        url_rtext = RTextList(url_title_rtext, url_link_rtext)
        return url_rtext


def on_load(server: PluginServerInterface, prev_module):
    builder.arg("url", Text)
    builder.register(server)
    server.logger.info("URLPreviewAPI loaded successfully!")


@new_thread("URLParser")
@builder.command("!!url <url>")
def on_test(src: CommandSource, ctx: CommandContext):
    if src.is_console:
        psi.logger.warning(
            "Some style features can't work in console, please view it in the JE client."
        )
    url = ctx["url"]
    rtext_url = RTextURL()
    rtext = rtext_url(url)
    psi.broadcast(rtext) if rtext is not None else psi.say("§cError parsing URL.")
