# ADB

我们刚刚讨论的文件系统布局只是 Android 其余部分赖以生存的骨架。在主板启动过程中，内核启动后，你可能最想确保在设备上运行的第一个 Android 软件可能是 adb。我们已经在第 3 章介绍了它的基本操作。现在我们将更深入地介绍它的使用。

### 工作原理

虽然使用起来非常简单，但 adb 是一个非常强大的工具，对应用开发和平台开发都有用处。Android 的若干领域建立于或替代传统嵌入式 Linux 系统中发现的功能，但在 Android 之前，在 Linux 世界中没有哪个项目或包提供了与 adb 类似的功能（至少据我所知）。因此，adb 填补了一个重要空白，是对主机-目标交互可以如何改进和调解的刷新式思路。

adb 实际上由多个组件构成，这些组件本身又连接到其他系统组件，以提供 adb 的综合功能集。图 6-3 展示了 adb 的互联和操作。

![图 6-3. ADB 及其互联](images/fig-6-3.png)

adb 既充当透明传输机制，也充当服务提供者。它最重要的两个组件是运行在主机上的 adb 服务器和运行在目标上的 adbd 守护进程。这两个组件有效地实现了一个代理协议，所有 adb 服务都在其上实现。它们可以通过 USB 或常规 TCP/IP 相互链接。两种情况下 adb 可用的命令集是相同的。

### 主要标志、参数和环境变量

adb 提供了大量命令。然而，adb 可以同时与多个 Android 设备和 AOSP 构建进行交互。因此，有几个标志、参数和环境变量来控制其行为。

**表 6-9. adb 的标志、参数和环境变量**

| 项目 | 说明 |
|------|------|
| -d | 此标志使 adb 执行在 USB 连接设备上传递的命令 |
| -e | 与 -d 类似，这使 adb 连接到正在运行的模拟器实例 |
| -s \<serial number\> | 这使 adb 连接到由给定序列号指定的 USB 设备或模拟器 |
| -p \<product name or path\> | 某些 adb 命令需要访问用于构建目标 AOSP 的源文件 |
| ANDROID_SERIAL | 如果你始终有多个设备连接，且想避免使用 -s 标志来指定你经常操作的一个设备的序列号 |
| ADB_TRACE | 如果你想调试或监控主机上 adb 服务器与目标上 adbd 守护进程之间的交互 |

### 基本本地命令

首先，如果你想手动启动 adb 服务器，可以这样做：

```bash
$ adb start-server
```

服务器会在任何其他 adb 命令需要时自动启动。但如果你的某些 adb 命令似乎挂起了，通常应该手动关闭服务器：

```bash
$ adb kill-server
```

### 设备连接和状态

如果你想查看哪些设备对 adb 可见，可以输入：

```bash
$ adb devices
```

如果你想连接到其 adbd 守护进程通过 TCP/IP（而非 USB）运行的远程设备，可以使用 connect 命令：

```bash
$ adb connect 192.168.202.79:7878
```

### 基本远程命令

Shell — 如果你是一个像我这样的技术爱好者，你最想做的事情之一就是登录到你的设备上探索一番：

```bash
$ adb shell
root@android:/ #
```

日志转储 — 如果你想转储 Android 的日志缓冲区，可以输入：

```bash
$ adb -d logcat
```

### 获取 bug 报告

adb 为 bugreport 提供了快捷方式，后者是转储系统状态以进行错误报告的目标命令：

```bash
$ adb -d bugreport
```

### 端口转发

adb 的另一个非常有趣的功能是允许你在主机和目标之间转发端口。例如，此命令将本地端口 8080 转发到目标的端口 80：

```bash
$ adb -d forward tcp:8080 tcp:80
```

### Dalvik 调试

adb 实际上是调试目标上任何 Java 的关键组件。当 adbd 守护进程在目标上启动时，它会打开"抽象"Unix 域套接字 jdwp-control 并等待连接。之后启动的 Dalvik 进程会连接到该套接字，从而使自己"可见"可供调试。

### 文件系统命令

adb 还允许你以各种方式操作和与目标的文件系统交互。

**push 和 pull** — 如果你想将文件复制到设备，可以使用 push：

```bash
$ adb push acme_user_manual.pdf /data/local
```

也可以从目标复制文件到主机：

```bash
$ adb pull /proc/cpuinfo
```

**remount** — 目标的文件系统并非所有部分都以相同权限挂载。例如，`/system` 通常以只读方式挂载。如果你想以读写模式重新挂载来添加或修改其上的文件：

```bash
$ adb remount
remount succeeded
```

**sync** — 如果你想更新目标 `/data` 或 `/system` 分区的全部内容，可以使用 sync 命令。它将进行类似于 rsync 的操作，确保目标的文件与主机上的文件同步：

```bash
$ adb sync
```

### 状态变更命令

**重启** — 最明显的命令之一：

```bash
$ adb reboot
```

你还可以传递参数告诉它重启到引导程序或恢复模式：

```bash
$ adb reboot bootloader
$ adb reboot recovery
```

**以 root 身份运行** — 在开发板上，大多数 adb 命令都能完全正常工作，因为目标上的 adbd 守护进程可能以 root 身份运行。在商用手机等生产系统上，adbd 可能不以 root 身份运行，而是以 shell 用户身份运行，权限少得多。在 userdebug 构建的情况下，你可以要求它以 root 身份重启：

```bash
$ adb root
restarting adbd as root
```
