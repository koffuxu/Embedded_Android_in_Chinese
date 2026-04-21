# ueventd

如前所述，init 包含处理内核热插拔事件的功能。当 `/init` 二进制文件通过 `/sbin/ueventd` 符号链接调用时，它立即将其身份从运行常规 init 切换为运行 ueventd。

![图 6-5. Android 的 ueventd](images/fig-6-5.png)

ueventd 是默认 init.rc 启动的最早服务之一。它读取其主要配置文件 `/ueventd.rc` 和 `/ueventd.\<device_name\>.rc`，重放所有内核 uevent（热插拔事件），然后等待监听所有未来 uevent。

与 init 不同，ueventd 的配置文件格式相当简单。本质上，每个设备条目用如下一行来描述：

```
/dev/<node>               <mode>   <user>       <group>
```
