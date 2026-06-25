# Vitis 工程版本管理指南

本工程使用 Git 管理 Vitis workspace，并通过脚本在新路径下自动重建可生成内容。

## 首次提交

1. 确认原 Vitis 工程可以正常编译。
2. 将以下文件放到 Vitis workspace 根目录：
   - `.gitignore`
   - `rebuild_workspace.py`
   - `rebuild_workspace.bat`
   - `README.md`
3. 在 workspace 根目录执行：
   ```powershell
   git status --short --ignored
   ```
4. 确认没有异常文件后提交第一版：
   ```powershell
   git add .
   git commit -m "Add Vitis workspace rebuild flow"
   ```

## 更换路径后重建

1. 将仓库 clone 或复制到新路径。
2. 双击运行：
   ```text
   rebuild_workspace.bat
   ```

脚本会自动调用 Vitis 并重建 platform 和 application。

## Vitis 安装路径

脚本默认使用：

```text
C:\AMDDesignTools\2025.2\Vitis\bin\vitis.bat
```

如果 Vitis 安装在其他位置，修改 `rebuild_workspace.bat` 中的 `VITIS_BAT`。
