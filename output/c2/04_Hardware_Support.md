> 翻译：[Ross.Zeng](https://github.com/zengrx)
> 校对：

### 硬件支持

安卓的硬件支持方式与典型的Linux内核和基于Linux的发行版大不相同。具体来看，硬件支持的实现方式、基于该硬件支持构建的抽象以及围绕最终代码许可和分发理念都是不同的。

#### Linux方式

一般为Linux提供新硬件支持的方式包含内核构建分或在运行时动态装载模块。相应的硬件随后通常可以通过进入*/dev*目录在用户空间访问。Linux驱动模型定义了三种基本的设备：字符设备，体现为字节流；块设备（基本为硬盘）以及网络设备。多年以来新增了很多额外设备与子系统，如USB或MTD设备。然而，*/dev*给到相应设备入口的API与接口方法仍然相当标准与稳定。

因此，这就允许了*/dev*节点上构建各样的软件栈，得以直接与硬件交互或应用程序通过调用公开的API访问硬件。实际上，绝大多数的Linux发行版都有相似的内核库与子系统，如ALSA音频库和X Window系统。都能够通过*/dev*访问硬件设备。

对于许可与发布方面，一般的“Linux”方式是始终将驱动作为主线内核的一部分进行合并与发布，并在GPL条款下发布。所以一般不建议将设备驱动独立开发与维护，甚至在其他协议下发布。实际上，在许可方面，非GPL的驱动一直是一个有争议的问题。因此，一般做法是用户和经销商最好从http://kernel.org中获取最新的主线内核驱动。这些内核在早先就已经在GPL下发布，尽管内核有添加，但仍然受GPL约束。

#### 安卓通用方式

尽管安卓构建在内核硬件抽象与功能上，方式却大不相同。从纯技术层面而言，最显著的区别在于其子系统与库不需要依赖标准的*/dev*来工作。反之，安卓更加依赖由制造商提供的共享库与硬件交互。实际上，安卓依赖于一个被称为硬件抽象层(HAL层)的结构，不过，正如我们所见的，不同类型硬件间组件的接口、行为与功能都差异巨大。

此外，大部分在Linux发行版上常见的软件栈并没有出现在安卓中。比如安卓中没有X Window系统。虽然有时也会用到ALSA驱动，但硬件制造商会决定提供何种共享库实现对HAL层音频的支持。所以功能访问这点上就与标准的Linux发行版不同。

图2-3呈现了安卓中典型的硬件抽象与支持方式，及相应的分发与许可。正如你所见的，安卓最终还是需要靠内核访问硬件。然而，这里的功能早就由设备制造商或AOSP中实现了。

这种方法的一大特点就是共享库的许可由硬件制造商决定。因此，设备制造商可以创建一个简单的设备驱动实现给定硬件的基础功能，并将驱动发布在GPL下。硬件不会透露过多的内容，因为驱动不会玩什么花活。接着驱动会通过**mmap()**或**ioctl()**接口将硬件公开给用户空间，那么各种复杂的操作将在用户空间专用的共享库中实现，并以此驱动硬件设备。

安卓并没有规定共享库、驱动或内核子系统应该如何交互。只有为上层提供API的共享库才由安卓指定。因此，只要能实现适用的API，你可以任意决定使用认为最适合的硬件驱动。不过，我们将在下章介绍使用与安卓的典型硬件方法。

而安卓相对不一致的地方是上层加载硬件支持共享库的方式。现在请注意，对于大多数的硬件类型，必须由AOSP或开发者提供*.so*类型文件，否则安卓就不能正常工作。

无论是哪种方式，都是为了装载硬件支持的共享库，响应硬件的系统服务主要负责加载和连接共享库。这类系统服务负责与其他系统服务协调，使硬件和系统其余部分以及供开发人员使用的API保持一致。如果你需要为一个给定的硬件添加支持，你需要尽可能详细地了解这部分相关的系统服务内部结构。通常系统服务分为两部分，java实现大部分安卓相关的内容，另一部分则由C完成，主要负责支持共享库及其他底层功能的硬件交互。

![Android's "Hardware Abstraction Layer"](https://i.bmp.ovh/imgs/2019/07/8075b50ec1af0b9c.png)

#### 装载与接口方法 Loading and Interfacing Methods

正如前文所提及，大体上系统服务与安卓有非常多的方法与硬件设备的共享库进行交互，从而实现对硬件的支持。很难完全理解为什么会存在如此多的方法，但是作者怀疑有一些是有组织地形成的。幸运的是，这似乎正在朝着更加统一的方式发展。鉴于安卓在以相当迅速的方式演化，这是在未来一个需要密切关注的领域，因为它或许一眨眼就进化了。

注意，这些方法的描述并不是互斥的。安卓技术栈中经常在加载或交互共享库及一些软件的前后时刻组合使用这些方法。

**dlopen()** - *通过硬件抽象层加载*
+ *相关：GPS，灯，传感器与显示*
一些硬件支持的共享库有libhardware库所装载。这个库属于安卓的硬件抽象层，并提供**hw_get_module()**接口，某些系统服务及子系统通过该接口显示加载特定硬件支持共享库（在**HAL**属于中成为“模块”）。**hw_get_module()**反过来依靠典型的**dlopen()**将加载到调用者的地址空间中。

连接器装载*.so*文件
+ *相关：音频，摄像头，wifi，马达及电源管理*
一般情况下，系统服务只是在构建时与指定的.so文件链接。因此，当二进制文件运行起来时，动态链接器会自动将共享库装载至进程的地址空间。

*硬编码**dlopen()***
+ *相关：StageFright与无线电接口层*
在一些场景下，内核赋予**dlopen()**直接获取硬件使能的共享库，无需再通过**libhardware**实现。目前还不清楚这种方法的原理。

*套接字*
+ *相关：蓝牙，网络管理，硬盘挂载和无线接口层*
系统服务或框架组件有时会使用套接字与硬件交互的远程守护进程及服务对话。

*文件系统条目（项）*
+ *相关：马达与电源管理*
文件系统（/sys）中的一些条目被用来控制硬件或内核子系统行为。在某些情况下，相比于用/dev中的条目，安卓会使用这个方法来控制硬件。

*/dev节点*
+ *相关：几乎所有类型的硬件*
可以肯定的是，任何硬件抽象都必须在某个时刻与*/dev*中的一个条目通信，这就是驱动向用户空间公开的方式。有些通信通过共享库的方式隐藏在安卓中。有时AOSP也会直接访问设备节点，比如输入管理器使用输入库的场景。

*D-Bus*
+ *相关：蓝牙*
D-Bus作为一个经典的信息系统，可以在几乎所有的Linux发行版找到，用于促进不同桌面组件间的通信。它之所以出现在安卓中，就是因为它是非GPL组件与GPL许可的BlueZ栈——Linux默认蓝牙堆栈对话的指定方式，如此一来在安卓中使用蓝牙就无需受到GPL再分发的要求。D-Bus本身有教育免费许可（AFL）与GPL的双重认可。关于D-Bus的更多信息，可以访问http://dbus.freedesktop.org。

#### 设备支持细节

表2-1汇总了安卓中支持每种类型硬件的方式。如你所注意到的，这里面包含了很多机制与接口组合。如果你打算实现特定硬件的支持，那么最好的方法就是从现有的示例中开始。AOSP专门为一些设备增加了硬件支持，主要是谷歌使用的最新测试机与一些旗舰机型。有时硬件支持来源十分广泛，例如三星Nexus S（代号俗称Crespo）。

唯一一个不太容易公开获取的硬件类型就是RIL。处于种种原因，最好不要让所有人都玩起无线电波。因此，制造商不提供此类实现。相反，如果你希望实现一个RIL，谷歌提供了其实现参考。

+ *表2-1. 安卓硬件支持方法与接口*

Hardware|System Service|Interface to user-space HW support|Interface to HW
-|-|-|-
Audio|Audio Flinger|Linker-loaded *libaudio.so*|Up to HW manufacturer, though ALSA is typical
Bluetooth|Bluetooth Service|Socket/D-Bus to BlueZ|BlueZ stack
Camera|Camera Service|Linker-loaded *libcamera.so*|Up to HW manufacturer, sometimes Video4Linux
Display|Suface Flinger|HAL-loaded *gralloc* module|*/dev/fb0 or /dev/graphics/fb0*
GPS|Location Manager|HAL-loaded *gps* module|Up to HW manufacturer
Input|Input Manager|Native library|Entries in */dev/input*
Lights|Lights Service|HAL-loaded *lights* module|Up to HW manufacturer
Media|N/A, StageFright framework within Media Service|dlopen on *libstagefrightw.so*|Up to HW manufacturer
Network interfaces|Network Management Service|Socket to netd|ioctl() on interfaces
Power Management|Power Manager Service|Linker-loaded libhardware_legacy.so|Entries in /sys/android_power/ or /sys/power 
Radio (phone)|N/A, entry point is telephony Java code|Socket to *rild*, which itself does a dlopen() on manufacturer-provided.so|Up to HW manufacturer
Storage|Mount Service|Socket to vold|System calls
Sensors|Sensor Service|HAL-loaded sensors module|Up to HW manufacturer
Vibrator|Vibrator Service|Linker-loaded libhardware_legacy.so|Up to HW manufacturer
Wifi|Wifi Service|Linker-loaded libhardware_legacy.so|Classic *wpa_supplicant*

-----------------------------------------