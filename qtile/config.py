import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = 'mod4'
terminal = guess_terminal('kitty')

keys = [
    # Move between windows
    Key([mod], 'Left', lazy.layout.left()),
    Key([mod], 'Right', lazy.layout.right()),
    Key([mod], 'Down', lazy.layout.down()),
    Key([mod], 'Up', lazy.layout.up()),

    # Move window position
    Key([mod, 'shift'], 'Left', lazy.layout.shuffle_left()),
    Key([mod, 'shift'], 'Right', lazy.layout.shuffle_right()),
    Key([mod, 'shift'], 'Down', lazy.layout.shuffle_down()),
    Key([mod, 'shift'], 'Up', lazy.layout.shuffle_up()),

    # Grow window size
    Key([mod, 'control'], 'Left', lazy.layout.grow_left()),
    Key([mod, 'control'], 'Right', lazy.layout.grow_right()),
    Key([mod, 'control'], 'Down', lazy.layout.grow_down()),
    Key([mod, 'control'], 'Up', lazy.layout.grow_up()),

    # Change to next window
    Key([mod], 'space', lazy.layout.next()),

    # Reset window sizes
    Key([mod], 'n', lazy.layout.normalize()),

    # Open terminal
    Key([mod], 'Return', lazy.spawn(terminal)),

    # Change between layouts
    Key([mod], 'Tab', lazy.next_layout()),

    # Close window
    Key([mod, 'shift'], 'q', lazy.window.kill()),

    # Reload config
    Key([mod, 'shift'], 'r', lazy.reload_config()),

    # Close qtile
    Key([mod, 'shift'], 'e', lazy.shutdown()),

    # Toggle Floating
    Key([mod, 'shift'], "t", lazy.window.toggle_floating()),

    # Open rofi
    Key([mod], 'x', lazy.spawn('rofi -show drun')),

    # Volume
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('pulseaudio-ctl up 1')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('pulseaudio-ctl down 1')),
    Key([], 'XF86AudioMute', lazy.spawn('pulseaudio-ctl mute')),
]

groups = [Group(i) for i in '123456789']

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
            ),
            Key(
                [mod, 'shift'],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
            ),
        ]
    )

layouts = [
    layout.Columns(
        border_normal='#282a36',
        border_focus='#bd93f9',
        border_width=4,
        margin=6
    ),
    layout.Max(),
]

widget_defaults = dict(
    font='FiraCode Nerd Font Mono',
    fontsize=18,
    padding=8,
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method='block',
                    borderwidth=12,
                    margin_x=0,
                    margin_y=3,
                    rounded=False,
                    this_current_screen_border='#bd93f9',
                    urgent_border='#ff5555'
                ),
                widget.Prompt(),
                widget.WindowName(),
                widget.Systray(),
                widget.Volume(
                    fmt='🔈{}',
                    foreground='#D8DEE9',
                    volume_down_command='pulseaudio-ctl down 1',
                    volume_up_command='pulseaudio-ctl up 1',
                ),
                widget.Backlight(
                    fmt='☀️ {}',
                    backlight_name='amdgpu_bl0',
                    foreground='#ffb86c'
                ),
                widget.Battery(
                    fmt='🔋 {}',
                    font='FiraCode Nerd Font Mono',
                    format='{char} {percent:2.0%}',
                    foreground='#50fa7b'
                ),
                widget.Clock(
                    fmt='📅 {}',
                    format='%d-%m-%Y',
                    foreground='#8be9fd'
                ),
                widget.Clock(
                    fmt='🕔 {}',
                    format='%a %I:%M %p',
                    foreground='#ff5555'
                ),
            ],
            32,
            background='#282a36',
            margin=6
        ),
    ),
]

mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),
        Match(wm_class='makebranch'),
        Match(wm_class='maketag'),
        Match(wm_class='ssh-askpass'),
        Match(title='branchdialog'),
        Match(title='pinentry'),
    ],
    border_normal='#282a36',
    border_focus='#bd93f9',
    border_width=4,
    margin=6
)
auto_fullscreen = True
focus_on_window_activation = 'smart'
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None

wmname = 'LG3D'


@hook.subscribe.startup_once
def start_once():
    home_path = os.path.expanduser('~')
    autostart_path = '/.config/qtile/scripts/autostart.sh'
    subprocess.call([home_path + autostart_path])
