# 基础 AOSP 技巧

你买这本书最大的目的可能就是——hack AOSP 来满足自己的需求。接下来几页中，我们会探讨一些你很可能最想尝试的常见技巧。当然，这里只是铺垫，主要涉及与编译系统相关的部分。

### 添加应用

为你的开发板添加一个应用相对直接。先创建一个存放应用源码的目录，例如在 `packages/apps/` 下新建一个目录，然后在其中创建 Android.mk 文件：

```bash
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := MyApp
LOCAL_SRC_FILES := $(call all-java-files-under, src)
include $(BUILD_PACKAGE)
```

构建时，执行 `make MyApp`，编译产物（.apk）会输出到 `out/target/product/<product>/system/app/`。

### 添加原生工具或守护进程

与上述添加应用的方式类似，也可以为开发板添加原生工具或守护进程。在 `external/` 或 `system/` 下创建对应的目录和 Android.mk：

```bash
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := my_tool
LOCAL_SRC_FILES := my_tool.c
include $(BUILD_EXECUTABLE)
```

守护进程还需要在 init 脚本中添加启动配置（init.rc）。

### 添加原生库

像应用和二进制文件一样，也可以为开发板添加原生库。创建 Android.mk 并使用相应的库模板：

```bash
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := libmylib
LOCAL_SRC_FILES := mylib.c
include $(BUILD_SHARED_LIBRARY)
```

使用 `make libmylib` 编译，库文件（.so）会输出到 `out/target/product/<product>/system/lib/`。

### 添加设备

添加自定义设备很可能是最高优先级的需求之一（如果不是排第一的话）。设备配置主要通过 `device/<vendor>/<device>/` 目录下的 BoardConfig.mk 文件完成，该文件指定：

- CPU 架构和变体
- 内核命令行参数
- 分区布局
- HAL 模块路径
- 产品特定配置

在 `device/<vendor>/<device>/` 下创建目录，添加 AndroidProducts.mk 和 BoardConfig.mk，然后在 `lunch` 菜单中选择对应的产品即可。

### 添加应用覆盖层

应用覆盖层（App Overlay）用于在不修改原始应用源码的情况下替换应用资源（图片、字符串、布局等）。在 `vendor/<vendor>/overlay/` 下创建对应应用名称的目录结构，按照标准 Android 资源组织方式放置替换文件即可。编译系统会自动将覆盖层资源优先于默认资源编译进最终镜像。
