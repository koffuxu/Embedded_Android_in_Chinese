# 附录 B：为新硬件添加支持

在某些情况下，你的嵌入式系统包含的硬件在 Android 中尚未得到支持。虽然你可以在 AOSP 内部完成部分模块化工作，但为新型硬件添加支持则更为复杂，因为它需要了解 Android 的一些内部机制。本附录向你展示如何扩展 Android 的各个层以支持你自己的硬件类型。

虽然你可能对在实际系统中为新型硬件添加支持不感兴趣，但如果你试图理解 Android 栈各个层实际如何组合在一起的复杂细节，你可能会觉得本附录具有指导意义。

此外，虽然本附录使用 2.3/Gingerbread 代码库演示修改，但在 4.2/Jelly Bean 中，被修改的机制和 Java 代码非常相似。在存在重大差异的地方，文中会指出。

## 基础

正如我们在第 2 章讨论的，与标准" vanilla Linux"不同，Android 在硬件上运行不仅仅需要适当的设备驱动程序。它实际上定义了一个新的**硬件抽象层**（HAL），该层为 Android 内核支持的每种硬件类型定义了一个 API。为了让硬件组件正确地与 Android 接口，它必须有一个符合为该类型硬件指定的 API 的相应硬件"模块"（与内核模块无关）。

通常，Android 支持的每种硬件类型都有相应的系统服务和 HAL 定义。有灯光服务和灯光 HAL 定义。有 WiFi 服务和 WiFi HAL 定义。电源管理、位置、传感器等也是如此。我们在第 2 章的图 2-3 中说明了 Android 硬件支持的总体架构。当然，这些系统服务中的大多数通常如我们之前讨论的那样在系统服务器内运行。

HAL 模块有两个大类：通过运行时调用 `dlopen()` 显式加载的模块，以及由动态链接器自动加载的模块（因为它们都链接到 `libhardware_legacy.so`）。前者的 API 在 `hardware/libhardware/include/hardware/` 中，后者的 API 在 `hardware/libhardware_legacy/include/hardware_legacy/` 中。趋势似乎是 Android 正在远离"遗留"方式。这些 `.so` 文件与实际驱动程序通过 `/dev` 条目或其他方式的接口由制造商指定。Android 不关心那个。它只关心找到适当的 HAL `.so` 模块。

我经常被问到的问题之一是："如何在 Android 中为我自己的硬件类型添加支持？"为了说明这一点，我创建了一个 `opersys-hal-hw` 类型，并在 GitHub 上发布了实现此 HAL 类型的代码，以及一个非常基本的环形缓冲区驱动程序。

如果你将 opersys-hal-hw 项目的内容复制到现有 AOSP 2.3.7_r1 版本并为模拟器构建它，你应该会得到一个带有 `opersys` 服务的镜像。后者依赖于环形缓冲区来实现一种非常基本的新型硬件类型。显然，这只是一个骨架，让你了解为新型硬件类型添加支持需要什么。你的硬件可能有完全不同的接口。

## 系统服务

为了说明如何实现新的系统服务，我首先在 `frameworks/base/services/java/com/android/server/` 中添加了一个 `OpersysService.java`。该文件实现了 `OpersysService` 类，它向外部世界提供两个非常基本的调用：

```java
public String read(int maxLength)
{
...
}
public int write(String mString)
{
...
}
```

如果你追踪新型硬件的代码，你会发现我如何在 Android 的每一层添加了这些调用的相应实现。例如，如果你查看系统服务的 `read()` 函数，它做了类似这样的事情：

```java
public String read(int maxLength)
{
    int length;
    byte[] buffer = new byte[maxLength];
    length = read_native(mNativePointer, buffer);
    return new String(buffer, 0, length);
}
```

这里最重要的部分是调用 `read_native()`，它本身在 `OpersysService` 类中声明如下：

```java
private static native int read_native(int ptr, byte[] buffer);
```

通过将方法声明为 `native`，我们指示编译器不要在任何 Java 代码中查找该方法。相反，它将在运行时通过 JNI 提供给 Dalvik。事实上，如果你查看 `frameworks/base/services/jni/` 目录，你会注意到 `Android.mk` 和 `onload.cpp` 被修改为包含一个新的 `com_android_server_OpersysService.cpp`。后者有一个 `register_android_server_OpersysService()` 函数，在加载 `libandroid_servers.so` 时被调用，而 `libandroid_servers.so` 本身是由我刚才提到的 `Android.mk` 生成的。那个注册函数告诉 Dalvik 关于 `com_android_server_OpersysService.cpp` 中为 `OpersysService` 类实现的原生方法以及如何调用它们：

```cpp
static JNINativeMethod method_table[] = {
    { "init_native", "()I", (void*)init_native },
    { "finalize_native", "(I)V", (void*)finalize_native },
    { "read_native", "(I[B)I", (void*)read_native },
    { "write_native", "(I[B)I", (void*)write_native },
    { "test_native", "(II)I", (void*)test_native},
};
int register_android_server_OpersysService(JNIEnv *env)
{
    return jniRegisterNativeMethods(env, "com/android/server/OpersysService",
            method_table, NELEM(method_table));
};
```

上述结构每个方法包含三个字段。第一个字段是在 Java 类中定义的方法名称，而最后一个字段是当前文件中相应的 C 实现。在这种情况下，名称是匹配的——它们在 Android 大多数情况下都是这样——但这不必是这种情况。中间参数看起来可能更神秘一些。括号内的内容是从 Java 传递的参数，括号右侧的字母是返回值。例如，`init_native()` 不接受任何参数并返回一个整数，而 `read_native()` 有两个参数：一个整数和一个字节数组，并返回一个整数。

随着你开始使用 Android 的内部结构，你经常会遇到像这样的 JNI 问题。我建议你看一下 Sheng Liang 的《Java Native Interface：程序员指南和规范》（Addison-Wesley）以获取有关 JNI 使用的更多信息。

以下是 `read_native()` 的实现：

```cpp
static int read_native(JNIEnv *env, jobject clazz, int ptr, jbyteArray buffer)
{
    opersyshw_device_t* dev = (opersyshw_device_t*)ptr;
    jbyte* real_byte_array;
    int length;
    real_byte_array = env->GetByteArrayElements(buffer, NULL);
    if (dev == NULL) {
        return 0;
    }
    length = dev->read((char*) real_byte_array, env->GetArrayLength(buffer));
    env->ReleaseByteArrayElements(buffer, real_byte_array, 0);
    return length;
}
```

首先，注意这里有两个比上面 JNI 声明更多的参数。所有 JNI 调用都以两个相同的参数开头：一个调用 VM 的句柄（`env`），以及一个与调用类对应的 `this` 对象（`clazz`）。另外，注意字节数组不是原样使用的。相反，在开始和结束时使用 `env->GetByteArrayElements()` 和 `env->ReleaseByteArrayElements()` 来获取并在之后释放一个可以被当前 C 代码使用的 C 数组。实际上，不要忘记 JNI 调用将 Java 类型对象带入 C 世界。虽然某些东西（如整数）可以原样使用，但其他对象（如数组）需要在使用之前和之后进行转换。

最重要的是，`read_native()` 的操作部分是调用 `dev->read()`。但这个函数指针指向什么？要理解那部分，你需要查看 `init_native()`：

```cpp
static jint init_native(JNIEnv *env, jobject clazz)
{
    int err;
    hw_module_t* module;
    opersyshw_device_t* dev = NULL;
    err = hw_get_module(OPERSYSHW_HARDWARE_MODULE_ID, (hw_module_t const**)
          &module);
    if (err == 0) {
        if (module->methods->open(module, "", ((hw_device_t**) &dev)) != 0)
           return 0;
    }
    return (jint)dev;
}
```

这个函数中发生了两件重要的事情。首先，调用 `hw_get_module()` 请求 HAL 加载实现 `OPERSYSHW_HARDWARE_MODULE_ID` 类型硬件支持的模块。其次，是对加载模块的 `open()` 函数的调用。我们将在下面看看这两者，但目前请注意，前者将导致一个 `.so` 被加载到系统服务的地址空间中，而后者将导致该库中实现的硬件特定函数（如 `read()` 和 `write()`）可以从 `com_android_server_OpersysService.cpp` 调用——这本质上是我们正在添加的新系统服务的 C 端。

## HAL 及其扩展

位于 `hardware/` 中的 HAL 提供了上面的 `hw_get_module()` 调用。如果你追踪代码，你会发现 `hw_get_module()` 最终调用了经典的 `dlopen()`，这使我们可以将共享库加载到进程的地址空间中。

如果你想在任何 Linux 工作站上获取有关 `dlopen` 及其用法的更多信息，请在上面输入 `man dlopen`。

然而，HAL 不会仅仅加载任何共享库。当你请求给定的硬件类型时，它会在 `/system/lib/hw` 中查找与该给定硬件类型及其运行的设备匹配的文件名。例如，在这种新型硬件的情况下，它会查找 `opersyshw.goldfish.so`，其中 goldfish 是模拟器的代号。用于文件名中间部分的设备实际名称是从以下全局属性之一检索的：`ro.hardware`、`ro.product.board`、`ro.board.platform` 或 `ro.arch`。此外，共享库必须有一个提供 HAL 信息且名为 `HAL_MODULE_INFO_SYM_AS_STR` 的结构。接下来我们将看到一个例子。

新型硬件类型本身的定义只是另一个头文件，在这种情况下是 `opersyshw.h`，与其他 `hardware/libhardware/include/hardware/` 中的硬件定义放在一起：

```cpp
#ifndef ANDROID_OPERSYSHW_INTERFACE_H
#define ANDROID_OPERSYSHW_INTERFACE_H
#include <stdint.h>
#include <sys/cdefs.h>
#include <sys/types.h>
#include <hardware/hardware.h>
__BEGIN_DECLS
#define OPERSYSHW_HARDWARE_MODULE_ID "opersyshw"
struct opersyshw_device_t {
    struct hw_device_t common;
    int (*read)(char* buffer, int length);
    int (*write)(char* buffer, int length);
    int (*test)(int value);
};
__END_DECLS
#endif // ANDROID_OPERSYSHW_INTERFACE_H
```

除了 `read()` 和 `write()` 的原型定义之外，还要注意这是定义 `OPERSYSHW_HARDWARE_MODULE_ID` 的地方。后者作为在文件系统中查找包含实际 HAL 模块实现的文件名的基础。

## HAL 模块

理论上，每个设备都需要一个不同的 HAL 模块来支持 Android 的给定硬件类型。例如，来自不同厂商的手机可能使用不同的图形芯片，因此可能有不同的 gralloc 模块。通常，HAL 模块被添加到 AOSP 源码中的 `device/<vendor>/<product>/` 内的 `lib*` 目录中。然而，在模拟器的情况下，它支持的虚拟设备在 `sdk/emulator/` 中，这就是我们的硬件类型的 Goldfish 实现被添加的地方。

`opersyshw` 硬件类型并不是很花哨，因此 Goldfish 的实现适合放在一个文件 `opersyshw_qemu.c` 中。为了使构建这个文件产生的库被识别为一个真正的 HAL 模块，它以以下片段结尾：

```cpp
static struct hw_module_methods_t opersyshw_module_methods = {
    .open = open_opersyshw
};
const struct hw_module_t HAL_MODULE_INFO_SYM = {
    .tag = HARDWARE_MODULE_TAG,
    .version_major = 1,
    .version_minor = 0,
    .id = OPERSYSHW_HARDWARE_MODULE_ID,
    .name = "Opersys HW Module",
    .author = "Opersys inc.",
    .methods = &opersyshw_module_methods,
};
```

注意名为 `HAL_MODULE_INFO_SYM` 的结构的存在。此外，要注意 `opersyshw_module_methods` 以及它包含的 `open()` 函数指针。这正是之前一旦 HAL 模块被加载时由 `init_native()` 调用的同一个 `open()`。以下是相应的 `open_opersyshw()` 做什么：

```cpp
static int open_opersyshw(const struct hw_module_t* module, char const* name,
        struct hw_device_t** device)
{
    struct opersyshw_device_t *dev = malloc(sizeof(struct opersyshw_device_t));
    memset(dev, 0, sizeof(*dev));
    dev->common.tag = HARDWARE_DEVICE_TAG;
    dev->common.version = 0;
    dev->common.module = (struct hw_module_t*)module;
    dev->read = opersyshw_read;
    dev->write = opersyshw_write;
    dev->test = opersyshw_test;
    *device = (struct hw_device_t*) dev;
    fd = open("/dev/circchar", O_RDWR);
    D("OPERSYS HW has been initialized");
    return 0;
}
```

这个函数的主要目的是初始化 `dev` 结构体（它是 `opersyshw_device_t` 类型，与 `opersyshw.h` 定义的那个相同），并打开 `/dev` 中相应的设备条目，从而连接到加载到内核中的底层设备驱动程序。显然，某些设备驱动程序可能需要在这里进行一些初始化，但对于我们的目的来说这就足够了。

最后，以下是 `opersyshw_read()` 做什么：

```cpp
int opersyshw_read(char* buffer, int length)
{
    int retval;
    D("OPERSYS HW - read()for %d bytes called", length);
    retval = read(fd, buffer, length);
    return retval;
}
```

我们这里没有做太多错误检查，但在你的情况下你应该做。例如，我们甚至没有检查打开设备驱动程序的调用是否成功。通常我们应该检查。不过，调用路径应该很清楚。系统服务的 `read()` 调用导致对 `read_native()` 的 JNI 调用，通过 HAL 导致对 HAL 模块的 `opersyshw_read()` 的调用。

现有系统服务和 HAL 组件具有类似的调用路径。然而，大多数在它们的系统服务中定义了更多数量的调用，因此在为它们的特定硬件类型提供支持所涉及的各个层之间发生的事情也更多。

## 调用系统服务

到目前为止，我们的重点主要是新系统服务如何与下层接口。我们还没有讨论系统服务如何让自己可以通过 Binder 被其他系统服务和应用调用。至少，必须有一个接口定义才能使系统服务可通过 Binder 调用。在 `opersys` 服务的情况下，我们可以将一个 `IOpersysService.aidl` 文件添加到 `frameworks/base/core/java/android/os/`：

```java
package android.os;
/**
* {@hide}
*/
interface IOpersysService {
/ String read(int maxLength);
 int write(String text);
}
```

## 通过 getSystemService() 调用

为了让管理器通过 `getSystemService()` 可用，还需要两个步骤。首先，我们将修改 `frameworks/base/core/java/android/content/Context.java`，以识别一种新的系统服务类型：

```java
// 在 Context 类中添加：
public static final String OPERSYS_SERVICE = "opersys";
```

然后，我们需要将服务注册到 `ServiceManager`。在 2.3/Gingerbread 中，这通常在 `SystemServer.java` 中完成。在 4.2/Jelly Bean 中，`getSystemService()` 的内部实现与你之前看到的代码非常不同。看看 `ContextImpl` 类中 `registerService()` 的使用方式。

## 注意事项和建议

我刚才向你展示的方法和我引用的代码对于向 AOSP 添加新型硬件类型非常有效。然而，这是非常特定于版本的，因为你需要修改的代码因 Android 版本而异。此外，HAL 接口往往随着每个新版本的 Android 而变化。

在尝试为 Android 添加新型硬件支持之前，我强烈建议你首先查看 Android 源代码中现有的 HAL 实现。例如，如果你想为一种新型传感器添加支持，看看现有的传感器 HAL 实现是如何工作的。这样你就可以更好地理解所需的接口和实现模式。

最后，如果你发现自己需要为 Android 添加新型硬件支持，这通常表明你的硬件供应商或 SoC 制造商应该已经提供了这种支持。在大多数情况下，他们应该有现成的 HAL 模块和文档，可以帮助你完成这个过程。
