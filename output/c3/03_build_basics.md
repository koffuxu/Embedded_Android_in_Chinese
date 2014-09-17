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


