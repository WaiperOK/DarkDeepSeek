"""
Модуль форматирования результатов для my-pentest-gpt
Создает красивый Markdown вывод с подсветкой синтаксиса
"""
from typing import Optional, Dict, Any
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

class MarkdownFormatter:
    """English docstring"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def format_exploit_report(self, code: str, task_type: str = "exploit",
                            reasoning: Optional[str] = None, metadata: Optional[Dict] = None) -> str:
        """English docstring"""

        extracted_code = self._create_code_section(code)

        if extracted_code:
            extracted_code = self._fix_code_formatting(extracted_code)

        sections = []

        sections.append(f"# 🎯 EXPLOIT REPORT - {task_type.upper()}")
        sections.append(f"**Время генерации:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if metadata:
            sections.append(f"**Модель:** {metadata.get('model', 'Unknown')}")
            sections.append(f"**Температура:** {metadata.get('temperature', 'Unknown')}")
            sections.append(f"**Токены:** {metadata.get('max_tokens', 'Unknown')}")

        sections.append("")

        if reasoning:
            short_reasoning = self._shorten_reasoning(reasoning)
            sections.append("## 🧠 Reasoning")
            sections.append(short_reasoning)
            sections.append("")

        non_code_content = self._remove_code_blocks(code)
        if non_code_content.strip():
            sections.append("## 📝 Description")
            sections.append(non_code_content.strip())
            sections.append("")

        if extracted_code:
            language = self._detect_language(extracted_code)
            sections.append("## 💻 Code")
            sections.append(f"```{language}")
            sections.append(extracted_code.strip())
            sections.append("```")
            sections.append("")

        sections.append("## ⚠️ Disclaimer")
        sections.append("This code is intended exclusively for educational purposes and security testing.")
        sections.append("Use for malicious purposes is prohibited.")

        return "\n".join(sections)

    def _shorten_reasoning(self, reasoning: str) -> str:
        """English docstring"""
        if not reasoning:
            return ""

        clean_reasoning = reasoning.replace('<think>', '').replace('</think>', '').strip()

        sentences = clean_reasoning.split('. ')
        if len(sentences) > 3:
            short_sentences = sentences[:3]
            return '. '.join(short_sentences) + '.'

        if len(clean_reasoning) > 200:
            return clean_reasoning[:200] + "..."

        return clean_reasoning

    def _fix_code_formatting(self, code: str) -> str:
        """English docstring"""
        if not code:
            return ""

        code = code.strip()

        code = re.sub(r'\s+', ' ', code)
        code = re.sub(r';\s*([a-zA-Z])', r';\n\1', code)
        code = re.sub(r'{\s*([a-zA-Z])', r'{\n\1', code)
        code = re.sub(r'}\s*([a-zA-Z])', r'}\n\1', code)

        return code

    def _aggressive_code_formatting(self, code: str) -> str:
        """English docstring"""

        formatted = self._fix_code_formatting(code)

        formatted = self._force_html_formatting(formatted)

        formatted = self._force_js_formatting(formatted)

        return formatted

    def _force_html_formatting(self, code: str) -> str:
        """English docstring"""

        html_patterns = [
            (r'<(\w+)([^>]*)>', r'<\1\2>\n'),
            (r'</(\w+)>', r'\n</\1>\n'),
            (r'><', r'>\n<'),
            (r'<head>', r'<head>\n'),
            (r'</head>', r'\n</head>\n'),
            (r'<body([^>]*)>', r'<body\1>\n'),
            (r'</body>', r'\n</body>\n'),
            (r'<script([^>]*)>', r'<script\1>\n'),
            (r'</script>', r'\n</script>\n'),
            (r'<style([^>]*)>', r'<style\1>\n'),
            (r'</style>', r'\n</style>\n'),
            (r'<div([^>]*)>', r'<div\1>\n'),
            (r'</div>', r'\n</div>\n'),
        ]

        for pattern, replacement in html_patterns:
            code = re.sub(pattern, replacement, code, flags=re.IGNORECASE)

        return code

    def _force_js_formatting(self, code: str) -> str:
        """English docstring"""

        js_patterns = [
            (r';\s*([a-zA-Z_$])', r';\n\1'),
            (r'{\s*([a-zA-Z_$])', r'{\n    \1'),
            (r'}\s*([a-zA-Z_$])', r'}\n\1'),
            (r'function\s+([a-zA-Z_$]\w*)', r'\nfunction \1'),
            (r'const\s+([a-zA-Z_$]\w*)', r'\nconst \1'),
            (r'let\s+([a-zA-Z_$]\w*)', r'\nlet \1'),
            (r'var\s+([a-zA-Z_$]\w*)', r'\nvar \1'),
            (r'if\s*\(', r'\nif ('),
            (r'for\s*\(', r'\nfor ('),
            (r'while\s*\(', r'\nwhile ('),
            (r'try\s*{', r'\ntry {'),
            (r'catch\s*\(', r'\ncatch ('),
            (r'}else{', r'} else {'),
            (r'}else\s+if\s*\(', r'} else if ('),
        ]

        for pattern, replacement in js_patterns:
            code = re.sub(pattern, replacement, code)

        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted_lines.append('')
                continue

            if stripped.startswith('}') or stripped.startswith('</'):
                indent_level = max(0, indent_level - 1)

            indented_line = '    ' * indent_level + stripped
            formatted_lines.append(indented_line)

            if stripped.endswith('{') or stripped.endswith('>') and '</' not in stripped:
                indent_level += 1

        return '\n'.join(formatted_lines)

    def _create_header(self, task_type: str = "exploit", metadata: Optional[Dict[str, Any]] = None) -> str:
        """English docstring"""
        task_names = {
            "exploit": "EXPLOIT GENERATION",
            "analyze": "VULNERABILITY ANALYSIS", 
            "reverse": "REVERSE ENGINEERING",
            "network": "NETWORK SECURITY",
            "web": "WEB SECURITY"
        }

        title = task_names.get(task_type, "CYBERSECURITY")

        if metadata and metadata.get("target"):
            title += f" - {metadata['target']}"

        header = f"# {title}\n"
        header += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"

        return header

    def _create_metadata_section(self, metadata: Dict[str, Any]) -> str:
        """English docstring"""
        section = "## 📊 Metadata\n"

        info_items = []
        if metadata.get("model"):
            info_items.append(f"**Model:** {metadata['model']}")
        if metadata.get("template"):
            info_items.append(f"**Template:** {metadata['template']}")
        if metadata.get("target"):
            info_items.append(f"**Target:** {metadata['target']}")
        if metadata.get("temperature"):
            info_items.append(f"**Temperature:** {metadata['temperature']}")

        section += "\n".join(info_items)
        return section

    def _create_code_section(self, code: str) -> str:
        """English docstring"""
        if not code.strip():
            return ""


        extracted_code = None

        import re
        code_blocks = re.findall(r'```(?:\w+)?\s*\n(.*?)\n```', code, re.DOTALL | re.IGNORECASE)
        if code_blocks:
            extracted_code = '\n'.join(code_blocks)

        if not extracted_code:
            code_blocks = re.findall(r'```\s*\n(.*?)\n```', code, re.DOTALL)
            if code_blocks:
                extracted_code = '\n'.join(code_blocks)

        if not extracted_code:
            markers = [
                r'(?i)(?:код|code)[:：]\s*\n(.*?)(?=\n\n|\n[А-Яа-яA-Za-z]|\Z)',
                r'(?i)(?:эксплойт|exploit)[:：]\s*\n(.*?)(?=\n\n|\n[А-Яа-яA-Za-z]|\Z)',
                r'(?i)(?:скрипт|script)[:：]\s*\n(.*?)(?=\n\n|\n[А-Яа-яA-Za-z]|\Z)',
                r'(?i)(?:команда|command)[:：]\s*\n(.*?)(?=\n\n|\n[А-Яа-яA-Za-z]|\Z)',
                r'(?i)(?:payload|пейлоад)[:：]\s*\n(.*?)(?=\n\n|\n[А-Яа-яA-Za-z]|\Z)',
                r'(?i)(?:инструмент|tool)[:：]\s*\n(.*?)(?=\n\n|\n[А-Яа-яA-Za-z]|\Z)'
            ]

            for marker in markers:
                matches = re.findall(marker, code, re.DOTALL)
                if matches:
                    extracted_code = '\n'.join(matches)
                    break

        if not extracted_code:
            deepseek_patterns = [
                r'(?i)(?:вот код|here\'s the code|code example)[:：]?\s*\n(.*?)(?=\n\n|\n[А-Яа-я]{20,}|\Z)',
                r'(?i)(?:пример кода|code sample)[:：]?\s*\n(.*?)(?=\n\n|\n[А-Яа-я]{20,}|\Z)',
                r'(?i)(?:решение|solution)[:：]?\s*\n(.*?)(?=\n\n|\n[А-Яа-я]{20,}|\Z)',
                r'(?i)(?:poc|proof of concept)[:：]?\s*\n(.*?)(?=\n\n|\n[А-Яа-я]{20,}|\Z)'
            ]

            for pattern in deepseek_patterns:
                matches = re.findall(pattern, code, re.DOTALL)
                if matches:
                    extracted_code = '\n'.join(matches)
                    break

        if not extracted_code:
            code_lines = []
            for line in code.split('\n'):
                line = line.strip()
                if line and self._is_code_line(line):
                    code_lines.append(line)

            if code_lines:
                extracted_code = '\n'.join(code_lines)

        if not extracted_code:
            extracted_code = self._extract_technical_content(code)

        if not extracted_code or len(extracted_code.strip()) < 10:
            potential_code = []
            for line in code.split('\n'):
                line = line.strip()
                if line and any(char in line for char in ['()', '{}', '[]', '<>', '==', '!=', '->', '=>', '&&', '||']):
                    potential_code.append(line)

            if potential_code:
                extracted_code = '\n'.join(potential_code)
            else:
                return ""

        extracted_code = extracted_code.strip()

        language = self._detect_language(extracted_code)

        section = "## 💻 Code\n"
        section += f"```{language}\n{extracted_code}\n```\n"

        return section

    def _is_code_line(self, line: str) -> bool:
        """English docstring"""
        import re

        if len(line) < 3:
            return False

        if re.match(r'^[А-Яа-яA-Za-z\s.,!?]+$', line) and len(line) > 20:
            return False

        code_keywords = [
            'import ', 'from ', 'def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'except:',
            'print(', 'len(', 'str(', 'int(', '__name__', '__main__', 'self.',

            'function ', 'var ', 'let ', 'const ', 'console.log', 'document.', 'window.',
            'alert(', 'setTimeout', 'getElementById', '.innerHTML', '.value',

            'curl ', 'wget ', 'echo ', 'grep ', 'sed ', 'awk ', 'cat ', 'ls ', 'cd ',
            'chmod ', 'chown ', 'sudo ', 'apt-get', 'yum ', 'pip ', 'npm ',

            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER',
            'UNION', 'WHERE', 'ORDER BY', 'GROUP BY', 'OR 1=1', "' OR '",

            '<script>', '<html>', '<body>', '<div>', '<span>', '<input>',
            '</script>', '</html>', '</body>', '</div>',

            'alert(', 'prompt(', 'confirm(', 'eval(', 'setTimeout(',
            'document.cookie', 'window.location', 'localStorage',

            'nmap ', 'sqlmap', 'metasploit', 'payload', 'exploit',
            'netcat', 'nc -', 'telnet ', '/etc/passwd', '/bin/sh',

            ' = ', ' == ', ' != ', ' >= ', ' <= ', ' && ', ' || ',
            ' += ', ' -= ', ' *= ', ' /= ', '=>', '->'
        ]

        line_lower = line.lower()
        for keyword in code_keywords:
            if keyword.lower() in line_lower:
                return True

        code_patterns = [
            r'^[a-zA-Z_][a-zA-Z0-9_]*\s*[=\(]',
            r'^\s*[#//]',
            r'^\s*<[a-zA-Z]',
            r'[{}\[\]();]',
            r'https?://',
            r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            r"['\"][^'\"]*['\"]",
            r'[A-Z0-9]{16,}',
        ]

        for pattern in code_patterns:
            if re.search(pattern, line):
                return True

        return False

    def _extract_technical_content(self, text: str) -> str:
        """English docstring"""
        import re

        patterns = [
            r'https?://[^\s]+',
            r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            r'[A-Z0-9]{32,}',
            r'[a-fA-F0-9]{8,}',
            r'\$[a-zA-Z_][a-zA-Z0-9_]*',
            r'[a-zA-Z_][a-zA-Z0-9_]*\(\)',
            r'--[a-zA-Z-]+',
            r'-[a-zA-Z]',
        ]

        technical_content = []
        for line in text.split('\n'):
            for pattern in patterns:
                if re.search(pattern, line):
                    technical_content.append(line.strip())
                    break

        return '\n'.join(technical_content) if technical_content else ""

    def _detect_language(self, code: str) -> str:
        """English docstring"""
        code_lower = code.lower()

        if any(keyword in code_lower for keyword in ['import ', 'def ', 'print(', 'if __name__']):
            return "python"

        if any(keyword in code_lower for keyword in ['#!/bin/bash', '#!/bin/sh', 'curl ', 'wget ', 'grep ']):
            return "bash"

        if any(keyword in code_lower for keyword in ['function ', 'var ', 'let ', 'const ', 'console.log']):
            return "javascript"

        if any(keyword in code_lower for keyword in ['select ', 'insert ', 'update ', 'delete ', 'union ']):
            return "sql"

        if any(keyword in code_lower for keyword in ['powershell', 'invoke-', 'get-', 'set-']):
            return "powershell"

        return "text"

    def _create_reasoning_section(self, reasoning: str) -> str:
        """English docstring"""
        section = "## 🧠 Reasoning\n"

        formatted_reasoning = self._format_reasoning_text(reasoning)
        section += formatted_reasoning

        return section

    def _format_reasoning_text(self, text: str) -> str:
        """English docstring"""
        text = re.sub(r'\n\s*\n', '\n\n', text.strip())

        lines = text.split('\n')
        formatted_lines = []

        for line in lines:
            line = line.strip()
            if line.startswith(('1.', '2.', '3.', '4.', '5.')):
                formatted_lines.append(f"**{line}**")
            elif line.startswith('-') or line.startswith('*'):
                formatted_lines.append(f"  {line}")
            else:
                formatted_lines.append(line)

        return '\n'.join(formatted_lines)

    def _remove_code_blocks(self, text: str) -> str:
        """Remove code blocks from text and return only non-code content"""
        import re
        
        # Remove triple backtick code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        
        # Remove single backtick inline code
        text = re.sub(r'`[^`]*`', '', text)
        
        # Remove lines that look like code
        lines = text.split('\n')
        non_code_lines = []
        
        for line in lines:
            if not self._is_code_line(line.strip()):
                non_code_lines.append(line)
        
        return '\n'.join(non_code_lines)

def format_markdown(code: str,
                   task_type: str = "exploit",
                   reasoning: Optional[str] = None,
                   metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Быстрое форматирование в Markdown

    Args:
        code: Код для форматирования
        task_type: Type задачи
        reasoning: Рассуждения
        metadata: Метаданные

    Returns:
        Отформатированный Markdown
    """
    formatter = MarkdownFormatter()
    return formatter.format_exploit_report(code, task_type, reasoning, metadata)

def create_simple_code_block(code: str, language: str = "python") -> str:
    """English docstring"""
    return f"```{language}\n{code.strip()}\n```"

def add_security_comment(code: str) -> str:
    """English docstring"""
    comment = "# WARNING: This code is for educational purposes only\n"
    return comment + code

if __name__ == "__main__":
    test_code = """
import requests

def test_sql_injection(url):
    payload = "' OR 1=1 --"
    response = requests.post(url, data={'username': payload})
    return response.text
"""

    formatter = MarkdownFormatter()
    result = formatter.format_exploit_report(
        code=test_code,
        task_type="exploit",
        metadata={"target": "SQL Injection", "model": "DeepSeek-R1-8B"}
    )

    print(result)
