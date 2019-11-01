> 翻译：[Ross.Zeng](https://github.com/zengrx)
> 校对：

### 原生用户空间

至此，我们已经覆盖了安卓的底层内容，接下来开始进入上一层。首先，我们需要了解安卓操作系统中的原生用户空间环境。关于“原生用户空间”，这里指的是所有用户空间组件都是运行在Dalvik虚拟机之外的。这之中包含了很多编译运行在目标CPU架构上的二进制文件。通常是自动或根据init进程的配置文件启动，或集成在命令行中由开发人员的脚本调用。这些二进制文件可以直接访问根文件系统与系统中包含的原生库。它们的功能被赋予其文件系统的权限限制，因为其运行在应用程序框架之外，所以并不会受到如安装框架对安卓应用的限制。

注意，安卓的用户空间基本是从一张白纸开始设计，与标准Linux发行版存在很大的不同。因此，下面将尽可能多的解释安卓用户空间与基于Linux系统的异同之处。

#### 文件系统布局

像其他基于Linux的发行版一样，安卓也使用一个根文件系统来存储应用，库和数据。但与这些发行版不同的是，安卓的根文件系统并不符合文件系统层次标准（FHS）。内核本身并不强制要求FHS，但大部分为Linux构建的软件包会假设它们运行的根文件系统符合FHS。因此，如果你打算将一个标准Linux应用移植到安卓中，你可能得费点力气以确保它依赖的文件路径依然有效。

考虑到运行在安卓用户空间的包基本都是为安卓专门编写的，上述的不一致性几乎没有影响。实际上，我们很快可以发现这也有一些好处。总之对学习安卓根文件系统还是很重要的。如果要在硬件上跑安卓系统，或者客制化硬件设备，最好还是在这上面花些时间。

安卓系统中的两个主要目录便是*/system*与*/data*。这两个目录并没有出现在FHS中。实际上，应该没有任何一个主流的Linux发行版会使用这两个目录。相反，这反应了安卓开发团队自己的设计。这或许是一个早起的迹象，暗示了安卓在同一套根文件系统上将自身与Linux发行版并至。我们同样安排在后文对这一点详细讨论。

*/system*目录用于存储由AOSP构建生成的不发生变化的组件，其中包括原生二进制文件，原生库，框架层包基于系统应用。它通常挂载在根文件系统独立出的镜像中，由其自身通过RAM盘镜像挂载。另一方面，*/data*分区用来存储则用来存储随时间会发生变化的文件，如数据及应用。其中包括由用户安装应用及系统组件运行时生成的内容。该分区也是在自己独立的镜像中被挂载。

安卓中也包含很多在任何Linux系统中常见的目录， 如 */dev*，*/proc*， */sys*， */sbin*， */root*， */mnt*和 */etc*。这些目录的作用与其他Linux系统中基本是相似的，尽管它们经常被删减，如*/sbin*与*/etc*，而像*/root*，有时是空的。

有趣的是，安卓没有包括*/bin*与*/lib*目录。这些目录在Linux中是至关重要的，它们中包含了基本的二进制文件与库文件。这也为安卓与标准Linux组件共存打开了一扇大门。

当然，对于安卓的根文件系统还有很多地方可聊。例如刚才的内容仅仅提到了目录与它们的层次结构。安卓的根文件系统还包含了这里未提及的其他目录。我们将在第五章中更加详细地回顾安卓根文件系统及其组成。

#### 库

安卓依赖着上百个动态装载库，这些库都被存储在*/system/lib*路径下。有一定数量的库来源于外部项目，这些项目最后也被合并入安卓的源码中，以使其能够可以运行在安卓上，但大部分的*/system/lib*库还是由AOSP本身生成的。

+ *表 2-2. 由AOSP收纳外部项目生成的库*

Library(ies)|Extemal Project|Original Location|License
-|-|-|-
*libcrypto.so and libssl.so*|OpenSSL|http://www.openssl.org|Custom, BSD-like
*libdbus.so*|D-Bus|http://dbus.freedesktop.org|AFL and GPL
*libexif.so*|Exif Jpeg header manipulation tool|http://www.sentex.net/~mwandel/jhead/|Public Domain
*libexpat.so*|Expat XML Parser|http://expat.sourceforge.net|MIT
*libFFTEm.so*|neven face recognition library|N/A|ASL
*libicui18n.so and libicuuc.so*|International Components for Unicode|http://icu-project.org|MIT
*libiprouteutil.so and libnetlink.so*|iproute2 TCP/IP networking and traffic control|http://www.linuxfoundation.org/collaborate/workgroups/networking/iproute2|GPL
*libjpeg.so*|libjpeg|http://www.ijg.org|Custom, BSD-like
*libnfc_ndef.so*|NXP Semiconductor's NFC library|N/A|ASL
*libskia.so and libskiagl.so*|skia 2D graphics library|http://code.google.com/p/skia/|ASL
*libsonivox*|Sonic Network's Audio Synthesis library|N/A|ASL
*libsqlite.so*|SQLite database|http://www.sqlite.org|Public Domain
*libSR_AudioIn.so and libsrec_jni.so*|Nuance Communications' Speech Recognition engine|N/A|ASL
*libstlport.so*|Implementation of the C++ Standard Template Library|http://stlport.sourceforge.net|Custom, BSD-like
*libttspico.so*|SVOX's Text-To-Speech speech synthesizer engine|N/A|ASL
*libvorbisidec.so*|Tremolo ARM-optimized Ogg Vorbis decompression library|http://wss.co.uk/pinknoise/tremolo/|Custom, BSD-like
*libwebcore.so*|WebKit Open Source Project|http://www.webkit.org|LGPL and BSD
*libwpa_client*|Library based on wpa_supplicant|http://hostap.epitest.fi/wpa_supplicant/|GPL and BSD
*libz.so*|zlib compression library|http://zlib.net|Custom, BSD-like

+ *表 2-3. 由AOSP生成的安卓定制库*

Category|Library(ies)|Description
-|-|-
Bionic|*libc.so; libm.so; libdl.so; libstdc++.so; libthread_db.so;*|C library; Math library; Dynamic linking library; Standard C++ library; Threads library;
Core|*libbinder.so; libutils.so, libcutils.so, libnetutils.so, and libsysutils.so;  libsystem_server.so, libandroid_servers.so, libaudioflinger.so, libsurfaceflinger.so, linsensorservice.so, and libcameraservice.so; libcamera_client.so* and *libsufaceflinger_client.so; libpixelflinger.so; libui.so; liblog.so;*|The Binder library; Various utility libraries; System-service-related libraries; Client libraries for certain system services; The PixelFlinger library; Low-level user-interface-related functionalities, such as user input events handling and dispatching and graphics buffer allocation and manipulation; Sensors-related functions library; The logging library; The Android runtime library;
Dalvik|*lidvm.so; libnativehepler.so*|The Dalvik VM library; JNI-related helper functions;
Hardware|*libhardware.so; libhardware_legacy.so; Various hardware-supporting shared libraries.*|The HAL library that provides hw_get_module() uses dlopen() to load hardware support modules (i.e. shared libraries that provide hardware support to the HAL) on demand; Library providing hardware support for wifi, powermanagement and vibrator; Libraries that provide support for various hardware components, some of which are loaded using through the HAL, while others are loaded automatically by the linker;
Media|*libmediaplayerservice.so; libmedia.so; libstagefright.so; libeffects.so* and the libraries in the *soundfx/* directory; *libdrm1.so* and *libdrm1_jni.so*|The Media Player service library; The low-level media functions used by the Media Player service; The many libraries that make-up the StageFright media framework; The sound effects libraries; The DRM b framework libraries;
OpenGL|*libEGL.so, libETC1.so, libGLESv2.so* and *egl/libGLES_android.so*|Android's OpenGL implementation

#### 初始化

当内核完成启动，它仅仅会调起一个进程，这个进程就是init进程。随后，init负责生成系统中所有其他进程和服务，并执行一些如重启之类的高危操作。传统的Linux发行版使用SystemV init提供init进程，尽管近年来许多发行版都使用了自己的修改版本。如Ubuntu就使用了upstart。在嵌入式Linux系统中，提供init的就是经典的BusyBox包。

安卓引入了自定义的init，也带来了一些新鲜玩意。

##### 配置语言

不同于传统的init，传统init根据当前运行等级配置或请求的脚本使用来决定的，而安卓init定义了自己的配置语义，并根据全局属性值来触发特定的指令。

init的主要配置文件存储在*/init.rc*中，同时也会有一个特定设备的配置文件*/init.**某某设备**.rc*。特定的设备脚本则为*/etc/init.**某某设备**.sh*，这里的**某某设备**指的是设备名称。可以通过修改这些文件达到对系统启动及其行为进行高度控制。例如，你可以禁止Zygote的自启动，并将其改为通过adb命令手动启动。

##### 全局属性

安卓init中非常有趣的一点是，它如何去管理一组全局属性，并且这些属性可以被系统中很多有适当权限的部分访问。有些属性在编译时确定，有些在init配置文件中，也有些在运行时才被设置。有些属性会被保存到存储中被永久使用。属性由init管理，因此它可以检测到任何修改，并根据其配置触发某组命令的执行。

例如之前提及的OOM调整，也是设置为从*init.rc*文件中启动。网络属性也是如此，编译时将该属性写入*/system/build.prop*文件中，并加上编译日期及编译系统详情。当运行时，系统中包含着从IP和GSM配置参数到电池电量上百个属性，使用*getprop*命令可以列出当前的属性及其值。

##### 内核设备管理器事件

正如之前所解释的，可以通过Linux的*/dev*目录访问设备。曾经Linux发行版在该目录中包含了上千目录，以适应可能遇到的设备配置。最终还是有些人提议将这些目录创建为动态形式。一段时间后，系统就使用了*udev*，它的工作依赖于每次向系统中添加或删除硬件时，内核生成的运行时事件。

在大部分Linux发行版中，udev热插拔事件由udevd守护进程处理。而安卓中，这些事件由作为安卓init部分构建的*ueventd*守护进程处理，通过符号链接将*/sbin/ueventd*链至*/init*来访问。想要知道*/dev*中创建了那些条目，*ueventd*依赖于*/ueventd.rc*和*/ueventd.**device_name**.rc*文件

#### 工具箱 Toolbox

如根文件系统目录层级一般，大部分的Linux发行版由FHS在/bin与/sbin路径下都存在着许多二进制文件。这些目录下的二进制文件由网上很多不同站点、不同的包编译而成。在一个嵌入式系统中，处理如此多不同的包或需要如此多分裂的二进制文件都不甚合理。

经典的BusyBox包采取的方法是编译一个独立的二进制文件，这个文件实际上是个巨大的switch-case结构，通过检查命令行中第一个参数，决定执行哪个响应功能。这些指令再软链到busybox命令中。例如当输入ls时，实际上还是在执行BusyBox，但BusyBox根据ls这个参数决定它的行为，就如同在标准命令行中运行这个命令一样。

安卓没有使用BusyBox，但引入了自己的工具——Toolbox。基本功能也是软链至Toolbox的命令中。不过Toolbox不如BusyBox强大，如果你使用过BusyBox，那基本会对Toolbox很失望。重新创造一个类似的工具似乎和许可有关，毕竟BusyBox是GPL许可。另外，一些安卓开发者们的目标是提供一个基于shell的简洁调试工具，并非与BusyBox一样完全取代shell。而使用BSD许可的Toolbox可以让制造商们在不需要向客户提供源码的前提下进行修改和分发。

你或许还是希望使用BusyBox替换Toolbox。如果由于许可原因，不希望将BusyBox作为定版软件的一部分，也可以暂时将BusyBox打包进系统用来调试，再在释放版本时移除。

#### 守护进程

作为系统启动的一部分，安卓的init会启动一些守护进程，并跑完整个系统的生命周期。而如*adbd*，则需要取决于全局属性的设置了。

*表 2-4. 安卓原生守护进程*
Daemon|Description
-|-
servicemanager|The Binder Context Manager. Acts as an index of all Binder services running in the system.
vold|The volume manager. Handles the mounting and formatting of mounted volumes and images.
netd|The network manager. Handles tethering, NAT, PPP, PAN, and USB RNDIS.
debugerd|The debugger daemon. Invoked by Bionic's linker when a process crashes to do a postmortem analysis. Allows *gdb* to connect from the host.
Zygote|The Zygote process. It's responsible for warming up the system's cache and starting the System Server. We'll discuss it in more detail later in this chapter.
mediaserver|The Media server. Hosts most media-related services. We'll discuss it in more detail later in this chapter.
dbus-daemon|The D-Bus message daemon. Acts as an inter mediary between D-Bus users. Have a look at its man page for more information.
bluetooth|The Bluetooth daemon. Manages Bluetooth devices. Provides services through D-Bus.
installd|The *.apk* installtion daemon. Takes care of installing and uninstalling *.apk* files and managing the related filesystem entries.
keystore|The KeyStore daemon. Manages an encrypted key-pair value store for cryptographic keys, SSL certs for instance.
system_server|Android's System Server. This daemon hosts the vast majority of system services that run in Android.
adbd|The ADB daemon. Manages all aspects of the connection between the target and the host's *adb* command.

#### 命令行组件 Command-Line Utilities

安卓根文件系统中分布着超过150个命令行组件。*/system/bin*中就包含了一大部分，也有一些“额外”的存在*/system/xbin*与*/sbin*中。*/system/bin*中有大约50个组件是*/system/bin/toolbox*的软链。余下的主要来自安卓系统框架，AOSP引入的外部项目或AOSP的其他地方。在第五章可以花时间看看这些二进制文件。