# 第一章：引言

将 Android 移植进嵌入式设备，是一项极为复杂的任务——既需要对 Android 内部构件有精细的认识，也需要对 Android 开放源代码项目（AOSP）及其运行所依赖的系统内核 Linux 进行巧妙的深度定制。在我们深入嵌入式 Android 开发细节之前，先来了解一些嵌入式开发者接触 Android 时必须考虑的基本要点：Android 的硬件需求、Android 的法律框架，以及在嵌入式场景下引入 Android 所带来的影响。首先，让我们了解 Android 的诞生及其发展历程。

---

> **关于本书版本说明**：本书基于 Android 2.3.x/Gingerbread 撰写。尽管在本书写作期间（2011–2013 年），Android 内部架构大体保持稳定，但由于 Android 采用封闭开发模式，关键变更可能随时悄无声息地出现。例如，在 2.2/Froyo 及更早版本中，状态栏（Status Bar）是 System Server 的一部分；而在 2.3/Gingerbread 中，状态栏被独立出来，成为一个与 System Server 分离的独立进程。
