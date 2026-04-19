# 功能和特点

Google 公布的 Android 主要特性如下：

**应用程序框架（Application Framework）**

应用程序框架是 App 开发者用来创建 Android 应用的工具。关于框架的使用方法，可以参考官方网站 http://developer.android.com ，以及 O'Reilly 的《Learning Android》等相关书籍。

**Dalvik 虚拟机（Dalvik Virtual Machine）**

Dalvik 是 Android 自研的字节码解释器，用于替代 Sun 公司的 Java 虚拟机。后者解释执行 .class 和 .jar 文件，而 Dalvik 执行的是 .dex 文件。.dex 文件由 JDK 中 Java 编译器生成的 .class 文件经 dx 工具转换而来。

**整合的浏览器（Integrated Browser）**

Android 内置了基于 WebKit 的浏览器，作为标准应用之一。开发者也可以通过 WebView 类在自己的应用中使用 WebKit 渲染引擎。

**优化的图形系统（Optimized Graphics）**

Android 提供了自己的 2D 图形库，3D 能力则依赖 OpenGL ES。

**SQLite**

Android 使用的是标准 SQLite 数据库（http://www.sqlite.org），通过应用程序框架向开发者提供。

**多媒体支持（Media Support）**

Android 通过自研的媒体框架 StageFright 支持多种媒体格式。在 2.2 版本之前，Android 使用的是 PacketVideo 的 OpenCore 框架。

**GSM 电话支持（GSM Telephony Support）**

电话功能依赖硬件实现，设备制造商必须提供相应的 HAL（硬件抽象层）模块才能让 Android 与其硬件对接。HAL 模块将在下一章详细讨论。

**蓝牙、EDGE、3G 和 WiFi**

Android 支持主流的无线连接技术。其中 EDGE 和 3G 等采用 Android 自有的实现方式，而蓝牙和 WiFi 则与标准 Linux 基本一致。

**相机、GPS、指南针和加速度计（Camera, GPS, Compass, and Accelerometer）**

与用户环境交互是 Android 的核心能力之一。应用程序框架提供了访问这些设备的 API，同时需要相应的 HAL 模块来启用硬件支持。

**丰富的开发环境（Rich Development Environment）**

这大概是 Android 最大的优势之一。Android 为开发者提供了极为友好的开发环境，上手门槛很低。SDK 可以免费获取，包含模拟器（Emulator）、Eclipse 插件以及一系列调试和性能分析工具。

当然，Android 的特性远不止以上这些——USB 支持、多任务、多点触控、SIP、网络共享、语音命令等等，不胜枚举。但上述列表足以让你对 Android 有一个整体的认识。需要注意的是，每个新版 Android 都会带来新的特性和改进，可以参考每版发布时公布的 Platform Highlights 来了解详细信息。
