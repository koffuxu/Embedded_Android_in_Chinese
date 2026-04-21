# 什么是"Android 框架层"？

回顾图 2-1，Android 框架层包括 android.* 包、系统服务、Android 运行时以及部分原生守护进程。从源码角度来说，Android 框架层通常由 AOSP 中 `frameworks/` 目录下所有代码组成。

在某种程度上，我在本书中使用"Android 框架层"来指代在原生用户空间之上运行的几乎所有"Android"相关的内容。因此，我在本章中的解释有时会超出 `frameworks/` 目录的范围——比如 Dalvik 和 HAL，它们本质上是 Android 框架层不可或缺的组成部分。
