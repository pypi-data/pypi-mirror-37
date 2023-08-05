# -*- coding:utf-8 -*-
from django.utils.html import format_html


__all__ = ['color_tag']


def color_tag(text, color, bold=False, italic=False, tag='span'):
    opts = {
        "text": text,
        "color": color,
        "tag": tag,
        "bold": " font-weight: bold;" if bold else "",
        "italic": " font-style: italic;" if italic else "",
    }
    return format_html(u'<{tag} style="color: {color};{bold}{italic}">{text}</{tag}>', **opts)
