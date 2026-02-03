# Installation Guide

## Methods to Install Ultimate Constructor Plugin

### Method 1: --plugin-dir Flag (Recommended for Development)

Run Claude Code with `--plugin-dir` flag:

```bash
claude --plugin-dir "/path/to/ultimate-constructor"
```

**Advantages:**
- Works immediately without additional setup
- Plugin changes apply on restart
- Can load multiple plugins:

```bash
claude --plugin-dir "./plugin1" --plugin-dir "./plugin2"
```

### Method 2: settings.json Configuration

Add plugin path to settings file:

**For user (all projects):**
`~/.claude/settings.json`

**For project:**
`.claude/settings.json`

```json
{
  "plugins": {
    "ultimate-constructor": {
      "path": "/path/to/ultimate-constructor",
      "enabled": true
    }
  }
}
```

### Метод 3: Через marketplace (когда плагин опубликован)

```bash
# Добавить marketplace
/plugin marketplace add your-marketplace-url

# Установить плагин
/plugin install ultimate-constructor@marketplace-name
```

### Метод 4: Через интерактивную команду /plugin

В Claude Code выполните:
```
/plugin
```
Выберите "Add plugin from path" и укажите путь к плагину.

## Проверка установки

После установки выполните:

```
/help
```

Должны появиться команды:
- `/uc:create` - Создание компонентов
- `/uc:extract` - Извлечение паттернов
- `/uc:improve` - Улучшение компонентов
- `/uc:status` - Статистика

## Использование

### Создание нового скилла
```
/uc:create skill
```

### Создание агента
```
/uc:create agent my-agent
```

### Создание плагина
```
/uc:create plugin my-plugin
```

### Создание хуков
```
/uc:create hook
```

## Troubleshooting

### Плагин не загружается

1. **Проверьте путь** - путь должен указывать на директорию с `.claude-plugin/plugin.json`

2. **Перезапустите Claude Code**:
```bash
# Выйти из текущей сессии
exit

# Запустить снова с плагином
claude --plugin-dir "путь/к/плагину"
```

3. **Включите отладку**:
```bash
claude --debug --plugin-dir "путь/к/плагину"
```

### Команды не появляются

1. Проверьте, что директория `commands/` находится в корне плагина (не внутри `.claude-plugin/`)

2. Проверьте структуру:
```
ultimate-constructor/
├── .claude-plugin/
│   └── plugin.json      ← Только манифест здесь
├── commands/            ← В корне плагина!
├── agents/              ← В корне плагина!
└── skills/              ← В корне плагина!
```

### Ошибки валидации

Используйте команду валидации:
```
/plugin validate
```

## Требования

- Claude Code версии 1.0.33 или выше
- Для проверки версии: `claude --version`

## Обновление

Для обновления плагина:
1. Получите новую версию
2. Перезапустите Claude Code
