
# Miaomiao Deployer

[中文版](README.md)

A lightweight, portable, and GUI-based tool for automating software installation on Windows. Designed for users setting up a new PC or reinstalling their system. No tutorials needed, just unpack and run.

Based on Python and PyQt6, this tool generates and executes PowerShell scripts to streamline installations via Winget and by opening specific download pages.

![Screenshot](https://github.com/lingming255/MiaomiaoDeployer/raw/main/screenshot.png)

## ✨ Features

*   **Graphical User Interface**: Clean, intuitive, and straightforward.
*   **Highly Customizable**: Freely add, delete, or edit software installation tasks and groups.
*   **Automated Execution**: Supports a mix of installation methods, including `Winget` and navigating to web pages. Support for local installers is planned.
*   **Persistent Configuration**: Set up your software list once, and it's saved forever in the `config.json` file.
*   **Smart & Portable**: When bundled into a single `.exe`, the `config.json` file is managed alongside it, making it perfect for carrying on a USB drive.

## 🚀 Getting Started

1.  Go to the **[Releases](https.github.com/lingming255/MiaomiaoDeployer/releases)** page.
2.  Download the latest `.zip` archive (e.g., `MiaomiaoDeployer-v1.0.0.zip`).
3.  Unzip the downloaded file.
4.  Double-click `MiaomiaoDeployer.exe` to run the application.

## 🛠️ How to Configure

The application's logic is controlled by the `config.json` file. You can edit it manually to batch-add your software list. Here is the structure:

```json
{
  "software_groups": [
    {
      "group_name": "Web Browsers",
      "apps": [
        {
          "name": "Google Chrome",
          "type": "winget",
          "id_or_url": "Google.Chrome",
          "args": "--silent"
        }
      ]
    },
    {
      "group_name": "Development Tools",
      "apps": [
        {
          "name": "Visual Studio Code",
          "type": "winget",
          "id_or_url": "Microsoft.VisualStudioCode",
          "args": "--scope machine"
        },
        {
          "name": "Git",
          "type": "winget",
          "id_or_url": "Git.Git",
          "args": ""
        }
      ]
    },
    {
      "group_name": "NVIDIA Drivers (Manual)",
      "apps": [
        {
          "name": "NVIDIA Driver Download",
          "type": "web",
          "id_or_url": "https://www.nvidia.com/Download/index.aspx",
          "args": ""
        }
      ]
    }
  ]
}
```

*   `type`: Can be `winget` or `web`.
    *   `winget`: Uses the Windows Package Manager to install the software.
    *   `web`: Opens the specified URL in your default browser.
*   `id_or_url`:
    *   For `winget`, this is the Package Identifier (e.g., `Google.Chrome`). You can find this using the `winget search <AppName>` command.
    *   For `web`, this is the full URL of the download page.
*   `args`: Optional command-line arguments, primarily for `winget` installations (e.g., `--silent`, `--scope machine`).

## 🛣️ Roadmap

*   [ ] Search for the fastest download mirror/CDN.
*   [ ] Implement a real-time search feature for `Winget` packages within the app.
*   [ ] Improve detection and execution for local installers.
*   [ ] General bug fixes and performance improvements.

## ⚠️ Current Limitations

*   The tool does not yet include a built-in search feature for packages. Users currently need to find package IDs manually using the `winget search` command or by visiting official sources.
