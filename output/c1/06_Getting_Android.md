> 翻译：[Ross.Zeng](https://github.com/zengrx)
> 校对：


# 得到"Android"

想要让 Android 在嵌入式设备上运行，需要两样关键组件：一个与 Android 兼容的 Linux 内核，以及 Android 平台（Android Platform）。

长期以来，获取一个与 Android 兼容的 Linux 内核是一件相当困难的事——直到本书写作时也是如此。与其从 http://kernel.org 获取一个"香草版"（vanilla）内核来运行 Android 平台，你需要使用 AOSP 中提供的某个内核版本，或者为 vanilla 内核打上使之和 Android 兼容的补丁。其根本原因在于，Android 开发者对内核做了大量修改，以使他们定制的平台能够运行；这些修改在历史上一直受到主线内核维护者的强烈抵制。

尽管下一章我们会详细讨论内核相关的问题，但要指出的是：从 2011 年在布拉格举行的内核峰会上开始，内核开发者们决定主动推进将运行 Android 平台所需的功能合并到官方 Linux 内核主线中。因此，许多必需的功能已经被合并，另一些则已被（或在本书写作时正在被）其他机制取代或更新。截至目前，获取 Android 适配内核最简便的方法是——向你的 SoC 供应商索取。考虑到 Android 的普及度，大多数主流 SoC 供应商都会为其产品提供完整的 Android 所需组件支持。

Android 平台本质上是一个定制的 Linux 发行版，包含组成"Android"的用户空间软件包。表 1-1 中所列的各版本，实际上都是平台版本。下一章我们将详细讨论平台的内容和架构。目前只需记住：平台版本的角色类似于 Ubuntu 或 Fedora 等标准 Linux 发行版——它是一组自洽的软件包，一旦构建完成，就通过特定的工具、接口和开发者 API 为用户提供特定的用户体验。

> **术语说明**：严格来说，运行在 Android 兼容内核之上的 Android 发行版源代码的正确名称是"Android 平台"（Android Platform），但在实践中它通常被称为"AOSP"——本书通篇采用这一叫法。实际上，托管在 http://android.googlesource.com/ 的 Android 开放源代码项目除了平台本身外，还包含一些额外的组件，如示例 Linux 内核树和额外软件包，这些在用常规 repo 命令获取平台时通常不会下载。

## 二进制逆向

尽管无法访问 Android 源代码，但这并没有阻止热心的逆向爱好者对 Android 进行hack和定制。例如，Android 3.x/Honeycomb 的源代码从未公开，但这并不能阻止逆向爱好者让它运行在 Barnes & Noble Nook 上。他们从 Honeycomb SDK 附带的模拟器镜像中提取可执行二进制文件，直接在 Nook 上使用——当然，代价是失去了硬件加速。类似的hack手法也被用来"root"或更新各型号设备的 Android 组件版本——即使制造商没有提供对应的源代码。
