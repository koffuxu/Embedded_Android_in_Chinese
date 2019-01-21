Embedded_Android_in_Chinese
===========================



## 描述:

- co-work基地:可夫小子
[公众号](!./source/)
- <Embedded Android>book pdf 文档位于source/下面，请依据这个文档进行翻译
 - <Embedded_Android.pdf>:简单版本
 - <Embedded_Android-full-ver.pdf>:完全版本


## 当前进度

> **很高兴你能参加这个翻译，但无如何，我会努力成这个任务的,不能让其成为我的技术债务**


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
  

## 认领目录

Preface
1. Introduction  
 * History      √by[wiikii]()
 * Features and Characteristics         √by[wiikii]() 
 * Development Model            √by[wiikii]()
 * Differences With "Classic" Open Source Projects      √by[CodeDiving]()
 * Feature Inclusion, Roadmaps, and New Releases        √by[CodeDiving]()
 * Ecosystem    √by[CodeDiving]
 * A Word on the Open Handset Alliance 
 * Getting "Android" 
 * Legal Framework 
 * Code Licenses 
 * Branding Use 
 * Google's Own Android Apps 
 * Alternative App Markets 
 * Oracle v Google 
 * Hardware and Compliance Requirements 
 * Compliance Definition Document 
 * Compliance Test Suite 
 * Development Setup and Tools 

2. Internals Primer
 * App Developer's View 
 * Android Concepts 
 * Framework Intro 
 * App Development Tools 
 * Native Development 
 * Overall Architecture 
 * Linux Kernel 
 * Wakelocks 
 * Low Memory Killer 
 * Binder 
 * Anonymous Shared Memory (ashmem) 
 * Alarm 
 * Logger 
 * Other Notable Androidisms 
 * Hardware Support 
 * The Linux Approach 
 * Android's General Approach 
 * Loading and Interfacing Methods 
 * Device Support Details 
 * Native User-Space 
 * Filesystem layout 
 * Libraries 
 * Init 
 * Toolbox 
 * Daemons 
 * Command-Line Utilities 
 * Dalvik and Android's Java 
 * Java Native Interface (JNI) 
 * System Services 
 * Service Manager and Binder Interaction 
 * Calling on Services 
 * A Service Example: the Activity Manager 
 * Stock AOSP Packages 
 * System Startup 

3. AOSP Jumpstart 
 * Getting the AOSP      √by[koffuxu](https://github.com/koffuxu) 
 * Inside the AOSP       √by[koffuxu](https://github.com/koffuxu)
 * Build Basics          √by[koffuxu](https://github.com/koffuxu)
 * Build System Setup 
 * Building Android 
 * Running Android 
 * Using ADB 
 * Mastering the Emulator 

4. The Build System
 * Comparisons With Other Build Systems 
 * Architecture 
 * Configuration 
 * envsetup.sh 
 * Directive Definitions
 * Main Make Recipes 
 * Cleaning 
 * Module Build Templates 
 * Output 
 * Build Recipes 
 * The Default droid Build 
 * Seeing the Build Commands 
 * Building the SDK for Linux and MacOS 
 * Building the SDK for Windows 
 * Building the CTS 
 * Building the NDK 
 * Updating the API 
 * Building a Single Module 
 * Building Out of Tree 
 * Basic AOSP Hacks 
 * Adding an App 
 * Adding a Native Tool or Daemon 
 * Adding a Native Library 
 * Adding a Device 
 * Adding an App Overlay
