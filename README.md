Embedded_Android_in_Chinese
===========================



## 描述

- co-work基地:可夫小子![公众号](source/wechat.jpg)
- <Embedded Android>book pdf 文档位于source/下面，请依据这个文档进行翻译
    - 第一期：<Embedded_Android.pdf>:简单版本
    - 第二期：<Embedded_Android-full-ver.pdf>:完全版本


## 想说的话

> 很感谢你能参加这个翻译项目，希望你能从中收获一二；
但我想对自己说，你需要努力完成这个任务，不能让其成为技术债务


## github参与简明流程

### 初始化项目
1. 进入项目地址，先fork这个项目到你的项目中
2. 把你fork的项目clone到你本地
3. `git branch dev` 新建一个分支
4. `git checkout dev` 切换到dev分支
5. `git remote add upstream https://github.com/koffuxu/Embedded_Android_in_Chinese` 把项目添加你的远程仓库
6. `git remote update` 把koffuxu的分支拿到你本地
7. `git fetch upstream master` 把koffuxu的maser分支更新到本地
8. `git rebase upstream/master` 更新合并
9. 如果你完成修改，使用 `git push -u origin dev` 提交更新
10. 然后进入你的github网站申请pull request

### 日常更新，之后更新使用如下命令
1. `git remote update upstream`  把koffuxu的修改更新到本地
2. `git rebase upstream/master` 更新合并

- 更多Github操作信息参考：http://blog.csdn.net/koffuxu/article/details/39010803



## 约定

- 使用Markdown进入文本格式，Markdwon[帮助文档](<https://help.github.com/articles/markdown-basics>)
  

## 翻译进度摘要

| 章节 | 状态 | 备注 |
|------|------|------|
| 1.1~1.9 Introduction | ✅ 全部完成 | 2026.04 |
| 2.1~2.9 Internals Primer | ✅ 大部分完成 | 2026.04 |
| 3.1~3.6 AOSP Jumpstart | ✅ 大部分完成 | 2026.04 |
| 4.1 Comparisons With Other Build Systems | ✅ 完成 | 2026.04 |
| 4.2 Architecture | ✅ 完成 | 2026.04 |
| 4.3 Build Recipes | ✅ 完成 | 2026.04 |
| 4.4 Basic AOSP Hacks | ✅ 完成 | 2026.04 |
| 5.1~5.10 Hardware Primer | ✅ 完成 | 2026.04 |
| 6.1~6.x Android Framework | ✅ 完成 | 2026.04 |
| 附录 A Legacy User-Space | ✅ 完成 | 2026.04 |
| 附录 B Adding Support for New Hardware | ✅ 完成 | 2026.04 |
| 附录 C Customizing Default Lists of Packages | ✅ 完成 | 2026.04 |
| 附录 D Default init.rc Files | ✅ 完成 | 2026.04 |
| 附录 E Resources | ✅ 完成 | 2026.04 |

> 本项目支持 AI 辅助翻译，详见 [.claude/skills/pdf-book-translate/](.claude/skills/pdf-book-translate/)

---

# 目录认领

Preface
1. Introduction  
    1. History                               √by[wiikii]()
    1. Features and Characteristics          √完成
    1. Development Model                     √by[wiikii]()
        * Differences With "Classic" Open Source Projects      √by[CodeDiving]()
        * Feature Inclusion, Roadmaps, and New Releases        √by[CodeDiving]()
    1. Ecosystem                             √by[CodeDiving]
        * A Word on the Open Handset Alliance
    1. Getting "Android"
    1. Legal Framework
        * Code Licenses
        * Branding Use
        * Google's Own Android Apps
        * Alternative App Markets
        * Oracle v Google
    1. Hardware and Compliance Requirements
        * Compliance Definition Document
        * Compliance Test Suite
    1. Development Setup and Tools

2. Internals Primer
    1. App Developer's View
        * Android Concepts
        * Framework Intro
        * App Development Tools
        * Native Development
    1. Overall Architecture
    1. Linux Kernel
        * Wakelocks
        * Low Memory Killer
        * Binder
        * Anonymous Shared Memory (ashmem)
        * Alarm
        * Logger
        * Other Notable Androidisms
    1. Hardware Support
        * The Linux Approach
        * Android's General Approach
        * Loading and Interfacing Methods
        * Device Support Details
    1. Native User-Space          ✅ 完成
        * Filesystem layout
        * Libraries
        * Init
        * Toolbox
        * Daemons
        * Command-Line Utilities
    1. Dalvik and Android's Java
        * Java Native Interface (JNI)
    1. System Services
        * Service Manager and Binder Interaction
        * Calling on Services
        * A Service Example: the Activity Manager
    1. Stock AOSP Packages
    1. System Startup

3. AOSP Jumpstart 
    1. Getting the AOSP      √by[koffuxu](https://github.com/koffuxu)
    1. Inside the AOSP       √by[koffuxu](https://github.com/koffuxu)
    1. Build Basics          √by[koffuxu](https://github.com/koffuxu)
        * Build System Setup
        * Building Android
    1. Running Android
    1. Using ADB
    1. Mastering the Emulator

4. The Build System
    1. Comparisons With Other Build Systems      √翻译中
    1. Architecture
        * Configuration
        * envsetup.sh
        * Directive Definitions
        * Main Make Recipes
        * Cleaning
        * Module Build Templates
        * Output
    1. Build Recipes
        * The Default droid Build
        * Seeing the Build Commands
        * Building the SDK for Linux and MacOS
        * Building the SDK for Windows
        * Building the CTS
        * Building the NDK
        * Updating the API
        * Building a Single Module
        * Building Out of Tree
    1. Basic AOSP Hacks
        * Adding an App
        * Adding a Native Tool or Daemon
        * Adding a Native Library
        * Adding a Device
        * Adding an App Overlay

5. Hardware Primer
    1. Embedded System Architecture
    1. The Baseband Processor
    1. Memory
    1.闪存存储
    1. NAND vs. NOR
    1. NAND
    1. NOR
    1. 串行闪存
    1. eMMC 和 eMCP
    1. Development Setup
    1. 评估板

6. Android Framework
    1. 什么是"Android框架层"？
    1. 框架层启动
    1. 系统服务
    1. 启动动画
    1. Dex优化
    1. 应用启动
    1. 工具和命令
    1. 支持守护进程
    1. 硬件抽象层

附录 A: Legacy User-Space
附录 B: Adding Support for New Hardware
附录 C: Customizing Default Lists of Packages
附录 D: Default init.rc Files
附录 E: Resources
