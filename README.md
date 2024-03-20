# dotfiles

## install

*To symlink all dotfiles into you configuration dir run:*
```bash
python3 dotfiles.py --files
```

> <b>⚠️ Warning<b> <br>
> Make sure to backup your files before running the install command.

*Switch between profiles by using the `--profile` flag:*
```bash
python3 dotfiles.py --profile [home, work]
```

## dependencies

- qtile
- qtile-extras
- picom
- [kitty](https://github.com/kovidgoyal/kitty)
- [rofi](https://github.com/davatorium/rofi)
- [dunst](https://github.com/dunst-project/dunst)
- [calcure](https://github.com/anufrievroman/calcure/tree/main)

> <b>🛈 Hint<b> <br>
> `qtile` may require additional packages for the bar
> such as `pulsectl-asyncio` and `dbus-next`.
>