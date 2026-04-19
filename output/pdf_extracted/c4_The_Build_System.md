# The Build System

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

Figure 3-3. How ADB's parts are interconnected
That was the part of the earlier output that said that a daemon was being started on
port 5037. You can actually ask that daemon what devices it sees:
$ adb devices
List of devices attached
emulator-5554 device
0000021459584822 device
emulator-5556 offline
This is the output with one emulator instance running, one device connected through
USB, and another emulator instance starting up. If there are multiple devices connected,
you can tell it which device you want to talk to using the -s flag to identify the serial
number of the device:
$ adb -s 0000021459584822 shell
$ id
uid=2000(shell) gid=2000(shell) groups=1003(graphics),1004(input), ...
$ su
su: permission denied
Note that in this case, I'm getting a $ for my shell prompt instead of a #. This means
that contrary to the earlier interaction, I'm not running as root, as can also be seen from
the output of the id command. This is actually a real commercial Android phone, and
my inability above to gain root priviledges using the su command is typical. Hence, my
ability to make any modifications to this device will be fairly limited. Unless, of course,
I find some way to "root" the phone (i.e. gain root access). Unfortunately, device man-
ufacturers have been historically very reluctant for various reasons to give root access
to their devices and have put in a number of provisions to make that as difficult as
possible, if not impossible. That's why "rooting" devices is held up as a holy grail by
76 | Chapter 3: AOSP Jumpstart

many power users and hackers. As of the summer of 2011, though, some manufacturers
such as Motorola and HTC have spelled out a change in policy where they seem to be
intent on making it easier for users to root their devices, with caveats of course. But
this isn't mainstream yet.
You may be tempted to try to root a commercial phone or device for
experimenting with Android platform development. I would suggest
you think this through carefully. While there are plenty of instructions
out there explaining how to replace your standard images with what is
often referred to as "custom ROMs" such as Cyanogenmod and others,
you need to be aware that any false step could well result in your "brick-
ing" the device (i.e. rendering it unbootable or erasing critical boot-time
code). You then have an expensive paper-weight (hence the term "brick-
ing") instead of a phone.
If you want to experiment with running custom AOSP builds on real
hardware, I suggest you get yourself something like a BeagleBoard xM
or a PandaBoard. These boards are made for tinkering. If nothing else,
they don't have a built-in flash chip that you may risk damaging. Instead,
the SoCs on those devices boot straight from SD cards. Hence, fixing a
broken image is simply a matter of unplugging the SD card from the
board, connecting it to your workstation, reprogramming it, and plug-
ging it back to the board.
adb can of course do a lot more than just give you a shell, and I encourage you to start
it without any parameters to look at its usage output:
$ adb
Android Debug Bridge version 1.0.26
-d - directs command to the only connected USB device
returns an error if more than one USB device is present.
-e - directs command to the only running emulator.
returns an error if more than one emulator is running.
-s <serial number> - directs command to the USB device or emulator with
the given serial number. Overrides ANDROID_SERIAL
...
device commands:
adb push <local> <remote> - copy file/dir to device
adb pull <remote> [<local>] - copy file/dir from device
adb sync [ <directory> ] - copy host->device only if changed
(-l means list but don't copy)
(see 'adb help all')
adb shell - run remote shell interactively
adb shell <command> - run remote shell command
adb emu <command> - run emulator console command
...
You can, for instance, use adb to dump the data contained in the main logger buffer:
Using ADB | 77

$ adb logcat
I/DEBUG ( 30): debuggerd: Sep 10 2011 13:44:19
I/Netd ( 29): Netd 1.0 starting
I/Vold ( 28): Vold 2.1 (the revenge) firing up
D/qemud ( 38): entering main loop
D/Vold ( 28): USB mass storage support is not enabled in the kernel
D/Vold ( 28): usb_configuration switch is not enabled in the kernel
D/Vold ( 28): Volume sdcard state changing -1 (Initializing) -> 0 (No-Media)
D/qemud ( 38): fdhandler_accept_event: accepting on fd 9
D/qemud ( 38): created client 0xe078 listening on fd 10
D/qemud ( 38): client_fd_receive: attempting registration for service 'boot-properties'
D/qemud ( 38): client_fd_receive: -> received channel id 1
D/qemud ( 38): client_registration: registration succeeded for client 1
I/qemu-props( 54): connected to 'boot-properties' qemud service.
I/qemu-props( 54): receiving..
I/qemu-props( 54): received: qemu.sf.lcd_density=160
I/qemu-props( 54): receiving..
I/qemu-props( 54): received: dalvik.vm.heapsize=16m
I/qemu-props( 54): receiving..
D/qemud ( 38): fdhandler_event: disconnect on fd 10
I/qemu-props( 54): exiting (2 properties set).
D/AndroidRuntime( 32):
D/AndroidRuntime( 32): >>>>>> AndroidRuntime START com.android.internal.os.ZygoteInit <<<<<<
D/AndroidRuntime( 32): CheckJNI is ON
I/ ( 33): ServiceManager: 0xad50
...
This is very useful to observe the runtime behavior of key system components, including
services run by the System Server.
You can also copy files to and from the device:
$ adb push data.txt /data/local
1 KB/s (87 bytes in 0.043s)
$ adb pull /proc/config.gz
95 KB/s (7087 bytes in 0.072s)
Again, given its centrality to Android development, I invite you to read up on ADB's
use. We will continue using it throughout the book and introduce more of its func-
tionalities as we go. Keep in mind, though, that ADB can have its quirks. First and
foremost, many have found its host-side daemon to be somewhat flaky. For some rea-
son or another, it sometimes doesn't correctly identify the state of connected devices
and continues to state that they are offline while you try connecting to them. Or adb
might just hang on the command line waiting for the device while the device is clearly
active and able to receive ADB commands. The solution to those issues is almost in-
variably to kill the host-side daemon:§
§It's actually somewhat interesting that the Android development team felt the need to build such functionality
right into adb. Clearly they were encountering issues with that daemon themselves.
78 | Chapter 3: AOSP Jumpstart

$ adb kill-server
Not to worry—the next time you issue any adb command, the daemon will get auto-
matically restarted. It's unclear what causes this behavior, and maybe this problem will
get resolved at some point in the future. In the mean time, keep in mind that if you see
some odd behavior when using ADB, killing the host-side daemon is usually something
you want to try before investigating other potential issues.
In addition to the command itself, another source of information on adb is the Android
Debug Bridge part of Google's Android Developers Guide. As Tim Bird‖ recommends,
you want to print a copy and put it under your pillow.
Mastering the Emulator
As I said earlier, you can go a long way in platform development by simply using the
emulator. It effectively emulates an ARM target with a minimal set of hardware. We'll
spend some time here going through some more advanced aspects of dealing with the
emulator. As many Android pieces, the emulator is quite a complex piece of software
in and of itself. Still, we can get a very good idea of it capabilities by surveying a few
key features.
Earlier we started the emulator by simply typing:
$ emulator &
But the emulator command can also take quite a few parameters. You can see the online
help by adding the -help flag on the command line:
$ emulator -help
Android Emulator usage: emulator [options] [-qemu args]
options:
-sysdir <dir> search for system disk images in <dir>
-system <file> read initial system image from <file>
-datadir <dir> write user data into <dir>
-kernel <file> use specific emulated kernel
-ramdisk <file> ramdisk image (default <system>/ramdisk.img
-image <file> obsolete, use -system <file> instead
-init-data <file> initial data image (default <system>/userdata.img
-initdata <file> same as '-init-data <file>'
-data <file> data image (default <datadir>/userdata-qemu.img
-partition-size <size> system/data partition size in MBs
...
‖Tim is the maintainer of http://elinux.org, the guy behind the Embedded Linux Conference, the chair of the
Linux Foundation's CE Workgroup, etc. and he's been doing a lot of cool Android stuff at Sony.
Mastering the Emulator | 79

One especially useful flag is -kernel. It allows you to tell the emulator to use another
kernel than the default prebuilt one found in prebuilt/android-arm/kernel/:
$ emulator -kernel path_to_your_kernel_image/zImage
If you want to use a kernel that has module support, for instance, you'll need to build
your own, because the prebuilt one doesn't have module support enabled by default.
Also, by default, the emulator won't show you the kernel's boot messages. You can,
however, pass the -show-kernel flag to see them:
$ emulator -show-kernel
Uncompressing Linux............................................................................................. done, booting the kernel.
Initializing cgroup subsys cpu
Linux version 2.6.29-00261-g0097074-dirty (digit@digit.mtv.corp.google.com)
(gcc version 4.4.0 (GCC) ) #20 Wed Mar 31 09:54:02 PDT 2010
CPU: ARM926EJ-S [41069265] revision 5 (ARMv5TEJ), cr=00093177
CPU: VIVT data cache, VIVT instruction cache
Machine: Goldfish
Memory policy: ECC disabled, Data cache writeback
Built 1 zonelists in Zone order, mobility grouping on. Total pages: 24384
Kernel command line: qemu=1 console=ttyS0 android.checkjni=1 android.qemud=ttyS1 android.ndns=3
Unknown boot option `android.checkjni=1': ignoring
Unknown boot option `android.qemud=ttyS1': ignoring
Unknown boot option `android.ndns=3': ignoring
PID hash table entries: 512 (order: 9, 2048 bytes)
Console: colour dummy device 80x30
Dentry cache hash table entries: 16384 (order: 4, 65536 bytes)
Memory: 96MB = 96MB total
Memory: 91548KB available (2616K code, 681K data, 104K init)
Calibrating delay loop... 403.04 BogoMIPS (lpj=2015232)
Mount-cache hash table entries: 512
Initializing cgroup subsys debug
Initializing cgroup subsys cpuacct
Initializing cgroup subsys freezer
CPU: Testing write buffer coherency: ok
...
You can also have the emulator print out information about its own execution using
the -verbose flag, thereby allowing you to see, for example, which images files it's using:
$ emulator -verbose
emulator: found Android build root: /home/karim/android/aosp-2.3.x
emulator: found Android build out: /home/karim/android/aosp-2.3.x/out/target/product/generic
emulator: locking user data image at /home/karim/android/aosp-2.3.x/out/target/product
/generic/userdata-qemu.img
emulator: selecting default skin name 'HVGA'
emulator: found skin-specific hardware.ini: /home/karim/android/aosp-2.3.x/sdk/emulator/skins
/HVGA/hardware.ini
emulator: autoconfig: -skin HVGA
emulator: autoconfig: -skindir /home/karim/android/aosp-2.3.x/sdk/emulator/skins
80 | Chapter 3: AOSP Jumpstart

emulator: keyset loaded from: /home/karim/.android/default.keyset
emulator: trying to load skin file '/home/karim/android/aosp-2.3.x/sdk/emulator/skins
/HVGA/layout'
emulator: skin network speed: 'full'
emulator: skin network delay: 'none'
emulator: no SD Card image at '/home/karim/android/aosp-2.3.x/out/target/product/generic
/sdcard.img'
emulator: registered 'boot-properties' qemud service
emulator: registered 'boot-properties' qemud service
emulator: Adding boot property: 'qemu.sf.lcd_density' = '160'
emulator: Adding boot property: 'dalvik.vm.heapsize' = '16m'
emulator: argv[00] = "emulator"
emulator: argv[01] = "-kernel"
emulator: argv[02] = "/home/karim/android/aosp-2.3.x/prebuilt/android-arm/kernel/kernel-qemu"
emulator: argv[03] = "-initrd"
emulator: argv[04] = "/home/karim/android/aosp-2.3.x/out/target/product/generic/ramdisk.img"
emulator: argv[05] = "-nand"
emulator: argv[06] = "system,size=0x4200000,initfile=/home/karim/android/aosp-2.3.x/out
/target/product/generic/system.img"
emulator: argv[07] = "-nand"
emulator: argv[08] = "userdata,size=0x4200000,file=/home/karim/android/aosp-2.3.x/out/target
/product/generic/userdata-qemu.img"
emulator: argv[09] = "-nand"
...
Up to this point, I've used the terms QEMU and emulator interchangeably. The reality,
though, is that the emulator command isn't actually QEMU: it's a custom wrapper
around it created by the Android development team. You can, however, interact with
the emulator's QEMU by using the -qemu flag. Anything you pass after that flag is passed
on to QEMU and not the emulator wrapper:
$ emulator -qemu -h
QEMU PC emulator version 0.10.50Android, Copyright (c) 2003-2008 Fabrice Bellard
usage: qemu [options] [disk_image]
'disk_image' is a raw hard image image for IDE hard disk 0
Standard options:
-h or -help display this help and exit
-version display version information and exit
-M machine select emulated machine (-M ? for list)
-cpu cpu select CPU (-cpu ? for list)
-smp n set the number of CPUs to 'n' [default=1]
-numa node[,mem=size][,cpus=cpu[-cpu]][,nodeid=node]
-fda/-fdb file use 'file' as floppy disk 0/1 image
-hda/-hdb file use 'file' as IDE hard disk 0/1 image
...
$ emulator -qemu -...
We saw earlier how we can use adb to interact with the AOSP running within the
emulator, and we just saw how we can use various options to change the way the
Mastering the Emulator | 81

emulator is started. Interestingly, we can also control the emulator's behavior at run-
time by telneting into it. Every emulator instance that starts is assigned a port number
on the host. Go back to Figure 3-2 and check the top-left corner of the emulator's
window. That number up there (5554 in this case) is the port number at which that
emulator instance is listening. The next emulator that starts simultaneously will get
5556, the next 5558, and so on. To get access to the emulator's special console, you
can use the regular telnet command:
$ telnet localhost 5554
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Android Console: type 'help' for a list of commands
OK
help
Android console command help:
help|h|? print a list of commands
event simulate hardware events
geo Geo-location commands
gsm GSM related commands
kill kill the emulator instance
network manage network settings
power power related commands
quit|exit quit control session
redir manage port redirections
sms SMS related commands
avd manager virtual device state
window manage emulator window
try 'help <command>' for command-specific help
OK
Using that console you can do some nifty tricks like redirecting a port from the host to
the target:
redir add tcp:8080:80
OK
redir list
tcp:8080 => 80
OK
From here on, anything accessing 8080 on your host will actually be speaking to what-
ever is listening to port 80 on that emulated Android. Nothing listens to that port by
default on Android, but you can, for example, have BusyBox's httpd running on Android
and connect to it in this way.
The emulator also exposes a few "magic" IPs to the emulated Android. IP address
10.0.2.2, for instance, is an alias to your workstation's 127.0.0.1. If you have Apache
82 | Chapter 3: AOSP Jumpstart

running on your workstation, you can open the emulator's browser and type http://
10.0.2.2 and you'll be able to browse whatever content is served up by Apache.
For more information on how to operate the emulator and its various options, have a
look at the Using the Android Emulator section of Google's Android Developers
Guide. It's written for an app developer audience, but it will still be very useful to you
even if you're doing platform work.
Mastering the Emulator | 83

The Build System
The goal of the past chapter was to get you up and running as fast as possible with
custom AOSP development. There's nothing precluding you from closing this book at
this point and start to dig in and modify your AOSP tree to fit your needs. All you need
to do to test your modifications is rebuild the AOSP, start the emulator again and, if
need be, shell back into it using ADB. If you want to maximize your efforts, however,
you'll likely want some insight on Android's build system.
Despite it being modular, Android's build system is fairly complex and doesn't resemble
any of the mainstream build systems out there; none that are used for most open source
projects at least. Specifically, it uses make in a fairly unconventional way and doesn't
provide any sort of menuconfig-based configuration (or equivalent for that matter.)
Android very much has its own build paradigm that takes some time to get used to. So
pack yourself a good coffee or two, things are about to get serious.
Comparisons With Other Build Systems
Before I start explaining how Android's build system works, allow me to begin by em-
phasizing how it differs from what you might already know. First and foremost, unlike
most make-based build systems, the Android build system doesn't rely on recursive
makefiles. Unlike the Linux kernel for instance, there isn't a top-level makefile that will
recursively invoke subdirectories' makefiles. Instead, there is a script that explores all
directories and subdirectories until it finds an Android.mk file, whereupon it stops and
doesn't explore the subdirectories underneath that file's location. Note that Android
doesn't rely on makefiles called Makefile. Instead, it's the Android.mk files that specify
how the local "module" is built.
Android build "modules" have nothing to do with kernel "modules."
Within the context of Android's build system, a "module" is any com-
ponent of the AOSP that needs to be built. This might be a binary, an
app package, a library, etc. and it might have to be built for the target
or the host, but it's still a "module" with regards to the build system.

Another Android specificity is the way the build system is configured. While most of
us are used to systems based on kernel-style menuconfig or GNU autoconf/automake,
Android relies on a set of variables that are either set dynamically as part of the shell's
environment by way of envsetup.sh and lunch, or are defined statically ahead of time in
a buildspec.mk file. Also—always seeming to be a surprise to newcomers—the level of
configurability made possible by Android's build system is fairly limited. So while you
can specify the properties of the target for which you want the AOSP to be built and,
to a certain extent, which apps should be included by default in the resulting AOSP,
there is no way for you enable/disable features as is possible a-la menuconfig. You can't,
for instance, decide that you don't want Wifi support or that you don't want the Lo-
cation Service to start by default.
Also, the build system doesn't generate object files or any sort of intermediate output
within the same location as the source files. You won't find the .o files alongside
their .c source files within the source tree, for instance. In fact, none of the existing
AOSP directories are used in any of the output. Instead, the build system creates an
out/ directory where it stores everything it generates. Hence, a make clean is very much
the same thing as a rm -rf out/. In other words, removing the out/ directory wipes out
anything that was built.
The last thing to say about the build system before we start exploring it in more detail
is that it's heavily tied to GNU make. And, more to the point, versions 3.81 or newer
of it. The build system in fact heavily relies on many GNU make-specific features such
as the define, include, and ifndef directives.
Some Background on the Design of Android's Build System
If you would like to get more insight as to the design choices that were made when
putting together Android's build system, have a look at the build/core/build-sys-
tem.html file in the AOSP. It's dated May 2006 and seems to have been the document
that went around within the Android dev team to get consensus on a rework of the
build system. Some of the information and hypothesis are out of date or have been
obsoleted, but most of the nuggets of the current build system are there. In general, I've
found that the further back the document was created by the Android dev team, the
more insightful it is regarding raw motivations and technical background. Newer docu-
ments tend to be "cleaned up" and abstract, if they exist at all.
If you want to understand the technical underpinnings of why Android's build system
doesn't use recursive make, have a look at the paper entitled "Recursive Make Consid-
ered Harmful" by Peter Miller in AUUGN Journal of AUUG Inc., 19(1), pp. 14-25. The
paper explores the issues surrounding the use of recursive makefiles and explains a
different approach involving the use of a single global makefile for building the entire
project based on module-provided .mk files, which is exactly what Android does.
86 | Chapter 4: The Build System

Figure 4-1. Android's build system
Architecture
As illustrated in Figure 4-1, the entry point to making sense of the build system is the
main.mk file found in the build/core/ directory, which is invoked through the top-level
makefile, as we saw earlier. The build/core/ directory actually contains the bulk of the
build system, and we'll cover key files from there. Again, remember that Android's build
system pulls everything into a single Makefile; it isn't recursive. Hence, each .mk file
you see eventually becomes part of single huge makefile that contains the rules for
building all the pieces in the system.
Why does make hang?
Every time you type make, you witness the aggregation of the .mk files into a single set
through what might seem like an annoying build artifact: the build system prints out
the build configuration and seems to hang for quite some time without printing any-
thing to the screen. After these long moments of screen silence, it then actually starts
proceeding again and builds every part of the AOSP, at which point you see regular
output to your screen as you'd expect from any regular build system. Anyone who's
built the AOSP has wondered what in the world is the build system doing during that
time. What it's doing is incorporating every Android.mk file it can find the AOSP.
If you want to see this in action, edit the build/core/main.mk and replace this line:
Architecture | 87

include $(subdir_makefiles)
with this:
$(foreach subdir_makefile, $(subdir_makefiles), \
$(info Including $(subdir_makefile)) \
$(eval include $(subdir_makefile)) \
)
subdir_makefile :=
The next time you type make, you'll actually see what's happening:
$ make -j16
============================================
PLATFORM_VERSION_CODENAME=REL
PLATFORM_VERSION=2.3.4
TARGET_PRODUCT=generic
...
============================================
Including ./bionic/Android.mk
Including ./development/samples/Snake/Android.mk
Including ./libcore/Android.mk
Including ./external/elfutils/Android.mk
Including ./packages/apps/Camera/Android.mk
Including ./device/htc/passion-common/Android.mk
...
Configuration
One of the first things the build system does is pull in the build configuration through
the inclusion of config.mk. The build can be configured either by the use of the env-
setup.sh and lunch commands or by providing a buildspec.mk file at the top-level di-
rectory. In either case, some of the following variables need to be set.
TARGET_PRODUCT
Android flavor to be built. Each recipe can, for instance, include a different set of
apps or locales or build different parts of the tree. Have a look at the various single
product .mk files included by the AndroidProducts.mk files in build/target/prod-
uct/, device/samsung/crespo/, and device/htc/passion/ for examples. Values include:
generic
The "vanilla" kind, the most basic build of the AOSP parts you can have.
full
The "all dressed" kind, with most apps and the major locales enabled.
full_crespo
Same as full but for Crespo (i.e. Samsung Nexus S.)
88 | Chapter 4: The Build System

sim
Android simulator (see sidebar.)
sdk
The SDK; includes a vast number of locales.
TARGET_BUILD_VARIANT
Selects which modules to install. Each module is supposed to have a LOCAL_MOD
ULE_TAGS variable set in its Android.mk to at least one of:* user, debug, eng, tests,
optional, or samples. By selecting the variant, you will tell the build system which
module subsets should be included. Specifically:
eng
Includes all modules tagged as user, debug or eng.
userdebug
Includes both modules tagged as user and debug.
user
Includes only modules tagged as user.
TARGET_BUILD_TYPE
Dictates whether or not special build flags are used or DEBUG variables are defined
in the code. The possible values here are either release or debug. Most notably, the
frameworks/base/Android.mk file chooses between either frameworks/base/core/
config/debug or frameworks/base/core/config/ndebug, depending on whether or not
this variable is set to debug. The former causes the ConfigBuildFlags.DEBUG Java
constant to be set to true, whereas the latter causes it to be set to false. Some code
in parts of the system services, for instance, is conditional on DEBUG. Typically,
TARGET_BUILD_TYPE is set to release.
TARGET_TOOLS_PREFIX
By default, the build system will use one of the cross-development toolchains ship-
ped with it underneath the prebuilt/ directory. However, if you'd like it to use an-
other toolchain, you can set this value to point to its location.
OUT_DIR
By default, the build system will put all build output into the out/ directory. You
can use this variable to provide an alternate output directory.
BUILD_ENV_SEQUENCE_NUMBER
If you use the template build/buildspec.mk.default to create your own build-
spec.mk fiile, this value will be properly set. However, if you create a build-
spec.mk with an older AOSP release and try to use it in a future AOSP release that
contains important changes to its build system and, hence, a different value, this
* If you do not provide a value, defaults will be used. For instance, all apps are set to optional by default. Also,
some modules are part of GRANDFATHERED_USER_MODULES in user_tags.mk. No LOCAL_MODULE_TAGS need be
specified for those; they're always included.
Architecture | 89

variable will act as a safety net. It will cause the build system to inform you that
your buildspec.mk file doesn't match your build system.
Android Simulator
If you go back to the menu printed by lunch in “Building Android” on page 69, you'll
notice an entry called simulator. In fact you'll find references to the simulator at a
number of locations, including quite a few Android.mk files and subdirectories in the
tree. The most important thing you need to know about the simulator is that it has
nothing to do with the emulator. They are two completely different things.
That said, the simulator appears to be a remnant of the Android's team early work to
create Android. Since at the time they didn't even have Android running in QEMU,
they used their desktop OSes and the LD_PRELOAD mechanism to simulate an Android
device, hence the term "simulator." It appears that they stopped using it as soon as
running Android on QEMU became possible. It's still there, though, as it can be useful
for building parts of the AOSP for development and testing on developer workstations.
That doesn't mean that you run the AOSP on your desktop. In fact you can't, if nothing
else because you need a kernel that has Binder included and you would need to be using
Bionic instead of your system's default C library. But, if you want to run parts of what's
built from the AOSP on your desktop, this product target will allow you to do so.
Various parts of the code build very differently if the target is the simulator. When
browsing the code, for example, you'll sometimes find conditional builds around the
HAVE_ANDROID_OS C macro.† The code that talks to the Binder is one of these. If
HAVE_ANDROID_OS is not defined, that code will return an error to its caller instead of
trying to actually talk to the Binder driver.
For the full story behind the simulator, have a look at Android developer Andrew
McFadden's response to a post entitled "Android Simulator Environment" on the an-
droid-porting mailing list in April 2009.
In addition to selecting which parts of the AOSP to build and which options to build
them with, the build system also needs to know about the target it's building for. This
is provided through a BoardConfig.mk file which will specify things such as the com-
mand line to be provided to the kernel, the base address at which the kernel should be
loaded, or the instruction set version most appropriate for the board's CPU (TAR
GET_ARCH_VARIANT.) Have a look at build/target/board/ for a set of per-target directories
that each contain a BoardConfig.mk file. Also have a look at the various device/*/TAR
GET_DEVICE/BoardConfig.mk files included in the AOSP. The latter are much richer than
the former because they contain a lot more hardware-specific information. The device
name (i.e. TARGET_DEVICE) is derived from the PRODUCT_DEVICE specified in the prod-
uct .mk file provided for the TARGET_PRODUCT set in the configuration. For example,
device/samsung/crespo/AndroidProducts.mk includes device/samsung/crespo/
†HAVE_ANDROID_OS is only defined when compiling for the simulator.
90 | Chapter 4: The Build System

full_crespo.mk, which sets PRODUCT_DEVICE to crespo. Hence, the build system looks for
a BoardConfig.mk in device/*/crespo/, and there happens to be one at that location.
The final piece of the puzzle with regard to configuration is the CPU-specific options
used to build Android. For ARM, those are contained in build/core/combo/arch/arm/
armv*.mk, with TARGET_ARCH_VARIANT determining the actual file to use. Each file lists
CPU-specific cross-compiler and cross-linker flags used for building C/C++ files. They
also contain a number of ARCH_ARM_HAVE_* variables that enable others parts of the AOSP
to build code conditionally based on whether a given ARM feature is found in the
target's CPU.
envsetup.sh
Now that you understand the kinds of configuration input the build system needs, we
can actually discuss the role of envsetup.sh in more detail. As its name implies, env-
setup.sh actually is for setting up a build environment for Android. It does only part of
the job, though. Mainly, it defines a series of shell commands that are useful to any sort
of AOSP work:
$ cd ~/android/aosp-2.3.x
$ . build/envsetup.sh
$ help
Invoke ". build/envsetup.sh" from your shell to add the following functions to your environment:
- croot: Changes directory to the top of the tree.
- m: Makes from the top of the tree.
- mm: Builds all of the modules in the current directory.
- mmm: Builds all of the modules in the supplied directories.
- cgrep: Greps on all local C/C++ files.
- jgrep: Greps on all local Java files.
- resgrep: Greps on all local res/*.xml files.
- godir: Go to the directory containing a file.
Look at the source to view more functions. The complete list is:
add_lunch_combo cgrep check_product check_variant choosecombo chooseproduct choosetype
choosevariant cproj croot findmakefile gdbclient get_abs_build_var getbugreports
get_build_var getprebuilt gettop godir help isviewserverstarted jgrep lunch m mm mmm
pgrep pid printconfig print_lunch_menu resgrep runhat runtest set_java_home setpaths
set_sequence_number set_stuff_for_environment settitle smoketest startviewserver
stopviewserver systemstack tapas tracedmdump
You'll likely find the croot and godir commands quite useful for traversing the tree.
Some parts of it are quite deep, given the use of Java and its requirement that packages
be stored in directory trees bearing the same hierarchy as each sub-part of the corre-
sponding fully-qualified package name.‡ Hence, it's not rare to find yourself 7 to 10
directories underneath the AOSP's top-level directory, and it rapidly becomes tedious
to type something like cd ../../../ ... to return to an upper part of the tree.
‡For instance, a file part of the com.foo.bar package must be stored under the com/foo/bar/ directory.
Architecture | 91

m and mm are also quite useful since they allow you to, respectively, build from the
top-level regardless of where you are or just build the modules found in the current
directory. For example, if you made a modification to the Launcher and are in packages/
apps/Launcher2, you can rebuild just that module by typing mm instead of cd'ing back
to the top-level and typing make. Note that mm doesn't rebuild the entire tree and,
therefore, won't regenerate AOSP images even if a dependent module has changed. m
will do that, though. Still, mm can be useful to test whether your local changes break
the build or not until you're ready to regenerate the full AOSP.
Although the online help doesn't mention lunch, it is one of the commands defined by
envsetup.sh. When you run lunch without any parameters, it shows you a list of po-
tential choices:
$ lunch
You're building on Linux
Lunch menu... pick a combo:
1. generic-eng
2. simulator
3. full_passion-userdebug
4. full_crespo4g-userdebug
5. full_crespo-userdebug
Which would you like? [generic-eng]
These choices are not static. Most depend on what's in the AOSP at the time env-
setup.sh runs. They're in fact individually added using the add_lunch_combo() function
that the script defines. So, for instance, by default envsetup.sh adds generic-eng and
simulator:
# add the default one here
add_lunch_combo generic-eng
# if we're on linux, add the simulator. There is a special case
# in lunch to deal with the simulator
if [ "$(uname)" = "Linux" ] ; then
add_lunch_combo simulator
fi
envsetup.sh also includes all the vendor supplied scripts it can find:
# Execute the contents of any vendorsetup.sh files we can find.
for f in `/bin/ls vendor/*/vendorsetup.sh vendor/*/build/vendorsetup.sh device/*/*/
vendorsetup.sh 2> /dev/null`
do
echo "including $f"
. $f
92 | Chapter 4: The Build System

done
The device/samsung/crespo/vendorsetup.sh file, for instance, does this:
add_lunch_combo full_crespo-userdebug
So that's how you end up with the menu we saw earlier. Note that the menu asks you
to choose a combo. Essentially, this is a combination of a TARGET_PRODUCT and TAR
GET_BUILD_VARIANT, with the exception of the simulator. The menu provides the default
combinations, but the others remain valid still and can be passed to lunch as parameters
on the command line:
$ lunch generic-user
============================================
PLATFORM_VERSION_CODENAME=REL
PLATFORM_VERSION=2.3.4
TARGET_PRODUCT=generic
TARGET_BUILD_VARIANT=user
TARGET_SIMULATOR=false
TARGET_BUILD_TYPE=release
TARGET_BUILD_APPS=
TARGET_ARCH=arm
HOST_ARCH=x86
HOST_OS=linux
HOST_BUILD_TYPE=release
BUILD_ID=GINGERBREAD
============================================
$ lunch full_crespo-eng
============================================
PLATFORM_VERSION_CODENAME=REL
PLATFORM_VERSION=2.3.4
TARGET_PRODUCT=full_crespo
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
Once lunch has finished running for a generic-eng combo, it will set up environment
variables described in Table 4-1 in your current shell to provide the build system with
the required configuration information.
Architecture | 93

Table 4-1. Environment variables set by lunch (in no particular order)
Variable Value
PATH $ANDROID_JAVA_TOOLCHAIN:$PATH:$ANDROID_BUILD_PATHS
ANDROID_EABI_TOOLCHAIN aosp-root/prebuilt/linux-x86/toolchain/arm-eabi-4.4.3/bin
ANDROID_TOOLCHAIN $ANDROID_EABI_TOOLCHAIN
ANDROID_QTOOLS aosp-root/development/emulator/qtools
ANDROID_BUILD_PATHS aosp-root/out/host/linux-x86:$ANDROID_TOOLCHAIN:
$ANDROID_QTOOLS:$ANDROID_TOOLCHAIN:$ANDROID_EABI_TOOL
CHAIN
ANDROID_BUILD_TOP aosp-root
ANDROID_JAVA_TOOLCHAIN $JAVA_HOME/bin
ANDROID_PRODUCT_OUT aosp-root/out/target/product/generic
OUT ANDROID_PRODUCT_OUT
BUILD_ENV_SEQUENCE_NUMBER 10
OPROFILE_EVENTS_DIR aosp-root/prebuilt/linux-x86/oprofile
TARGET_BUILD_TYPE release
TARGET_PRODUCT generic
TARGET_BUILD_VARIANT eng
TARGET_BUILD_APPS empty
TARGET_SIMULATOR false
PROMPT_COMMAND \"\033]0;[${TARGET_PRODUCT}-${TARGET_BUILD_VARIANT}] $
{USER}@${HOSTNAME}: ${PWD}\007\"
JAVA_HOME /usr/lib/jvm/java-6-sun
Using ccache
If you've already done any AOSP building while reading these pages, you've noticed
how long the process is. Obviously, unless you can construct yourself a bleeding edge
build farm, any sort of speedup on your current hardware would be greatly appreciated.
As a sign that the Android development team might itself also feel the pain of the rather
long builds, they've added support for ccache. ccache stands for Compiler Cache and is
part of the Samba Project. It's a mechanism that caches the object files generated by the
compiler based on the preprocessor's output. Hence, if under two separate builds the
preprocessor's output is identical, use of ccache will result in the second build not
actually using the compiler to build the file. Instead, the cached object file will be copied
to the destination where the compiler's output would have been.
To enable the use of ccache, all you need to do is make sure that the USE_CCACHE envi-
ronment variable is set to 1 before you start your build:
94 | Chapter 4: The Build System

$ export USE_CCACHE=1
You won't gain any acceleration the first time you run since the cache will be empty at
that time. Every other time you build from scratch, though, the cache will help accel-
erate the build process. The only downside is that ccache is for C/C++ files only. Hence,
it can't accelerate the build of any Java file, I must add sadly. There are about 15,000
C/C++ files in the AOSP and 18,000 Java files. So while the cache isn't a panacea, it's
interesting.
If you'd like to learn more about ccache, have a look at the article titled "Improve col-
laborative build times with ccache" by Martin Brown on IBM's developerWorks' site.
The article also explores the use of distcc, which allows you to distribute builds over
several machines, allowing you to pool your team's workstations caches together.
Of course, if you get tired of always typing . build/envsetup.sh and lunch, all you need
to do is copy the build/buildspec.mk.default into the top-level directory, rename it to
buildspec.mk, and edit it to match the configuration that would have otherwise set by
running those commands. The file already contains all the variables that you need to
provide; it's just a matter of uncommenting the corresponding lines and setting the
values appropriately. Once you've done that, all you have to do is go to the AOSP's
directory and invoke make directly. You can skip envsetup.sh and lunch.
Directive Definitions
Because the build system is fairly large—there are about 40 files in build/core/ alone—
there are benefits in being able to reuse as much code as possible. This is why the build
system defines a large number of directives§ in the definitions.mk file. That file is actually
the largest one in the build system at about 60KB, with about 140 directives on ~1,800
lines of makefile code. Directives offer a variety of functionalities, including file lookup
(e.g., all-makefiles-under and all-c-files-under), transformation (e.g., transform-c-
to-o and transform-java-to-classes.jar), copying (e.g., copy-file-to-target) and
utility (e.g., my-dir.)
Not only are these directives used throughout the rest of the build system's components
and act as its core library, but they're sometimes also directly used in modules' An-
droid.mk files. Here's an example snippet from the Calculator app's Android.mk:
LOCAL_SRC_FILES := $(call all-java-files-under, src)
Although thoroughly describing definitions.mk is outside the scope of this book, it
should be fairly easy for you to explore it on your own. If nothing else, most of the
directives in it are preceeded with a comment explaining what they do. For example:
§Makefile directives are very much akin to functions in a programming language.
Architecture | 95

###########################################################
## Find all of the java files under the named directories.
## Meant to be used like:
## SRC_FILES := $(call all-java-files-under,src tests)
###########################################################
define all-java-files-under
$(patsubst ./%,%, \
$(shell cd $(LOCAL_PATH) ; \
find $(1) -name "*.java" -and -not -name ".*") \
)
endef
Main Make Recipes
At this point you might be wondering where any of the goodies are actually generated.
How are the various images such as RAM disk generated or how is the SDK put together,
for example? Well, I hope you won't hold a grudge, but I've been keeping the best for
last. So without further ado, have a look at the Makefile in build/core/ (not the top-level
one). The file start with an innocuous-looking comment:
# Put some miscellaneous rules here
But don't be fooled. This is where some of the best meat is. Here's the snippet that takes
care of generating the RAM disk for example:
# -----------------------------------------------------------------
# the ramdisk
INTERNAL_RAMDISK_FILES := $(filter $(TARGET_ROOT_OUT)/%, \
$(ALL_PREBUILT) \
$(ALL_COPIED_HEADERS) \
$(ALL_GENERATED_SOURCES) \
$(ALL_DEFAULT_INSTALLED_MODULES))
BUILT_RAMDISK_TARGET := $(PRODUCT_OUT)/ramdisk.img
# We just build this directly to the install location.
INSTALLED_RAMDISK_TARGET := $(BUILT_RAMDISK_TARGET)
$(INSTALLED_RAMDISK_TARGET): $(MKBOOTFS) $(INTERNAL_RAMDISK_FILES) | $(MINIGZIP)
$(call pretty,"Target ram disk: $@")
$(hide) $(MKBOOTFS) $(TARGET_ROOT_OUT) | $(MINIGZIP) > $@
And here's the snippet that creates the certs packages for checking OTA‖ updates:
# -----------------------------------------------------------------
‖Over-The-Air
96 | Chapter 4: The Build System

# Build a keystore with the authorized keys in it, used to verify the
# authenticity of downloaded OTA packages.
#
# This rule adds to ALL_DEFAULT_INSTALLED_MODULES, so it needs to come
# before the rules that use that variable to build the image.
ALL_DEFAULT_INSTALLED_MODULES += $(TARGET_OUT_ETC)/security/otacerts.zip
$(TARGET_OUT_ETC)/security/otacerts.zip: KEY_CERT_PAIR := $(DEFAULT_KEY_CERT_PAIR)
$(TARGET_OUT_ETC)/security/otacerts.zip: $(addsuffix .x509.pem,$(DEFAULT_KEY_CERT_PAIR))
$(hide) rm -f $@
$(hide) mkdir -p $(dir $@)
$(hide) zip -qj $@ $<
.PHONY: otacerts
otacerts: $(TARGET_OUT_ETC)/security/otacerts.zip
Obviously there's a lot more than I can fit here, but have a look at Makefile for infor-
mation on how any of the following are created:
• Properties (including the target's /default.prop and /system/build.prop)
• RAM disk
• Boot image (combining the RAM disk and a kernel image)
• NOTICE files
• OTA keystore
• Recovery image
• System image (the target's /system directory)
• Data partition image (the target's /data directory)
• OTA update package
• SDK
Nevertheless, some things aren't in this file:
Kernel images
Don't look for any rule to build these. There is no kernel part of the AOSP. Instead,
you need to find an Androidized kernel for your target, build it separately from the
AOSP, and feed it to the AOSP. You can find a few examples of this in the devices
in the device/ directory. device/samsung/crespo/, for example, includes a kernel im-
age (file called kernel) and a loadable module for the Crespo's Wifi (bcm4329.ko
file.) Both of these are built outside the AOSP and copied in binary form into the
tree for inclusion with the rest of the build.
NDK
While the code to build the NDK is in the AOSP, it's entirely separate from the
AOSP's build system in build/. Instead, the NDK's build system is in ndk/build/.
We'll discuss how to build the NDK shortly.
CTS
The rules for building the CTS are in build/core/tasks/cts.mk.
Architecture | 97

Cleaning
As I mentioned earlier, a make clean is very much the equivalent of wipping out the
out/ directory. The clean target itself is defined in main.mk. There are, however, other
clean up targets. Most notably, installclean, which is defined in cleanbuild.mk, is
automatically invoked whenever you change TARGET_PRODUCT or TARGET_BUILD_VAR
IANT. For instance, if I had first built the AOSP for the generic-eng combo and then
used lunch to switch the combo to full-eng, the next time I start make, some of the
build output will be automatically pruned using installclean:
$ make -j16
============================================
PLATFORM_VERSION_CODENAME=REL
PLATFORM_VERSION=2.3.4
TARGET_PRODUCT=full
TARGET_BUILD_VARIANT=eng
...
============================================
*** Build configuration changed: "generic-eng-{mdpi,nodpi}" -> "full-eng-{en_US,en_GB,
fr_FR,it_IT,de_DE,es_ES,mdpi,nodpi}"
*** Forcing "make installclean"...
*** rm -rf out/target/product/generic/data/* out/target/product/generic/data-qemu/*
out/target/product/generic/userdata-qemu.img out/host/linux-x86/obj/NOTICE_FILES
out/host/linux-x86/sdk out/target/product/generic/*.img out/target/product/generic/*.txt
out/target/product/generic/*.xlb out/target/product/generic/*.zip
out/target/product/generic/data out/target/product/generic/obj/APPS
out/target/product/generic/obj/NOTICE_FILES out/target/product/generic/obj/PACKAGING
out/target/product/generic/recovery out/target/product/generic/root
out/target/product/generic/system out/target/product/generic/dex_bootjars
out/target/product/generic/obj/JAVA_LIBRARIES
*** Done with the cleaning, now starting the real build.
In contrast to clean, installclean doesn't wipe out the entirety of out/. Instead, it only
nukes the parts that need rebuilding given the combo configuration change. There's
also a clobber target which is essentially the same thing as a clean.
Module Build Templates
What I just described is the build system's architecture and the mechanics of its core
components. Having read that, you should have a much better idea of how Android is
built from a top-down perspective. Very little of that, however, permeates down to the
level of AOSP modules' Android.mk files. The system has in fact been architectured so
that module build recipes are pretty much independent from the build system's inter-
nals. Instead, build templates are provided so that module authors can get their mod-
ules built appropriately. Each template is tailored for a specific type of module and
module authors can use a set of documented variables, all prefixed by LOCAL_, to mod-
ulate the templates' behavior and output. Of course, the templates and underlying
support files (mainly base_rules.mk) closely interact with the rest of the build system
98 | Chapter 4: The Build System

to deal properly with each module's build output. But that's invisible to the module's
author.
The templates are themselves found in the same location as the rest of the build system
in build/core/. Android.mk gets access to them through the include directive. Here's an
example:
include $(BUILD_PACKAGE)
As you can see, Android.mk files don't actually include the .mk templates by name.
Instead, they include a variable that is set to the corresponding .mk file. Table 4-2
provides the full list of available module templates.
Table 4-2. Module build templates list
Variable Template What the tem- Most notable use
plate builds
BUILD_EXECUTABLE executable.mk Target binaries Native commands and daemons
BUILD_HOST_EXECUTABLE host_executable.mk Host binaries Development tools
BUILD_RAW_EXECUTABLE raw_executable.mk Target binaries that Code in the bootloader/ directory
run on bare metal
BUILD_JAVA_LIBRARY java_library.mk Target Java libaries Apache Harmony and Android
framework
BUILD_STATIC_JAVA_LIBRARY static_java_library.mk Target static Java li- N/A, few modules use this
braries
BUILD_HOST_JAVA_LIBRARY host_java_library.mk Host Java libraries Development tools
BUILD_SHARED_LIBRARY shared_library.mk Target shared libra- A vast number of modules, includ-
ries ing many in external/ and frame-
works/base/
BUILD_STATIC_LIBRARY static_library.mk Target static libra- A vast number of modules, includ-
ries ing many in external/
BUILD_HOST_SHARED_LIBRARY host_shared_library.mk Host shared libra- Development tools
ries
BUILD_HOST_STATIC_LIBRARY host_static_library.mk Host static libraries Development tools
BUILD_RAW_STATIC_LIBRARY raw_static_library.mk Target static libra- Code in bootloader/
ries that run on bare
metal
BUILD_PREBUILT prebuilt.mk For copying pre- Configuration files and binaries
built target files
BUILD_HOST_PREBUILT host_prebuilt.mk For copying pre- Tools in prebuilt/ and configura-
built host files tion files
BUILD_MULTI_PREBUILT multi_prebuilt.mk For copying pre- Rarely used
built modules of
Architecture | 99

Variable Template What the tem- Most notable use
plate builds
multiple but
known type, like
Java libraries or ex-
ecutables
BUILD_PACKAGE package.mk Built-in AOSP apps All stock AOSP apps
(i.e. anything that
ends up being
an .apk
BUILD_KEY_CHAR_MAP key_char_map.mk Device character All device character maps in AOSP
maps
These build templates allow Android.mk files to be usually fairly light-weight:
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
LOCAL_VARIABLE_1 := value_1
LOCAL_VARIABLE_2 := value_2
...
include $(BUILD_MODULE_TYPE)
Tells the build template where the current module is located.
Clears all previously set LOCAL_* variables that might have been set for other
modules.
Sets various LOCAL_* variables to module-specific values.
Invokes the build template that corresponds to the current module's type.
Note that CLEAR_VARS, which is provided by clear_vars.mk, is very im-
portant. Recall that the build system includes all Android.mk into what
amounts to a single huge makefile. Including CLEAR_VARS ensures that
the LOCAL_* values set for modules preceeding yours are zeroed out by
the time your Android.mk is included. Also, a single Android.mk can
describe multiple modules one after the other. Hence, CLEAR_VARS en-
sures that previous module recipes don't pollute subsequent ones.
Here's the Service Manager's Android.mk for instance (frameworks/base/cmds/service-
manager/):#
LOCAL_PATH:= $(call my-dir)
100 | Chapter 4: The Build System

include $(CLEAR_VARS)
LOCAL_SHARED_LIBRARIES := liblog
LOCAL_SRC_FILES := service_manager.c binder.c
LOCAL_MODULE := servicemanager
ifeq ($(BOARD_USE_LVMX),true)
LOCAL_CFLAGS += -DLVMX
endif
include $(BUILD_EXECUTABLE)
And here's the one from the Desk Clock app (packages/app/DeskClock/):*
LOCAL_PATH:= $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE_TAGS := optional
LOCAL_SRC_FILES := $(call all-java-files-under, src)
LOCAL_PACKAGE_NAME := DeskClock
LOCAL_OVERRIDES_PACKAGES := AlarmClock
LOCAL_SDK_VERSION := current
include $(BUILD_PACKAGE)
include $(call all-makefiles-under,$(LOCAL_PATH))
As you can see, essentially the same structure is used in both modules, even though
they provide very different input and result in very different output. Notice also the last
line from the Desk Clock's Android.mk, which basically includes all subdirectories'
Android.mk files. As I said earlier, the build system looks for the first makefile in a
hierarchy and doesn't look in any subdirectories underneath the directory where one
was found, hence the need to manually invoke those. Obviously the code here just goes
out and looks for all makefiles underneath. However, some parts of the AOSP either
explicitly list subdirectories or conditionnally select them based on configuration.
The documentation at http://source.android.com used to provide an exhaustive list of
all the LOCAL_* variables with their meaning and use. Unfortunately, at the time of this
writing, this list is no longer available. The build/core/build-system.html file, however,
contains an earlier version of that list and you should refer to that one until up-to-date
lists become available again. Here are some of the most frequently-encountered
LOCAL_* variables:
#This version is cleaned up a little (removed commented code for instance) and slightly reformatted for pretty-
print.
* Also slightly modified to remove white-space and comments.
Architecture | 101

LOCAL_PATH
The path of the current module's sources, typically provided by invoking $(call
my-dir).
LOCAL_MODULE
The name to attribute to this module's build output. The actual filename or output
and its location will depend on the build template you include. If this is set to
foo, for example, and you build an executable, the final executable will be a com-
mand called foo and it will be put in the target's /system/bin/. If LOCAL_MODULE is set
to libfoo and you include BUILD_SHARED_LIBRARY instead of BUILD_EXECUTABLE, the
build system will generate libfoo.so and put it in /system/lib/.
LOCAL_SRC_FILES
The source files used to build the module. You may provide those by using one the
build system's defined directives, as the Desk Clock uses all-java-files-under, or
you may list the files explicitly, as the Service Manager does.
LOCAL_PACKAGE_NAME
Unlike all other modules, apps use this variable instead of LOCAL_MODULE to provide
their names, as you can witness by comparing the two Android.mk shown earlier.
LOCAL_SHARED_LIBRARIES
Use this to list all the libraries your module depends on. As mentioned earlier, the
Service Manager depends on liblog instead of this variable.
LOCAL_MODULE_TAGS
As I mentioned earlier, this allows you to control under which TARGET_BUILD_VAR
IANT this module is built.
LOCAL_MODULE_PATH
Use this to override the default install location for the type of module you're build-
ing.
A good way to find out about more LOCAL_* variables is to look at existing An-
droid.mk files in the AOSP. Also, clear_vars.mk contains the full list of variables that
are cleared. So while it doesn't give you the meaning of each, it certainly lists them all.
Also, in addition to the cleaning targets that affect the AOSP globally, each module can
define its own cleaning rules by providing a CleanSpec.mk, much like modules provide
Android.mk files. Unlike the latter, though, the former aren't required. By default, the
build system has cleaning rules for each type of module. But you can specify your own
rules in a CleanSpec.mk in case your module's build does something the build system
doesn't generate by default and, therefore, wouldn't typically know how to clean up.
Output
Now that we've looked at how the build system works and how module build templates
are used by modules, let's look at the output it creates in out/. At a fairly high level, the
102 | Chapter 4: The Build System

build output operates in three stages and in two modes, one for the host and one for
the target:
1. Intermediates are generated using the module sources. These intermediates' format
and location depend on the module's sources. They may be .o files for C/C++ code,
for example, or .jar files for Java-based code.
2. Intermediates are used by the build system to create actual binaries and packages:
taking .o files, for example, and linking them into an actual binary.
3. The binaries and packages are assembled together into the final output requested
of the build system. Binaries, for instance, are copied into directories containing
the root and /system filesystems and images of those filesystems are generated for
use on the actual device.
out/ is mainly separated into two directories, reflecting its operating modes: host/ and
target/. In each directory, you will find a couple of obj/ directories that contain the
various intermediates generated during the build. Most of these are stored in subdir-
ectories named similarly to one the BUILD_* macros presented earlier or serve a specific
complementary purpose during the build system's operation:
• EXECUTABLES/
• JAVA_LIBRARIES/
• SHARED_LIBRARIES/
• STATIC_LIBRARIES/
• APPS/
• DATA/
• ETC/
• KEYCHARS/
• PACKAGING/
• NOTICE_FILES/
• include/
• lib/
The directory you'll likely be most interested in is out/target/product/PRODUCT_DEVICE/.
That's where the output images will be located for the PRODUCT_DEVICE defined in the
corresponding product configuration's .mk. Table 4-3 explains the content of that di-
rectory.
Table 4-3. Product output
Entry Description
android-info.txt Contains the codename for the board for which this product is configured.
clean_steps.mk Contains a list of steps that must be executed to clean the tree, as provided in CleanSpec.mk files by
calling the add-clean-step directive.
Architecture | 103

Entry Description
data/ The target's /data directory.
installed-files.txt A list of all the files installed in data/ and system/ directories.
obj/ The target product's intermediaries.
previous_build_con- The last build target; will be used on the next make to check if the config has changed, thereby forcing
fig.mk an installclean.
ramdisk.img The RAM disk image generated based on the content of the root/ directory.
root/ The content of the target's root filesystem.
symbols/ Unstripped versions of the binaries put in the root filesystem and /system directory.
system/ The target's /system directory.
system.img The /system image, based on the content of the system/ directory.
userdata.img The /data image, based on the content of the data/ directory.
Have a look back at Chapter 2 for a refresher on the root filesytem, /system, and /
data. Essentially, though, when the kernel boots, it will mount the RAM disk image
and execute the /init found inside. That binary, in turn, will run the /init.rc script that
will mount both the /system and /data images at their respective locations.
Build Recipes
With the build system's architecture and functioning in mind, let's take a look at some
of the most common, and some slightly uncommon, build recipes. We'll only lightly
touch on the use of the results of each recipe, often because the topic is best discussed
elsewhere, but you should have enough information to get you started.
The Default droid Build
Earlier, we went through a number of plain make commands but never really explained
the default target. When you run plain make, it's as if you had typed:†
$ make droid
droid is in fact the default target as defined in main.mk. You don't usually need to specify
this target manually. I'm providing it here for completeness, so that you know it exists.
†This assumes you had already run envsetup.sh and lunch.
104 | Chapter 4: The Build System

Seeing the Build Commands
When you build the AOSP, you'll notice that it doesn't actually show you the commands
it's running. Instead, it only prints out a summary of each step it's at. If you want to see
everything it does, like the gcc command lines for example, add the showcommands target
to the command line:
$ make showcommands
....
host Java: apicheck (out/host/common/obj/JAVA_LIBRARIES/apicheck_intermediates/classes)
for f in ; do if [ ! -f $f ]; then echo Missing file $f; exit 1; fi; unzip -qo $f -d
out/host/common/obj/JAVA_LIBRARIES/apicheck_intermediates/classes; (cd out/host/common
/obj/JAVA_LIBRARIES/apicheck_intermediates/classes && rm -rf META-INF); done
javac -J-Xmx512M -target 1.5 -Xmaxerrs 9999999 -encoding ascii -g -extdirs "" -d
out/host/common/obj/JAVA_LIBRARIES/apicheck_intermediates/classes \@out/host/common/obj
/JAVA_LIBRARIES/apicheck_intermediates/java-source-list-uniq || ( rm -rf out/host/common
/obj/JAVA_LIBRARIES/apicheck_intermediates/classes ; exit 41 )
rm -f out/host/common/obj/JAVA_LIBRARIES/apicheck_intermediates/java-source-list
rm -f out/host/common/obj/JAVA_LIBRARIES/apicheck_intermediates/java-source-list-uniq
jar -cfm out/host/common/obj/JAVA_LIBRARIES/apicheck_intermediates/javalib.jar build
/tools/apicheck/src/MANIFEST.mf -C out/host/common/obj/JAVA_LIBRARIES/apicheck_intermediates
/classes .
Header: out/host/linux-x86/obj/include/libexpat/expat.h
cp -f external/expat/lib/expat.h out/host/linux-x86/obj/include/libexpat/expat.h
Header: out/host/linux-x86/obj/include/libexpat/expat_external.h
cp -f external/expat/lib/expat_external.h out/host/linux-x86/obj/include/libexpat/expat_external.h
Header: out/target/product/generic/obj/include/libexpat/expat.h
cp -f external/expat/lib/expat.h out/target/product/generic/obj/include/libexpat/expat.h
...
Which, to illustrate what I just explained in the previous section, is also the same as:
$ make droid showcommands
As you'll rapidly notice when using this, it generates a lot of output and is therefore
hard to follow. You may, however, want to save the standard output and standard error
into files if you'd like to analyze the actual commands used to build the AOSP:
$ make showcommands > aosp-build-stdout 2> aosp-build-stderr
Building the SDK for Linux and MacOS
The official Android SDK is available at http://developer.android.com. You can, how-
ever, build your own SDK using the AOSP if, for instance, you extended the core APIs
to expose new functionality and would like to distribute the result to developers so they
can benefit from your new APIs. To do so, you'll need to select a special combo:
Build Recipes | 105

$ . build/envsetup.sh
$ lunch sdk-eng
$ make sdk
Once this is done, the SDK will be in out/host/linux-x86/sdk/ when built on Linux and
out/host/darwin-x86/sdk/ when built on a Mac. There will be two copies, one a zip file,
much like the one distributed at http://developer.android.com, and one uncompressed
and ready to use.
Assuming you had already configured Eclipse for Android development using the in-
structions at http://developer.android.com, you'll need to carry out two additional steps
to use your newly-built SDK. First, you'll need to tell Eclipse the location of the new
SDK. To do so, go to Window→Preferences→Android, enter the path to the new SDK
in the ”SDK Location” box, and click OK. Also, for reasons that aren't entirely clear to
the author at the time of this writing, you also need to go to Window→"Android SDK
and AVD Manager"→"Installed Packages" and click on "Update All..." That will display
a wizard. Reject all the items selected except the first one, "Android SDK Tools, revision
api_level", and click on "Install." Once that is done, you'll be able to create new projects
using the new SDK and access any new APIs you expose in it. If you don't do that second
step, you'll be able to create new Android projects, but none of them will resolve Java
libraries properly and will, therefore, never build.
Building the SDK for Windows
The instructions for building the SDK for Windows are slightly different from Linux
and MacOS:
$ . build/envsetup.sh
$ lunch sdk-eng
$ make win_sdk
The resulting output will be in out/host/windows/sdk/.
Building the CTS
If you want to build the CTS, you don't need to use envsetup.sh or lunch. You can go
right ahead and type:
$ make cts
...
Generating test description for package android.sax
Generating test description for package android.performance
Generating test description for package android.graphics
Generating test description for package android.database
Generating test description for package android.text
106 | Chapter 4: The Build System

Generating test description for package android.webkit
Generating test description for package android.gesture
Generating test plan CTS
Generating test plan Android
Generating test plan Java
Generating test plan VM
Generating test plan Signature
Generating test plan RefApp
Generating test plan Performance
Generating test plan AppSecurity
Package CTS: out/host/linux-x86/cts/android-cts.zip
Install: out/host/linux-x86/bin/adb
The cts commands includes its own online help:
$ cd out/host/linux-x86/bin/
$ ./cts
Listening for transport dt_socket at address: 1337
Android CTS version 2.3_r3
$ cts_host > help
Usage: command options
Avaiable commands and options:
Host:
help: show this message
exit: exit cts command line
Plan:
ls --plan: list available plans
ls --plan plan_name: list contents of the plan with specified name
add --plan plan_name: add a new plan with specified name
add --derivedplan plan_name -s/--session session_id -r/--result result_type: derive
a plan from the given session
rm --plan plan_name/all: remove a plan or all plans from repository
start --plan test_plan_name: run a test plan
start --plan test_plan_name -d/--device device_ID: run a test plan using the specified device
start --plan test_plan_name -t/--test test_name: run a specific test
...
$ cts_host > ls --plan
List of plans (8 in total):
Signature
RefApp
VM
Performance
AppSecurity
Android
Java
CTS
Once you have a target up and running, such as the emulator for instance, you can
launch the test suite and it will use adb to run tests on the target:
$ ./cts start --plan CTS
Listening for transport dt_socket at address: 1337
Build Recipes | 107

Android CTS version 2.3_r3
Device(emulator-5554) connected
cts_host > start test plan CTS
CTS_INFO >>> Checking API...
CTS_INFO >>> This might take several minutes, please be patient...
...
Building the NDK
As I had mentioned earlier, the NDK has its own separate build system, with its own
setup and help system, which you can invoke like this:
$ cd ndk/build/tools
$ export ANDROID_NDK_ROOT=aosp-root/ndk
$ ./make-release --help
Usage: make-release.sh [options]
Valid options (defaults are in brackets):
--help Print this help.
--verbose Enable verbose mode.
--release=name Specify release name [20110921]
--prefix=name Specify package prefix [android-ndk]
--development=path Path to development/ndk directory [/home/karim/opersys-dev/
android/aosp-2.3.4/development/ndk]
--out-dir=path Path to output directory [/tmp/ndk-release]
--force Force build (do not ask initial question) [no]
--incremental Enable incremental packaging (debug only). [no]
--darwin-ssh=hostname Specify Darwin hostname to ssh to for the build.
--systems=list List of host systems to build for [linux-x86]
--toolchain-src-dir=path Use toolchain sources from path
When you are ready to build the NDK, you can invoke make-release as follows, and
witness its rather emphatic warning:
$ ./make-release
IMPORTANT WARNING !!
This script is used to generate an NDK release package from scratch
for the following host platforms: linux-x86
This process is EXTREMELY LONG and may take SEVERAL HOURS on a dual-core
machine. If you plan to do that often, please read docs/DEVELOPMENT.TXT
that provides instructions on how to do that more easily.
Are you sure you want to do that [y/N]
y
Downloading toolchain sources...
Using git clone prefix: git://android.git.kernel.org/toolchain
108 | Chapter 4: The Build System

downloading sources for toolchain/binutils
...
Updating the API
The build systems has safeguards in case you modify the AOSP's core API. If you do,
the build will fail by default with a warning such as this:
******************************
You have tried to change the API from what has been previously approved.
To make these errors go away, you have two choices:
1) You can add "@hide" javadoc comments to the methods, etc. listed in the
errors above.
2) You can update current.xml by executing the following command:
make update-api
To submit the revised current.xml to the main Android repository,
you will need approval.
******************************
make: *** [out/target/common/obj/PACKAGING/checkapi-current-timestamp] Error 38
make: *** Waiting for unfinished jobs....
As the error message suggests, to get the build to continue, you'll need to do something
like this:
$ make update-api
...
Install: out/host/linux-x86/framework/apicheck.jar
Install: out/host/linux-x86/framework/clearsilver.jar
Install: out/host/linux-x86/framework/droiddoc.jar
Install: out/host/linux-x86/lib/libneo_util.so
Install: out/host/linux-x86/lib/libneo_cs.so
Install: out/host/linux-x86/lib/libneo_cgi.so
Install: out/host/linux-x86/lib/libclearsilver-jni.so
Copying: out/target/common/obj/JAVA_LIBRARIES/core_intermediates/emma_out/lib
/classes-jarjar.jar
Install: out/host/linux-x86/framework/dx.jar
Install: out/host/linux-x86/bin/dx
Install: out/host/linux-x86/bin/aapt
Copying: out/target/common/obj/JAVA_LIBRARIES/bouncycastle_intermediates
/emma_out/lib/classes-jarjar.jar
Copying: out/target/common/obj/JAVA_LIBRARIES/ext_intermediates/emma_out/lib
/classes-jarjar.jar
Install: out/host/linux-x86/bin/aidl
Copying: out/target/common/obj/JAVA_LIBRARIES/core-junit_intermediates/emma_out
/lib/classes-jarjar.jar
Copying: out/target/common/obj/JAVA_LIBRARIES/framework_intermediates/emma_out
Build Recipes | 109

/lib/classes-jarjar.jar
Copying current.xml
The next time you start make, you won't get any more errors regarding API changes.
Building a Single Module
Up to now, we've looked at building the entire tree. You can also build individual
modules. Here's how you can ask the build system to build the Launcher2 module (i.e.,
the Home screen):
$ make Launcher2
You can also clean modules individually:
$ make clean-Launcher2
If you'd like to force the build system to regenerate the system image to include your
updated module, you can add the snod target to the command line:
$ make Launcher2 snod
============================================
PLATFORM_VERSION_CODENAME=REL
PLATFORM_VERSION=2.3.4
TARGET_PRODUCT=generic
...
target Package: Launcher2 (out/target/product/generic/obj/APPS/Launcher2_intermediates/package.apk)
'out/target/common/obj/APPS/Launcher2_intermediates//classes.dex' as 'classes.dex'...
Install: out/target/product/generic/system/app/Launcher2.apk
Install: out/host/linux-x86/bin/mkyaffs2image
make snod: ignoring dependencies
Target system fs image: out/target/product/generic/system.img
Building Out of Tree
If ever you'd like to build code against the AOSP and its Bionic library but don't want
to incorporate that into the AOSP, you can use a makefile such as the following to get
the job done:‡
# Paths and settings
TARGET_PRODUCT = generic
ANDROID_ROOT = /home/karim/android/aosp-2.3.x
‡This makefile is inspired by a blog post by Row Boat developer Amit Pundir and is based on the example
makefile provided in Chapter 4 of Building Embedded Linux Systems, 2nd ed. (O'Reilly).
110 | Chapter 4: The Build System

BIONIC_LIBC = $(ANDROID_ROOT)/bionic/libc
PRODUCT_OUT = $(ANDROID_ROOT)/out/target/product/$(TARGET_PRODUCT)
CROSS_COMPILE = \
$(ANDROID_ROOT)/prebuilt/linux-x86/toolchain/arm-eabi-4.4.3/bin/arm-eabi-
# Tool names
AS = $(CROSS_COMPILE)as
AR = $(CROSS_COMPILE)ar
CC = $(CROSS_COMPILE)gcc
CPP = $(CC) -E
LD = $(CROSS_COMPILE)ld
NM = $(CROSS_COMPILE)nm
OBJCOPY = $(CROSS_COMPILE)objcopy
OBJDUMP = $(CROSS_COMPILE)objdump
RANLIB = $(CROSS_COMPILE)ranlib
READELF = $(CROSS_COMPILE)readelf
SIZE = $(CROSS_COMPILE)size
STRINGS = $(CROSS_COMPILE)strings
STRIP = $(CROSS_COMPILE)strip
export AS AR CC CPP LD NM OBJCOPY OBJDUMP RANLIB READELF \
SIZE STRINGS STRIP
# Build settings
CFLAGS = -O2 -Wall -fno-short-enums
HEADER_OPS = -I$(BIONIC_LIBC)/arch-arm/include \
-I$(BIONIC_LIBC)/kernel/common \
-I$(BIONIC_LIBC)/kernel/arch-arm
LDFLAGS = -nostdlib -Wl,-dynamic-linker,/system/bin/linker \
$(PRODUCT_OUT)/obj/lib/crtbegin_dynamic.o \
$(PRODUCT_OUT)/obj/lib/crtend_android.o \
-L$(PRODUCT_OUT)/obj/lib -lc -ldl
# Installation variables
EXEC_NAME = example-app
INSTALL = install
INSTALL_DIR = $(PRODUCT_OUT)/system/bin
# Files needed for the build
OBJS = example-app.o
# Make rules
all: example-app
.c.o:
$(CC) $(CFLAGS) $(HEADER_OPS) -c $<
example-app: ${OBJS}
$(CC) -o $(EXEC_NAME) ${OBJS} $(LDFLAGS)
install: example-app
test -d $(INSTALL_DIR) || $(INSTALL) -d -m 755 $(INSTALL_DIR)
$(INSTALL) -m 755 $(EXEC_NAME) $(INSTALL_DIR)
clean:
Build Recipes | 111

rm -f *.o $(EXEC_NAME) core
distclean:
rm -f *~
rm -f *.o $(EXEC_NAME) core
In this case, you don't need to care about either envsetup.sh or lunch. You can just go
ahead and type the magic incatation:
$ make
Obviously this won't add your binary to any of the images generated by the AOSP. Even
the install target here will be of value only if you're mounting the target's filesystem
off NFS; and that's valuable only during debugging, which is what this makefile is
assumed to be useful for. To an extent, it could also be argued that using such a makefile
is actually counter-productive since it's far more complicated than the equivalent An-
droid.mk had this code been added as a module part of the AOSP.
Still, this kind of hack can have its uses. Under certain circumstances, for instance, it
might make sense to modify the conventional build system used by a rather large code
base to build that project against the AOSP yet outside of it; the alternative being to
copy the project into the AOSP and create Android.mk files to reproduce the mechanics
of its original conventional build system, which might turn out to be a substantial
endeavour in and of itself.
Basic AOSP Hacks
You most likely bought this book with one thing in mind: to hack the AOSP to fit your
needs. Over the next few pages, we'll start looking into some of the most obvious hacks
you'll likely want to try. Of course we're only setting the stage here with the parts that
pertain to the build system, which is where you'll likely want to start anyway. The next
chapters will allow to push what we see here much further.
Adding an App
If you would like to add a default app in addition to the stock ones, you'll need to start
by creating a directory for it in packages/apps/. As a starter, try creating a "HelloWorld!"
app with Eclipse and the default SDK; by default all new Android projects in Eclipse
are a "HelloWorld!". Then copy that app from the Eclipse workspace to its destination:
$ cp -a ~/workspace/HelloWorld ~/android/aosp-2.3.x/packages/apps/
You'll then have to create an Android.mk in aosp-rootpackages/apps/HelloWorld to
build that app:
112 | Chapter 4: The Build System

LOCAL_PATH:= $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE_TAGS := optional
LOCAL_SRC_FILES := $(call all-java-files-under, src)
LOCAL_PACKAGE_NAME := HelloWorld
include $(BUILD_PACKAGE)
Given that we're tagging this module as optional, it won't be included by default in the
AOSP build. To get it to be included, you'll need to add it to the default PRODUCT_PACK
AGES listed in aosp-root/build/target/product/core.mk.
Note that the commands I've shown so far means you're adding the app globally to
all products. That might not be what you're looking for, though. If you want to add
the app to just your product, which you likely should if it's going to be available only
on your device, you should add the app into your product's entry in device/ instead of
packages/apps/. We'll cover how to add your own device shortly.
Adding a Native Tool or Daemon
There are a number of locations in the tree where native tools and daemons are located.
Here are the most important ones:
system/core/ and system/
Custom Android binaries that are meant to be used outside the Android framework
or are stand-alone pieces.
frameworks/base/cmds/
Binaries that are tightly coupled to the Android framework. This is where the Serv-
ice Manager and installd are found, for example.
external/
Binaries that are generated by an external project that is imported into the AOSP.
strace, for instance, is here.
Now that you most likely know where the code generating the binary should go, you'll
also need to provide an Android.mk in the directory containing the code to build that
module:
LOCAL_PATH:= $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := hello-world
LOCAL_MODULE_TAGS := optional
LOCAL_SRC_FILES := hello-world.cpp
LOCAL_SHARED_LIBRARIES := liblog
Basic AOSP Hacks | 113

include $(BUILD_EXECUTABLE)
Again, you'll also need to make sure hello-world is also part of the default PRODUCT_PACK
AGES listed in aosp-root/build/target/product/core.mk. And again, what you'd be doing
here is adding that binary to all products. So, much like a custom app, the best location
for your binary may actually be in your product-specific directory in device/.
Adding a Native Library
Like binaries, libraries are typically found in a number of locations in the tree. Unlike
binaries, though, a lot of libraries are used within a single module but nowhere else.
Hence, these libraries will typically be placed within that module's code and not in the
typical locations where libraries used system-wide are found. The latter are typically in:
system/core
Libraries used by many parts of the system, including some outside the Android
framework. This is where liblog is, for instance.
frameworks/base/libs/
Libraries intimately tied to the framework. This is where libbinder is.
external/
Libraries generated by external projects imported in the AOSP. OpenSSL's libssl is
here.
Whether your library best belongs in one of these locations, within another module,
or in your product's device/ entry, you'll need an Android.mk to build it:
LOCAL_PATH:= $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := libmylib
LOCAL_MODULE_TAGS := optional
LOCAL_PRELINK_MODULE := false
LOCAL_SRC_FILES := $(call all-c-files-under,.)
include $(BUILD_SHARED_LIBRARY)
Library Prelinking
To reduce the time it takes to load libraries, Android prelinks most of its libraries. This
is done by specifying ahead of time the address location where the library will be loaded
instead of letting it be figured out at run time. The file where the addresses are specifies
is build/core/prelink-linux-arm.map and the tool that does the mapping is called apri-
ori. It contains entries such as these:
# core system libraries
libdl.so 0xAFF00000 # [<64K]
114 | Chapter 4: The Build System

libc.so 0xAFD00000 # [~2M]
libstdc++.so 0xAFC00000 # [<64K]
libm.so 0xAFB00000 # [~1M]
liblog.so 0xAFA00000 # [<64K]
libcutils.so 0xAF900000 # [~1M]
libthread_db.so 0xAF800000 # [<64K]
libz.so 0xAF700000 # [~1M]
libevent.so 0xAF600000 # [???]
libssl.so 0xAF400000 # [~2M]
...
# assorted system libraries
libsqlite.so 0xA8B00000 # [~2M]
libexpat.so 0xA8A00000 # [~1M]
libwebcore.so 0xA8300000 # [~7M]
libbinder.so 0xA8200000 # [~1M]
libutils.so 0xA8100000 # [~1M]
libcameraservice.so 0xA8000000 # [~1M]
libhardware.so 0xA7F00000 # [<64K]
libhardware_legacy.so 0xA7E00000 # [~1M]
...
If you want to add a custom native library, you need either to add it to the list of libraries
in prelink-linux-arm.map or to set the LOCAL_PRELINK_MODULE to false. The build will
fail if you forget to do one of these.
To use this library, you must add it to the list of libraries listed by the Android.mk file
of whichever binaries depend on it:
LOCAL_SHARED_LIBRARIES := libmylib
You'll also likely need to add relevant headers to an include/ directory located in about
the same location as you put your library so that the code that need to link against your
library can find said headers, such as system/core/include/ or frameworks/base/include/
Adding a Device
Adding a custom device is most likely one of the topmost items (if not the topmost) on
your list if you're reading this book. You'll likely therefore want to bookmark this sec-
tion, as I'm about to show you how to just that. Of course I'm actually only showing
you the build aspects of the work. There are a lot more steps involved in porting Android
to new hardware as we'll see through the rest of the book. Still, adding the new device
to the build system will definitely be one of the first things you do. Fortunately, doing
that is relatively straight-forward.
For the benefit of the current exercise, assume you work for a company called ACME
and that you're tasked with delivering its latest gizmo: the CoyotePad, intended to be
the best platform for playing all bird games. Let's get started by creating an entry for
our new device in device/:
Basic AOSP Hacks | 115

$ cd ~/android/aosp-2.3.x
$ . build/envsetup.sh
$ mkdir -p device/acme/coyotepad
$ cd device/acme/coyotepad
The first thing we'll need in here is an AndroidProducts.mk file to describe the various
AOSP products that could be built for the CoyotePad:
PRODUCT_MAKEFILES := \
$(LOCAL_DIR)/full_coyotepad.mk
While we could've had several products,§ the typical case is to just have one as in this
case, and it's described in full_coyotepad.mk:
$(call inherit-product, $(SRC_TARGET_DIR)/product/languages_full.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full.mk)
DEVICE_PACKAGE_OVERLAYS :=
PRODUCT_PACKAGES +=
PRODUCT_COPY_FILES +=
PRODUCT_NAME := full_coyotepad
PRODUCT_DEVICE := coyotepad
PRODUCT_MODEL := Full Android on CoyotePad, meep-meep
It's worth taking a closer look at this makefile. First, we're using the inherit-product
directive to tell the build system to pull in other product descriptions as the basis of
ours. This allows us to build on other people's work and not have to specify from scratch
every bit and piece of the AOSP that we'd like to include. languages_full.mk will pull
in a vast number of locales and full.mk will make sure we get the same set of modules
as if we had built using the full-eng combo.
With regard to the other variables:
DEVICE_PACKAGE_OVERLAYS
Allows us to specify a directory which will form the basis of an overlay that will be
applied onto the AOSP's sources, thereby allowing us to substitute default package
resources with device-specific resources. You'll find this useful if you'd like to set
custom layouts or colors for Launcher2 or other apps, for instance. We'll look at
how to use this in the next section.
§See build/target/product/AndroidProducts.mk for an example
116 | Chapter 4: The Build System

PRODUCT_PACKAGES‖
Allows us to specify packages we'd like to have this product include in addition to
those specified in the products we're already inheriting from. If you have custom
apps, binaries, or libraries located within device/acme/coyotepad/, for instance,
you'll want to add them here so that they get included in the final images generated.
PRODUCT_COPY_FILES
Allows us to list specific files we'd like to see copied to the target's filesystem and
the location where they need to be copied. Each source/destination pair is colon-
separated and pairs are space-separated amongst themselves. This is useful for
configuration files and prebuilt binaries such as firmware images or kernel mod-
ules.
PRODUCT_NAME
The TARGET_PRODUCT, which you can set either by selecting a lunch combo or passing
it as a part of the combo parameter to lunch as in:
$ lunch full_coyotepad-eng
PRODUCT_DEVICE
The name of the actual finished product shipped to the customer. TARGET_DEVICE
derives from this variable. PRODUCT_DEVICE has to match an entry in device/acme/,
since that's where the build looks for the corresponding BoardConfig.mk. In this
case, the variable is the same as the name of the directory we're already in.
PRODUCT_MODEL
The name of this product as provided in the "Model number" in the "About the
phone" section of the settings. This variable actually gets stored as the ro.prod
uct.model global property accessible on the device.
Now that we've described the product, we must also provide some information re-
garding the board the device is using through a BoardConfig.mk file:
TARGET_NO_KERNEL := true
TARGET_NO_BOOTLOADER := true
TARGET_CPU_ABI := armeabi
BOARD_USES_GENERIC_AUDIO := true
USE_CAMERA_STUB := true
This is a very skinny BoardConfig.mk and only ensures that we actually build success-
fully. For a real-life version of that file, have a look at device/samsung/crespo/Board-
ConfigCommon.mk.
‖Notice the use of the += sign. It allows us to append to the existing values in the variable instead of subtituting
its content.
Basic AOSP Hacks | 117

You'll also need to provide a conventional Android.mk in order to build all the modules
that you might have included in this device's directory:
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
ifneq ($(filter coyotepad,$(TARGET_DEVICE)),)
include $(call all-makefiles-under,$(LOCAL_PATH))
endif
It's in fact the preferred modus operandi to put all device-specific apps, binaries, and
libraries within the device's directory instead of globally within the rest of the AOSP as
was shown earlier. If you do add modules here, don't forget to also add them to PROD
UCT_PACKAGES as I explained earlier. If you just put them here and provide them valid
Android.mk files, they'll build, but they won't be in the final images.
Lastly, let's close the loop by making the device we just added visible to envsetup.sh
and lunch. To do so, you'll need to add a vendorsetup.sh in your device's directory:
add_lunch_combo full_coyotepad-eng
You also need to make sure that it's executable if it's to be operational:
$ chmod 755 vendorsetup.sh
We can now go back to the AOSP's root and take our brand new ACME CoyotePad
for a runchase:
$ croot
$ . build/envsetup.sh
$ lunch
You're building on Linux
Lunch menu... pick a combo:
1. generic-eng
2. simulator
3. full_coyotepad-eng
4. full_passion-userdebug
5. full_crespo4g-userdebug
6. full_crespo-userdebug
Which would you like? [generic-eng] 3
============================================
PLATFORM_VERSION_CODENAME=REL
PLATFORM_VERSION=2.3.4
TARGET_PRODUCT=full_coyotepad
TARGET_BUILD_VARIANT=eng
118 | Chapter 4: The Build System

TARGET_SIMULATOR=false
TARGET_BUILD_TYPE=release
TARGET_BUILD_APPS=
TARGET_ARCH=arm
HOST_ARCH=x86
HOST_OS=linux
HOST_BUILD_TYPE=release
BUILD_ID=GINGERBREAD
============================================
$ make -j16
As you can see, the AOSP now recognizes our new device and prints the information
correspondingly. When the build is done, we'll also have the same type of output pro-
vided in any other AOSP build, except that it will be a product-specific directory:
$ ls -al out/target/product/coyotepad/
drwxr-xr-x 7 karim karim 4096 2011-09-21 19:20 .
drwxr-xr-x 4 karim karim 4096 2011-09-21 19:08 ..
-rw-r--r-- 1 karim karim 7 2011-09-21 19:10 android-info.txt
-rw-r--r-- 1 karim karim 4021 2011-09-21 19:41 clean_steps.mk
drwxr-xr-x 3 karim karim 4096 2011-09-21 19:11 data
-rw-r--r-- 1 karim karim 20366 2011-09-21 19:20 installed-files.txt
drwxr-xr-x 14 karim karim 4096 2011-09-21 19:20 obj
-rw-r--r-- 1 karim karim 327 2011-09-21 19:41 previous_build_config.mk
-rw-r--r-- 1 karim karim 2649750 2011-09-21 19:43 ramdisk.img
drwxr-xr-x 11 karim karim 4096 2011-09-21 19:43 root
drwxr-xr-x 5 karim karim 4096 2011-09-21 19:19 symbols
drwxr-xr-x 12 karim karim 4096 2011-09-21 19:19 system
-rw------- 1 karim karim 87280512 2011-09-21 19:20 system.img
-rw------- 1 karim karim 1505856 2011-09-21 19:14 userdata.img
Also, have a look at the build.prop file in system/. It contains various global properties
that will be available at runtime on the target and that relate to our configuration and
build:
# begin build properties
# autogenerated by buildinfo.sh
ro.build.id=GINGERBREAD
ro.build.display.id=full_coyotepad-eng 2.3.4 GINGERBREAD eng.karim.20110921.190849 test-keys
ro.build.version.incremental=eng.karim.20110921.190849
ro.build.version.sdk=10
ro.build.version.codename=REL
ro.build.version.release=2.3.4
ro.build.date=Wed Sep 21 19:10:04 EDT 2011
ro.build.date.utc=1316646604
ro.build.type=eng
ro.build.user=karim
ro.build.host=w520
ro.build.tags=test-keys
Basic AOSP Hacks | 119

ro.product.model=Full Android on CoyotePad, meep-meep
ro.product.brand=generic
ro.product.name=full_coyotepad
ro.product.device=coyotepad
ro.product.board=
ro.product.cpu.abi=armeabi
ro.product.manufacturer=unknown
ro.product.locale.language=en
ro.product.locale.region=US
ro.wifi.channels=
ro.board.platform=
# ro.build.product is obsolete; use ro.product.device
ro.build.product=coyotepad
# Do not try to parse ro.build.description or .fingerprint
ro.build.description=full_coyotepad-eng 2.3.4 GINGERBREAD eng.karim.20110921.190849 test-keys
ro.build.fingerprint=generic/full_coyotepad/coyotepad:2.3.4/GINGERBREAD
/eng.karim.20110921.190849:eng/test-keys
# end build properties
...
As you can imagine, there's a lot more to be done here to make sure the AOSP runs on
our hardware. But the preceding steps give us the starting point.
Adding an App Overlay
Overlays are a mechanism included in the AOSP to allow device manufacturers to
change the resources provided (such as for apps), without actually modifying the orig-
inal resources included in the AOSP. To use this capability you must create an overlay
tree and tell the build system about it. The easiest location for an overlay is within a
device-specific directory such as the one we just created in the previous section:
$ cd device/acme/coyotepad/
$ mkdir overlay
To tell the build system to take this overlay into account, we need to modify our
full_coyotepad.mk such that:
DEVICE_PACKAGE_OVERLAYS := device/acme/coyotepad/overlay
At this point, though, our overlay isn't doing much. Let's say we want to modify the
Launcher2's default strings. We could then do something like this:
$ mkdir -p overlay/packages/apps/Launcher2/res/values
$ cp aosp-root/packages/apps/Launcher2/res/values/strings.xml \
> overlay/packages/apps/Launcher2/res/values/
120 | Chapter 4: The Build System

You are then free to modify your copy of strings.xml to suite your needs. Your device
will have a Launcher2 that has your custom strings, but the default Launcher2 will still
have its original strings. So if someone relies on the same AOSP sources you're using
to build for another product, they'll still get the original strings. You can, of course,
replace most resources like this, including images and XML files. So long as you put
the files in the same hierarchy as they are found in the AOSP but within device/acme/
coyotepad/overlay/, they'll be taken into account by the build system.
Basic AOSP Hacks | 121

