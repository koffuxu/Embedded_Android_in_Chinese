> 翻译：[koffuxu](https://github.com/koffuxu)

> 校对：

# 编译基础
现在我们已经下载好了AOSP，那我们就产生一个里面有什么的想法，所以，我们让其运行起来。但，最重要的是我们首先要能够编译它。我们需要确认在我们的Ubuntu上已经安装了必要的包。接下来的操作是基于Ubuntu 11.04。就算你是使用比这新或者旧版本的基于Debian的Linux改造版本，这些操作应该也是相近的。（参考[在非Ubuntu系统或者虚拟机上编译]()72页那些能够编译AOSP的其它系统）

## 编译系统设置

首先，在我们的开发系统中安装一些基础的包。如果你在其它开发的过程中安装了一些这种包，OK，没问题。Ubuntu系统包管理系统将忽略这些包安装。

```
$ sudo apt-get install bison flex gperf git-core gnupg zip tofrodos \ 
> build-essential g++-multilib libc6-dev libc6-dev-i386 ia32-libs mingw32 \ 
> zlib1g-dev lib32z1-dev x11proto-core-dev libx11-dev \ 
> lib32readline5-dev libgl1-mesa-dev lib32ncurses5-dev

```

你也许也需要修正一些符号链接：

```
$ sudo ln -s /usr/lib32/libstdc++.so.6 /usr/lib32/libstdc++.so
$ sudo ln -s /usr/lib32/libz.so.1 /usr/lib32/libz.so
```

最后，你需要安装 Sun公司的JDK：

```
$ sudo add-apt-repository "deb http://archive.canonical.com/ natty partner"
$ sudo apt-get update
$ sudo apt-get install sun-java6-jdk
```

你的系统现在可以准备编译Android了。明显地，在你的以后编译Android的时候，不需要再安装这些包。在你每台Android开发系统只需要设置一次。

## 编译Android

现在我们开始编译Andorid，首先进入下载好源码的目录，设置编译系统：


```

$ cd ~/android/aosp-2.3.x
$ . build/envsetup.sh
$ lunch
You're building on Linux
Lunch menu... pick a combo:
     1. generic-eng
     2. simulator
     3. full_passion-userdebug
     4. full_crespo4g-userdebug
     5. full_crespo-userdebug
Which would you like? [generic-eng] ENTER
============================================
PLATFORM_VERSION_CODENAME=REL
PLATFORM_VERSION=2.3.4
TARGET_PRODUCT=generic
TARGET_BUILD_VARIANT=eng
TARGET_SIMULATOR=false
TARGET_BUILD_TYPE=release
TARGET_BUILD_APPS=
TARGET_ARCH=arm
HOST_ARCH=x86
HOST_OS=linux
HOST_BUILD_TYPE=release
BUILD_ID=GINGERBREAD
============================================

```

注意，我们输入点（.），`空格`，和`build/envsetup.sh`。这是在当面终端强制Shell运行这个`envsetup.sh`脚本。当我们运行这个脚本，Shell将产生一个新的Shell命令和运行这个Shell的脚本。在设置之前，envsetuo.sh中定义的Shell命令将不能使用，同时，接下来的编译需要设置环境变量。

以后我们来再深入了解`evnsetup.sh`和`lunch`。现在，注意`generic-eng` *combo*意思是我们配置编译系统，产生一个运行在Android模拟器的镜像。应用开发人员在工作站上使用SDK来开发APP程序，可以放在这个模拟器上测试，尽管这将运行客户化的图片，而不是SDK默认的部分。当Android开发小组手头没有Android设备的时候，他们就可以使用模拟器来开发。所以这个不是真实的硬件，同时这并不是很完美的目标。但这仍然是有意义的，它基本上考虑了较多种情况。只要你知道你确定的平台，你就能适配以下章节提到的这些指令，也许参考(*Building Embedded Linux Systems*)[]就有些帮助，去得到定制化的Android镜像，加载到你的设备上，然后你的硬件启动它们。

现在环境已经设置好了，我们就能真正的开始编译Android了。

```
$ make -j16
============================================
PLATFORM_VERSION_CODENAME=REL
PLATFORM_VERSION=2.3.4
TARGET_PRODUCT=generic
TARGET_BUILD_VARIANT=eng
TARGET_SIMULATOR=false
TARGET_BUILD_TYPE=release
TARGET_BUILD_APPS=
TARGET_ARCH=arm
HOST_ARCH=x86
HOST_OS=linux
HOST_BUILD_TYPE=release
BUILD_ID=GINGERBREAD
============================================
Checking build tools versions...
find: `frameworks/base/frameworks/base/docs/html': No such file or directory
find: `out/target/common/docs/gen': No such file or directory
find: `frameworks/base/frameworks/base/docs/html': No such file or directory
find: `out/target/common/docs/gen': No such file or directory
find: `frameworks/base/frameworks/base/docs/html': No such file or directory
find: `out/target/common/docs/gen': No such file or directory
find: `frameworks/base/frameworks/base/docs/html': No such file or directory
find: `out/target/common/docs/gen': No such file or directory
find: `frameworks/base/frameworks/base/docs/html': No such file or directory
find: `out/target/common/docs/gen': No such file or directory
host Java: apicheck (out/host/common/obj/JAVA_LIBRARIES/apicheck_intermediates/classes)
Header: out/host/linux-x86/obj/include/libexpat/expat.h
Header: out/host/linux-x86/obj/include/libexpat/expat_external.h
Header: out/target/product/generic/obj/include/libexpat/expat.h
Header: out/target/product/generic/obj/include/libexpat/expat_external.h
Header: out/host/linux-x86/obj/include/libpng/png.h
Header: out/host/linux-x86/obj/include/libpng/pngconf.h
Header: out/host/linux-x86/obj/include/libpng/pngusr.h
Header: out/target/product/generic/obj/include/libpng/png.h
Header: out/target/product/generic/obj/include/libpng/pngconf.h
Header: out/target/product/generic/obj/include/libpng/pngusr.h
Header: out/target/product/generic/obj/include/libwpa_client/wpa_ctrl.h
Header: out/target/product/generic/obj/include/libsonivox/eas_types.h
Header: out/target/product/generic/obj/include/libsonivox/eas.h
Header: out/target/product/generic/obj/include/libsonivox/eas_reverb.h
Header: out/target/product/generic/obj/include/libsonivox/jet.h
Header: out/target/product/generic/obj/include/libsonivox/ARM_synth_constants_gnu.inc
host Java: clearsilver (out/host/common/obj/JAVA_LIBRARIES/clearsilver_intermediates/classes)
target Java: core (out/target/common/obj/JAVA_LIBRARIES/core_intermediates/classes)
host Java: dx (out/host/common/obj/JAVA_LIBRARIES/dx_intermediates/classes)
Notice file: frameworks/base/libs/utils/NOTICE -- out/host/linux-x86/obj
    /NOTICE_FILES/src//lib/libutils.a.txt
Notice file: system/core/libcutils/NOTICE -- out/host/linux-x86/obj/NOTICE_FILES/src//lib
    /libcutils.a.txt
...
```

现在，你可以去吃点零售，或者看看今天晚上的曲棍球比赛。需要引起你注意的是，你编译的时间是依赖于你的系统性能。在一台启用超线程的四核CORE i7的笔记本电脑中，装备8G内存，执行这个命令后大概20分钟编译完AOSP。在一台老式笔记本电脑上，双核 Centro 2的Inter处理器，拥有2G内存，执行`*make -j4*`来编译同一套AOSP的话大概要花费一个小时。注意在`*make*`之后接的`*-j*`参数是指定并行多少个任务。有一种说法是这个最佳值是你的处理器核的2倍，那就是我们刚才指定的。另一种说法是你处理器核的数量再加2。按按照这种说法，我们应该使用10和4而不是16和4。 


> ## 在非Ubuntu系统和虚拟机上编译
我经常被问到在虚拟机上编译AOSP的问题；大部分是因为开发团队，或者IT部门的标准工作环境是Windows。然后这项工作是整理我自己的图片来完成，你的结果也许有点不一样。在虚拟机上编译与在真实的机器上编译通常要花费多两倍时间。所以，如果你有许多工作要在AOSP上完成，我强烈建议你在真实的机器上编译。是的，你手头需要一台Linux环境的电脑。
越来越多的开发者更喜欢在Mac OS X上开发，而不是Linux或者Windows。包括Google自己内部员工。因此，官方在[http://source.android.com]()的编译说明是基于Mac的描述。这些说明倾向于Mac OS更新后被打断，对于基于Mac开发者，幸运的是，他们数量众多，而且是热心的。因此，在Mac OS更新之后，你在网站或者在众多的Google小组里面最终会找到怎样编译AOSP，更新的说明。这有一篇文章是说明怎样在Mac OS X Lion上编译Gingerbread：[Building Gingerbread on OS X Lion]()。记住，我在(第一章)[]已经提到，Google自己的Android是在基于Ubuntu上顺利编译。如果你选择在Mac OS上编译，那么你将一直扮演一个对接角色。最坏的情况，你可以在Windows使用VM虚拟机这种情况。
如果你选择走VM路线，确保你的配置是VM虚拟机使用你系统具备的多个CPU。我之前看到的许多BIOS设置中，“使能CPU指令集允许多CPU虚拟化”这项是禁止的。例如，当这些指令集禁的时候，如果你申请多个CPU时，在*VitrualBox*平台会产生*obscur错误*。你必须进入BIOS，并且使能这个选项，授权你的虚拟机使用多个CPU。

这还有些编译的事需要考虑到。首先，注意在打印编译配置和打印真正的编译（这里会打印`“host Java: apicheck (out/host/common/o...”`）之间，除了打印`“No such file or directory”`这个之外，将持续一段时间没有任何打印。我在后面将解决这种延时。现在要说的就是，找出怎样编译AOSP的每一部分，在整个编译的过程中。

同样也要注意，你将看到一些警告声明。这些是正常的，不是与维护软件质量那么地位重要，但是在整个Android的编译的过程是常见了。这对最终产品的编译不会有什么影响的。所以，与我们中最好的软件工程师相反的是，我必须建议你完全忽略这些警告，专注于解决错误上来。当然，这些警告要防止它们来自你的添加部分上。也就是说，确保你不能新加警告。
