# password-generator

CLI tool for generating passwords and passphrases.

## Installation

```bash
git clone git@github.com:deployfriday13/password-generator.git
cd password-generator
uv sync
```

## Usage

### Password

```bash
pw              # 15 characters, all charsets
pw 20           # 20 characters
pw --no-symbols # no special characters
pw -n 5         # generate 5 passwords
pw --no-copy    # print only, skip clipboard
```

### Passphrase

```bash
pwp                        # 6 words, delimiter "-"
pwp 4                      # 4 words
pwp --delimiter _          # custom delimiter
pwp -n 3                   # generate 3 passphrases
```

Flags can be combined:

```bash
pw 20 --no-symbols -n 5 --no-copy
```

## Config

On first run defaults are used. To override, create the config file:

- macOS / Linux: `~/.config/genpass/config.toml`
- Windows: `%APPDATA%\genpass\config.toml`

```toml
[password]
length = 20
uppercase = true
lowercase = true
digits = true
symbols = false

[phrase]
length = 4
delimiter = "_"
```

CLI arguments always override config values.
