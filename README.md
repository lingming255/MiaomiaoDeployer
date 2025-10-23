# 妙妙部署小工具 (Miaomiao Deployer)

## 面向刚拿到新电脑，或者重装系统的用户，是一个通过图形化界面批量装指定软件的工具，不需要任何教程，开箱即用


基于 Python 和 PyQt6 的 Windows 环境自动化部署。一键生成 PowerShell 脚本来执行 Winget 安装和打开指定网页。

---

![alt text](https://youke1.picui.cn/s1/2025/10/23/68fa198ed9012.png)

## ✨ 功能特性

- **图形化界面**：逻辑清晰，功能直接。
- **高度自定义**：可以自由添加/删除/编辑软件安装任务和分组。
- **永久存档**：一次配置，永久使用，保存在 `config.json` 文件中。
- **自动化执行**：混合使用 Winget、指定下载网页、甚至本地安装包。
- **智能路径**：打包成 exe 后，配置文件会自动保存在 exe 旁边，便于携带。
- **目前的缺点**：没法主动搜索软件，依赖用户自己查找winget的官方包名并填写，我提供的config.json不够全面。

## 🚀 如何使用

1.  前往 [Releases 页面](https://github.com/待定/待定/releases)。
2.  下载最新的 `MiaomiaoDeployer.zip` 文件。
3.  解压后，双击运行 `MiaomiaoDeployer.exe` 即可。

## 🛠️ 对于开发者

本项目使用 Python 3 和 PyQt6 编写。
还没测试自动安装本地安装包的部分，之后准备加上自动识别同文件夹下的所有安装包的功能

**克隆仓库:**
```bash  
git clone https://github.com/lingming255/MiaomiaoDeployer
cd MiaomiaoDeployer
```
**注**
使用Google Gemini辅助完成
