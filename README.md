# Hands-On Version Control in Vitis Unified IDE Embedded Design

本工程提供Vitis Unified IDE Embedded Design的通用gitignore文件，并在新路径下通过脚本可快速重建。

> !! Vitis Unified IDE 2025.2 版本已测试

## 首次提交

1. 确认原 Vitis 工程可以正常编译。
2. 将以下文件放到 Vitis workspace 根目录：
   - `.gitignore`
   - `rebuild_workspace.py`
   - `rebuild_workspace.bat`
   - `README.md`
3. 系统环境变量添加vitis路径。eg: `C:\AMDDesignTools\2025.2\Vitis\bin\`
4. 参考本工程./logs/builder.py文件，修改rebuild_workspace.py的配置参数

## 更换路径后重建

1. 将仓库 clone 或复制到新路径。
2. 双击运行：
   ```text
   rebuild_workspace.bat
   ```

脚本会自动调用 Vitis 并重建 platform 和 application。
