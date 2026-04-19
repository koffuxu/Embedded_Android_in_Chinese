# 附录 D：默认 init.rc 文件

本附录包含 2.3/Gingerbread 和 4.2/Jelly Bean 中的默认 init.rc 文件。我通常不喜欢在书中整页整页地打印文件内容，在我的作品中你不会找到太多这样的内容。然而，init.rc 是一个最好的解释方式就是直接展示给你的情况。为了让你更容易地跟踪文件中执行的操作，我在整个文件中添加了一些标注，以深入了解文件的关键部分。关于 init.rc 文件中使用的操作、触发器、命令、服务和服务选项的更多信息，请参阅第 6 章。

## 2.3/Gingerbread 的默认 init.rc

以下是 2.3/Gingerbread 的默认 init.rc 文件。文件内容为英文配置格式，关键注释已翻译。

```rc
# 早期初始化阶段
on early-init 
    start ueventd

# 主初始化阶段
on init 
    sysclktz 0
    loglevel 3

# 设置全局环境变量
    export PATH /sbin:/vendor/bin:/system/sbin:/system/bin:/system/xbin
    export LD_LIBRARY_PATH /vendor/lib:/system/lib
    export ANDROID_BOOTLOGO 1
    export ANDROID_ROOT /system
    export ANDROID_ASSETS /system/app
    export ANDROID_DATA /data
    export EXTERNAL_STORAGE /mnt/sdcard
    export ASEC_MOUNTPOINT /mnt/asec

# BOOTCLASSPATH：启动时 Dalvik 虚拟机加载的核心框架 JAR 文件
    export BOOTCLASSPATH /system/framework/core.jar:/system/framework/bouncycastle.jar:/system/framework/ext.jar:/system/framework/framework.jar:/system/framework/android.policy.jar:/system/framework/services.jar:/system/framework/core-junit.jar

# 向后兼容：创建符号链接
    symlink /system/etc /etc
    symlink /sys/kernel/debug /d
    symlink /system/vendor /vendor

# 创建挂载点
    mkdir /mnt 0775 root system
    mkdir /mnt/sdcard 0000 system system

# 为 CPU 统计创建 cgroup 挂载点
    mkdir /acct
    mount cgroup none /acct cpuacct
    mkdir /acct/uid

# 创建 cgroup 挂载点用于进程组
    mkdir /dev/cpuctl
    mount cgroup none /dev/cpuctl cpu
    chown system system /dev/cpuctl
    chown system system /dev/cpuctl/tasks
    chmod 0777 /dev/cpuctl/tasks
    write /dev/cpuctl/cpu.shares 1024
    mkdir /dev/cpuctl/fg_boost
    chown system system /dev/cpuctl/fg_boost/tasks
    chmod 0777 /dev/cpuctl/fg_boost/tasks
    write /dev/cpuctl/fg_boost/cpu.shares 1024
    mkdir /dev/cpuctl/bg_non_interactive
    chown system system /dev/cpuctl/bg_non_interactive/tasks
    chmod 0777 /dev/cpuctl/bg_non_interactive/tasks
    # 5.0%
    write /dev/cpuctl/bg_non_interactive/cpu.shares 52

# 文件系统阶段：挂载 MTD 分区
on fs 
    mount yaffs2 mtd@system /system
    mount yaffs2 mtd@userdata /data
    mount yaffs2 mtd@cache /cache

# 关键系统服务启动阶段
on post-fs-data
    # 创建 dalvik-cache 目录
    mkdir /data/dalvik-cache 0771 system system

# Zygote 服务：Android 应用框架的核心启动器
service zygote /system/bin/app_process -Xzygote /system/bin --zygote --start-system-server 
    socket zygote stream 666
    onrestart write /sys/android_power/request_state wake
    onrestart write /sys/power/state on
    onrestart restart media
    onrestart restart netd

# 系统服务器：由 Zygote fork 启动的核心系统服务进程
service system_server /system/bin/servicemanager
    class main
    user system
    group system
    critical

# 媒体服务：处理音频、视频和相机
service media /system/bin/mediaserver
    user media
    group system audio camera graphics inet net_bt net_bt_admin net_raw
    ioprio rt 4

# 安装守护进程：处理 APK 安装和 dex 优化
service installd /system/bin/installd
    socket installd stream 600 system system

# Vold 守护进程：处理存储卷挂载
service vold /system/bin/vold
    socket vold stream 0660 root mount
    ioprio be 2
```

**关键说明：**

- `on early-init`：系统启动的最早阶段，启动 ueventd 处理设备事件
- `export BOOTCLASSPATH`：这些 JAR 文件在 Dalvik 虚拟机启动时必须可用
- `service zygote`：这是 Android 框架的起点，通过 app_process 启动
- `zygote --start-system-server` 标志：指示 Zygote 在初始化后启动系统服务器
- `socket zygote stream 666`：Zygote 用于接收 fork 新应用请求的套接字

## 4.2/Jelly Bean 的默认 init.rc（主要差异）

4.2/Jelly Bean 中的 init.rc 相比 2.3/Gingerbread 有以下主要变化：

1. **Surface Flinger 独立启动**：Surface Flinger 在 Zygote 之前启动，不再作为系统服务器的一部分
2. **新增 USB 服务**：增加了 USB 管理服务
3. **网络管理增强**：netd 守护进程增加了更多套接字
4. **调度策略改进**：CPU cgroup 控制更精细

```rc
# Surface Flinger 在 Zygote 之前启动
service surfaceflinger /system/bin/surfaceflinger
    class main
    user system
    group graphics drmrpc
    onrestart restart zygote
```

**init.rc 关键路径说明：**

- `/system/bin/app_process`：实际的可执行文件，Zygote 是其别名
- `/dev/socket/zygote`：Activity Manager 和 Zygote 之间的通信套接字
- `/data/dalvik-cache`： dexopt 优化后的 .odex 文件存放位置
