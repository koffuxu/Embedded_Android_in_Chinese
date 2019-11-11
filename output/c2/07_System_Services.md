> 翻译：[Ross.Zeng](https://github.com/zengrx)
> 校对：

### 系统服务

系统服务是安卓系统中的幕后人物。就算没有在谷歌开发者文档中特别提及，任何和安卓相关的东西基本都会使用到其中某一个系统服务。这些服务在一起提供了Linux上层的面向对象功能，也就是Binder机制，所有系统服务构建的目的所在。刚才讨论过的原生用户空间就像是安卓系统服务的一个支持环境。所以了解系统服务的存在，知道它们之间及与系统其他部分如何工作是非常重要的。我们已经包含了一些与安卓硬件支持有关的讨论。

图2-4相较于图2-1第一次详细地展示了系统服务。可以看到这其中包含了很多主要的进程。大部分是系统服务，都跑在*system_server*这个进程下。基本是由一个Java字节码编写的服务与两个C/C++服务组成。系统服务中也包含一些原生代码，经过JNI允许一些基于Java的服务访问系统底层。其他的系统服务位于Media Service中，以*media-server*运行。这些服务都是由C/C++编写，与StageFright及audio effects等多媒体相关的组件一起打包。

注意，尽管只有两个进程撑起了整个安卓系统服务，它们都是以独立的方式通过Binder对服务连接。以下是在安卓模拟器中输出的对*service*组件的结果。

> **# 服务列表**
Found 50 servics:
0    phone: [com.android.internal.telephony.ITelephony]
1    iphonesubinfo: [com.android.internal.telephony.IPhoneSubInfo]
2    simphonebook: [com.android.internal.telephony.IIccPhoneBook]
3    isms: [com.android.internal.telephony.ISms]
4    diskstats: []
5    appwidget: [com.android.internal.appwidget.IAppWidgetService]
6    backup: [android.app.backup.IBackupManager]
7    uimode: [android.app.IUiModeManager]
8    usb: [android.hardware.usb.IUsbManager]
9    audio: [android.media.IAudioService]
10    wallpaper: [android.app.IWallpaperManager]
11    dropbox: [com.android.internal.os.IDropBoxManagerService]
12    search: [android.app.ISearchManager]
13    location: [android.location.ILocationManager]
14    devicestoragemonitor: []
15    notification: [android.app.INotificationManager]
16    mount: [IMountService]
17    accessibility: [android.view.accessibility.IAccessibilityManager]
18    throttle: [android.net.IThrottleManager]
19    connectivity: [android.net.IConnectivityManager]
20    wifi: [android.net.wifi.IWifiManager]
21    network_management: [android.os.INetworkManagementService]
22    netstat: [android.os.INetStatService]
23    input_method: [com.android.internal.view.IInputMethodManager]
24    clipboard: [android.text.IClipboard]
25    statusbar: [com.android.internal.statusbar.IStatusBarService]
26    device_policy: [android.app.admin.IDevicePolicyManager]
27    window: [android.view.IWindowManager]
28    alarm: [android.app.IAlarmManager]
29    vibrator: [android.os.IVibratorService]
30    hardware: [android.os.IHardwareService]
31    battery: []
32    content: [android.content.IContentService]
33    account: [android.accounts.IAccountManager]
34    permission: [android.os.IPermissionController]
35    cpuinfo: []
36    meminfo: []
37    activity: [android.app.IActivityManager]
38    package: [android.content.pm.IPackageManager]
39    telephony.registry: [com.android.internal.telephony.ITelephonyRegistry]
40    usagestats: [com.android.internal.app.IUsageStats]
41    batteryinfo: [com.android.internal.app.IBatteryStats]
42    power: [android.os.IPowerManager]
43    entropy: []
44    sensorservice: [android.gui.SensorServer]
45    SurfaceFlinger: [android.ui.ISurfaceComposer]
46    media.audio_policy: [android.media.IAudioPolicyService]
47    media.camera: [android.hardware.ICameraService]
48    media.player: [android.media.IMediaPlayerService]
49    media.audio_flinger: [android.media.IAudioFlinger]

目前没有太多文档描述各个服务的操作。感兴趣的话可以看看它们的源码，理解和分析它们是如何相互工作的。


#### 服务管理器与Binder交互

如之前所解释的，Binder机制用于系统服务底层面向对象的远程方法调用。一个系统进程通过Binder调用系统服务，首先需要拿到这个服务的句柄。例如，Binder会让应用开发人员在电源管理中通过**WakeLock**类的**acquire()**方法请求一个休眠唤醒锁，在这个调用完成前，开发人员首先需要获取电源管理服务的句柄。在下一章节可以看到，应用实际上将获取句柄的细节隐藏起来，抽象出了一个接口给开发者，如图2-5所示，所有系统服务句柄查找都是通过服务管理器完成的。

![Service Manager and Binder interaction](https://upload-images.jianshu.io/upload_images/2424151-1643d2e062f3ad33.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
*图2-5. 服务管理器与绑定器交互*


将服务管理器想象成系统中可以服务的黄页，如果一个系统服务没有经过服务管理器注册，那它就无法作用于剩下的系统。为了提供这个检索功能，服务管理器会在所有服务起来前被*init*调起。然后服务管理器再打开*/dev/binder*并使用特殊的**ioctl()**使自己成为Binder的*上下文管理器*（见图2-5中的A1）。此后，系统中任何试图与Binder ID 0（即代码各部分中的“magic”Binder或“magic object”）通信的进程，实际上都是通过Binder在与服务管理器通信。

当系统服务起来后，它会通过服务管理器（A2）注册它实例化的每一个服务。之后，当有应用想要访问系统服务，例如电源管理服务，管理器就会问服务（B1）要一个句柄并调用服务的方法（B2）。总之，一个服务组件的调用是应用直接通过Binder（C1）进行的，并不会由服务管理器经手。

服务管理器还会由“dumpsys”单元这一特殊方式使用，它能让你把单个或全部系统服务的状态转出来。为了得到所有服务的列表，它会循环获取系统服务（D1），在迭代器中请求n<sup>th</sup>+1直到不存在。它会通过服务管理器定位到有特殊句柄的那个服务（D2），并调用服务的**dump()**函数在终端中打印出状态信息（D3）

#### 调用服务

上文中解释的这些，基本都是对用户不可见的。下面这一小段示例代码为我们展示应用程序一般是如何申请休眠唤醒锁接口的。

> PowerManager pm = (PowerManager) getSystemService(POWER_SERVICE);
PowerManager.WakeLock wakeLock = pm.newWakeLock(PowerManager.FULL_WAKE_LOCK, "myPerciousWakeLock");
wakeLock.acquire(100);

可以看到这里没有任何服务管理器的痕迹，取而代之的是通过**getSystemService()**传递了**POWER_SERVICE**参数。当然在内部，**getSystemService()**还是使用服务管理器搜索到电源管理服务，并申请创建了一个休眠唤醒锁。

#### 服务示例：活动管理器

虽说介绍每一个系统服务不在本书的范围内，但还是快速过一下活动管理器这个关键的系统服务。活动管理器的资源实际上包含了超过20个文件和两万行代码，非常接近安卓的核心了。它负责启动活动或服务这样的新组件，以及获取内容提供者与上下文广播。如果你之前就见过ANR（应用无响应）对话框。其实活动管理器还参与了内核低内存处理规划，权限以及任务管理等。

例如用户在主屏幕上点击应用图标，启动了一个应用程序，首先启动器的**onClick()**回调被调用。启动器会通过Binder告知活动管理服务通过**startActivity()**方法来处理这个事件。服务继而调用**startViaZygote()**方法，通过套接字通知Zygote启动一个活动。在阅读完本章的最后一节后就可以清晰地理解这些操作。

如果你熟悉Linux的内部结构，将安卓文件中的*kernel/*目录理解为Linux的内核源码，这是一个理解活动管理器的好方法。