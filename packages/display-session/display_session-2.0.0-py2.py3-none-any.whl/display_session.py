import colorama.ansi as ca

__title__ = "display-session"
__version__ = "2.0.0"
__author__ = "Nicholas Lawrence"
__license__ = "MIT"
__copyright__ = "Copyright 2018-2019 Nicholas Lawrence"

_ALIGN_TEMPLATE = " {0:{fill}{align}{width}} "
_ALIGN_MAPPING = {"center": "^", "left": "<", "right": ">"}


def construct_ansi_dict():
    collected_colors = {}
    color_dict_mapping = {'FORE': ca.Fore, 'BACK': ca.Back, 'STYLE': ca.Style}

    for class_name, ansi_class in color_dict_mapping.items():
        for color_name, ansi in ansi_class.__dict__.items():
            breadcrumbed_name = f'{color_name}_{class_name}'.lower()
            collected_colors[breadcrumbed_name] = ansi

    return collected_colors


class _Pallette:
    __slots__ = tuple(construct_ansi_dict())


for style, ansi in construct_ansi_dict().items():
    setattr(_Pallette, style, ansi)


def header(msg, align="center", justify_char="_", width=100):
    f_header = _ALIGN_TEMPLATE.format(msg, fill=justify_char, align=_ALIGN_MAPPING[align], width=width)
    print(f_header)


def style_text(msg, styles):
    ansi_prefix = "".join([getattr(_Pallette, style) for style in styles])
    return "".join([ansi_prefix, msg, "\033[0m"])


class Display:

    def byline_colored_modules(self):
        return []

    def report(self, msg, style=None, byline_module_style=None):
        byline = self.__repr__()
        modules = self.byline_colored_modules()

        if modules:
            module_styles = byline_module_style or ["bright_style"]
            styled_modules = [style_text(item, module_styles) for item in modules]
            byline = byline.format(*styled_modules)

        if style:
            msg = style_text(msg, style)

        print(": ".join([byline, msg]))
