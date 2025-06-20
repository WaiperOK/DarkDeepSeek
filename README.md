# 🔥 DarkDeepSeek - Elite AI Cybersecurity Platform

<div align="center">
  <img src="DarkDeepSeek.png" alt="DarkDeepSeek Logo" width="200" height="200">
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![DeepSeek](https://img.shields.io/badge/AI-DeepSeek--R1-red.svg)](https://github.com/deepseek-ai)
  [![Ollama](https://img.shields.io/badge/Local-Ollama-orange.svg)](https://ollama.ai/)
</div>

## 🚀 Overview

**DarkDeepSeek** is an advanced AI-powered cybersecurity platform that combines cutting-edge AI reasoning with comprehensive security testing capabilities. Built on DeepSeek-R1's revolutionary Chain-of-Thought technology, it provides both educational cybersecurity tools and unrestricted AI chat functionality.

### ✨ Key Features

- 🧠 **Advanced AI Reasoning** - DeepSeek-R1 with Chain-of-Thought processing
- 🎯 **20+ Exploit Categories** - XSS, SQL Injection, SSRF, RCE, and more
- 💬 **Dual Chat Modes** - Cybersecurity-focused and unrestricted conversation
- 🎨 **Retro Terminal UI** - Matrix-style interface with customizable themes
- 🔧 **Local AI Processing** - Complete privacy with Ollama integration
- 📋 **Template System** - Customizable exploit templates and prompts
- 🎓 **LoRA Training** - Fine-tune models with your own data
- 🌐 **Multilingual** - English and Russian interface support

## 🛡️ Cybersecurity Arsenal

### Exploit Generation Categories

| Category | Description | Complexity | Examples |
|----------|-------------|------------|----------|
| 🔥 **XSS Exploits** | Cross-Site Scripting attacks | ⭐⭐⭐ | Reflected, Stored, DOM |
| 💉 **SQL Injection** | Database attack vectors | ⭐⭐⭐⭐ | Union, Blind, Time-based |
| 🔓 **Authentication Bypass** | Login system exploits | ⭐⭐⭐⭐⭐ | JWT, OAuth, 2FA |
| 📁 **File Upload Exploits** | Malicious file upload | ⭐⭐⭐⭐ | PHP, ASP, JSP |
| 🌐 **SSRF & XXE** | Server-side attacks | ⭐⭐⭐⭐ | AWS, Internal, XML |
| 📊 **LFI/RFI Exploits** | File inclusion attacks | ⭐⭐⭐ | PHP, Log, Wrapper |
| 💥 **Buffer Overflow** | Memory corruption | ⭐⭐⭐⭐⭐ | Stack, Heap, ROP |
| 🔐 **Cryptographic Attacks** | Encryption weaknesses | ⭐⭐⭐⭐⭐ | RSA, AES, Hash |
| 🌍 **CSRF & SSRF** | Request forgery | ⭐⭐ | POST, GET, JSON |
| 🏃 **Race Conditions** | Timing attacks | ⭐⭐⭐⭐ | File, DB, Memory |

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/WaiperOK/DarkDeepS.git
cd DarkDeepS

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

### With Ollama (Recommended)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Auto-install DeepSeek model
python install_ollama_auto.py

# Launch DarkDeepSeek
python run.py
```

### Docker Deployment

```bash
# Build and run
docker-compose up --build
```

## 💬 Chat System

### Cybersecurity Mode (Prompts 1-7)
- **Web Security Expert** - XSS, CSRF, injection attacks
- **Network Penetration** - Network protocols and exploits  
- **Malware Analysis** - Reverse engineering and analysis
- **Social Engineering** - Human-based attack vectors
- **Mobile Security** - Android/iOS application testing
- **Cloud Exploits** - AWS, Azure, GCP vulnerabilities
- **AI/ML Attacks** - Adversarial and model poisoning

### Normal Chat Mode (Prompts 8-14)
- **Helpful Assistant** - General purpose AI helper
- **Coding Assistant** - Programming and development
- **Creative Writer** - Content creation and writing
- **Teacher** - Educational support and tutoring
- **Business Consultant** - Strategy and analysis
- **Casual Chat** - Friendly conversation
- **Unrestricted Chat** - No limitations or censorship

## 🎨 Visual Customization

### Built-in Themes
- 🟢 **Classic Hacker** - Traditional green-on-black
- 🟣 **Cyberpunk** - Neon purple and cyan
- 🔴 **Matrix** - Green digital rain aesthetic
- 🟡 **Retro Amber** - Warm amber terminal glow
- 🔵 **Dark Blue** - Cool blue professional

### Retro Effects
- ⌨️ **Typewriter Mode** - Character-by-character typing
- ⚡ **Glitch Effects** - Digital text distortion
- 👁️ **Cursor Animation** - Blinking terminal cursor
- 🔊 **Sound Effects** - ASCII beeps and alerts
- 📺 **CRT Scanlines** - Old monitor simulation
- 📡 **Background Noise** - Static interference

## 🛠️ Advanced Features

### Model Training (LoRA)
Fine-tune AI models with your own cybersecurity data:

```json
{"messages": [
  {"role": "user", "content": "How to detect SQL injection?"},
  {"role": "assistant", "content": "SQL injection detection methods..."}
]}
```

### Template System
Create custom exploit templates:

```json
{
  "name": "Custom XSS",
  "category": "web_security", 
  "content": "<script>{payload}</script>",
  "variables": ["payload"],
  "examples": ["alert('XSS')", "document.cookie"]
}
```

### Secret Commands
Discover hidden features:
- `matrix` - Matrix rain effect
- `hacker` - ASCII hacker art  
- `glitch` - Digital glitch demo
- `bios` - Retro BIOS startup
- `modem` - Dial-up connection sounds
- `manifest` - The Hacker Manifesto (1986)

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Linux, macOS
- **Python**: 3.8 or higher
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space

### Recommended Setup
- **RAM**: 16GB+ for large models
- **GPU**: NVIDIA GPU with CUDA (optional)
- **Storage**: SSD for better performance
- **Network**: Stable internet for model downloads

## 🔧 Configuration

### Settings File (`visual_settings.json`)
```json
{
  "primary_color": "bright_green",
  "secondary_color": "green",
  "accent_color": "bright_yellow", 
  "console_width": 120,
  "language": "en",
  "retro_effects": {
    "typewriter": true,
    "glitch": false,
    "cursor_blink": true
  }
}
```

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Add** tests if applicable
5. **Submit** a pull request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/your-username/DarkDeepS.git
cd DarkDeepS

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**DarkDeepSeek** is designed for **educational purposes and authorized security testing only**. 

- ✅ **Authorized penetration testing**
- ✅ **Security research and education**  
- ✅ **Vulnerability assessment on owned systems**
- ❌ **Unauthorized access to systems**
- ❌ **Malicious activities or attacks**
- ❌ **Violation of laws or regulations**

Users are responsible for ensuring compliance with all applicable laws and regulations.

## 🙏 Acknowledgments

- **[DeepSeek](https://github.com/deepseek-ai)** - Revolutionary R1 reasoning model
- **[Ollama](https://ollama.ai/)** - Local AI model infrastructure
- **[Rich](https://github.com/Textualize/rich)** - Beautiful terminal interfaces
- **Python Community** - Amazing open-source ecosystem

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/WaiperOK/DarkDeepS/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/WaiperOK/DarkDeepS/discussions)
- 📧 **Contact**: Create an issue for direct communication

## 🚀 What's Next?

- 🔄 Additional AI model integrations (GPT-4, Claude, Llama)
- 🎨 Advanced visual effects and animations
- 📱 Web interface for remote access
- 🔌 Plugin system for custom modules
- 📊 Analytics dashboard and reporting
- 🌐 Multi-language support expansion

---

<div align="center">
  
**⭐ Star this project if you find it useful! ⭐**

*Built with ❤️ for the cybersecurity community*

**Elite Cybersecurity Platform by [WaiperOK](https://github.com/WaiperOK)**

</div> 
