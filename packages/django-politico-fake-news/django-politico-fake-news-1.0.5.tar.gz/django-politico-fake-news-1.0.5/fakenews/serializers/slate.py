class BaseSlateSerializer:
    def __init__(self, slate_state, tags={}):
        self.slate_state = slate_state

        self.tags = {
            "bold": "b",
            "blockquote": "blockquote",
            "bulleted-list": "ul",
            "figure": "figure",
            "heading-three": "h3",
            "iframe": "iframe",
            "italic": "em",
            "image": "img",
            "link": "a",
            "list-item": "li",
            "numbered-list": "ol",
            "paragraph": "p",
            "small": "small",
        }

        for label, tag in tags.items():
            self.tags[label] = tag

        self.flags = []

    def render(self):
        """
        Renders an entire slate state instance.
        Param requires a "document" key with "nodes".
        """
        html = ""
        for node in self.slate_state["document"]["nodes"]:
            html += self.render_node(node)

        html = self.handle_flags(html)

        return html

    def render_node(self, node):
        """
        Renders an individual slate node.
        If the node has nodes of its own, it calls itself to render them.
        """
        html = ""

        if node["object"] == "block" or node["object"] == "inline":
            if hasattr(self, "render_{}".format(node["type"])):
                render_func = getattr(self, "render_{}".format(node["type"]))
                html = render_func(node)
            elif "nodes" in node:
                for inner_node in node["nodes"]:
                    html += self.render_node(inner_node)
                html = self.wrap(node["type"], html, node["data"])

        elif node["object"] == "text":
            if "leaves" in node:
                for leaf in node["leaves"]:
                    html += self.render_leaf(leaf)

        return html

    def render_leaf(self, leaf):
        """
        Renders an individual slate leaf
        (i.e. a block of text).
        """
        html = leaf["text"]

        for mark in leaf["marks"]:
            html = self.render_mark(mark, html)

        return html

    def render_mark(self, mark, html):
        """
        Renders a slate mark block.
        (e.g. <b>, <em>, <small>).
        """
        return self.wrap(mark["type"], html, mark["data"])

    def activate_flag(self, flag):
        """
        Activate a flag to be handled after procesing.
        """
        if flag not in self.flags:
            self.flags.append(flag)

    def handle_flags(self, html):
        """
        Handles plugin flags if they are activated and exist.
        """
        for flag in self.flags:
            if hasattr(self, "handle_flag_{}".format(flag)):
                flag_func = getattr(self, "handle_flag_{}".format(flag))
                html = flag_func(html)

        return html

    def wrap(self, type="", html="", data={}):
        """
        Wrap "html" code within a tag of a given "type" with the attributes
        listed in "data".
        """
        tag = self.tags[type]
        props = ""

        for prop, value in data.items():
            if isinstance(prop, bool) and prop:
                props += " {}".format(prop)
            else:
                props += ' {}="{}"'.format(prop, value)

        return "<{tag}{props}>{html}</{tag}>".format(
            tag=tag, props=props, html=html
        )


class CodePlugin:
    def render_code(self, node):
        """
        Render embed code that should be passed through.
        """
        return self.wrap("figure", node["data"]["code"])


class IFramePlugin:
    def render_iframe(self, node):
        """
        Render embed code within an iframe.
        """
        data = {"srcdoc": node["data"]["code"].replace('"', "&quot;")}

        iframe = self.wrap("iframe", "", data)
        figure = self.wrap("figure", iframe, {"class": "code-embed"})
        return figure


class ImagePlugin:
    def render_image(self, node):
        """
        Render an image.
        """
        return self.wrap("image", "", node["data"]["img"])


class TwitterPlugin:
    def render_tweet(self, node):
        """
        Render a Tweet embed with the appropriate render script.
        """
        self.activate_flag("tweet")
        return node["data"]["html"]

    def handle_flag_tweet(self, html):
        script_tag = '<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'  # noqa
        html = html + script_tag

        return html


class YouTubePlugin:
    def render_youtube(self, node):
        """
        Render a YouTube embed.
        """
        return self.wrap("figure", node["data"]["html"], {"class": "yt-embed"})


class SlateSerializer(
    BaseSlateSerializer,
    CodePlugin,
    IFramePlugin,
    ImagePlugin,
    TwitterPlugin,
    YouTubePlugin,
):
    pass
