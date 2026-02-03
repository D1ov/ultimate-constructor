# Output Styles Documentation

Configure Claude Code's response formatting and communication style.

## Overview

Output styles control how Claude formats responses in the terminal. Configure styles to match your preferences for verbosity, formatting, and communication patterns.

## Configuration

### Location
```
~/.claude/settings.json
```

### Basic Structure
```json
{
  "outputStyle": {
    "format": "markdown",
    "verbosity": "normal",
    "codeBlocks": true,
    "colors": true
  }
}
```

## Format Options

### Markdown (Default)
```json
{
  "format": "markdown"
}
```
- Headers, lists, code blocks
- Tables and emphasis
- Full formatting support

### Plain Text
```json
{
  "format": "plain"
}
```
- No markdown formatting
- Simple text output
- Useful for piping to other tools

### Minimal
```json
{
  "format": "minimal"
}
```
- Bare essentials
- No decorations
- Machine-readable output

## Verbosity Levels

### Verbose
```json
{
  "verbosity": "verbose"
}
```
- Detailed explanations
- Step-by-step reasoning
- Full context

### Normal (Default)
```json
{
  "verbosity": "normal"
}
```
- Balanced output
- Relevant details
- Standard communication

### Concise
```json
{
  "verbosity": "concise"
}
```
- Brief responses
- Essential information only
- Minimal explanation

### Terse
```json
{
  "verbosity": "terse"
}
```
- Extremely brief
- Commands and results only
- No elaboration

## Code Block Settings

### Enable Code Blocks
```json
{
  "codeBlocks": true
}
```
- Syntax highlighting
- Language tags
- Copy-friendly formatting

### Disable Code Blocks
```json
{
  "codeBlocks": false
}
```
- Inline code only
- No block formatting
- Simpler output

## Color Settings

### Enable Colors
```json
{
  "colors": true
}
```
- Syntax highlighting
- Status indicators
- Visual hierarchy

### Disable Colors
```json
{
  "colors": false
}
```
- Monochrome output
- Pipe-friendly
- Accessibility option

## Custom Styles

### Define Custom Style
```json
{
  "outputStyle": {
    "custom": {
      "codeLanguage": "typescript",
      "listStyle": "numbered",
      "headerLevel": 2,
      "maxLineLength": 80
    }
  }
}
```

### Style Presets

**Developer Mode:**
```json
{
  "outputStyle": {
    "format": "markdown",
    "verbosity": "concise",
    "codeBlocks": true,
    "showFilePaths": true,
    "showLineNumbers": true
  }
}
```

**Documentation Mode:**
```json
{
  "outputStyle": {
    "format": "markdown",
    "verbosity": "verbose",
    "codeBlocks": true,
    "includeExamples": true
  }
}
```

**CI/CD Mode:**
```json
{
  "outputStyle": {
    "format": "plain",
    "verbosity": "terse",
    "codeBlocks": false,
    "colors": false
  }
}
```

## Response Patterns

### Code-First
Prioritize code output, minimal explanation:
```json
{
  "responsePattern": "code-first"
}
```

### Explain-First
Explain approach before showing code:
```json
{
  "responsePattern": "explain-first"
}
```

### Interactive
Ask clarifying questions:
```json
{
  "responsePattern": "interactive"
}
```

## File References

### Show Full Paths
```json
{
  "filePaths": "full"
}
```
Output: `/home/user/project/src/file.ts`

### Show Relative Paths
```json
{
  "filePaths": "relative"
}
```
Output: `src/file.ts`

### Show Filename Only
```json
{
  "filePaths": "name"
}
```
Output: `file.ts`

## Error Formatting

### Verbose Errors
```json
{
  "errors": {
    "verbosity": "verbose",
    "showStack": true,
    "showContext": true
  }
}
```

### Concise Errors
```json
{
  "errors": {
    "verbosity": "concise",
    "showStack": false,
    "showContext": false
  }
}
```

## Progress Indicators

### Show Progress
```json
{
  "progress": {
    "show": true,
    "style": "spinner"
  }
}
```

### Hide Progress
```json
{
  "progress": {
    "show": false
  }
}
```

## Example Configurations

### Default
```json
{
  "outputStyle": {
    "format": "markdown",
    "verbosity": "normal",
    "codeBlocks": true,
    "colors": true,
    "filePaths": "relative"
  }
}
```

### Minimal Developer
```json
{
  "outputStyle": {
    "format": "markdown",
    "verbosity": "concise",
    "codeBlocks": true,
    "colors": true,
    "filePaths": "relative",
    "responsePattern": "code-first"
  }
}
```

### Verbose Teacher
```json
{
  "outputStyle": {
    "format": "markdown",
    "verbosity": "verbose",
    "codeBlocks": true,
    "colors": true,
    "includeExamples": true,
    "responsePattern": "explain-first"
  }
}
```

### CI Pipeline
```json
{
  "outputStyle": {
    "format": "plain",
    "verbosity": "terse",
    "codeBlocks": false,
    "colors": false,
    "progress": {"show": false}
  }
}
```

## CLI Overrides

Override settings via CLI flags:
```bash
# Verbose output
claude --verbose

# Quiet output
claude --quiet

# No colors
claude --no-color

# Plain format
claude --format plain
```

## Best Practices

1. **Match your workflow**: Use concise for experienced users, verbose for learning
2. **CI/CD**: Disable colors and use plain format for logs
3. **Documentation**: Use verbose with examples
4. **Debugging**: Enable full paths and line numbers
5. **Piping**: Use plain format without colors
