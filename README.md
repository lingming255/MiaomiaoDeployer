# 妙妙部署小工具 (Miaomiao Deployer)

## 面向刚拿到新电脑，或者重装系统的用户，是一个通过图形化界面批量装指定软件的工具，不需要任何教程，开箱即用


基于 Python 和 PyQt6 的 Windows 环境自动化部署。一键生成 PowerShell 脚本来执行 Winget 安装和打开指定网页。

---

![alt text](https://youke1.picui.cn/s1/2025/10/23/68fa198ed9012.png)

## ✨ 功能特性

- **图形化界面**：使用 PyQt6 构建，直观易用。
- **高度自定义**：可以自由添加/删除/编辑软件安装任务和分组。
- **配置持久化**：所有配置保存在一个 `config.json` 文件中，方便迁移和备份。
- **自动化执行**：一键生成并以管理员权限运行 PowerShell 脚本，自动完成所有安装任务。
- **智能路径**：打包成 exe 后，配置文件会自动保存在 exe 旁边，便于携带。

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

**注**
使用Google Gemini辅助完成
