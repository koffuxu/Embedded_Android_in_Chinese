# Dex 优化

启动动画期间启动的系统服务之一是**包管理器**（Package Manager）。我们还没有详细介绍它的功能，但简而言之，包管理器管理系统中所有的 `.apk`。除其他外，它处理 `.apk` 的安装和卸载，并帮助活动管理器解析 intent。

包管理器的职责之一也是在相应的 Java 代码执行之前，确保任何 DEX 字节码的 JIT 优化版本都可用。为了实现这一点，包管理器服务（实现为 Java 类）的构造函数会遍历系统中所有的 `.apk` 和 `.jar` 文件，并请求 installd 对它们运行 dexopt 命令。

这个过程只应在首次启动时发生。随后，`/data/dalvik-cache` 目录将包含所有 .dex 文件的 JIT 优化版本，后续启动应该会快得多。如果你查看首次启动时 logcat 的输出，你实际上会看到这样的条目：

```
D/dalvikvm(   32): DexOpt: --- BEGIN 'core.jar' (bootstrap=1) ---
D/dalvikvm(   62): Ignoring duplicate verify attempt on Ljava/lang/Object;
D/dalvikvm(   62): Ignoring duplicate verify attempt on Ljava/lang/Class;
D/dalvikvm(   62): DexOpt: load 349ms, verify+opt 4153ms
D/dalvikvm(   32): DexOpt: --- END 'core.jar' (success) ---
D/dalvikvm(   32): DEX prep '/system/framework/core.jar': unzip in 405ms, rewrite 5337ms
D/dalvikvm(   32): DexOpt: --- BEGIN 'bouncycastle.jar' (bootstrap=1) ---
D/dalvikvm(   63): DexOpt: load 54ms, verify+opt 779ms
D/dalvikvm(   32): DexOpt: --- END 'bouncycastle.jar' (success) ---
D/dalvikvm(   32): DEX prep '/system/framework/bouncycastle.jar': unzip in 48ms, rewrite 1023ms
...
```

最初，包管理器服务尚未运行，因此我们可以看到 Dalvik 直接运行 dexopt 来处理某些 `.jar` 文件，而不是像包管理器服务请求时那样由 installd 运行。一旦包管理器启动，它会按以下顺序运行其余的优化过程：

1. init.rc 中 `BOOTCLASSPATH` 变量中列出的 `.jar` 文件
2. `/system/etc/permission/platform.xml` 中作为库列出的 `.jar` 文件
3. `/system/framework` 中找到的 `.apk` 和 `.jar` 文件
4. `/system/app` 中找到的 `.apk` 文件
5. `/vendor/app` 中找到的 `.apk` 文件
6. `/data/app` 中找到的 `.apk` 文件
7. `/data/app-private` 中找到的 `.apk` 文件

显然，这个过程需要一些时间。在我的四核 CORE i7 上，新编译的 2.3/Gingerbread AOSP 模拟器镜像的首次完整启动（即到主屏幕）需要 75 秒，后续启动需要 24 秒。在生产系统（如手机）上，这样的启动时间可能是无法接受的。

因此，你可能会很高兴听到，你实际上可以在构建时而不是启动时执行这个优化过程。构建 AOSP 时只需设置 `WITH_DEXPREOPT` 构建标志为 true：

```
$ make WITH_DEXPREOPT=true -j16
```

你也可以将这个变量设置在你的设备的 `BoardConfig.mk` 中，从而避免每次都要在 make 命令中添加它。就模拟器构建而言，在 2.3/Gingerbread 中默认没有这样做，但在 4.2/Jelly Bean 中是这样做的。

构建当然会花费更多时间，但在首次启动时会明显更快。在前面提到的工作站上，构建 2.3/Gingerbread 需要 30 分钟而不是 20 分钟（使用 `WITH_DEXPREOPT` 标志）。然而，模拟器镜像在首次启动时 40 秒而不是 75 秒就能启动。当使用该选项时，首次启动后目标的 `/data/dalvik-cache` 目录最终将为空。相反，在构建时，`.odex` 文件被放置在与它们对应的 `.jar` 和 `.apk` 文件相同的文件系统路径中。
