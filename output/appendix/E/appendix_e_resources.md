# 附录 E：资源

关于 Android 的内容比任何一本书所能涵盖的都要多。首先，Android 围绕它有一个活生生的生态系统，很多社区项目。本附录重点介绍随着你 Android 工作的进展你应该探索的主要资源。

## 网站和社区

大量网站和社区与 Android 直接或间接相关。我已在下面尽可能整齐地对它们进行了分类。

### Google

**Android Open Source Project**

Google 的 Android 平台主要网站。它历史上包含更多关于系统的信息，但已被删除。它仍然是获取源码和如何设置开发系统来构建 AOSP 的非常好的参考。它还包含 Android 兼容性计划的最新文档，包括合规性定义文档（Compliance Definition Document）。

**Android Developer**

这是 Google 的应用开发者网站。与平台网站不同，这个网站的文档非常丰富。它包含教程、API 参考、图形设计师指南等。总之，如果你在开发应用，这个网站可以很好地帮助你。

**Android Tools Project Site**

这是包含 Android 开发者工具信息的网站。包括 SDK、Eclipse 插件、NDK 等。

### SoC 供应商

**TI Android Development Kit for Sitara**

这个开发套件包括一组已定制为在基于 TI 芯片（如 BeagleBone）的开发板上运行的 AOSP 源码。你也可以在这里找到可用的移植信息。

**Linaro Android**

根据其网站，"Linaro 是一个非营利性工程组织，整合和优化开源 Linux 软件和工具，为 ARM 架构服务。"实际上，它是一个为多个 SoC 供应商服务的组织，帮助他们进行平台使能工作。他们为其成员维护一个可免费下载的 Android 树。

**CodeAurora**

这是 Linux Foundation Labs 的一部分，为 Qualcomm 芯片的各种开源项目提供使能。因此，它维护着一个 Android 树。

### 分支版本

除了在它们网站上提供的信息之外，其中许多分支版本都有公开的邮件列表，你可能会觉得有用。

**CyanogenMod**

这可能是最受欢迎的 Android 分支版本。它本质上是一个面向技术人员和高级用户的售后 AOSP 发行版，具有附加功能和改进。最有趣的是，所有开发都是开放的。

**Android-x86**

这是一个与英特尔将 x86 支持合并到主要 AOSP 树的工作分开的项目。相反，这是面向将 Android 移植到 PC、上网本和笔记本电脑的项目。

**RowBoat**

这是由 TI 维护的社区项目，TI Android 开发套件由此派生。

**Replicant**

这个项目旨在尽可能用自由软件替换尽可能多的 Android 组件。例如，它包括 F-Droid，一个自由软件应用目录（本质上是 Google Play 的自由软件版本）。

除了上面的列表之外，还有大量且仍在增长的 AOSP 闭源分支版本。请记住，Android 的许可非常宽松。

### 文档和论坛

**Linux Weekly News**

所有与内核开发相关事物的主要新闻网站。Android 在相关时会被报道，但重点肯定是经典 Linux 发行版和 Linux 内核。

**Embedded Linux Wiki**

一个包含大量与嵌入式 Linux 相关信息的 wiki 站点。一段时间以来，它也有一个 Android 部分。

**OMAPpedia**

这个 wiki 包含有关在 TI OMAP 处理器上使用 Linux 和 Android 的信息。有些文章包含非常详细的说明。

**XDA Developers**

虽然这个网站传统上是模组制作者常去的地方，但它有时包含的信息在其他地方很难获得。看看 Android 部分。这里发现的大多数有价值的信息都在网站的论坛中。

**Slideshare**

这是一个用于分享幻灯片的通用网站。它包含大量 Android 相关的幻灯片，包括许多关于其内部结构或各种内部组件的内容。

**Vogella**

这个网站由 Lars Vogel 维护，提供各种关于 Android 应用开发的教程。它是与 Google 发布的官方 Android 应用开发信息的非常好的补充。

### 嵌入式 Linux 构建工具

**BuildRoot**

这个项目已经存在了十多年，允许你基于提供给它的配置（使用基于菜单的系统）为嵌入式 Linux 目标构建根文件系统和工具。

**Yocto Project**

与 BuildRoot 类似，但目标更为宏大。它包含用于生成完整嵌入式 Linux 发行版的框架和工具。

### 硬件项目

**BeagleBoard 和 BeagleBone**

市场上有许多廉价的评估板。然而，BeagleBoard 和 BeagleBone 已经积累了非常活跃的社区。提供了原理图。

## 图书

**《构建嵌入式 Linux 系统》第 2 版**，Karim Yaghmour、Jon Masters、Gilad Ben-Yossef 和 Philippe Gerum 著（O'Reilly，2008）

关于嵌入式 Linux 主题的经典书籍，最初由我撰写，此后在 Jon Masters 的带领下进行了更新。

**《嵌入式 Linux 入门》第 2 版**，Christopher Hallinan 著（Prentice Hall，2010）

另一本好的嵌入式 Linux 书籍。

**《Linux 设备驱动程序》第 3 版**，Jonathan Corbet、Alessandro Rubini 和 Greg Kroah-Hartman 著（O'Reilly，2005）

尽管年代久远，这仍然是 Linux 设备驱动程序作者的参考书。

**《Linux 内核开发》第 3 版**，Robert Love 著（Addison-Wesley，2010）

经受住时间考验的内核内部书籍之一。

**《Linux 内核架构》**，Wolfgang Mauerer 著（Wrox，2008）

另一本内部结构方面的书籍。

**《编程 Android》第 2 版**，Zigurd Mednieks、Laird Dornin、Blake Meike 和 Masumi Nakamura 著（O'Reilly，2012）

一本关于应用开发的深度书籍。

**《学习 Android》**，Marko Gargenta 著（O'Reilly，2011）

一本关于应用开发的入门书籍。

**《专业 Android 4 应用开发》**，Reto Meier 著（Wrox，2012）

Google Android 开发者关系团队技术负责人写的应用开发书籍。

## 会议和活动

**Android Builders Summit**

AOSP 栈内部进行开发的人员的主要活动。

**Embedded Linux Conference**

所有嵌入式 Linux 相关事物的主要活动。

**Embedded Linux Conference Europe**

ELC 的欧洲站。

**Linaro Connect**

Linaro 用于将其成员和开发者聚集在一起的活动。

**AnDevCon**

主要的应用开发者会议。也有一些平台演讲。
