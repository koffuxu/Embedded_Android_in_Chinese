# AOSP Jumpstart

Figure 2-4. System Services
System Services
System services are Android's man behind the curtain. Even if they aren't explicitly
mentioned in Google's app development documentation, anything remotely interesting
in Android goes through one of about 50 system services. These services cooperate
together to collectively provide what essentially amounts to an object-oriented OS built
on top of Linux, which is exactly what Binder— the mechanism on which all system
services are built—was intended for. The native user-space we just covered is actually
designed very much as a support environment for Android's system services. It's there-
fore crucial to understand what system services exist, and how they interact with each
other and with the rest of the system. We've already covered some of this as part of
discussing Android's hardware support.
Figure 2-4 illustrates in greater detail the system services first introduced in Fig-
ure 2-1. As you can see, there are in fact a couple of major processes involved. Most
prominent is the System Server, whose components all run under the sames process,
system_server, and which is mostly made up of Java-coded services with two services
written in C/C++. The System Server also includes some native code access through
JNI to allow some of the Java-based services to interface to Android's lower layers. The
rest of the system services are housed within the Media Service which runs as media-
server. These services are all coded in C/C++ and are packaged alongside media-related
components such as the StageFright and audio effects.
Note that despite there being only two processes to house the entirety of the Android's
system services, they all appear to operate independently to anyone connecting to their
System Services | 53

services through Binder. Here's the output of the service utility on the Android emula-
tor:
# service list
Found 50 services:
0 phone: [com.android.internal.telephony.ITelephony]
1 iphonesubinfo: [com.android.internal.telephony.IPhoneSubInfo]
2 simphonebook: [com.android.internal.telephony.IIccPhoneBook]
3 isms: [com.android.internal.telephony.ISms]
4 diskstats: []
5 appwidget: [com.android.internal.appwidget.IAppWidgetService]
6 backup: [android.app.backup.IBackupManager]
7 uimode: [android.app.IUiModeManager]
8 usb: [android.hardware.usb.IUsbManager]
9 audio: [android.media.IAudioService]
10 wallpaper: [android.app.IWallpaperManager]
11 dropbox: [com.android.internal.os.IDropBoxManagerService]
12 search: [android.app.ISearchManager]
13 location: [android.location.ILocationManager]
14 devicestoragemonitor: []
15 notification: [android.app.INotificationManager]
16 mount: [IMountService]
17 accessibility: [android.view.accessibility.IAccessibilityManager]
18 throttle: [android.net.IThrottleManager]
19 connectivity: [android.net.IConnectivityManager]
20 wifi: [android.net.wifi.IWifiManager]
21 network_management: [android.os.INetworkManagementService]
22 netstat: [android.os.INetStatService]
23 input_method: [com.android.internal.view.IInputMethodManager]
24 clipboard: [android.text.IClipboard]
25 statusbar: [com.android.internal.statusbar.IStatusBarService]
26 device_policy: [android.app.admin.IDevicePolicyManager]
27 window: [android.view.IWindowManager]
28 alarm: [android.app.IAlarmManager]
29 vibrator: [android.os.IVibratorService]
30 hardware: [android.os.IHardwareService]
31 battery: []
32 content: [android.content.IContentService]
33 account: [android.accounts.IAccountManager]
34 permission: [android.os.IPermissionController]
35 cpuinfo: []
36 meminfo: []
37 activity: [android.app.IActivityManager]
38 package: [android.content.pm.IPackageManager]
39 telephony.registry: [com.android.internal.telephony.ITelephonyRegistry]
40 usagestats: [com.android.internal.app.IUsageStats]
41 batteryinfo: [com.android.internal.app.IBatteryStats]
42 power: [android.os.IPowerManager]
43 entropy: []
44 sensorservice: [android.gui.SensorServer]
45 SurfaceFlinger: [android.ui.ISurfaceComposer]
46 media.audio_policy: [android.media.IAudioPolicyService]
47 media.camera: [android.hardware.ICameraService]
48 media.player: [android.media.IMediaPlayerService]
54 | Chapter 2: Internals Primer

49 media.audio_flinger: [android.media.IAudioFlinger]
There is unfortunately not much documentation on how each of these services operates.
You'll have to look at each service's source code to get a precise idea of how it works
and how it interacts with other services.
Reverse Engineering Source Code
Fully understanding the internals of Android's system services is like trying to swallow
a whale. There are about 85k lines of Java code in the System Server alone, spread across
100 different files. And that doesn't count any system service code written in C/C++.
To add insult to injury, so to speak, the comments are few and far between and the
design documents non-existent. Arm yourself with a good dose of patience if you want
to dig further here.
One trick is to create a new Java project in Eclipse and import the System Server's code
inside that project. This won't compile in any way, but it'll allow you to benefit from
Eclipse's Java browsing capabilities to help in trying to understand the code. For in-
stance, you can open a single Java file, right-click on the source browsing scrollbar area,
and select Folding → Collapse All. This will essentially collapse all methods into a single
line next to a plus sign (+) and will allow you to see the trees (the method names lined-
up one after another) instead of the leaves (the actual content of each method.) You'll
very much still be in a forest, though.
You can also try using one of the commercial source code analysis tools on the market
from vendors such as Imagix, Rationale, Lattix, or Scitools. Although there are some
open source analysis tools out there, most seem geared towards locating bugs, not
reverse-engineering the code being analyzed.
Service Manager and Binder Interaction
As I explained earlier, the Binder mechanism used as system services' underlying fabric
enables object-oriented remote method invocation. For a process in the system to in-
voke a system service through Binder, though, it must first have a handle to it. For
instance, Binder will enable an app developer to request a wakelock from the Power
Manager by invoking the acquire() method of its WakeLock nested class. Before that call
can be made, though, the developer must first get a handle to the Power Manager
service. As we'll see in the next section, the app development API actually hides the
details of how it gets this handle in an abstraction to the developer, but under the hood
all system service handle lookups are done through the Service Manager, as illustrated
in Figure 2-5.
Think of the Service Manager as a YellowPages book of all services available in the
system. If a system service isn't registered with the Service Manager, it's effectively
invisible to the rest of the system. To provide this indexing capability, the Service Man-
ager is started by init before any other service. It then opens /dev/binder and uses a
System Services | 55

Figure 2-5. Service Manager and Binder interaction
special ioctl() call to set itself as the Binder's Context Manager ("A1" in Figure 2-5.)
Thereafter, any process in the system that attempts to communicate with Binder ID 0
(a.k.a. the "magic" Binder or "magic object" in various parts of the code), is actually
communicating through Binder to the Service Manager.
When the System Server starts, for instance, it registers every single service it instanti-
ates with the Service Manager ("A2".) Later, when an app tries to talk to a system service,
such as the Power Manager service, it first asks the Service Manager for a handle to the
service ("B1") and then invokes that service's methods ("B2"). In contrast, a call to a
service component running within an app goes directly through Binder ("C1"), and is
noy looked up through the Service Manager.
The Service Manager is also used in a special way by the dumpsys utility, which allows
you to dump the status of a single or all system services. To get the list of all services,
it loops around to get every system service ("D1"), requesting the nth plus one at every
iteration until there aren't any more. To get each service, it just asks the Service Manager
to locate that specific one ("D2".) With a service handle in hand, it invokes that service's
dump() function to dump its status ("D3") and displays that on the terminal.
56 | Chapter 2: Internals Primer

Calling on Services
All of what I just explained is, as I said earlier, almost invisible to the user. Here's a
snippet, for instance, that allows us to grab a wakelock within an app using the regular
application development API:
PowerManager pm = (PowerManager) getSystemService(POWER_SERVICE);
PowerManager.WakeLock wakeLock = pm.newWakeLock(PowerManager.FULL_WAKE_LOCK, "myPreciousWakeLock");
wakeLock.acquire(100);
Notice that we don't see any hint of the Service Manager here. Instead, we're using
getSystemService() and passing it the POWER_SERVICE parameter. Internally, though, the
code that implements getSystemService() does actually use the Service Manager to
locate the Power Manager service so that we create a wakelock and acquire it.
A Service Example: the Activity Manager
Although covering each and every system service is outside the scope of this book, let's
have a quick look at the Activity Manager, one of the key system services. The Activity
Manager's sources actually span over 30 files and 20k lines of code. If there's a core to
Android's internals, this service is very much near it. It takes care of the starting of new
components, such as Activities and Services, along with the fetching of Content Pro-
viders and intent broadcasting. If you ever got the dreaded ANR (Application Not
Responding) dialog box, know that the Activity Manager was behind it. It's also in-
volved in the maintenance of OOM adjustments used by the in-kernel low-memory
handler, permissions, task management, etc.
For instance, when the user clicks on a icon to start an app from his home screen, the
first that happens is that the Launcher's* onClick() callback is called. To deal with the
event, the Launcher will then call, through Binder, the startActivity() method of the
Activity Manager service. The service will then call the startViaZygote() method,
which will open a socket to the Zygote and ask it to start the Activity. All this may make
more sense after you read the final section of this chapter.
If you're familiar with Linux's internals, a good way to think of the Activity Manager is
that it's to Android what the content of the kernel/ directory in the kernel's sources is
to Linux. It's that important.
Stock AOSP Packages
The AOSP ships with a certain number of default packages that are found in most
Android devices. As I mentioned in the previous chapter, though, some apps such as
* The Launcher is the default app packaged with the AOSP that takes care of the main interface with the user,
the home screen.
Stock AOSP Packages | 57

Maps, YouTube, and Gmail aren't part of the AOSP. Let's take a look at some of those
packages included by default. Table 2-5 lists the stock apps included in the AOSP,
Table 2-6 lists the stock content providers included in the AOSP, and Table 2-7 lists
the stock IMEs (Input Method Editors) included in the AOSP.
While these are coded very much like standard apps, most won't build
outside the AOSP using the standard SDK. Hence, if you'd like to create
your own version of one of these apps (i.e., fork it), you'll either have to
do it inside the AOSP or invest some time in getting the app to build
outside the AOSP with the standard SDK. For one thing, these apps
sometimes use APIs that are accessible within the AOSP but aren't ex-
ported through the standard SDK.
Table 2-5. Stock AOSP Apps
App in AOSP Name displayed in Launcher Description
AccountsAndSettings N/A Accounts management app
Bluetooth N/A Bluetooth manager
Browser Browser Default Android browser, includes bookmark widget
Calculator Calculator Calculator app
Camera Camera Camera app
CertInstaller N/A UI for installing certificates
Contacts Contacts Contacts manager app
DeskClock Clock Clock and alarm app, including the clock widget
DownloadsUI Downloads UI for DownloadProvider
Email Email Default Android email app
Development Dev Tools Miscellaneous dev tools
Gallery Gallery Default gallery app for viewing pictures
Gallery3D Gallery Fancy gallery with "sexier" UI
HTMLViewer N/A App for viewing HTML files
Launcher2 N/A Default home screen
Mms Messaging SMS/MMS app
Music Music Music player
PackageInstaller N/A App install/uninstall UI
Phone Phone Default phone dialer/UI
Protips N/A Home screen tips
Provision N/A App for setting a flag indicating whether a device was provisioned
QuickSearchBox Search Search app and widget
Settings Settings Settings app, also accessible through home screen menu
58 | Chapter 2: Internals Primer

App in AOSP Name displayed in Launcher Description
SoundRecorder N/A Sound recording appa
SpeechRecorder Speech Recorder Speech recording app
SystemUI N/A Status bar
a This one is activated when a recording intent is sent. It can't be accessed directly by the user.
Table 2-6. Stock AOSP Providers
Provider Description
ApplicationProvider Provider for search installed apps
CalendarProvider Main Android calendar storage and provider
ContactsProvider Main Android contacts storage and provider
DownloadProvidera Download management, storage and access
DrmProvider Management and access of DRM-protected storage
MediaProvider Media storage and provider
TelephonyProvider Carrier and SMS/MMS storage and provider
UserDictionnaryProvider Storage and provider for user-defined words dictionary
a Interestingly, this package's source code includes a design document, a rarety in the AOSP.
Table 2-7. Stock AOSP Input Methods
Input Method Description
LatinIME Latin keyboard
OpenWnn Japanese keyboard
PinyinIME Chinese keyboard
System Startup
The best way to bring together all that we discussed is to look at Android's startup. As
you can see in Figure 2-6, the first cog to turn is the CPU. It typically has a hard-coded
address from which it fetches its first instructions. That address usually points to a chip
that has the bootloader programmed on it. The bootloader then initializes the RAM,
puts basic hardware in a quiescent state, loads the kernel and RAM disk, and jumps
into the kernel. More recent System-on-Chip (SoC) devices, which include a CPU and
a slew of peripherials in a single chip, can actually boot straight from a properly for-
matted SD card or SD-card-like chip. The PandaBoard and recent editions of the Bea-
gleBoard, for instance, don't have any on-board flash chips because they boot straight
from an SD card.
The initial kernel startup is very hardware dependent, but its purpose is to set things
up so that the CPU can start executing C code as early as possible. Once that's done,
the kernel jumps to the architecture-independent start_kernel() function, initializes
System Startup | 59

Figure 2-6. Android's boot sequence
its various subsystems, and proceed to call the "init" functions of all built-in drivers.
The majority of messages printed out by the kernel at startup come from these steps.
The kernel then mounts its root filesystem and starts the init process.
That's when Android's init kicks in and executes the instructions stored in its /init.rc
file to set up environment variables such as the system path, create mount points, mount
filesystems, set OOM adjustments, and start native daemons. We've already covered
the various native daemons active in Android, but it's worth focusing a little on the
Zygote. The Zygote is a special daemon whose job is to launch apps. Its functionality
is centralized here in order to unify the components shared by all apps and to shorten
their start-up time. init doesn't actually start the Zygote directly; instead it uses the
app_process command to get Zygote started by the Android runtime. The runtime then
starts the first Dalvik VM of the system and tells it to invoke the Zygote's main().
Zygote is active only when a new app needs to be launched. To achieve a speedier app
launch, the Zygote starts by preloading all Java classes and resources that an app may
potentially need at runtime. This effectively loads those into the system's RAM. The
Zygote then listens for connections on its socket (/dev/socket/zygote) for requests to
start new apps. When it gets a request to start an app, it forks itself and launches the
new app. The beauty of having all apps fork from the Zygote is that it's a "virgin" VM
that has all the system classes and resources an app may need preloaded and ready to
60 | Chapter 2: Internals Primer

be used. In other words, new apps don't have to wait until those are loaded to start
executing.
All of this works because the Linux kernel implements a Copy-On-Write (COW) policy
for forks. As you may know, forking in Unix involves creating a new process that is an
exact same copy of the parent process. With COW, Linux doesn't actually copy any-
thing. Instead, it maps the pages of the new process over to those of the parent process
and makes copies only when the new process writes to a page. But in fact the classes
and resources loaded are never written to, because they're the default ones and are
pretty much immutable within the lifetime of the system. So all processes directly fork-
ing from the Zygote are essentially using its own mapped copies. And therefore, re-
gardless of the number of apps running on the system, only one copy of the system
classes and the resources is ever loaded in RAM.
Although the Zygote is designed to listen to connections for requests for forking new
apps, there is one "app" that the Zygote actually starts explicitly: the System Server.
This is the first app started by the Zygote and it continues to live on as an entirely
separate process from its parent. The System Server then starts initializing each system
service it houses and registering it with the previously-started Service Manager. One of
the services it starts, the Activity Manager, will end its initialization by sending an intent
of type Intent.CATEGORY_HOME. This starts the Launcher app, which then displays the
home screen familiar to all Android users.
When the user clicks on an icon on the home screen, the process I described in “System
Services” on page 53 takes place. The Launcher asks the Activity Manager to start the
process, which in turn "forwards" that request on to the Zygote, which itself forks and
starts the new app, which is then displayed to the user.
Once the system has finished starting up, the process list will look something like this:
# ps
USER PID PPID VSIZE RSS WCHAN PC NAME
root 1 0 268 180 c009b74c 0000875c S /init
root 2 0 0 0 c004e72c 00000000 S kthreadd
root 3 2 0 0 c003fdc8 00000000 S ksoftirqd/0
root 4 2 0 0 c004b2c4 00000000 S events/0
root 5 2 0 0 c004b2c4 00000000 S khelper
root 6 2 0 0 c004b2c4 00000000 S suspend
root 7 2 0 0 c004b2c4 00000000 S kblockd/0
root 8 2 0 0 c004b2c4 00000000 S cqueue
root 9 2 0 0 c018179c 00000000 S kseriod
root 10 2 0 0 c004b2c4 00000000 S kmmcd
root 11 2 0 0 c006fc74 00000000 S pdflush
root 12 2 0 0 c006fc74 00000000 S pdflush
root 13 2 0 0 c0079750 00000000 D kswapd0
root 14 2 0 0 c004b2c4 00000000 S aio/0
root 22 2 0 0 c017ef48 00000000 S mtdblockd
root 23 2 0 0 c004b2c4 00000000 S kstriped
root 24 2 0 0 c004b2c4 00000000 S hid_compat
root 25 2 0 0 c004b2c4 00000000 S rpciod/0
System Startup | 61

root 26 1 232 136 c009b74c 0000875c S /sbin/ueventd
system 27 1 804 216 c01a94a4 afd0b6fc S /system/bin/servicemanager
root 28 1 3864 308 ffffffff afd0bdac S /system/bin/vold
root 29 1 3836 304 ffffffff afd0bdac S /system/bin/netd
root 30 1 664 192 c01b52b4 afd0c0cc S /system/bin/debuggerd
radio 31 1 5396 440 ffffffff afd0bdac S /system/bin/rild
root 32 1 60832 16348 c009b74c afd0b844 S zygote
media 33 1 17976 1104 ffffffff afd0b6fc S /system/bin/mediaserver
bluetooth 34 1 1256 280 c009b74c afd0c59c S /system/bin/dbus-daemon
root 35 1 812 232 c02181f4 afd0b45c S /system/bin/installd
keystore 36 1 1744 212 c01b52b4 afd0c0cc S /system/bin/keystore
root 38 1 824 272 c00b8fec afd0c51c S /system/bin/qemud
shell 40 1 732 204 c0158eb0 afd0b45c S /system/bin/sh
root 41 1 3368 172 ffffffff 00008294 S /sbin/adbd
system 65 32 123128 25232 ffffffff afd0b6fc S system_server
app_15 115 32 77232 17576 ffffffff afd0c51c S com.android.inputmethod.latin
radio 120 32 86060 17952 ffffffff afd0c51c S com.android.phone
system 122 32 73160 17656 ffffffff afd0c51c S com.android.systemui
app_27 125 32 80664 22900 ffffffff afd0c51c S com.android.launcher
app_5 173 32 74404 18024 ffffffff afd0c51c S android.process.acore
app_2 212 32 73112 17032 ffffffff afd0c51c S android.process.media
app_19 284 32 70336 16672 ffffffff afd0c51c S com.android.bluetooth
app_22 292 32 72752 17844 ffffffff afd0c51c S com.android.email
app_23 320 32 70276 15792 ffffffff afd0c51c S com.android.music
app_28 328 32 70744 16444 ffffffff afd0c51c S com.android.quicksearchbox
app_14 345 32 69708 15404 ffffffff afd0c51c S com.android.protips
app_21 354 32 70912 17152 ffffffff afd0c51c S com.cooliris.media
root 366 41 2128 292 c003da38 00110c84 S /bin/sh
root 367 366 888 324 00000000 afd0b45c R /system/bin/ps
This output actually comes from the Android emulator, so it contains some emulator-
specific artefacts such as the qemud daemon. Notice that the apps running all bare their
fully-qualified package names despite being forked from the Zygote. This is a neat trick
that can be pulled in Linux by using the prctl() system call with PR_SET_NAME to tell
the kernel to change the calling process' name. Have a look at prctl()'s man page if
you're interested in it. Note also that the first process started by init is actually ue-
ventd. All processes prior to that are actually started from within the kernel by subsys-
tems or drivers.
62 | Chapter 2: Internals Primer

AOSP Jumpstart
Now that you have a solid understanding of the basics, let's start getting our hands dirty
with the AOSP. We'll start by covering how to get the AOSP repo from http://android
.git.kernel.org/. Before actually building and running the AOSP, we'll spend some time
exploring the AOSP's contents and explain how the sources reflect what we just saw in
the previous chapter. Finally, we'll close the chapter by covering the use of adb and the
emulator, two very important tools when doing any sort of platform work.
Above all, this chapter is meant to be fun. The AOSP is an exciting piece of software
with a tremendous amount of innovations. Ok, ok, I'll admit it's not all rosy and some
parts do have rough edges. Still, some other parts are pure genius. The most amazing
thing of all obviously is that we can all download it, modify it, and ship our own custom
products based on it. So roll up your sleeves and let's get started.
Getting the AOSP
As I had mentioned earlier, the official AOSP is available at http://android.git.kernel
.org, which sports a Gitweb interface.* When you visit the site, you will see a fairly large
number of git repositories you can pull from that location. Needless to say, pulling each
and every one of these manually would be rather tedious; there are over a hundred.
And, in fact, pulling them all would be quite useless because only a subset of these
projects is needed. The right way to pull the AOSP is to use the repo tool which is
available at the very same location. First, though, you'll need to get repo itself:
$ sudo apt-get install curl
$ curl https://android.git.kernel.org/repo > ~/bin/repo
$ chmod a+x ~/bin/repo
* The web interface for the git tool.

Under Ubuntu, ~/bin is automatically added to your path when you log
in, if it already exists. So, if you don't have a bin/ directory in your home
directory, create it, then log out and log back in to make it part of your
path. Otherwise, the shell won't be able to find repo, even if you fetch
it as I just showed.
You don't have to put repo in ~/bin, but it has to be in your path. So
regardless of where you put it, just make sure it's available to you in all
locations in the filesystem from the command line.
Despite its structure as a single shell script, repo is actually quite an intricate tool and
we'll take a deeper look at it later. For now, though, consider repo as a tool that can
simultaneously pull from multiple git repositories to create an Android distribution.
The repositories it pulls from are given to it through a manifest file, which is an XML
file describing the projects that need to pulled from and their location. repo is in fact
layered on top of git and each project it pulls from is an independent git repository.
Confusing as it may be, note that repo's "manifest" file has absolutely
nothing to do with "manifest" files (AndroidManifest.xml) used by app
developers to describe their apps to the system. Their formats and uses
are completely different. Fortunately, they rarely have to be used within
the same context, so while you should keep this fact in mind we won't
need to worry too much about it in the coming explanations.
Now that we've got repo, let's get ourselves a copy of the AOSP:
$ mkdir -p ~/android/aosp-2.3.x
$ cd ~/android/aosp-2.3.x
$ repo init -u git://android.git.kernel.org/platform/manifest.git -b gingerbread
$ repo sync
The last command should run for quite some time as it goes and fetches the sources of
all the projects described in the manifest file. After all, the AOSP is about 4GB in size
uncompiled. Keep in mind therefore that network bandwidth and latencies will play a
big role in how long this takes. Note also that we are fetching a specific branch of the
tree, Gingerbread. That's the -b gingerbread part of the third command. If you omit
that part, you will be getting the master branch. It's been the experience of many people
that the master branch doesn't always build or run properly, because it contains the tip
of the open development branch. Tagged branches, on the other hand, mostly work
out of the box.
64 | Chapter 3: AOSP Jumpstart

Inside the AOSP
Now that we've got a copy of the AOSP, let's start looking at what's inside and, most
importantly, connect that to what we just saw in the previous chapter. Feel free to skip
over this section and come back to it after the next section if you're too eager to get
your own custom Android running. For those of you still reading, have a look at Ta-
ble 3-1 for a summary of the AOSP's top-level directory.
Table 3-1. AOSP content summary
Directory Content Size (in MB)
bionic Android's custom C library 14
device Device-specific files and components 17
packages Stock Android apps, providers and IMEs 117
prebuilt Prebuilt binaries, including toolchains 1,389
system "Embedded Linux" platform that houses Android 32
As you can see, prebuilt and external are the two largest directories in the tree, ac-
counting for close to 75% of its size. Interestingly, both these directories are mostly
made up of content from other open source projects and include things like various
GNU toolchain versions, kernel images, common libraries and frameworks such as
OpenSSL and WebKit, etc. libcore is also from another open source project, Apache
Harmony. In essence, this is further evidence of how much Android relies heavily on
the rest of the open source ecosystem to exist. Still, Android contains a fair bit of "orig-
inal" (or near to) code; about 800MB of it in fact.
To best understand Android's sources, it's useful to refer back to Figure 2-1, which
illustrated Android's architecture in the previous chapter. Figure 3-1 is a variant of that
figure that illustrates the location of each Android component in the AOSP sources.
Obviously, a lot of key components come from frameworks/base/, which is where the
Inside the AOSP | 65

Figure 3-1. Android's architecture
bulk of Android's "brains" are located. It's in fact worth taking a closer look at that
directory and system/core/, in Table 3-2 and Table 3-3 respectively, as they contain a
large chunk of the moving parts you'll likely be interested in interfacing with or mod-
ifying as an embedded developer.
Table 3-2. Content summary for frameworks/base/
Directory Content
cmds Native commands and daemons
core The android.* packages
data Fonts and sounds
graphics 2D graphics and Renderscript
include C-language include files
keystore Security key store
libs C libraries
location Location provider
media Media Service, StageFright, codecs, etc.
native Native code for some framework components
obex Bluetooth Obex
66 | Chapter 3: AOSP Jumpstart

Directory Content
opengl OpenGL library and Java code
packages A few core packages such as the Status Bar
services System services
telephony Telephony API, which talks to the rild radio layer interface
tools A few core tools such as aapt and aidl
voip RTP and SIP APIs
vpn VPN Manager
wifi Wifi Manager and API
Table 3-3. Content summary for system/core/a
Directory Content
adb The ADB daemon and client
cpio mkbootfs tool used to generate RAM disk imagesb
fastboot fastboot utility used to communicate with Android bootloaders using the "fastboot" protocol
include C-language headers for all things "system"
init Android's init
libacc "Almost" C Compiler library for compiling C-like code; used by RenderScriptc
libcutils Various C utility functions not part of the standard C library; used throughout the tree
libdiskconfig For reading and configuring disks; used by vold
liblinenoise BSD-licensed readline() replacement from http://github.com/antirez/linenoise; used by Android's shell
liblog Logting library that interfaces with the Android kernel logger as seen in Figure 2-2; used throughout the tree
libmincrypt Basic RSA and SHA functions; used by the recovery mechanism and mkbootimg utility
libnetutils Network configuration library; used by netd
libpixelflinger Low-level graphic rendering functions
libsysutils Utility functions for talking with various components of the system, including the framework; used by netd and
vold
libzipfile Wrapper around zlib for dealing with zip files
logcat The logcat utility
logwrapper Utility that forks and runs the command passed to it while redirecting stdout and stderr to Android's logger
mkbootimg Utility for creating a boot image using a RAM disk and a kernel
netcfg Network configuration utility
rootdir Default Android root directory structure and content
run-as Utility for running a program as a given user ID
sh Android shell
Inside the AOSP | 67

Directory Content
toolbox Android's Toolbox (BusyBox replacement)
a Some entries have been omitted because they aren't currently used by any part of the AOSP. They are likely legacy components.
b This is used to create both the default RAM disk image used to boot Android and the recovery image.
c This description might not make any sense to you unless you know what RenderScript is. Have a look at Google's documentation for
RenderScript, the relevance of libacc in that context should be clearer.
In addition to base/, frameworks/ contains a few other directories, but they are nowhere
near as fundamental as base/. Likewise, in addition to core/, system/ also includes a few
more directories such as netd/ and vold/, which contain the netd and vold daemons
respectively.
In addition to the top-level directories, the root directory also includes a single Makefile.
That file is however mostly empty, its main use being to include the entry point to
Android's build system:
### DO NOT EDIT THIS FILE ###
include build/core/main.mk
### DO NOT EDIT THIS FILE ###
As you've likely figured already, there's far more to the AOSP than what I just presented
to you. There are, after all, more than 14,000 directories and 100,000 files in 2.3.x/
Gingerbread. By most standards, it's a fairly large project. In comparison, early 3.0.x
releases of the Linux kernel have about 2,000 directories and 35,000 files. We will
certainly get the chance to explore more parts of the AOSP's sources as we move for-
ward. I highly recommend, though, you start exploring and experimenting with the
sources in earnest as it will likely take you several months before you can comfortably
navigate your way through.
Build Basics
So now we have an AOSP, and a general idea of what's inside, so let's get it up and
running. There's one last thing we need to do before we can build it, though. We need
to make sure we've got all the packages necessary on our Ubuntu install. Here are the
instructions based on Ubuntu 11.04. Even it you are using a older or newer version of
some Debian-based Linux distribution, the instructions will be fairly similar. (See also
“Building on Virtual Machines or Non-Ubuntu Systems” on page 72 for other systems
on which you can build the AOSP.)
Build System Setup
First, let's get some of the basic packages installed on our development system. You
might have some of these already installed as part of other development work you've
68 | Chapter 3: AOSP Jumpstart

been doing and that's fine. Ubuntu's package management system will ignore your
request to install those packages.
$ sudo apt-get install bison flex gperf git-core gnupg zip tofrodos \
> build-essential g++-multilib libc6-dev libc6-dev-i386 ia32-libs mingw32 \
> zlib1g-dev lib32z1-dev x11proto-core-dev libx11-dev \
> lib32readline5-dev libgl1-mesa-dev lib32ncurses5-dev
You might also need to fix a few symbolic links:
$ sudo ln -s /usr/lib32/libstdc++.so.6 /usr/lib32/libstdc++.so
$ sudo ln -s /usr/lib32/libz.so.1 /usr/lib32/libz.so
Finally, you need to install Sun's JDK:†
$ sudo add-apt-repository "deb http://archive.canonical.com/ natty partner"
$ sudo apt-get update
$ sudo apt-get install sun-java6-jdk
Your system is now ready to build Android. Obviously you don't need to do this pack-
age installation process every time you build Android. You'll need to do it only once
for every Android development system you set up.
Building Android
We are now ready to build Android. Let's go to the directory where we downloaded
Android and configure the build system:
$ cd ~/android/aosp-2.3.x
$ . build/envsetup.sh
$ lunch
You're building on Linux
Lunch menu... pick a combo:
1. generic-eng
2. simulator
3. full_passion-userdebug
4. full_crespo4g-userdebug
5. full_crespo-userdebug
Which would you like? [generic-eng] ENTER
============================================
PLATFORM_VERSION_CODENAME=REL
†The OpenJDK and gcj won't do.
Build Basics | 69

PLATFORM_VERSION=2.3.4
TARGET_PRODUCT=generic
TARGET_BUILD_VARIANT=eng
TARGET_SIMULATOR=false
TARGET_BUILD_TYPE=release
TARGET_BUILD_APPS=
TARGET_ARCH=arm
HOST_ARCH=x86
HOST_OS=linux
HOST_BUILD_TYPE=release
BUILD_ID=GINGERBREAD
============================================
Note that we typed a period (.), SPACE, and then build/envsetup.sh. This forces the
shell to run the envsetup.sh script within the current shell. If we were to just run the
script, the shell would spawn a new shell and run the script in that new shell. That
would be useless since envsetup.sh defines new shell commands, such as lunch, and sets
up environment variables required for the rest of the build.
We will explore envsetup.sh and lunch in more detail later. For the moment, though,
note that the generic-eng combo means that we configured the build system to create
images for running in the Android emulator. This is the same QEMU emulator software
used by app developers to test their apps when developing using the SDK on a work-
station, albeit here it will be running our own custom images instead of the default ones
shipped with the SDK. It's also the same emulator that was used by the Android de-
velopment team to develop Android while there were no devices for it yet. So while it's
not real hardware and is therefore by no means a pefect target, it's still more than
sufficient to cover most of the terrain we need to cover. Once you know your specific
target, you should be able to adapt the instructions found in the rest of this book, with
possibly some help from the book Building Embedded Linux Systems, to get your custom
Android images loaded on your device and your hardware to boot them.
Now that the environment has been set up, we can actually build Android:
$ make -j16
============================================
PLATFORM_VERSION_CODENAME=REL
PLATFORM_VERSION=2.3.4
TARGET_PRODUCT=generic
TARGET_BUILD_VARIANT=eng
TARGET_SIMULATOR=false
TARGET_BUILD_TYPE=release
TARGET_BUILD_APPS=
TARGET_ARCH=arm
HOST_ARCH=x86
HOST_OS=linux
HOST_BUILD_TYPE=release
BUILD_ID=GINGERBREAD
============================================
Checking build tools versions...
70 | Chapter 3: AOSP Jumpstart

find: `frameworks/base/frameworks/base/docs/html': No such file or directory
find: `out/target/common/docs/gen': No such file or directory
find: `frameworks/base/frameworks/base/docs/html': No such file or directory
find: `out/target/common/docs/gen': No such file or directory
find: `frameworks/base/frameworks/base/docs/html': No such file or directory
find: `out/target/common/docs/gen': No such file or directory
find: `frameworks/base/frameworks/base/docs/html': No such file or directory
find: `out/target/common/docs/gen': No such file or directory
find: `frameworks/base/frameworks/base/docs/html': No such file or directory
find: `out/target/common/docs/gen': No such file or directory
host Java: apicheck (out/host/common/obj/JAVA_LIBRARIES/apicheck_intermediates/classes)
Header: out/host/linux-x86/obj/include/libexpat/expat.h
Header: out/host/linux-x86/obj/include/libexpat/expat_external.h
Header: out/target/product/generic/obj/include/libexpat/expat.h
Header: out/target/product/generic/obj/include/libexpat/expat_external.h
Header: out/host/linux-x86/obj/include/libpng/png.h
Header: out/host/linux-x86/obj/include/libpng/pngconf.h
Header: out/host/linux-x86/obj/include/libpng/pngusr.h
Header: out/target/product/generic/obj/include/libpng/png.h
Header: out/target/product/generic/obj/include/libpng/pngconf.h
Header: out/target/product/generic/obj/include/libpng/pngusr.h
Header: out/target/product/generic/obj/include/libwpa_client/wpa_ctrl.h
Header: out/target/product/generic/obj/include/libsonivox/eas_types.h
Header: out/target/product/generic/obj/include/libsonivox/eas.h
Header: out/target/product/generic/obj/include/libsonivox/eas_reverb.h
Header: out/target/product/generic/obj/include/libsonivox/jet.h
Header: out/target/product/generic/obj/include/libsonivox/ARM_synth_constants_gnu.inc
host Java: clearsilver (out/host/common/obj/JAVA_LIBRARIES/clearsilver_intermediates/classes)
target Java: core (out/target/common/obj/JAVA_LIBRARIES/core_intermediates/classes)
host Java: dx (out/host/common/obj/JAVA_LIBRARIES/dx_intermediates/classes)
Notice file: frameworks/base/libs/utils/NOTICE -- out/host/linux-x86/obj
/NOTICE_FILES/src//lib/libutils.a.txt
Notice file: system/core/libcutils/NOTICE -- out/host/linux-x86/obj/NOTICE_FILES/src//lib
/libcutils.a.txt
...
Now is a good time to go for a snack or watch tonight's hockey game.‡ On a more
serious note, though, your build time will obviously depend on your system's capabil-
ities. On a laptop equiped with a quad-core CORE i7 Intel processor with hyper-
threading enabled and 8GB of RAM, this actua command will take about 20 minutes
to build the AOSP. On an older laptop with a dual-core Centro 2 Intel processor and
2GB of RAM, a make -j4 would take about an hour to build the same AOSP. Note that
the -j parameter of make allows you to specify how many jobs to run in parallel. Some
say that it's best to use your number of processors times 2, which is what I'm doing
here. Others say it's best to add 2 to the number of processors you have. Following that
advice, I would've used 10 and 4 instead of 16 and 4.
‡It's a Canadian thing, I can't help it.
Build Basics | 71

Building on Virtual Machines or Non-Ubuntu Systems
I often get asked about building the AOSP in virtual machines; most often because the
development team, or their IT department, is standardized on Windows. While I've
seen this work and have put together images to do that myself, your results will vary.
It'll usually take more than twice as much time to build in a VM than building natively
on the same system. So if you're going to do a lot of work on the AOSP, I highly suggest
you build it natively. And yes, this involves having a Linux machine at hand.
An increasing number of developers also prefer MacOS X over Linux and Windows,
including many at Google itself. Hence, the official instructions at http://source.android
.com also describe how to build on a Mac. These instructions, though, tend to break
after Mac OS updates. Fortunately for Mac-based developers, they are many and they
are rather zealous. Hence, you'll eventually find updated instructions on the web or on
the various Google Groups about how to build the AOSP on your new version of MacOS
X. Here's one posting explaining how to build Gingerbread on MacOS X Lion: Building
Gingerbread on OS X Lion. Bear in mind, though, that as I mentioned in Chapter 1,
Google's own Android build farms are Ubuntu-based. If you choose to build on MacOS
X, you'll likely always be playing catch-up. At worst, you can use a VM as in the Win-
dows case.
If you do choose to go down the VM route, make sure you configure the VM to use as
many CPUs as there are available in your system. Most BIOSes I've seen seem to disable
by the default the option for enabling CPU instructions sets allowing mutlitple CPU
virtualization. VirtualBox, for instance, will complain about some obscur error if you
try to allocate more than one CPU to an image while those instruction sets are disabled.
You must go to the BIOS and enable those options for your VM software to be able to
grant the guest OS multiple CPUs.
There are a few other things to consider regarding the build. First, note that in between
printing out the build configuration and the printing of the first output of the actual
build (where it prints out: "host Java: apicheck (out/host/common/o..."), there will be
a rather long delay where nothing will get printed out, save for the "No such file or
directory" warnings. I'll explain this delay in more detail later, but suffice it to say for
now that during that time the build system is figuring out the rules of how to build
every part of the AOSP.
Note also that you'll see plenty of warning statements. These are rather "normal," not
so much in terms of maintaining software quality, but in that they are pervasive in
Android's build. They usually won't have an impact on the final product being com-
piled. So, contrary to the best of my software engineeering instincts, I have to recom-
mend you completely ignore warnings and stick to fixing errors only. Unless, of course,
those warnings stem from software you added yourself. Then, by all means, make sure
you get rid of those warnings.
72 | Chapter 3: AOSP Jumpstart

Figure 3-2. Android emulator running custom images
Running Android
With the build completed, all you need to do is start the emulator to run your own
custom-built images:
$ emulator &
This will start the emulator window that will boot into a full Android environment as
illustrated in Figure 3-2.
You can then interact with the AOSP you just built very much in the same way as if it
were running on a real device. Since your monitor is likely not a touch screen, however,
you will need to use your mouse as if it was your finger. A single touch is a click and
swipping is done by holding down the mouse button, moving around and letting go of
the mouse button to signify that your finger has been removed from the touchscreen.
You also have a full keyboard at your disposal, with all the buttons you would find on
a phone equipped with a QWERTY keyboard, although you can use your regular key-
board to input text in text boxes.
Despite its features and realism, the emulator does have its issues. For one thing, it
takes some time to boot. It will take longest to boot the first time, because Dalvik is
Running Android | 73

creating a JIT cache for the apps running on the phone. Even later, though, you might
find it heavy, especially if you're in a modify-compile-test loop. Also, the emulator
doesn't perfectly emulate everything. For instance, it traditionally has a hard time firing
off rotation change events when it's made to rotate using F11 or F12. This issue,
though, is mostly an issue for app developers.
If for any reason you close the shell where you had configured, built, and started An-
droid, or if you need to start a new one and have access to all the tools and binaries
created from the build, you must invoke the envsetup.sh script and the lunch commands
again in order to set up environment variables. Here are commands from a new shell,
for instance:
$ cd ~/android/aosp-2.3.x
$ emulator &
No command 'emulator' found, did you mean:
Command 'qemulator' from package 'qemulator' (universe)
emulator: command not found
$ . build/envsetup.sh
$ lunch
You're building on Linux
Lunch menu... pick a combo:
1. generic-eng
2. simulator
3. full_passion-userdebug
4. full_crespo4g-userdebug
5. full_crespo-userdebug
Which would you like? [generic-eng] ENTER
============================================
PLATFORM_VERSION_CODENAME=REL
PLATFORM_VERSION=2.3.4
TARGET_PRODUCT=generic
TARGET_BUILD_VARIANT=eng
...
============================================
$ emulator &
$
Note that the second time we issued emulator, the shell didn't complain that the com-
mand was missing anymore. The same goes for a lot of other Android tools such as the
adb command we're about to look at. Note also that we didn't need to issue any
make commands, because we had already built Android. In this case, we just needed
to make sure the environment variables were properly set in order for the results of the
previous build to be available to us again.
74 | Chapter 3: AOSP Jumpstart

Using ADB
One of the most interesting aspects of the development environment put together by
the Android development team is that you can shell into the running emulator, or any
real device connected through USB for that matter, using the adb tool:
$ adb shell
* daemon not running. starting it now on port 5037 *
* daemon started successfully *
# cat /proc/cpuinfo
Processor : ARM926EJ-S rev 5 (v5l)
BogoMIPS : 405.50
Features : swp half thumb fastmult vfp edsp java
CPU implementer : 0x41
CPU architecture: 5TEJ
CPU variant : 0x0
CPU part : 0x926
CPU revision : 5
Hardware : Goldfish
Revision : 0000
Serial : 0000000000000000
This is issued in the same shell where you started the emulator from.
This is the target's shell, and cat is actually running on the "target" (i.e., the
emulator.)
As you can see, the kernel running in the emulator reports that it's seeing an ARM
processor, which is in fact the predominant platform used with Android. Also, the
kernel says it's running on a platform called Goldfish. This is the code-name for the
emulator and you will see it in quite a few places.
Now that you've got a shell into the emulator and you are root, which is the default in
the emulator, you can run any command much like if you had shelled into a remote
machine or a traditional network-connected embedded Linux system. ADB is what
makes this possible and Figure 3-3 illustrates its many components and how they're
connected.
To exit an ADB shell session, all you need to do is type CTRL-D:
# CTRL-D
$
This is in the target shell
This is back on the host
When you start adb for the first time on the host, it starts a server in the background
whose job is to manage the connections to all Android devices connected to the host.
Using ADB | 75

