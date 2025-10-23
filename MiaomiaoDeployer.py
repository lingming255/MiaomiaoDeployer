import sys
import os
import json
import subprocess
import copy
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QTreeWidget, QTreeWidgetItem, QDialog, QLineEdit, QComboBox,
    QFormLayout, QDialogButtonBox, QMessageBox, QMenu, QStatusBar, QFileDialog
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

# ------------------------------
# 配置文件与数据 (保持不变)
# ------------------------------
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
DEFAULT_CONFIG_DATA = {
    "核心开发与设计套件": [
        {"id": "Microsoft.VisualStudioCode", "name": "Visual Studio Code", "type": "winget", "checked": True, "custom_args": "--scope machine", "notes": "代码编辑器。"},
        {"id": "Git.Git", "name": "Git", "type": "winget", "checked": True, "custom_args": "", "notes": "版本控制系统。"},
    ],
    "常用工具与浏览器": [
        # --- 【错误修正】---
        # 将 "custom_args" 和 "notes" 之间的冒号 : 改为逗号 ,
        {"id": "Google.Chrome", "name": "Google Chrome", "type": "winget", "checked": True, "custom_args": "--silent", "notes": "网页浏览器。"},
        {"id": "Tencent.WeChat", "name": "微信", "type": "winget", "checked": True, "custom_args": "", "notes": "社交软件。"},
    ],
    "需要手动操作的任务": [
        # 为 web 类型的任务补充缺失的字段，保持数据结构一致
        {"id": "", "name": "NVIDIA 显卡驱动 (GFE)", "type": "web", "checked": False, "custom_args": "", "url": "https://www.nvidia.cn/geforce/geforce-experience/download/", "notes": "将为您打开驱动下载页面，建议手动安装。"},
    ]
}



# ------------------------------
# 最终安装脚本执行线程 (极大简化)
# ------------------------------
class Worker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, script_path):
        super().__init__()
        self.script_path = script_path
        self.proc = None

    def run(self):
        self.progress.emit("ℹ️ 正在请求管理员权限以启动安装脚本...")
        self.progress.emit("请在弹出的新 PowerShell 窗口中查看详细安装过程和日志。")
        
        cmd_list = [
            "powershell", "-Command",
            f"Start-Process powershell -Verb RunAs -ArgumentList '-ExecutionPolicy Bypass -File \"{self.script_path}\"'"
        ]
        try:
            # 我们只负责启动它，不关心它的输出，因为它会在新窗口独立运行
            self.proc = subprocess.Popen(cmd_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.proc.wait() # 等待启动器进程结束
            
            if self.proc.returncode != 0:
                self.progress.emit(f"❌ 启动器进程返回错误码: {self.proc.returncode}。可能是UAC被拒绝。")
                self.finished.emit(self.proc.returncode)
            else:
                self.progress.emit("✅ 脚本执行窗口已成功启动。")
                self.finished.emit(0)
        except FileNotFoundError:
            self.progress.emit("❌ 严重错误: 找不到 'powershell' 命令。")
            self.finished.emit(1)
        except Exception as e:
            self.progress.emit(f"❌ 执行最终脚本时发生未知错误: {e}")
            self.finished.emit(1)

# ------------------------------
# 主界面
# ------------------------------
# ------------------------------
# 主界面 (包含所有方法的完整版本)
# ------------------------------
class AppInstaller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("妙妙部署小工具 v6.1 (完整版)")
        self.resize(800, 600)
        self.worker = None
        self._build_ui()
        self.load_config_and_populate_tree() # 这个调用现在会找到对应的方法

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        top_bar = QHBoxLayout()
        add_group_btn = QPushButton("➕ 添加分组")
        add_task_btn = QPushButton("➕ 添加任务")
        remove_btn = QPushButton("➖ 删除选中")
        save_btn = QPushButton("💾 保存配置")
        add_group_btn.clicked.connect(self.add_group)
        add_task_btn.clicked.connect(self.add_task)
        remove_btn.clicked.connect(self.remove_item)
        save_btn.clicked.connect(self.save_config)
        top_bar.addWidget(add_group_btn)
        top_bar.addWidget(add_task_btn)
        top_bar.addWidget(remove_btn)
        top_bar.addStretch(1)
        top_bar.addWidget(save_btn)
        layout.addLayout(top_bar)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["任务名称", "类型", "ID/URL/Path", "自定义参数", "说明"])
        self.tree.setColumnWidth(0, 220); self.tree.setColumnWidth(1, 80); self.tree.setColumnWidth(2, 150); self.tree.setColumnWidth(3, 150)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.open_context_menu)
        self.tree.itemDoubleClicked.connect(self.edit_item)
        layout.addWidget(self.tree)

        self.log = QTextEdit(readOnly=True)
        self.log.setStyleSheet("background-color: #2b2b2b; color: #f0f0f0; font-family: Consolas, monospace;")
        self.log.setMaximumHeight(150)
        
        self.run_btn = QPushButton("🚀 生成在线安装脚本并执行")
        self.run_btn.setStyleSheet("font-size: 14px; padding: 8px;")
        self.run_btn.clicked.connect(self.run_tasks)
        
        layout.addWidget(self.log)
        layout.addWidget(self.run_btn)
        self.setStatusBar(QStatusBar())

# 在 AppInstaller 类中，找到 run_tasks 方法并替换它

# 在 AppInstaller 类中，找到 run_tasks 方法并完整替换为以下内容

# 在 AppInstaller 类中，找到 run_tasks 方法并完整替换为以下内容

    def run_tasks(self):
        selected_tasks = []
        for i in range(self.tree.topLevelItemCount()):
            group_item = self.tree.topLevelItem(i)
            for j in range(group_item.childCount()):
                task_item = group_item.child(j)
                if task_item.checkState(0) == Qt.CheckState.Checked:
                    selected_tasks.append(task_item.data(0, Qt.ItemDataRole.UserRole))
        
        if not selected_tasks:
            QMessageBox.information(self, "提示", "未选择任何任务。")
            return

        self.log.clear()
        self.log.append("🚀 开始生成在线安装脚本...")

        winget_tasks = [t for t in selected_tasks if t.get('type') == 'winget']
        web_tasks = [t for t in selected_tasks if t.get('type') == 'web']

        lines = [
            '# 妙妙部署小工具 - 在线安装脚本 v6.6 (The Final Truth)',
            'Write-Host "==================================================" -ForegroundColor Cyan',
            'Write-Host "🚀 开始执行在线安装任务..." -ForegroundColor Cyan',
            'Write-Host "==================================================" -ForegroundColor Cyan\n'
        ]

        if winget_tasks:
            lines.append('Write-Host "--- 正在使用 Winget 安装软件 ---" -ForegroundColor Yellow')
            for task in winget_tasks:
                task_id = task.get("id")
                args = task.get('custom_args', '')
                
                # --- 【v6.6 最终修正】---
                # 使用最简单且正确的 <query> 格式，不再添加任何可能导致问题的 winget 参数。
                # 正确的 ID 和参数将从修复后的 config.json 中读取。
                command = f'winget install "{task_id}" {args}'
                
                lines.append(f'\nWrite-Host "正在安装: {task["name"]} (ID: {task_id})... "')
                lines.append(f'Write-Host "生成的命令: {command}"')
                lines.append(command)
        
        if web_tasks:
            lines.append('\nWrite-Host "--- 正在打开需要手动操作的网页 ---" -ForegroundColor Yellow')
            for task in web_tasks:
                lines.append(f'Write-Host "正在打开: {task["name"]}..."')
                lines.append(f'Start-Process "{task["url"]}"')

        lines.extend([
            '\nWrite-Host "==================================================" -ForegroundColor Green',
            'Write-Host "✅ 所有自动化任务已提交执行完毕。" -ForegroundColor Green',
            'Read-Host "按 Enter 键退出此脚本窗口..."',
        ])
        
        script_content = "\n".join(lines)
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_install.ps1")

        try:
            with open(script_path, "w", encoding="utf-8-sig") as f: f.write(script_content)
            self.log.append(f"✅ 脚本已生成: {script_path}")
            self.log.append("--- 脚本内容预览 ---")
            self.log.append(script_content)
            self.log.append("--------------------")

        except Exception as e:
            QMessageBox.critical(self, "执行失败", f"无法创建安装脚本：\n{e}")
            return
            
        self.run_btn.setText("⚙️ 正在启动脚本...")
        self.run_btn.setEnabled(False)
        self.worker = Worker(script_path)
        self.worker.progress.connect(self.log.append)
        self.worker.finished.connect(lambda: (
            self.run_btn.setText("🚀 生成在线安装脚本并执行"),
            self.run_btn.setEnabled(True),
            self.log.append("\n🎉 任务结束。")
        ))
        self.worker.start()

    def load_config_and_populate_tree(self):
        self.tree.clear()
        try:
            if not os.path.exists(CONFIG_FILE_PATH):
                with open(CONFIG_FILE_PATH, "w", encoding="utf-8-sig") as f:
                    json.dump(DEFAULT_CONFIG_DATA, f, ensure_ascii=False, indent=4)
                config = DEFAULT_CONFIG_DATA
            else:
                with open(CONFIG_FILE_PATH, "r", encoding="utf-8-sig") as f:
                    config = json.load(f)
            for group_name, tasks in config.items():
                g_item = QTreeWidgetItem(self.tree, [group_name])
                g_item.setData(0, Qt.ItemDataRole.UserRole, {"is_group": True, "name": group_name})
                g_item.setFlags(g_item.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
                g_item.setCheckState(0, Qt.CheckState.Unchecked)
                for task_data in tasks:
                    task_data["is_group"] = False
                    t_item = QTreeWidgetItem(g_item)
                    t_item.setData(0, Qt.ItemDataRole.UserRole, task_data)
                    t_item.setFlags(t_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    self.update_tree_item_display(t_item, task_data)
            self.tree.expandAll()
            self.statusBar().showMessage("配置加载成功。", 3000)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载配置文件失败: {e}")

    def update_tree_item_display(self, item, data):
        item.setText(0, data.get("name", "未命名"))
        item.setText(1, data.get("type", ""))
        item.setText(2, data.get("id", "") or data.get("url", "") or data.get("path", ""))
        item.setText(3, data.get("custom_args", ""))
        item.setText(4, data.get("notes", ""))
        item.setCheckState(0, Qt.CheckState.Checked if data.get("checked", False) else Qt.CheckState.Unchecked)

    def add_group(self):
        g_item = QTreeWidgetItem(self.tree, ["新分组"])
        g_item.setData(0, Qt.ItemDataRole.UserRole, {"is_group": True, "name": "新分组"})
        g_item.setFlags(g_item.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
        self.tree.setCurrentItem(g_item)
        self.tree.editItem(g_item, 0)

    def add_task(self):
        selected_item = self.tree.currentItem()
        if not selected_item: return QMessageBox.information(self, "提示", "请先选择一个分组。")
        parent_item = selected_item if selected_item.data(0, Qt.ItemDataRole.UserRole).get("is_group") else selected_item.parent()
        if not parent_item: return QMessageBox.warning(self, "错误", "无法添加到根目录。")
        new_task_data = {"name": "新任务", "is_group": False, "type": "winget", "checked": True, "id": "", "custom_args": "", "notes": ""}
        t_item = QTreeWidgetItem(parent_item)
        t_item.setData(0, Qt.ItemDataRole.UserRole, new_task_data)
        t_item.setFlags(t_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        self.update_tree_item_display(t_item, new_task_data)
        parent_item.setExpanded(True)
        self.tree.setCurrentItem(t_item)
        self.tree.editItem(t_item, 0)

    def remove_item(self):
        item = self.tree.currentItem()
        if not item: return
        if QMessageBox.question(self, "确认删除", f"确定删除 '{item.text(0)}' 吗？") == QMessageBox.StandardButton.Yes:
            (item.parent() or self.tree.invisibleRootItem()).removeChild(item)

    def edit_item(self, item, column):
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if not data: return
        if data.get("is_group"):
            if column == 0: self.tree.editItem(item, column)
            return
        dialog = TaskEditorDialog(data, self)
        if dialog.exec():
            updated_data = dialog.get_updated_data()
            item.setData(0, Qt.ItemDataRole.UserRole, updated_data)
            self.update_tree_item_display(item, updated_data)
            self.statusBar().showMessage(f"任务 '{updated_data['name']}' 已更新。", 3000)

    def open_context_menu(self, pos):
        menu, item = QMenu(self), self.tree.itemAt(pos)
        if item:
            if item.data(0, Qt.ItemDataRole.UserRole).get("is_group", False):
                menu.addAction("组内全选", lambda: self.set_group_checkstate(item, Qt.CheckState.Checked))
                menu.addAction("组内全不选", lambda: self.set_group_checkstate(item, Qt.CheckState.Unchecked))
            else:
                menu.addAction("✏️ 编辑任务属性...", lambda: self.edit_item(item, 0))
        else:
            menu.addAction("全局全选", lambda: self.set_global_checkstate(Qt.CheckState.Checked))
            menu.addAction("全局全不选", lambda: self.set_global_checkstate(Qt.CheckState.Unchecked))
        menu.exec(self.tree.viewport().mapToGlobal(pos))

    def set_group_checkstate(self, group_item, state):
        for i in range(group_item.childCount()): group_item.child(i).setCheckState(0, state)

    def set_global_checkstate(self, state):
        for i in range(self.tree.topLevelItemCount()): self.set_group_checkstate(self.tree.topLevelItem(i), state)

    def export_data_to_dict(self):
        config_dict = {}
        for i in range(self.tree.topLevelItemCount()):
            group_item = self.tree.topLevelItem(i)
            group_name = group_item.text(0)
            config_dict[group_name] = []
            for j in range(group_item.childCount()):
                task_item = group_item.child(j)
                task_data = task_item.data(0, Qt.ItemDataRole.UserRole)
                if task_data:
                    task_data['name'] = task_item.text(0)
                    task_data['checked'] = task_item.checkState(0) == Qt.CheckState.Checked
                    config_dict[group_name].append(task_data)
        return config_dict

    def save_config(self):
        """
        智能保存配置：
        - 在开发环境，保存在脚本旁边。
        - 在打包后（.exe），保存在 .exe 文件旁边，实现配置持久化。
        """
        
        # 步骤 1: 动态判断正确的保存路径
        try:
            # getattr(sys, 'frozen', False) 是一个标准技巧，用于判断程序是否被 PyInstaller 等工具打包
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                # 程序被打包了，将 config.json 定位到 exe 文件所在的目录
                # sys.executable 指向的就是 MiaomiaoDeployer.exe 的绝对路径
                base_path = os.path.dirname(sys.executable)
            else:
                # 程序没被打包（在开发环境中直接运行 .py），则定位到脚本文件所在的目录
                # __file__ 指向当前脚本文件
                base_path = os.path.dirname(os.path.abspath(__file__))
                
            # 组合出最终的、绝对的配置文件路径
            config_path = os.path.join(base_path, 'config.json')

        except Exception as e:
            QMessageBox.critical(self, "路径错误", f"无法确定配置文件保存路径：\n{e}")
            return # 如果路径都确定不了，直接返回，不再继续

        # 步骤 2: 执行保存操作
        try:
            # 使用上面计算出的 config_path 进行写入
            with open(config_path, "w", encoding="utf-8-sig") as f:
                # 调用您已经写好的数据导出方法
                json.dump(self.export_data_to_dict(), f, ensure_ascii=False, indent=4)
            
            # 在状态栏给出成功反馈
            self.statusBar().showMessage(f"配置已成功保存到: {config_path}", 5000) # 显示5秒

        except Exception as e:
            # 如果写入失败，弹出错误提示
            QMessageBox.critical(self, "保存失败", f"无法写入配置文件到 {config_path}：\n{e}")

            
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出程序', "是否在退出前保存对配置的修改？",
                                     QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
        if reply == QMessageBox.StandardButton.Save: self.save_config(); event.accept()
        elif reply == QMessageBox.StandardButton.Discard: event.accept()
        else: event.ignore()


# 任务编辑器对话框也需要相应更新
class TaskEditorDialog(QDialog):
     def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.task_data = copy.deepcopy(task_data)
        self.setWindowTitle("编辑任务属性")
        self.layout = QFormLayout(self)

        self.name_edit = QLineEdit(self.task_data.get("name", ""))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["winget", "web"]) # 简化类型，因为local已无意义
        self.type_combo.setCurrentText(self.task_data.get("type", "winget"))
        self.id_edit = QLineEdit(self.task_data.get("id", ""))
        self.url_edit = QLineEdit(self.task_data.get("url", ""))
        self.custom_args_edit = QLineEdit(self.task_data.get("custom_args", ""))
        self.custom_args_edit.setPlaceholderText("例如: --scope machine 或 --location D:\\MyApps") #【重要】参数示例更新
        self.notes_edit = QTextEdit(self.task_data.get("notes", ""))

        self.layout.addRow("名称:", self.name_edit)
        self.layout.addRow("类型:", self.type_combo)
        self.layout.addRow("Package ID (winget):", self.id_edit)
        self.layout.addRow("URL (web):", self.url_edit)
        self.layout.addRow("自定义参数 (winget):", self.custom_args_edit)
        self.layout.addRow("说明:", self.notes_edit)

# ------------------------------
# 入口函数 (确保这部分代码存在且完整)
# ------------------------------
def main():
    """程序主入口函数"""
    app = QApplication(sys.argv)
    win = AppInstaller()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()