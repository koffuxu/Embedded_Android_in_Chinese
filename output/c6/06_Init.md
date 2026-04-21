# Init

系统中最重要的任务之一是在内核完成初始化设备驱动程序和自己的内部结构后初始化用户空间环境。正如第 2 章所讨论的，这是内核启动后 init 进程的职责。而且，正如我们当时讨论的，Android 有自己定制的 init，有自己特定的功能。现在我们已经介绍了原生用户空间可用的大部分内容，让我们仔细看看负责启动一切的进程。

### 工作原理

图 6-4 展示了 init 如何与 Android 组件的其余部分集成。在被内核启动后，它本质上会读取其配置文件，打印启动徽标或文本到屏幕，打开属性服务的套接字，并启动所有带来整个 Android 用户空间的守护进程和服务。

![图 6-4. Android 的 init](images/fig-6-4.png)

### Android init 与"普通"init

在典型的 Linux 系统中，init 的角色仅限于启动守护进程，但由于其属性服务，Android 的 init 是特殊的。然而，与任何 Linux init 一样，Android 的 init 不应被期望会退出。init 是内核启动的第一个进程，因此其 PID 始终为 1。如果它死了，内核会 panic。

### 配置文件

控制 init 行为的主要方式是通过其配置文件。init 主要配置文件位于根目录（/）。这是你找到实际 init 二进制文件及其两个配置文件的地方：`init.rc` 和 `init.\<device_name\>.rc`。

### 语义

init 的 .rc 文件包含一系列声明，分为两类：动作（actions）和服务（services）：

```
on <trigger>
   <command>
   <command>
...

service <name> <pathname> [ <argument> ]*
   <option>
   <option>
...
```

### 触发器

init 定义了一组可在 init 配置文件中使用的预定义触发器，按特定顺序运行：

- early-init
- init
- early-fs
- fs
- post-fs
- early-boot
- boot

### init 的命令

**表 6-18. init 的命令**

| 命令 | 说明 |
|------|------|
| chdir \<directory\> | 与 cd 命令相同 |
| chmod \<octal-mode\> \<path\> | 更改路径的访问权限 |
| chown \<owner\> \<group\> \<path\> | 更改路径的所有权 |
| mkdir \<path\> [mode] [owner] [group] | 创建具有适当权限和所有权的路径目录 |
| mount \<type\> \<device\> \<dir\> [\<mountoption\>]\* | 将设备挂载到 dir |
| setprop \<name\> \<value\> | 将属性 name 设置为 value |
| start \<service\> | 启动服务 |
| stop \<service\> | 停止服务 |
| symlink \<target\> \<path\> | 创建符号链接 |
| write \<path\> \<string\> [\<string\>]\* | 打开文件并向其中写入字符串 |

### 服务声明

init 只引用服务名称，不能识别要运行进程的文件路径。因此，必须首先将进程分配给服务：

```
service <name> <pathname> [ <argument> ]*
```

### 服务选项

**表 6-20. init 的服务选项**

| 选项 | 说明 |
|------|------|
| class \<name\> | 此服务属于名为 name 的类，默认类为 default |
| console | 服务需要并运行在控制台上 |
| critical | 如果此服务崩溃五次，则重启进入恢复模式 |
| disabled | 不要自动启动此服务。需要使用 start 手动启动 |
| group \<groupname\> [\<groupname\>]\* | 以给定的组运行此服务 |
| oneshot | 服务只运行一次。退出时服务被设置为 disabled |
| onrestart \<command\> | 如果服务重启，运行 command |
| socket \<name\> \<type\> \<perm\> [\<user\> [\<group\>]] | 创建 Unix 域套接字 |
| user \<username\> | 以 username 身份运行此服务 |

### 主板特定的 .rc 文件

如果你需要为 init 添加特定板的配置指令，最佳方式是使用针对你系统的 `init.\<device_name\>.rc`。

### 全局属性

尽管我已经多次提到全局属性，但我们尚未深入了解 Android 的这一方面。Android 的全局属性是整个架构的重要部分——作为 Windows 注册表的一个远亲，Android 的全局属性通常作为一种简单的方式在栈的所有部分之间共享重要但相对稳定的值。

### 工作原理

如前所述，init 将属性服务作为其其他职责的一部分进行维护。有两种方式将此属性服务暴露给系统其余部分：

**/dev/socket/property_service** — 这是一个 Unix 域套接字，进程可以打开它与属性服务通信并让它设置和/或更改全局属性的值。

**/dev/__properties__** — 这是一个"隐形"文件（在 tmpfs 挂载的 /dev 中创建），被内存映射到 init 启动的所有服务的地址空间中。

### 属性命名和集合

顾名思义，以 `ro.` 开头的属性是只读的。它们只能在系统生命周期内设置一次。唯一更其值的方法是更改其信息来源并重启系统。

以 `persist.` 开头的属性在每次设置时被提交到持久存储。

`ctl.*` 属性用于启动/停止服务。
