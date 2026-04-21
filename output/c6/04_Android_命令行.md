# Android 命令行

正如我之前所说，你最早遇到的 Android 特定工具之一是 adb，它最常见的用途之一是登录到目标进行 shell 操作。由于在主板启动期间，在拥有可用 UI 之前你可能会在命令行上花费大量时间，现在介绍 Android 的命令行是合适的。

### Shell（截至 2.3/Gingerbread）

Android 2.3/Gingerbread 及之前版本中使用的标准 shell 位于 AOSP 的 `system/core/sh/` 中，生成的二进制文件是目标上的 `/system/bin/sh`。与系统中的许多组件不同，Android 没有在这里重新发明轮子，而是使用了极少改动的 NetBSD sh 实用程序。

不幸的是，这个 shell 比 bash 或 BusyBox 的 ash 基础得多。例如，它没有 tab 补全或文件颜色编码。至少在开发过程中，这些限制是开发者在目标上包含 BusyBox 的充分理由。

### Shell（自 4.0/Ice-Cream Sandwich 起）

从 4.0/Ice-Cream Sandwich 起，Android 现在依赖 MirBSD Korn Shell。它位于 AOSP 的 `external/mksh/` 目录中，二进制文件是目标上的 `/system/bin/mksh`。

mksh 比 sh 强大得多。它包含 tab 补全等功能，虽然不支持文件颜色编码，但具有 bash/ksh93/zsh 类似的扩展。

### Toolbox

与任何其他基于 Linux 的系统一样，Android 的 shell 只提供了具有可用命令行所需的绝对最低限度。其余功能来自从 shell 单独启动的提供特定功能的各个工具。正如第 2 章所讨论的，Android 中提供这些工具的包称为 Toolbox，以 BSD 许可证分发。Toolbox 位于 AOSP 的 `system/core/toolbox/` 中。

**表 6-13. Toolbox 的常见 Linux 命令**

| 命令 | 说明 |
|------|------|
| cat | 将给定文件的内容转储到标准输出 |
| chmod | 更改文件或目录的访问权限 |
| chown | 更改文件或目录的所有权 |
| cmp | 比较两个文件 |
| date | 打印当前日期和时间 |
| dd | 复制文件并转换和格式化内容 |
| df | 打印文件系统的磁盘使用情况 |
| dmesg | 转储内核日志缓冲区 |
| hd | 以十六进制格式转储文件 |
| id | 打印当前用户和组 ID |
| ifconfig | 配置网络接口 |
| insmod | 加载内核模块 |
| kill | 向进程发送 TERM 信号 |
| ls | 列出目录内容 |
| lsmod | 列出当前加载的内核模块 |
| mkdir | 创建目录 |
| mount | 打印已挂载文件系统列表或挂载新文件系统 |
| mv | 重命名文件 |
| netstat | 打印网络统计信息 |
| ps | 打印运行中的进程 |
| reboot | 重启系统 |
| rm | 删除文件 |
| rmmod | 移除内核模块 |
| route | 打印/修改内核路由表 |
| sleep | 休眠指定秒数 |
| sync | 将文件系统缓存刷新到持久存储 |
| top | 实时监控进程 |
| umount | 卸载文件系统 |

### 全局属性

第 2 章解释了 Android init 的特性之一是维护一组全局属性，系统任何地方都可以访问这些属性。Toolbox 提供了几个与这些全局属性交互的工具：

```bash
getprop <key>
setprop <key> <value>
watchprops
```

### 控制服务

Android 的 init 为各种目的启动许多原生守护进程。通常，这些在 init 的配置脚本中被描述为服务。无论如何，你可以使用以下命令启动和停止服务：

```bash
start <servicename>
stop <servicename>
```

### 日志

Toolbox 的另一个有趣功能是允许你将自己的事件添加到 Android 的日志中：

```bash
log [-p <prioritychar>] [-t <tag>] <message>
```

### 擦除设备

在某些极端情况下，有必要销毁 Android 设备上的数据。这个极端且不可逆转的操作通过 Toolbox 的 wipe 命令实现：

```bash
wipe <system|data|all>
```
