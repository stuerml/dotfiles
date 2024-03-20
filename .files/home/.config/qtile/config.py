# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List
from libqtile import bar, hook, layout, qtile
from libqtile.config import Click, Drag, DropDown, Group, Key, Match, Screen, ScratchPad
from libqtile.lazy import lazy
from libqtile.log_utils import logger

from qtile_extras.widget.decorations import RectDecoration, BorderDecoration
from qtile_extras import widget

import subprocess
import os

from themes import CatppuccinMocha
from user_profile import check_profile

mod = "mod4"
launcher = "rofi_launcher"
powermenu = "rofi_powermenu"

if check_profile() == "work":
    terminal = "kitty"
    browser = "chrome"
    browser_launch = "chrome --app"
else:
    terminal = "alacritty"
    browser = "brave"
    browser_launch = "brave --app"

font = "CaskaydiaCove Nerd Font"
wallpaper = os.path.expanduser("~/.local/share/wallpapers/wallpaper.jpg")

theme = {
    "background": CatppuccinMocha["crust"],
    "background2": CatppuccinMocha["surface0"],
    "foreground": CatppuccinMocha["text"],
    "foreground2": CatppuccinMocha["subtext0"],
    "primary": CatppuccinMocha["teal"],
    "secondary": CatppuccinMocha["mauve"],
}

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "control"], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "v", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.spawn(powermenu), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn(launcher), desc="Spawn a command using a prompt widget"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

dropdown_config = {
    "y": 0.008,
    "width": 0.8,
    "height": 0.6,
    "on_focus_lost_hide": True,
    "warp_pointer": True,
}

scratchpad = ScratchPad("scratch", dropdowns=[
    DropDown(
        "terminal",
        terminal,
        **dropdown_config),
    DropDown(
        "htop",
        terminal + " htop",
        **dropdown_config),
    DropDown(
        "cal",
        terminal + " calcure",
        **dropdown_config),
    ],
    single=True,
)

keys.extend(
    [
        Key([mod], "space", lazy.group["scratch"].dropdown_toggle("terminal")),
        Key([mod, "control"], "space", lazy.group["scratch"].dropdown_toggle("htop")),
        Key([mod, "mod1"], "space", lazy.group["scratch"].dropdown_toggle("cal")),
    ]
)

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

groups.append(scratchpad)

layout_defaults = {
    "border_width": 2,
    "border_focus": theme["primary"],
    "border_normal": theme["background2"],
    "margin": 8,
}


layouts = [
    layout.MonadTall(**layout_defaults, name="Monad"),
]

widget_defaults = dict(
    font=font,
    fontsize=16,
    padding=12,
    foreground=theme["foreground"]
)

bar_defaults = {
    "size": 28, 
    "border_width": 4, 
    "background": theme["background"],
    "border_color": theme["background"],
    "margin": [5, 5, 0, 5]
}


extension_defaults = widget_defaults.copy()

def border(color: str, size=2):
    return {
        "decoration": [
            BorderDecoration(
                colour = color,
                border_width= [0, 0, size, 0]
            )
        ]
    }

def open_calendar():
    qtile.groups_map["scratch"].dropdowns["cal"].toggle()
    

def get_bar_widgets():
    return [
        widget.Spacer(length=8),
        widget.TextBox(
            text="󱓞",
            foreground=theme["primary"],
            mouse_callbacks = {'Button1': lambda: qtile.spawn(launcher)},
        ),
        widget.Spacer(length=8),
        widget.CurrentLayoutIcon(
            foreground=theme["primary"],
            padding=7,
            scale=0.6,
            **border(theme["primary"])
        ),
        widget.Spacer(length=8),
        widget.GroupBox(
            active=theme["secondary"],
            this_current_screen_border=theme["primary"],
            borderwidth=2,
            hide_unused=False,
            highlight_method="block",
            inactive= theme["foreground2"],
            rounded=True,
            margin_x=0,
            margin_y=3,
            padding_x=5,
            padding_y=8,
            urgent_alert_method='line',
            visible_groups = ["1", "2", "3", "4", "5", "6"],
            **border(theme["primary"])
        ),
        widget.Spacer(),
        widget.WindowName(
            width=bar.CALCULATED,
            **border(theme["foreground"]),
            empty_group_string=""
        ),
        widget.Spacer(),
        widget.DF(
            format='  {r:.0f}%',
            visible_on_warn=False,
            foreground=theme["primary"],
            **border(theme["primary"]),
        ),
        widget.Spacer(length=8),        
        widget.Memory(
            format='󰍛  {MemPercent}%',
            foreground=theme["primary"],
            **border(theme["primary"])
        ),
        widget.Spacer(length=8),        
        widget.CPU(
            format='  {load_percent}%',
            foreground=theme["primary"],
            **border(theme["primary"])
        ),
        widget.Spacer(length=8),
        widget.PulseVolume(
            volume_app = 'pavucontrol',
            foreground = theme["foreground2"],
            emoji=True,
            emoji_list=['󰝟', '󰕿', '󰖀', '󰕾'],
            fontsize=20,
            **border(theme["background2"])
        ),
        widget.PulseVolume(
            volume_app = 'pavucontrol',
            foreground = theme["foreground2"],
            padding = 0,
            **border(theme["background2"])
        ),
        widget.Spacer(length=12, **border(theme["primary"])),
        widget.Spacer(length=8),
        widget.Clock(
            format="󰔛  %I:%M",
            mouse_callbacks = {"Button1": lambda: open_calendar()},
            foreground = theme["secondary"],
            **border(theme["secondary"])
        ),
        widget.Spacer(length=8),
        widget.TextBox(
            text="",
            foreground=theme["secondary"],
            mouse_callbacks = {'Button1': lambda: qtile.spawn(powermenu)},
        ),
        widget.Spacer(length=8),
    ]

screens = [
    Screen(
        top = bar.Bar(
            get_bar_widgets(),
            **bar_defaults
        ),
        wallpaper=os.path.join(os.path.expanduser("~"), wallpaper),
        wallpaper_mode="fill",
    ),
    Screen(
        top = bar.Bar(
            get_bar_widgets(),
            **bar_defaults
        ),
        wallpaper=os.path.join(os.path.expanduser("~"), wallpaper),
        wallpaper_mode="fill"
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

floating_defaults = {
    "border_focus": theme["secondary"],
    "border_normal": theme["primary"],
    "border_width": 2, 
    "max_border_width": 0,
    "fullscreen_border_width": 0,
}
    

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    **floating_defaults,
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


# Needed when started as GNOME session
# @hook.subscribe.startup
# def dbus_register():
#     id = os.environ.get("DESKTOP_AUTOSTART_ID")
#     if not id:
#         return
    
#     subprocess.Popen(['dbus-send',
#                   '--session',
#                   '--print-reply',
#                   '--dest=org.gnome.SessionManager',
#                   '/org/gnome/SessionManager',
#                   'org.gnome.SessionManager.RegisterClient',
#                   'string:qtile',
#                   'string:' + id])
    
@hook.subscribe.startup_once
def autostart():
    profile = check_profile()

    processes: List[List[str]] = []
    if profile == "home":
        processes = [
            ["picom", "-b"],
            ["setxkbmap", "de"]
        ]
    elif profile == "work":
        processes = [
            ["picom", "--experimental-backends", "-b"],
            ["setxkbmap", "de"]
        ]

    for p in processes:
        subprocess.Popen(p)

