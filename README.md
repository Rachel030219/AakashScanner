# AakashScanner
F**k off, Aakash.

[AakashScanner](https://telegram.me/Rachel_bot)

### How to use

#### 0. Install pyTelegramBotAPI

Go to [Getting started](https://github.com/eternnoir/pyTelegramBotAPI#getting-started)

#### 1. Change TOKEN

Replace `<TOKEN>` with your own.

#### 2. RUN

```shell
python aakashscanner.py
```

#### 3. That's all

### Database file format

```
type posibility_value regexp
```

#### `type`

Defines where the rule is used.

0. `name` - When a new member joins
1. `text` - When anyone's message content includes
2. `equal_text` - When anyone's message content equals

#### `posibility_value`

Defines the possibility added when triggered in integer.

#### `regexp`

Defines the text used to trigger. Use `,` to separate multi conditions.