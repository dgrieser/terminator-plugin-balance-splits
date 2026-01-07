# Terminator Balance Splits Plugin

Balance the sizes of split panes in the current Terminator tab. Works for both
horizontal and vertical splits and only activates when a split is present.

## Installation

```bash
mkdir -p ~/.config/terminator/plugins
cd ~/.config/terminator/plugins
wget --no-check-certificate https://github.com/dgrieser/terminator-plugin-balance-splits/raw/main/balance_splits.py
```

Then enable it in Terminator:

1. Open Terminator Preferences.
2. Go to the Plugins tab.
3. Check "Balance Splits".

## Usage

- Right-click inside a terminal and choose "Balance Splits".
- Or press `Ctrl+Shift+B` (default).

## Custom keybinding

You can override the default keybinding by adding this to your Terminator
config (`~/.config/terminator/config`):

```
[keybindings]
plugin_balance_splits = <Shift><Control>b
```
