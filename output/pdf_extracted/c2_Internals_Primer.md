# Internals Primer

Unlike the GPL, the ASL does not require that derivative works be published under a
specific license. In fact, you can choose whatever license best suits your needs for the
modifications you make. Here are the relevant portions from the ASL (the full license
is available at http://www.apache.org/licenses/):
• "Subject to the terms and conditions of this License, each Contributor hereby
grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, ir-
revocable copyright license to reproduce, prepare Derivative Works of, publicly
display, publicly perform, sublicense, and distribute the Work and such Derivative
Works in Source or Object form."
• "... You may add Your own copyright statement to Your modifications and may
provide additional or different license terms and conditions for use, reproduction,
or distribution of Your modifications, or for any such Derivative Works as a whole,
provided Your use, reproduction, and distribution of the Work otherwise complies
with the conditions stated in this License."
Furthermore, the ASL explicitly provides a patent license grant, meaning that you do
not require any patent license from Google for using the ASL-licensed Android code.
It also imposes a few "administrative" requirements such as the need to clearly mark
modified files, to provide recipients with a copy of the ASL license, to preserve NO-
TICE files as-is, etc. Essentially, though, you are free to license your modifications under
the terms that fit your purpose. The BSD license that covers Bionic and Toolbox allows
similar binary-only distribution.
Hence, manufacturers can take the AOSP and customize it to their needs while keeping
those modifications proprietary if they wish, so long as they continue abiding by the
rest of the provisions of the ASL. If nothing else, this dimishes the burden of having to
implement a process to track all modifications in order to provide those modifications
back to recipients who would be entitled to request them had the GPL been used in-
stead.
Adding GPL-licensed components
Although every effort has been made to keep the GPL out of Android's user-space in
as much as possible, there are cases where you may want to explicitly add GPL-licensed
components to your Android distribution. For example, you want to include either
glibc of uClibc which are two POSIX-compliant C libraries—in contrast to Android's
Bionic which is not—because you would like to run pre-existing Linux applications on
Android without having to port them over to Bionic. Or you may want to use BusyBox
in addition to Toolbox since the latter is much more limited in functionality that the
former.
These additions may be specific to your development environment and may be removed
in the final product or they may be permanent fixtures or your own customized An-
droid. No matter which avenue you decide on, whether it be plain Android or Android
Legal Framework | 11

with some additional GPL packages, remember that you must follow the licenses' re-
quirements.
Branding Use
While being very generous with Android's source code, Google controls most Android-
related branding elements more strictly. Let's take a look at some of those elements and
their associated terms of use. For the official list along with the official terms, have a
look at http://www.android.com/branding.html.
Android Robot
This is the familiar green robot seen everywhere around all things Android. Its role
is similar to the Linux penguin and the permissions for its use are similarly per-
missive. In fact Google states that it "can be used, reproduced, and modified freely
in marketing communications." The only requirement is that proper attibution be
made according to the terms of the Creative Commons Attribution license.
Android Logo
This is the set of letters in custom typeface that spell out the letters A-N-D-R-O-I-
D and that appear during the device and emulator bootup, and on the android
.comwebsite. You are not authorized to use that logo under any circumstance.
Android Custom Typeface
This is the custom typeface used to render the Android logo and its use is as re-
stricted as the logo.
"Android" in Official Names
As Google states, "the word 'Android' may be used only as a descriptor, 'for An-
droid'" and so long as proper trademark attribution is made. You cannot, for in-
stance, name your product "Foo Android" without Google's permission. As the
FAQ for the Android Compatiblity Program (ACP), which we will cover later in
this chapter, states: "... if a manufacturer wishes to use the Android name with
their product ... they must first demonstrate that the device is compatible." Brand-
ing your device as being "Android" is therefore a privilege which Google intends
to police. In essence, you will have to make sure your device is compliant and then
talk to Google and enter into some kind of agreement with them before you can
advertize your device as being "Foo Android."
"Droid" in Official Names
You may not use "Droid" alone in a name, such as "Foo Droid" for example. For
some reason the author hasn't yet entirely figured out, "Droid" is a trademark of
Lucasfilm. Achieve a Jedi rank you likely must before you can use it.
"Android" in Messaging
It is permitted to use "Android" "... in text as a descriptor, as long as it is followed
by a proper generic term (e.g. "Android™ application")." And here too, proper
trademark attribution must be made.
12 | Chapter 1: Introduction

Google's Own Android Apps
While the AOSP contains a core set of applications which are available under the ASL,
"Android"-branded phones usually contain an additional set of "Google" applications
that are not part of the AOSP, such as the "Android Market", YouTube, "Maps and
Navigation", Gmail, etc. Obviously, users expect to have these apps as part of Android,
and you might therefore want to make them available on your device. If that is the case,
you will need to abide by the ACP and enter in agreement with Google, very much in
line with what you need to do to be allowed to use "Android" in your product's name.
We will cover the ACP shortly.
Alternative App Markets
Though the main app market is the one hosted by Google and made available to users
through the "Android Market" app installed on "Android"-branded devices, other play-
ers are leveraging Android's open APIs and open source licensing to offer their own
alternative app markets. Such is the case of online merchants like Amazon and
Barnes&Noble, as well as mobile network operators such as Verizon and Sprint. There
is, in fact, nothing to the author's knowledge that precludes you from creating your
own app store. There is even at least one open source project, FDroid Repository (http:
//f-droid.org/repository/), that provides both an app market application and a corre-
sponding server backend under the GPL.
Oracle v Google
As part of acquiring Sun Microsystem, Oracle also acquired Sun's intellectual property
(IP) rights to the Java language and, according to Java creator James Gosling,‖ it was
clear during the acquisition process that Oracle intended from the onset to go after
Google with Sun's Java IP portfolio. And in August 2010 it did just that, filing suit
against Google, claiming that it infringed on serveral patents and commited copyright
violations.
Without going into the merits of the case, it's obvious that Android does indeed heavily
rely on Java. And clearly Sun created Java and owned a lot of intellectual property
around the language it created. In what appears to have been an effort to anticipate any
claims Sun may put forward against Android, nonetheless, the Android development
team went out of its way to make the OS use as little of Sun's Java as possible. Java is
in fact comprised mainly of three things: the language and its semantics, the virtual
machine that runs the Java bytecode generated by the Java compiler, and the class
library that contains the packages used by Java applications at run time.
‖See Gosling's blog postings on the topic at http://nighthacks.com/roller/jag/entry/the_shit_finally_hits_the and
http://nighthacks.com/roller/jag/entry/quite_the_firestorm for more details.
Legal Framework | 13

The official versions of the Java components are provided by Oracle as part of the Java
Development Kit (JDK) and the Java Runtime Environment (JRE). Android, on the
other hand, relies only the Java compiler found in the JDK. Instead of using Oracle's
Java VM, Android relies on Dalvik, a VM custom-built for Android, and instead of
using the official class library, Android relies on Apache Harmony, a clean-room re-
implementation of the class library. Hence, it would seem that Google did every rea-
sonable effort to at least avoid any copyright and/or distribution issues.
Still, it remains to be seen where these legal proceedings will go. And it likely will take
a few years to get resolved. In the interim, however, it appears that the judge presiding
over the case wants to get the matter resolved in earnest. In May 2011, he ordered
Oracle to cut its claims from 132 down to 3 and ordered Google to cut their prior art
references down from several hundreds to 8. According to Groklaw,# he even seems
to be asking the parties whether "they anticipate that a trial will end up being moot."
Another indirectly related, yet very relevant, development is that IBM joined Oracle's
OpenJDK efforts in October 2010. IBM had been the main driving force behind the
Apache Harmony, which is the class library used in Android, and its departure pretty
much ensures the project has become orphaned. How this development impacts An-
droid is unknown at the time of this writing.
Incidently, James Gosling joined Google in March 2011.
Hardware and Compliance Requirements
In principle, Android should run on any hardware that runs Linux. Android has in fact
been made to run on ARM, x86, MIPS, SuperH, and PowerPC, all architectures sup-
ported by Linux. A corrolary to this is that if you want to port Android to your hardware,
you must first port Linux to it. Beyond being able to run Linux, though, there are few
other hardware requirements for running the AOSP, apart from the logical requirement
of having some kind of display and pointer mechanism to allow users to interact with
the interface. Obviously, you might have to modify the AOSP to make it work on your
hardware configuration, if you don't support a peripheral it expects. For instance, if
you don't have a GPS, you might want to provide a mock GPS HAL module, as the
Android emulator does, to the AOSP. You will also need to make sure that you have
enough memory to store the Android images and a sufficiently powerful CPU to give
the user a decent experience.
In sum, therefore, there are few restrictions if you just want to get the AOSP up and
running on your hardware. If, however, you are working on a device that must carry
"Android" branding or must include the standard Google-owned applications found
in typical consumer Android devices such as the Maps or Market applications, you
need to go through the ACP that I mentioned earlier. There are two separate yet com-
#See the full analysis here: http://groklaw.net/article.php?story=2011050505150858.
14 | Chapter 1: Introduction

plementary parts to the ACP: the Compliance Definition Document (CDD) and the
Compliance Test Suite (CTS). Even if you don't intend to participate in the ACP, you
might still want to take a look at the CDD and the CTS, as they give a very good idea
about the general mindset that went into the design goals of the Android version you
intend to use.
Every Android release has its own CDD and CTS. You must therefore
use the CDD and CTS that match the version you intend to use for your
final product. If you switch Android releases mid-way through your
project, because for instance a new Android release comes out with cool
new features you'd like to have, you will need to make sure you comply
with that release's CDD and CTS. Keep in mind also that you need to
interact with Google to confirm compliance. Hence, switching may in-
volve jumping through a few hoops and potential product delivery de-
lays.
The overarching goal of the ACP, and therefore the CDD and the CTS, is to ensure a
uniform ecosystem for users and application developers. Hence, before you are allowed
to ship an "Android"-branded device, Google wants to make sure that you aren't frag-
menting the Android ecosystem by introducing incompatible or crippled products.
This, in turn, makes sense for manufacturers since they are benefiting from the com-
pliance of others when they use the "Android" branding. For more detail about the
ACP, have a look at http://source.android.com/compatibility/.
Note that Google reserves the right to decline your participation in the
Android ecosystem, and therefore be able to ship the "Android Market"
app with your device and use the "Android" branding. As stated on their
site: "Unfortunately, for a variety of legal and business reasons, we aren't
able to automatically license Android Market to all compatible devices."
Compliance Definition Document
The CDD is the policy part of the ACP and is available at the ACP URL above. It specifies
the requirements that must be met for a device to be considered compatible. The lan-
guage in the CDD is based on RFC2119 with a heavy use of "MUST," "SHOULD,"
"MAY," etc. to describe the different attributes. Around 25 pages in length, it covers
all aspects of the device's hardware and software capabilities. Essentially, it goes over
every aspect that cannot simply be automatically tested using the CTS. Let's go over
some of what the CDD requires.
This discussion is based on the Android 2.3/Gingerbread CDD. The
specific version you use will likely have slightly different requirements.
Hardware and Compliance Requirements | 15

Software
This section lists the Java and Native APIs along with the web, virtual machine and
user interface compatibility requirements. Essentially, if you are using the AOSP, you
should readily conform to this section of the CDD.
Application Packaging Compatibility
This section specifies that your device must be able to install and run .apk files. All
Android apps developed using the Android SDK are compiled into .apk files, and these
are the files that are distributed through the Android Market and installed on users'
devices.
Multimedia Compatibility
Here, the CDD describes the media codecs (decoders and encoders), audio recording,
and audio latency requirements for the device. The AOSP includes the StageFright
multi-media framework, and you can therefore conform to the CDD by using the AOSP.
However, you should read the audio recording and latency sections, as they contain
specific technical information that may impact the type of hardware or hardware con-
figuration your device must be equipped with.
Developer Tool Compatibility
This section lists the Android-specific tools that must be supported on your device.
Basically, these are the common tools used during app development and testing: adb,
ddms, and monkey. Typically, developers don't interact with these tools directly. In-
stead, they usually develop within the Eclipse development environment and use the
Android Development Tool (ADT), plugin which takes care of interacting the lower-
level tools.
Hardware Compatibility
This is probably the most important section for embedded developers as it likely has
profound ramifications on the design decisions made for the targeted device. Here's a
summary of what each subsection spells out.
Display and Graphics
• Your device's screen must be at least 2.5" in physical diagonal size.
• Its density must be at least 100dpi.
• Its aspect ratio must be between 4:3 and 16:9.
• It must support dynamic screen orientation from portrait to landscape and vice-
versa. If orientation can't be changed, it must support letterboxing since apps
may force orientation changes.
• It must support OpenGL ES 1.0 though it may omit 2.0 support
16 | Chapter 1: Introduction

Input Devices
• Your device must support the Input Method Framework, which allows devel-
opers to create custom on-screen, soft keyboards.
• It must provide at least one soft keyboard.
• It can't include a hardware keyboard that doesn't conform the API.
• It must provide "HOME," "MENU," and "BACK" buttons.
• It must have a touchscreen, whether it be capacitive or resistive.
• It should support independent tracked points (multi-touch) if possible.
Sensors
While all sensors are qualified using "SHOULD," meaning that they aren't com-
pulsory, your device must accurately report the presence or absence of sensors and
must return an accurate list of supported sensors.
Data Connectivity
The most important item here is an explicit statement that Android may be used
on devices that don't have telephony hardware. This was added to allow for An-
droid-based tablet devices. Furthermore, the document says that your device
should have hardware support for 802.11x, Bluetooth, and NFC. Ultimately, your
device must support some form of networking that permits a bandwidth of
200Kbits/s.
Cameras
Your device should include a rear-facing camera and may include a front-facing
one as well.
Memory and Storage
• Your device must have at least 128MB for storing the kernel and user space.
• It must have at least 150MB for storing user data.
• It must have at least 1GB of "shared storage," essentially meaning the SD card.
• It must also provide a mechanism to access shared data from a PC. In other
words, when the device is connected through USB, the content of the SD card
must be accessible on the PC.
USB
This requirement is likely the one that most heavily demonstrates how user-centric
"Android"-branded devices must be, since it essentially assumes the user owns the
device and therefore requires you to allow users to fully control the device when
it's connected to a PC. In some cases this might be a show-stopper for you, as you
may not actually want or may not be able to have users connect your embedded
device to a user's PC. Nevertheless, the CDD says that:
• Your device must implement a USB client which would be connectable through
USB-A.
Hardware and Compliance Requirements | 17

• It must implement the Android Debug Bridge (ADB) protocol as provided in
the adb command over USB.
• It must implement USB mass storage, thereby allowing the device's SD card to
be accessed on the host.
Performance Compatibility
Although the CDD doesn't specify CPU speed requirements, it does specify app-related
time limitations that will impact your choice of CPU speed. For instance:
• The Browser app must launch in less than 1300ms.
• The MMS/SMS app must launch in less than 700ms.
• The AlarmClock app must launch in less than 650ms.
• Relaunching an already running app must take less time than the original launch.
Security Model Compatibility
Your device must conform to the security environment enforced by the Android ap-
plication framework, Dalvik, and the Linux kernel. Specifically, apps must have access
and be submitted to the permission model described as part of the SDK's documenta-
tion. Apps must also be constrained by the same sandboxing limitations they have by
running as separate processes with distinct UIDs in Linux. The filesystem access rights
must also conform to those described in the developer documentation. Finally, if you
aren't using Dalvik, whatever VM you use should impose the same security behavior
as Dalvik.
Software Compatibility Testing
Your device must pass the CTS, including the human-operated CTS Verifier part. In
addition, you device must be able to run specific reference applications from the An-
droid Market.
Updatable Software
There has to be a mechanism for your device to be updated. This may be done over-
the-air (OTA) with an offline update via reboot. It also may be done using a "tethered"
update via a USB connection to a PC, or be done "offline" using removable storage.
Compliance Test Suite
The CTS comes as part of the AOSP, and we will discuss it in Chapter 10. The AOSP
includes a special build target that generates the cts command-line tool, the main in-
terface for controling the test suite. The CTS relies on adb to push and run tests on the
USB-connected target. The tests are build on to the JUnit Java unit testing framework
and exercise different parts of the framework, such as the APIs, Dalvik, Intents, Per-
18 | Chapter 1: Introduction

missions, etc. Once the tests are done, they will generate a .zip file containing XML files
and screen-shots that you need to submit to cts@android.com.
Development Setup and Tools
There are two separate sets of tools for Android development: those used for application
development and those used for platform development. If you want to set up an ap-
plication development environment, have a look at Learning Android or Google's online
documentation. If you want do platform development, as we will do here, your tools
needs will vary, as we will see later in this book.
At the most basic level, though, you need to have a Linux-based workstation to build
the AOSP. In fact, at the time of this writing, Google's only supported build environ-
ment is 64-bit Ubuntu 10.04. That doesn't mean that another Ubuntu version won't
work or that you won't be able to build the AOSP on a 32-bit system, but essentially
that configuration reflects Google's own Android compile farms configuration. An easy
way to get your hands dirty with AOSP work without changing your workstation OS
is to create an Ubuntu virtual machine using your favorite virtualization tool. I typically
use VirtualBox, since I've found that it makes it easy to access the host's serial ports in
the guest OS.
No matter what your setup is, keep in mind that the AOSP is about 4GB in size, un-
compiled, and that it will grow to about 10GB once compiled. If you factor in that you
are likely going to operate on a few separate versions, for testing purposes if for no other
reason, you rapidly realize that you'll need tens of GBs for serious AOSP work. Also
note that on what is fairly recent machine at the time of this writing (dual-core high-
end laptop), it takes about an hour to build the AOSP from scratch. Even a minor
modification may result in a 5 min run to complete the build. You will therefore also
likely want to make sure you have a fairly powerful machine when developing Android-
based embedded systems.
Development Setup and Tools | 19

Internals Primer
As we've just seen, Android's sources are freely available for you to download, modify,
and install for any device you choose. In fact, it is fairly trivial to just grab the code,
build it, and run it in the Android emulator. To customize the AOSP to your device
and its hardware, however, you'll need to first understand Android's internals to a
certain extent. So we'll get a high-level view of Android internals in this chapters, and
get the opportunity in later chapters to dig into parts of internals in greater detail,
including tying said internals to the actual AOSP sources.
The discussion in this book is based on Android 2.3.x/Gingerbread.
Although Android's internals have remained fairly stable over its lifetime
up to the time of this writing, critical changes can come unannounced
thanks to Android's closed development process. For instance, in 2.2/
Froyo and previous versions, the Status Bar was an integral part of the
System Server. In 2.3/Gingerbread, the Status Bar was moved out of the
System Server and now runs indepedently from it.*
App Developer's View
Given that Android's development API is unlike any other existing API, including any-
thing found in the Linux world, it's important to spend some time understanding what
"Android" looks like from the app developers' perspective, even though it's very differ-
ent from what Android looks like for anyone hacking the AOSP. As an embedded
developer working on embedding Android on a device, you might not have to actually
deal directly with the idiosyncracies of Android's app development API, but some of
your colleagues might. If nothing else, you might as well share a common linguo with
* Some speculate that this change was triggered because some app developers were doing too
many fancy tricks with notification that were haing negative impacts on the System Server, and
that the Android team hence decided to make the Status Bar a separate process from the System
Server.

app developers. Of course, this section is merely a summary, and I recommend you
read up on Android app development for more in-depth coverage.
Android Concepts
Application developers must take a few key concepts into account when developing
Android apps. These concepts shape the architecture of all Android apps and dictate
what developers can and cannot do. Overall, they make the users' life better, but they
can sometimes be challenging to deal with.
Components
Android applications are made of loosely-tied components. Components of one app
can invoke/use components of other apps. Most importantly, there is no single entry
point to an Android app: no main() function or any equivalent. Instead, there are pre-
defined events called intents that developers can tie their components to, thereby ena-
bling their components to be activated on the occurrence of the corresponding events.
A simple example is the component that handles the user's contacts database, which
is invoked when the user presses a Contacts button in the Dialer or another app. An
app therefore can have as many entry points as it has components.
There are four main types of components:
Activities
Just as the "window" is the main building block of all visual interaction in window-
based GUI systems, activities are the building block in an Android app. Unlike a
window, however, activities cannot be "maximized," "minimized," or "resized."
Instead, activities always take the entirety of the visual area and are made to be
stacked up on top of each other in the same way as a browser remembers web-
pages in the sequence they were accessed, allowing the user to go "back" to where
he was previously. In fact, as described in the previous chapter, all Android devices
must have a "BACK" button to make this behavior available to the user. In contrast
to web browsing, though, there is no button corresponding to the "forward"
browsing action; only "back" is possible.
One globally defined Android intent allows an activity to be displayed as an icon
on the app launcher (the main app list on a phone.) Because the vast majority of
apps want to appear on the main app list, they provide at least one activity that is
defined as capable of responding to that intent. Typically, the user will start from
a particular activity and move through other end up creating a stack of activities
all related to the one they originally launched; this stack of activities is a task. The
user can then switch to another task by clicking the HOME button and starting
another activity stack from the app launcher.
Services
Android services are akin to background processes or daemons in the Unix world.
Essentially, a service is activated when another component requires its services and
22 | Chapter 2: Internals Primer

typically remains active for the duration required by its caller. Most importantly,
though, services can be made available to components outside an app, thereby
exposing some of that app's core functionality to other apps. There is usually no
visual sign of a service being active.
Broadcast Receivers
Broadcast receivers are akin to interrupt handlers. When a key event occurs, a
broadcast receiver is triggered to handle that event on the app's behalf. For instance,
an app might want to be notified when the battery level is low or when "airplane
mode" (to shut down the wireless connections) has been activated. When not han-
dling a specific event for which they are registered, broadcast receivers are other-
wise inactive.
Content Providers
Content providers are essentially databases. Usually, an app will include a content
provider if it needs to make its data accessible to other apps. If you're building a
Twitter client app, for instance, you could give other apps on the device access the
tweet feed you're presenting to the user through a content provider. All content
providers present the same API to apps, regardless of how they are actually imple-
mented internally. Most content providers rely on the SQLite functionality inclu-
ded in Android, but they can also use files or other types of storage.
Intents
Intents are one of the most important concepts in Android. They are the late-binding
mechanisms that allow components to interact. An app developer could send an intent
for an activity to "view" a web page or "view" a PDF, hence making it possible for the
user to view a designated HTML or PDF document even if the requesting app itself
doesn't include the capabilities to do so. More fancy use of intents is also possible. An
app developer could, for instance, send a specific intent to trigger a phone call.
Think of intents as polymorphic Unix signals that don't necessarily have to be prede-
fined or require a specific designated target component or app. The intent itself is a
passive object. It's its contents (payload), the mechanism used to fire it along with the
system's rules that will gate its behavior. One of the system's rules, for instance, is that
intents are tied to the type of component they are sent to. An intent sent to a service,
for example, can only be received by a service, not an activity or a broadcast receiver.
Components can be declared as capable of dealing with given intent types using filters
in the manifest file. The system will thereafter match intents to that filter and trigger
the corresponding component at runtime. An intent can also be sent to an explicit
component, bypassing the need to declare that intent within the receiving component's
filter. The explicit invocation, though, requires the app to know about the designated
component ahead of time, which typically applies only when intents are sent within
components of the same app.
App Developer's View | 23

Component Lifecycle
Another central tenant of Android is that the user should never have to manage task
switching. Hence, there is no task-bar or any equivalent functionality in Android. In-
stead, the user is allowed to start as many apps as he wants and "switch" between apps
by clicking HOME to go to the home screen and clicking on any other app. The app
he clicks may be an entirely new one, or one that he previously started and for which
an activity stack (a.k.a. a "task") already exists.
The corrollary to, or consequence of, this design decision is that apps gradually use up
more and more system resources as they are started, which can't go on forever. At some
point, the system will have to start reclaiming the resources of the least recently used
or non-priority components in order to make way for newly-activated components. Yet
still, this resource recycling should be entirely transparent to the user. In other words,
when a component is taken down to make way for new one, and then the user returns
to the original component, it should start up at the point where it was taken down and
act as if it was waiting in memory all along.
To make this behavior possible, Android defines a standard lifecycle components. An
app developer must manage her components' lifecycle by implementing a series of call-
backs for each component that are triggered by events related to the component life-
cycle. For instance, when an activity is no longer in the foreground (and therefore more
likely to be destroyed than if it's in the foreground), its onPause() callback is triggered.
Managing component lifecycles is one of the greatest challenges faced by app devel-
opers, because they must carefully save and restore component states on key transi-
tional events. The desired end result is that the user never needs to "task switch" be-
tween apps or be aware that components from previously-used apps were destroyed to
make way for new ones he started.
Manifest File
If there has to be a "main" entry point to an app, the manifest file is likely it. Basically,
it informs the system of the app's components, the capabilities required to run the app,
the minimum level of the API required, any hardware requirements, etc. The manifest
is formatted as an XML file and resides at the top-most directory of the app's sources
as AndroidManifest.xml. The apps' components are typically all described statically in
the manifest file. In fact, apart from broadcast receivers, which can be registered at
runtime, all other components must be declared at build time in the manifest file.
Processes and Threads
Whenever an app's component is activated, whether it be by the system or another app,
a process will be started to house that app's components. And unless the app developer
does anything to overide the system defaults, all other components of that app that
start after the initial component is activated will run within the same process as that
component. In other words, all components of an app are comprised within a single
24 | Chapter 2: Internals Primer

Linux process. Hence, developers should avoid making long or blocking operations in
standard components and use threads instead.
And because the user is essentially allowed to activate as many components as he wants,
several Linux processes are typically active at any time to serve the many apps con-
taining the user's components. When there are too many processes running to allow
for new ones to start, the Linux kernel's Out-Of-Memory (OOM) killing mechanisms
will kick in. At that point, Android's in-kernel OOM handler will get called and it will
determine which processes must be killed to make space.
Put simply, the entirety of Android's behavior is predicated on low-memory conditions.
If the developer of the app whose process is killed by Android's OOM handler has
implemented his components' lifecycles properly, the user should see no adverse be-
havior. For all practical purposes, in fact, the user should not even notice that the
process housing the app's components went away and got recreated "automagically"
later.
Remote Procedure Calls (RPC)
Much like many other components of the system, Android defines its own RPC/IPC†
mechanism: Binder. So communication across components is not done using the typical
System V IPC or sockets. Instead, components use the in-kernel Binder mechanism,
accessible through /dev/binder, which will be covered later in this chapter.
App developers, however, do not use the Binder mechanism directly. Instead, they must
define and interact with interfaces using Android's Interface Definition Language (IDL).
Interface definitions are usually stored in an .aidl file and are processed by the aidl tool
to generate the proper stubs and marshalling/unmarshalling code required to transfer
objects and data back and forth using the Binder mechanism.
Framework Intro
In addition to the concepts we just discussed, Android also defines its own development
framework, which allows developers to access functionality typically found in other
development frameworks. Let's take a brief look at this framework and its capabilities.
User Interface
UI elements in Android include traditional widgets such as buttons, text boxes,
dialogs, menus, and event handlers. This part of the API is relatively straight-for-
ward and developers usually find their way around it fairly easily if they've already
coded for any other UI framework.
All UI objects in Android are built as descendants of the View class and are organized
within a hierarchy of ViewGroups. An activity's UI can actually be specified either
†Inter-Process Communication
App Developer's View | 25

statically in XML (which is the usual way) or declared dynamically in Java. The UI
can also be modified at runtime in Java if need be. An activity's UI is displayed
when its content is set as the root of a ViewGroup hierarchy.
Data Storage
Android presents developers with several storage options. For simple storage
needs, Android provides shared preferences, which allows developers to store key-
pair values either in a data-set shared by all components of the app or within a
specific separate file. Developers can also manipulate files directly. These files may
be stored privately by the app, and therefore inaccessible to other apps, or made
readable and/or writeable by other apps. App developers can also use the SQLite
functionality included in Android to manage their own private database. Such a
database can then be made available to other apps by hosting it within a content
provider component.
Security and Permissions
Security in Android is enforced at the process level. In other words, Android relies
on Linux's existing process isolation mechanisms to implement its own policies.
To that end, every app installed gets its own UID and GID. Essentially, it's as if
every app is a separate "user" in the system. And as in any multi-user Unix system,
these "users" cannot access each others' resources unless permissions are explicitely
granted to do so. In effect, each app lives in its own separate sandbox.
To exit the sandbox and access key system functionality or resources, apps must
use Android's permission mechanisms, which require developers to statically de-
clare the permissions needed by an app in its manifest file. Some permissions, such
as the right to access the Internet (i.e. use sockets), dial the phone, or use the
camera, are predefined by Android. Other permissions can be declared by app
developers and then be required for other apps to interact with a given app's com-
ponents. When an app is installed, the user is prompted to approve the permissions
required to run an app.
Access enforcement is based on per-process operations and requests to access a
specific URI,‡ and the decision to grant access to a specific functionality or resource
is based on certificates and user prompts. The certificates are the ones used by app
developers to sign the apps they make available on the Android Market. Hence,
developers can restrict access to their apps' functionality to other apps they them-
selves created in the past.
The Android development framework provides a lot more functionality, of course, than
can be covered here. I invite you to read up on Android app development elsewhere or
visit developer.android.com for more information on 2D and 3D graphics, multi-media,
location and maps, Bluetooth, NFC, etc.
‡Universal Resource Indentifier.
26 | Chapter 2: Internals Primer

App Development Tools
The typical way to develop Android applications is to use the freely available Android
Software Development Kit (SDK). This SDK, along with Eclipse, its corresponding
Android Development Tools (ADT) plugin, and the QEMU-based emulator in the SDK,
allow developers to do the vast majority of development work straight from their
workstation. Developers will also usually want to test their app on real devices prior to
making it available on the Android Market, as there usually are runtime behavior dif-
ferences between the emulator and actual devices. Some software publishers take this
to the extreme and test their apps on several dozens of devices before shipping a new
release.
Even if you aren't going to plan to develop any apps for your embedded system, I highly
suggest you set up the development environment used by app developers on your
workstation. If nothing else, this will allow you to validate the effects of modifications
you make to the AOSP using basic test applications. It will also be essential if you plan
on extending the AOSP's API and therefore create and distribute your own custom SDK.
To set up an app development environment, follow the instructions provided by Google
at the developer kit site just mentioned, or have a look at the book Learning Android
(O'Reilly).
Native Development
While the majority of apps are developed exclusively in Java using the development
environment we just discussed, certain developers need to run some C code natively.
To this end, Google has made the Native Development Kit (NDK) available to devel-
opers. As advertized, this is mostly aimed at game developers needing to squeeze every
last possible bit of performance out of the device their game is running on. And as such,
the APIs made available within the context of the NDK are mostly geared towards
graphics rendering and sensor input retrieval. The infamous Angry Birds game, for
example, relies heavily on code running natively.
Another possible use of the NDK is obviously to port over an existing codebase to
Android. If you've developed a lot of legacy C code over several years (a common sit-
uation for development houses that have created applications for other mobile devices),
you won't necessarily want to rewrite it in Java. Instead, you can use the NDK to compile
it for Android and package it with some Java code to use some of the more Android-
specific functionality made available by the SDK. The Firefox browser, for instance,
relies heavily on the NDK to run some of its legacy code on Android.
As I just hinted, the nice thing about the NDK is that you can combine it with the SDK
and therefore have part of your app in Java and parts of your app in C. That said, it's
crucial to understand that the NDK gives you access only to a very limited subset of
the Android API. There is, for instance, no way to presently send an intent from within
C code compiled with the NDK; the SDK must be used to do it in Java instead. Again,
App Developer's View | 27

Figure 2-1. Android's architecture
the APIs made available through the NDK are mostly geared towards game develop-
ment.
Sometimes embedded and system developers coming to Android expect to be able to
use the NDK to do platform-level work. The word "native" in the NDK can be mis-
leading in that regard, because the use of the NDK still involves all of the limitations
and requirements that I've said to apply to Java app developers. So, as an embedded
developer, remember that the NDK is useful for app developers to run C code that they
can call from their Java code. Apart from that, the NDK will be of little to no use for
the type of work you are likely to undertake.
Overall Architecture
Figure 2-1 is probably one of the most important diagrams presented in this book, and
I suggest you find a way to bookmark its location as we will often refer back to it, if not
explicitly then implicitely. Although it's a simplified view—and we will get the chance
to enrich it as we go—it gives a pretty good idea of Android's architecture and how the
various bits and pieces fit together.
If you are familiar with some form of Linux development, the first thing that should
strike you is that beyond the Linux kernel itself, there is little in that stack that resembles
anything typically seen in the Linux or Unix world. There is no glibc, no X Window
28 | Chapter 2: Internals Primer

System, no GTK, no BusyBox, and so on. Many veteran Linux and embedded Linux
practitioners have indeed noted that Android feels very alien. Though the Android stack
starts from a clean slate with regards to user-space, we will discuss how to get "legacy"
or "classic" Linux applications and utilities to coexist side-by-side with the Android
stack.
The Google developer documentation presents a different architectural
diagram from that shown in Figure 2-1. The former is likely well suited
for app developers, but omits key information that must be understood
by embedded developers. For instance, Google's diagram and developer
documentationthere offer little to no reference at the time of this writing
to the System Server. Yet, as an embedded developer, you need to know
what that component is, because it's one of the most important parts of
Android and you might need to extend or interact with it directly.
This is especially important to understand because you'll see Google's
diagram presented and copied in several documents and presentations.
If nothing else, remember that the System Server is rarely if at all exposed
to app developers and that the bulk of information out there is aimed
at app developers, not developers doing platform work.
Let's take a deeper look into each part of Android's architecture, starting from the
bottom of Figure 2-1 and going up. Once we are done covering the various components,
we'll end this chapter by going over the system's startup process.
Linux Kernel
The Linux kernel is the center-piece of all distributions traditionally labeled as "Linux,"
including mainstream distributions such as Ubuntu, Fedora, and Debian. And while
it's available in "vanilla" form from the Linux Kernel Archives, most distributions apply
their own patches to it to fix bugs and enhance the performance or customize the
behavior of certain aspects of it before distributing it to their users. Android, as such,
is no different in that the Android developers patch the "vanilla" kernel to meed their
needs.
Android differs from standard practice, however, in relying on several custom func-
tionalities that are significantly different from what is found in the "vanilla" kernel. In
fact, whereas the kernel shipped by a Linux distribution can easily be replaced by a
kernel from kernel.org with little to no impact to the rest of the distribution's compo-
nents, Android's user-space components will simply not work unless they're running
on an "Androidized" kernel. As I had mentioned in the previous chapter, Android kenels
are, in sum, forks from the mainline kernel.
Although it's beyond the scope of this book to discuss the Linux kernel's internals, let's
go over the main "Androidisms" added to the kernel. You can get information about
Linux Kernel | 29

the kernel's internals by having a look at Robert Love's Linux Kernel Development, 3rd
ed. and starting to follow the Linux Weekly News (LWN) site. LWN contains several
seminal articles on the kernel's internals and provides the latest news regarding the
Linux kernel's development.
Note that the following subsections cover only the most important Androidisms. An-
droid-ified kernels typical contain several hundred patches over the standard kernel,
often to provide device-specific functionality, fixes and enhancements. You can use
git to do an exhaustive analysis on the commit deltas between one of the kernels at
http://android.git.kernel.org and the mainline kernel they were forked from. Also, note
that some of the functionality that appears in some Android-ified kernels, such as the
PMEM driver for instance, is device-specific and isn't necessarily used in all Android
devices.
Wakelocks
Of all the Androidisms, this is likely the most contentious. The discussion threads
covering its inclusion into the mainline kernel generated close to 2,000 emails and yet
still, there's no clear path for merging the wakelock functionality.
To understand what wakelocks are and do, we must first discuss how power manage-
ment is typically used in Linux. The most common use case of Linux's power manage-
ment is a laptop computer. When the lid is closed on a laptop running Linux, it will
usually go into "suspend" or "sleep" mode. In that mode, the system's state is preserved
in RAM but all other parts of the hardware are shut down. Hence, the computer uses
as little battery power as possible. When the lid is raised, the laptop "wakes up" and
the user can resume using it almost instantaneously.
That modus operandi works fine for a laptop and desktop-like devices, but it doesn't
fit mobile devices such as handsets as well. Hence, Android's development team devised
a mechanism that changes the rules slightly to make them more palatable to such use
cases. Instead of letting the system be put to sleep at the user's behest, an Androidized
kernel is made to go to sleep as soon and as often as possible. And to keep the system
from going to sleep while important processing is being done or while an app is waiting
for the user's input, wakelocks are provided to... keep the system awake.
The wakelocks and early suspend functionality are actually built on top of Linux's
existing power management functionality. However, they introduce a different devel-
opment model, since application and driver developers must explicitely grab wakelocks
whenever they conduct critical operations or must wait for user input. Usually, app
developers don't need to deal with wakelocks directly, because the abstractions they
use automatically take care of the required locking. They can, nonetheless, communi-
cate with the Power Manager Service if they require explicit wakelocks. Driver devel-
opers, on the other hand, can call on the added in-kernel wakelock primitives to grab
and release wakelocks. The downside of using wakelocks in a driver, however, is that
30 | Chapter 2: Internals Primer

it becomes impossible to push that driver into the mainline kernel, because the mainline
doesn't include wakelock support.
The following LWN articles describe wakelocks in more detail and ex-
plain the various issues surrounding their inclusion into the mainline
kernel:
• Wakelocks and the embedded problem
• From wakelocks to a real solution
• Suspend block
• Blocking suspend blockers
• What comes after suspend blockers
• An alternative to suspend blockers
Low Memory Killer
As I mentioned earlier, Android's behavior is very much predicated on low-memory
conditions. Hence, out-of-memory behavior is crucial. For this reason, the Android
development team has added an additional low memory killer to the kernel that kicks
in before the default kernel OOM killer. Android's low-memory killer applies the pol-
icies described in the app development documentation, weeding out processes hosting
components that haven't been used in a long time and that are not high-priority.
This low memory killer is based on the OOM adjustments mechanism availalble in
Linux that enables the enforcement of different OOM kill priorities for different pro-
cesses. Basically, the OOM adjustments allow user space to control part of the kernel's
OOM killing policies. The OOM adjustments range from -17 to 15, with a higher
number meaning the associated process is a better candidate for being killed if the
system is out of memory.
Android therefore attributes different OOM adjustment levels to different types of
processes according to the components they are running, and configures its own low
memory killer to apply different thresholds for each category of process. This effectively
allows it to preempt the activation of the kernel's own OOM killer—which only kicks
in when the system has no memory left—by kicking in when the given thresholds are
reached, not when the system runs out of memory.
The user-space policies are themselves applied by the init process at startup (see
“Init” on page 47), and readjusted and partly enforced at runtime by the Activity
Manager Service, which is part of the System Server. The Activity Manager is one of
the most important services in the System Server and is responsible, amongst many
other things, for carrying out the component lifecycle presented earlier.
Linux Kernel | 31

Have a look at the Taming the OOM killer LWN article if you'd like to
get more information regarding the kernel's OOM killer and how An-
droid builds on it.
Binder
Binder is an RPC/IPC mechanism akin to COM under Windows. Its roots actually date
back to work done within BeOS prior to Be's assets being bought by Palm. It continued
life within Palm and the fruits of that work were eventually released as the Open-
Binder project. Though OpenBinder never survived as a stand-alone project, a few key
developers who had worked on it, such as Dianne Hackborn and Arve Hjønnevåg,
eventually ended up working within the Android development team.
Android's Binder mechanism is therefore inspired by that previous work, but Android's
implementation does not derive from the OpenBinder code. Instead, it's a clean room
rewrite of a subset of the OpenBinder functionality. The OpenBinder Documenta-
tion remains a must-read if you want to understand the mechanism's underpinings and
its design philosophy.
In essence, Binder attempts to provide remote object invocation capabilities on top of
a classic OS. In other words, instead of re-engineering traditional OS concepts, Binder
"attempts to embrace and transcend them." Hence, developers get the benefits of deal-
ing with remote services as objects without having to deal with a new OS. It therefore
becomes very easy to extend a system's functionality by adding remotely-invocable
objects instead of implementing new daemons for providing new services, as would
usually be the case in the Unix philosophy. The remote object can therefore be imple-
mented in any desired language and may share the same process space as other remote
services or have its own separate process. All that is needed to invoke its methods is its
interface definition and a reference to it.
And as you can see in Figure 2-1, Binder is a conerstone of Android's architecture. It's
what allows apps to talk the System Server and it's what apps use to talk to each others'
service components, although, as I mentioned earlier, app developers don't actually
talk to the Binder directly. Instead, they use the interfaces and stubs generated by the
aidl tool. Even when apps interface with the System Server, the android.* APIs abstract
its services and the developer never actually sees that Binder is being used.
32 | Chapter 2: Internals Primer

Though they sound semantically similar, there is a very big difference
between services running within the System Server and services exposed
to other apps through the "service" component model I introduced in
“Components” on page 22 as being one of the components available to
app developers. Most importantly, service components are subject to
the same system mechanics as any other component. Hence, they are
lifecycle-managed and run within the same priviledge sandbox associ-
ated as the app they are part of. Services running within the System
Server, on the other hand, typically run with system priviledges and live
from boot to reboot. The only things these two types of services share
together are: a) their name, b) the use of Binder to interact with them.
The in-kernel driver part of the Binder mechanism is a character driver accessible
through /dev/binder. It's used to transmit parcels of data in between the communicating
parties using calls to ioctl(). It also allows one process to designate itself as the "Con-
text Manager." The importance of the Context Manager along with the actual user-
space use of the Binder driver will be discussed in more detail later in this chapter.
Anonymous Shared Memory (ashmem)
Another IPC mechanism available in most OSes is shared memory. In Linux, this is
usually provided by the POSIX SHM functionality, part the System V IPC mechanisms.
If you look at the ndk/docs/system/libc/SYSV-IPC.html file included in the AOSP, how-
ever, you'll discover that the Android development team seems to have a dislike for
SysV IPC. Indeed, the argument is made in that file that the use of SysV IPC mechanisms
in Linux can lead to resource leakage within the kernel, opening the door in turn for
malicious or misbehaving software to cripple the system.
Though it isn't stated as such by Android developers or any of the documentation within
the ashmem code or surrounding its use, ashmem very likely owes part of its existence
to SysV IPC's shortcomings as seen by the Android development team. Ashmem is
therefore described as being similar to POSIX SHM "but with different behavior." For
instance, it does reference counting to destroy memory regions when all processes re-
ferring to them have exited and will shrink mapped regions if the system is in need of
memory. It will also enable memory regions to be shrunk in case the system is under
memory pressure. "Unpinning" a region allows it to be shrunk, whereas "pinning" a
region disallows the shrinking.
Typically, a first process creates a shared memory region using ashmem and uses Binder
to share the corresponding file descriptor with other processes with which it wishes to
share the region. Dalvik's JIT code cache, for instance, is provided to Dalvik instances
through ashmem. A lot of System Server components, such as the Surface Flinger and
Linux Kernel | 33

the Audio Flinger, rely on ashmem, though not directly but through the IMemory§ in-
terface.
Alarm
The alarm driver added to the kernel is another case where the default kernel func-
tionality wasn't sufficient for Android's requirements. Android's alarm driver is actually
layered on top of the kernel's existing Real-Time Clock (RTC) and High-Resolution
Timers (HRT) functionalities. The kernel's RTC functionality provides a framework
for driver developers to create board-specific RTC functions, while the kernel exposes
a single hardware-independent interface through the main RTC driver. The kernel HRT
functionality, on the other hand, allows callers to get woken up at very specific points
in time.
In "vanilla" Linux, application developers typically call the setitimer() system call to
get a signal when a given time value expires.‖ The system call allows for a handful of
types of timers, one of which, ITIMER_REAL, uses the kernel's High-Resolution Timer
(HRT). This functionality, however, doesn't work when the system is suspended. In
other words, if an application uses setitimer() to request being woken up at a given
time and then, in the interim, the device is suspended, that application will get its signal
only when the device is woken up again.
Separately from the setitimer() system call, the kernel's RTC driver is accessible
through /dev/rtc and enables its users to use an ioctl(), among other things, to set an
alarm that will be activated by the RTC hardware device in the system. That alarm will
fire off whether the system is suspended or not, since it's predicated on the behavior or
the RTC device, which remains active even when the rest of the system is suspended.
Android's alarm driver cleverly combines the best of both worlds. By default, the driver
uses the kernel's High-Resolution Timer (HRT) functionality to provide alarms to its
users, much like the kernel's own built-in timer functionality. However, if the system
is about to suspend itself, it programs the RTC so that the system gets woken up at the
appropriate time. Hence, whenever an application from user space needs a specific
alarm, it just needs to use Android's alarm driver to be woken up at the appropriate
time, regardless of whether the system is suspended in the interim.
From user-space, the alarm driver appears as the /dev/alarm character device and allows
its users to set up alarms and adjust the system's time (wall time) through ioctl() calls.
There are a few key AOSP components that rely on /dev/alarm. For instance, Toolbox
and the SystemClock class, available through the app development API, rely on it to set/
get the system's time. Most importantly, though, the Alarm Manager service part of the
§IMemory is an internal interface available only within the AOSP, not to app developers. The closest class
exposed to app developers is MemoryFile.
‖For more information, see the setitimer()'s man page.
34 | Chapter 2: Internals Primer

System Server uses it to provide alarm services to apps that are exposed to app devel-
opers through the AlarmManager class.
Both the driver and Alarm Manager use the wakelock mechanism wherever appropriate
to maintain consistency between alarms and the rest of Android's wakelock-related
behavior. Hence, when an alarm is fired, its consuming app gets the chance to do
whatever operation is required before the system is allowed to suspend itself again, if
need be.
Logger
Logging is yet another essential component of any Linux system, embedded ones in-
cluded. Being able to analyze a system's logs for errors or warnings either in post-mor-
tem or in real-time can be vital to isolate fatal errors, especially transient ones. By de-
fault, most Linux distributions include two logging systems: the kernel's own log, typ-
ically accessed through the dmesg command, and the system logs, typically stored in
files in the /var/log directory. The kernel's log usually contains the messages printed
out by the various printk() calls made within the kernel, either by core kernel code or
by device drivers. For their part, the system logs contain messages coming from various
daemons and utilities running in the system. In fact, you can use the logger command
to send your own messages to the system log.
With regard to Android, the kernel's logging functionality is used as-is. However, none
of the usual system logging software packages typically found in most Linux distribu-
tions is found in Android. Instead, Android defines its own logging mechanisms based
on the Android logger driver added to the kernel. syslog relies on sending messages
through sockets, and therefore generates a task switch. It also uses files to store its
information, therefore generating writes to a storage device. In contrast, Android's log-
ging functionality manages a handful of separate kernel-hosted buffers for logging data
coming from user-space. Hence, no task-switches or file writes are required for each
event being logged. Instead, the driver maintains circular buffers where it logs every
incoming event and returns immediately back to the caller.
Because of its light-weight and efficient design, Android's logger can actually be used
by user-space components at run-time to regularly log events. In fact, the Log class
available to app developers more or less directly invokes the logger driver to write to
the main event buffer. Obviously, all good things can be abused and it's preferable to
keep the logging light, but still the level of use made possible by exposing Log through
the app API along with the level of use of logging within the AOSP itself would have
likely been very difficult to sustain had Android's logging been based on syslog.
Figure 2-2 describes Android's logging framework in more detail. As you can see, the
logger driver is the core building block on which all other logging-related functionality
relies. Each buffer it manages is exposed as a separate entry within /dev/log/. However,
no user-space component directly interacts with that driver. Instead, they all rely on
liblog which provides a number of different logging functions. Depending on the func-
Linux Kernel | 35

Figure 2-2. Android's logging framework
tions being used and the parameters being passed, events will get logged to different
buffers. The liblog functions used by the Log and Slog classes, for instance, will test
whether the event being dispatched comes from a radio-related module. If so, the event
is sent to the "radio" buffer. If not, the Log class will send the event to the "main" buffer
whereas the Slog class will send it to the "system" buffer. The "main" buffer is the one
whose events are shown by the logcat command when it's issued without any param-
eters.
Both the Log and EventLog classes are exposed through the app development API, while
Slog is for internal AOSP use only. Despite being available to app developers, though,
EventLog is clearly identified in the documentation aas mainly or system integrators,
not app developers. In fact, the vast majority of code samples and examples provided
as part of the developer documentation use the Log class. Typically, EventLog is used
by system components to log binary events to the Android's "events" buffer. Some
system components, especially System Server-hosted services, will use a combination
of Log, Slog, and EventLog to log different events. An event that might be relevant to
app developers, for instance, might be logged using Log, while an event relevant to
platform developers or system integrators might be logged using either Slog or
EventLog.
36 | Chapter 2: Internals Primer

Note that the logcat utility, which is commonly used by app developers to dump the
Android logs, also relies on liblog. In addition to providing access functions to the
logger driver, liblog also provides functionality for formatting events for pretty printing
and filtering. Another feature of liblog is that it requires every event being logged to
have a priority, a tag, and data. The priority is one of verbose, debug, info, warn, or
error. The tag is a unique string that identifies the component or module writing to
the log, and the data is the actual information that needs to be logged. This description
should in fact sound fairly familiar to anyone exposed to the app developpment API,
as this is exactly what's spelled out by the developer documentation for the Log class.
The final piece of the puzzle here is the adb command. As we'll discuss later, the AOSP
includes an Android Debug Bridge (ADB) daemon that runs on the Android device and
that is accessed from the host using the adb command-line tool. When you type adb
logcat on the host, the daemon actually launches the logcat command locally on the
target to dump its "main" buffer and then transfers that back to the host to be shown
on the terminal.
Other Notable Androidisms
A few other Androidisms, in addition to those already covered, are worth mentioning,
even if we don't cover them in as much detail.
Paranoid Networking
Usually in Linux, all processes are allowed to create sockets and interact with the
network. Per Android's security model, however, access to network capabilities
has to be controlled. Hence, an option is added to the kernel to gate access to socket
creation and network interface administration based on whether the current proc-
ess belongs to a certain group of processes or possesses certain capabilities. This
applies to IPv4, IPv6, and Bluetooth.
RAM Console
As I mentioned earlier, the kernel manages its own log, which you can access using
the dmesg command. The content of this log is very useful, as it often contains
critical messages from drivers and kernel subsystems. On a crash or a kernel panic,
its content can be instrumental for post-mortem analysis. Since this information is
typically lost on reboot, Android adds a driver that registers a RAM-based console
that survives reboots and makes its content accessible through /proc/last_kmsg.
Physical Memory (pmem)
Like ashmem, the pmem driver allows for sharing memory between processes.
However, unlike ashmem, it allows the sharing of large chunks of physically-con-
tiguous memory regions, not virtual memory. In addition, these memory regions
may be shared between processes and drivers. For the G1 handset, for instance,
pmem heaps are used for 2D hardware acceleration. Note, though, that pmem isn't
used in all devices. In fact, according to Brian Swetland, one of the Android kernel
Linux Kernel | 37

development team members, it was written to specifically target the
MSM7201A's# limitations.
Hardware Support
Android's hardware support approach is significantly different from the classic ap-
proach typically found in the Linux kernel and in Linux-based distributions. Specifi-
cally, the way hardware support is implemented, the abstractions built on that hard-
ware support, and the mindset surrounding the licensing and distribution of the re-
sulting code are all different.
The Linux Approach
The usual way to provide support for new hardware in Linux is to create device drivers
that are either built as part of the kernel or loaded dynamically at runtime through
modules. The corresponding hardware is thereafter generally accessible in user-space
through entries in /dev. Linux's driver model defines three basic types of devices: char-
acter devices, devices that appear as a stream of bytes, block devices (essentially hard
disks), and networking devices. Over the years, quite a few additional device and sub-
system types have been added, such as for USB or MTD devices. Nevertheless, the APIs
and methods for interfacing with the /dev entry corresponding to a given type of device
have remained fairly standardized and stable.
This, therefore, has allowed various software stacks to be built on top of /dev nodes to
either interact with the hardware directly or expose generic APIs that are used by user
applications to provide access to the hardware. The vast majority of Linux distributions
in fact ship with a similar set of core libraries and subsystems, such as the ALSA audio
libraries and the X Window System, to interface with hardware devices exposed
through /dev.
With regard to licensing and distribution, the general "Linux" approach has always
been that drivers should be merged and maintained as part of the mainline kernel and
distributed with it under the terms of the GPL. So, while some device drivers are de-
veloped and maintained independently and some are even distributed under other li-
censes, the consensus has been that that isn't the preferred approach. In fact, with
regard to licensing, non-GPL drivers have always been a contentious issue. Hence, the
conventional wisdom is that users' and distributors' best bet to get the latest drivers is
usually to get the latest mainline kernel from http://kernel.org. This has been true since
the kernel's early days and remains true despite some additions having been made to
the kernel to allow the creation of user-space drivers.
#The MSM7201A is the G1's processor.
38 | Chapter 2: Internals Primer

Android's General Approach
Although Android builds on the kernel's hardware abstractions and capabilities, its
approach is very different. On a purely technical level, the most glaring difference is
that its subsystems and libraries don't rely on standard /dev entries to function properly.
Instead, the Android stack typically relies on shared libraries provided by manufactur-
ers to interact with hardware. In effect, Android relies on what can be considered a
Hardware Abstraction Layer (HAL), although, as we will see, the interface, behavior
and function of abstracted hardware components differ greatly from type to type.
In addition, most software stacks typically found in Linux distributions to interact with
hardware are not found in Android. There is no X Window System, for instance, and
while ALSA drivers are sometimes used—a decision left up to the hardware manufac-
turer who provides the shared library implementing audio support for the HAL—access
to their functionality is different from that on standard Linux distributions.
Figure 2-3 presents the typical way in which hardware is abstracted and supported in
Android, and the corresponding distribution and licensing. As you can see, Android
still ultimately relies on the kernel to access the hardware. However, this is done
through shared libraries that are either implemented by the device manufacturer or
provided as part of the AOSP.
One of the main features of this approach is that the license under which the shared
library is distributed is up to the hardware manufacturer. Hence, a device manufacturer
can create a simplistic device driver that implements the most basic primitives to access
a given piece of hardware and make that driver available under the GPL. Not much
would be revealed about the hardware, since the driver wouldn't do anything fancy.
That driver would then expose the hardware to user-space through mmap() or ioctl()
and the bulk of the intelligence would be implemented within a proprietary shared
library in user-space that uses those functions to drive the hardware.
Android does not in fact specify how the shared library and the driver or kernel sub-
system should interact. Only the API provided by the shared library to the upper layers
is specified by Android. Hence, it's up to you to determine the specific driver interface
that best fits your hardware, so long as the shared library you provide implements the
appropriate API. Nevertheless, we will cover the typical methods used by Android to
interface to hardware in the next section.
Where Android is relatively inconsistent is the way the hardware-supporting shared
libraries are loaded by the upper layers. Remember for now that for most hardware
types, there has to be a .so file that is either provided by the AOSP or that you must
provide for Android to function properly.
No matter which mechanism is used to load a hardware-supporting shared library, a
system service corresponding to the type of hardware is typically responsible for loading
and interfacing with the shared libary. That system service will be responsible for in-
teracting and coordinating with the other system services to make the hardware behave
Hardware Support | 39

Figure 2-3. Android's "Hardware Abstraction Layer"
coherently with the rest of the system and the APIs exposed to app developers. If you're
adding support for a given type of hardware, it's therefore crucial that you try to un-
derstand in as much detail as possible the internals of the system service corresponding
to your hardware. Usually, the system service will be split in two parts, one part in Java
that implements most of the Android-specific intelligence and another part in C whose
main job is to interact with the hardware-supporting shared library and other low-level
functions.
Loading and Interfacing Methods
As I mentioned earlier, there are various ways in which system services and Android in
general interact with the shared libraries implementing hardware support and hardware
devices in general. It's difficult to fully understand why there is such a variety of meth-
ods, but I suspect that some of them evolved organically. Luckily, there seems to be a
movement towards a more uniform way of doing things. Given that Android moves at
a fairly rapid pace, this is one area that will require keeping an eye on for the forseeable
future, as it's likely to evolve.
40 | Chapter 2: Internals Primer

Note that the methods described here are not necessarily mutually exclusive. Often a
combination of these is used within the Android stack to load and interface with a
shared library or some software layer before or after it. I'll cover specific hardware in
the next section.
dlopen()-loading through HAL
Applies to: GPS, Lights, Sensors, and Display
Some hardware-supporting shared libraries are loaded by the libhardware library.
This library is part of Android's HAL and exposes hw_get_module(), which is used
by some system services and subsystems to explicitly load a given specific hard-
ware-supporting shared library (a.k.a. a "module" in HAL terminology*).
hw_get_module() in turn relies on the classic dlopen() to load libraries into the
caller's address space.
Linker-loaded .so files
Applies to: Audio, Camera, Wifi, Vibrator, and Power Management
In some cases, system services are simply linked against a given .so file at build
time. Hence, when the corresponding binary is run, the dynamic linker automat-
ically loads the shared library into the process's address space.
Hardcoded dlopen()s
Applies to: StageFright and Radio Interface Layer (RIL)
In a few cases, the code invokes dlopen() directly instead of going through
libhardware to fetch a hardware-enabling shared library. The rationale for using
this method instead of the HAL is unclear.
Sockets
Applies to: Bluetooth, Network Management, Disk Mounting, and Radio Interface
Layer (RIL)
Sockets are sometimes used by system services or framework components to talk
to a remote daemon or service that actually interacts with the hardware.
Sysfs entries
Applies to: Vibrator and Power Management
Some entries in sysfs (/sys) can be used to control the behavior of hardware and/
or kernel subsystems. In some cases, Android uses this method instead of /dev
entries to control the hardware.
/dev nodes
Applies to: Almost every type of hardware
Aguably, any hardware abstraction must at some point communicate with an entry
in /dev, because that's how drivers are exposed to user-space. Some of this com-
* Not to be confused with loadable kernel modules, which are a completely different and unrelated software
construct, even though they share some similar properties.
Hardware Support | 41

munication is likely hidden to Android itself because it interacts with a shared
library instead, but in some other cases AOSP components directly access device
nodes. Such is the case of input libraries used by the Input Manager.
D-Bus
Applies to: Bluetooth
D-Bus is a classic messaging system found in most Linux distributions for facili-
tating communication between various desktop components. It's included in An-
droid because it's the prescribed way for a non-GPL component to talk to the GPL-
licensed BlueZ stack—Linux's default Bluetooth stack and the one used in Android
—without being subject to the GPL's redistribution requirements; D-Bus itself be-
ing dual-licensed under the Academic Free License (AFL) and the GPL. Have a
look at http://dbus.freedesktop.org for more information about D-Bus.
Device Support Details
Table 2-1 summarizes the way in which each type of hardware is supported in Android.
As you'll notice, there is a wide variety of combinations of mechanisms and interfaces.
If you plan on implementing support for a specific type of hardware, the best way
forward is to start from an existing sample implementation. The AOSP typically in-
cludes hardware support code for a few handsets, generally those which were used by
Google to develop new Android releases and therefore served as flagship devices.
Sometimes the sources for the hardware support are quite extensive, as was the case
for the Samsung Nexus S (a.k.a. "Crespo", its code-name).
The only type of hardware for which you are unlikely to find publicly-available imple-
mentations on which to base your own is the RIL. For various reasons, it's best not to
let everyone be able to play with the airwaves. Hence, manufacturers don't make such
implementations available. Instead, Google provides a reference RIL implementation
in the AOSP should you want to implement a RIL.
Table 2-1. Android's hardware support methods and interfaces
Hardware System Service Interface to user-space HW support Interface to HW
Audio Audio Flinger Linker-loaded libaudio.so Up to HW manufacturer, though
ALSA is typical
Bluetooth Bluetooth Serv- Socket/D-Bus to BlueZ BlueZ stack
ice
Camera Camera Service Linker-loaded libcamera.so Up to HW manufacturer, some-
times Video4Linux
Display Surface Flinger HAL-loaded gralloc module /dev/fb0 or /dev/graphics/fb0
GPS Location Man- HAL-loaded gps module Up to HW manufacturer
ager
Input Input Manager Native library Entries in /dev/input/
42 | Chapter 2: Internals Primer

Hardware System Service Interface to user-space HW support Interface to HW
Lights Lights Service HAL-loaded lights module Up to HW manufacturer
Media N/A, StageF- dlopen on libstagefrighthw.so Up to HW manufacturer
right frame-
work within
Media Service
Network interfa- Network Man- Socket to netd ioctl() on interfaces
cesa agement Serv-
ice
Power Manage- Power Manager Linker-loaded libhardware_legacy.so Entries in /sys/android_power/
ment Service or /sys/power/
Radio (Phone) N/A, entry- Socket to rild, which itself does a Up to HW manufacturer
point is teleph- dlopen()on manufacturer-provided .so
ony Java code
Storage Mount Service Socket to vold System calls
Sensors Sensor Service HAL-loaded sensors module Up to HW manufacturer
Vibrator Vibrator Service Linker-loaded libhardware_legacy.so Up to HW manufacturer
Wifi Wifi Service Linker-loaded libhardware_legacy.so Classic wpa_supplicantb
a This is for Tether, NAT, PPP, PAN, USB RNDIS (Windows). It isn't for Wifi.
b The wpa_supplicant is the same software package used on any Linux desktop to manage Wifi networks and connections.
Native User-Space
Now that we've covered the low-level layers on which Android is built, let's start going
up the stack. First off, we'll cover the native user-space environment in which Android
operates. By "native user-space" I mean all the user-space components that run outside
the Dalvik virtual machine. This includes quite a few binaries that are compiled to run
natively on the target's CPU architecture. These are generally started either automati-
cally or as needed by the init process according to its configuration files, or are available
to to be invoked on the command line once a developer shells into the device. Such
binaries usually have direct access the root filesystem and the native libraries included
in the system. Their capabilities would be gated by the filesystem rights granted to them
and wouldn't be subject to any of the restrictions imposed on a typical Android app by
the Android framework because they are running outside of it.
Note that Android's user-space was designed pretty much from a blank slate and differs
greatly from what you'd find in a standard Linux distribution. Hence, I will try in as
much as possible in the following to explain where Android's user-space is different or
similar to what you'd usually find in a Linux-based system.
Native User-Space | 43

Filesystem layout
Like any other Linux-based distribution, Android uses a root filesystem to store appli-
cations, libraries, and data. Unlike the vast majority of Linux-based distributions,
however, the layout of Android's root filesystem does not adhere to the Filesystem
Hierarchy Standard (FHS).† The kernel itself doesn't enforce the FHS, but most soft-
ware packages built for Linux assume that the root filesystem they are running on
conforms to the FHS. Hence, if you intend to port a standard Linux application to
Android, you'll likely need to do some legwork to ensure that the filepaths it relies on
are still valid.
Given that most of the packages running in Android's user space were written from
scratch specifically for Android, this lack of conformity is of little to no consequence
to Android itself. In fact, it has some benefits, as we'll see shortly. Still, it's important
to learn how to navigate Android's root filesystem. If nothing else, you'll likely have to
spend quite some time inside of it as you bring Android up on your hardware or cus-
tomize it for that hardware.
The two main directories in which Android operates are /system and /data. These di-
rectories do not emanate from the FHS. In fact, I can't think of any mainstream Linux
distribution that uses either of these directories. Rather, they reflect the Android de-
velopment team's own design. This is one of the first signs hinting to the fact that it
might be possible to host Android side-by-side with a common Linux distribution on
the same root filesystem. As I said earlier, we'll actually examine this possibility in more
detail later in the book.
/system is the main Android directory for storing immutable components generated by
the build of the AOSP. This includes native binaries, native libraries, framework pack-
ages, and stock apps. It's usually mounted from a separate image from the root filesys-
tem, which is itself mounted from a RAM disk image. /data, on the other hand, is
Android's main directory for storing data and apps that change over time. This includes
the data generated and stored by apps installed by the user alongside data generated
by Android system components at runtime. It too is usually mounted from its own
separate image.
Android also includes many directories commonly found in any Linux system, such
as: /dev, /proc, /sys, /sbin, /root, /mnt, and /etc. These directories often serve similar if
not identical purposes to the the ones they serve on any Linux system, although they
are very often trimmed down, as is the case of /sbin and /etc, and in some cases are
empty, such as /root.
Interestingly, Android doesn't include any /bin or /lib directories. These directories are
typically crucial in a Linux system, containing, respectively, essential binaries and es-
†The FHS is a community standard that describes the contents and use of the various directories within a
Linux root filesystem.
44 | Chapter 2: Internals Primer

sential libraries. This is yet another artefact that opens the door for making Android
coexist with standard Linux components.
There is of course more to be said about Android's root filesystem. The directories just
mentioned, for instance, contain their own hierarchies. Also, Android's root filesystem
contains other directories that I haven't covered here. We will revist the Android root
filesystem and its make-up in more detail in Chapter 5.
Libraries
Android relies on about a hundred dynamically-loaded libraries, all stored in the /sys-
tem/lib directory. A certain number of these come from external projects that were
merged into Android's codebase to make their functionality available within the An-
droid stack, but a large portion of the libraries in /system/lib are actually generated from
within the AOSP itself. Table 2-2 lists the libraries included in the AOSP that come
from external projects, whereas Table 2-3 summarizes the Android-specific libraries
generated from within the AOSP.
Table 2-2. Libraries generated from external projects imported into the AOSP
Library(ies) External Project Original Location License
libcrypto.so and libssl.so OpenSSL http://www.openssl.org Custom, BSD-like
libdbus.so D-Bus http://dbus.freedesktop.org AFL and GPL
libexif.so Exif Jpeg header manipulation http://www.sentex.net/ Public Domain
tool ~mwandel/jhead/
libexpat.so Expat XML Parser http://expat.sourceforge.net MIT
libFFTEm.so neven face recognition library N/A ASL
libicui18n.so and libicuuc.so International Components for http://icu-project.org MIT
Unicode
libiprouteutil.so and libnetlink.so iproute2 TCP/IP networking http://www.linuxfoundation GPL
and traffic control .org/collaborate/workgroups/
networking/iproute2
libjpeg.so libjpeg http://www.ijg.org Custom, BSD-like
libnfc_ndef.so NXP Semiconductor's NFC li- N/A ASL
brary
libskia.so and libskiagl.so skia 2D graphics library http://code.google.com/p/ ASL
skia/
libsonivox Sonic Network's Audio Synthe- N/A ASL
sis library
libsqlite.so SQLite database http://www.sqlite.org Public Domain
libSR_AudioIn.so and libsrec_jni.so Nuance Communications' N/A ASL
Speech Recognition engine
Native User-Space | 45

Library(ies) External Project Original Location License
libstlport.so Implementation of the C++ http://stlport.sourceforge.net Custom, BSD-like
Standard Template Library
libttspico.so SVOX's Text-To-Speech speech N/A ASL
synthesizer engine
libvorbisidec.so Tremolo ARM-optimized Ogg http://wss.co.uk/pinknoise/ Custom, BSD-like
Vorbis decompression library tremolo/
libwebcore.so WebKit Open Source Project http://www.webkit.org LGPL and BSD
libwpa_client Library based on wpa_suppli- http://hostap.epitest.fi/wpa GPL and BSD
cant _supplicant/
libz.so zlib compression library http://zlib.net Custom, BSD-like
Table 2-3. Android-specific libraries generated from within the AOSP
Category Library(ies) Description
Bionic libc.so C library
libm.so Math library
libdl.so Dynamic linking library
libstdc++.so Standard C++ library
libthread_db.so Threads library
Corea libbinder.so The Binder library
libutils.so, libcutils.so, libnetutils.so, and libsysutils.so Various utility libraries
libsystem_server.so, libandroid_servers.so, libaudioflinger.so, System-services-related libraries
libsurfaceflinger.so, linsensorservice.so, and libcameraser-
vice.so
libcamera_client.so and libsurfaceflinger_client.so Client libraries for certain system services
libpixelflinger.so The PixelFlinger library
libui.so Low-level user-interface-related functionali-
ties, such as user input events handling and dis-
patching and graphics buffer allocation and ma-
nipulation
libgui.so Sensors-related functions library
liblog.so The logging library
libandroid_runtime.so The Android runtime library
Dalvik libdvm.so The Dalvik VM library
libnativehelper.so JNI-related helper functions
Hardware libhardware.so The HAL library that provides
hw_get_module() uses dlopen() to load
hardware support modules (i.e. shared libraries
46 | Chapter 2: Internals Primer

Category Library(ies) Description
that provide hardware support to the HAL) on
demand.
libhardware_legacy.so Library providing hardware support for wifi,
power-management and vibrator
Various hardware-supporting shared libraries. Libraries that provide support for various hard-
ware components, some of which are loaded
using through the HAL, while others are loaded
automatically by the linker
Media libmediaplayerservice.so The Media Player service library
libmedia.so The low-level media functions used by the Me-
dia Player service
libstagefright*.so The many libraries that make-up the StageF-
right media framework
libeffects.so and the libraries in the soundfx/ directory The sound effects libraries
libdrm1.so and libdrm1_jni.so The DRMb framework libraries
OpenGL libEGL.so, libETC1.so, libGLESv1_CM.so, libGLESv2.so, and egl/ Android's OpenGL implementation
ligGLES_android.so
a I'm using this category as catch-all for many core Android functionalities.
b Digital Rights Management
Init
When the kernel finishes booting, it starts just one process, the init process. This process
is then responsible for spawning all other processes and services in the system and for
conducting critical operations such as reboots. The package traditionally provided by
Linux distributions for the init process uses SystemV init, although in recent years many
distributions have created their own variants. Ubuntu, for instance, uses Upstart. In
embedded Linux systems, the classic package that provides init is BusyBox.
Android introduces its own custom init, which brings with it a few novelties.
Configuration language
Unlike traditional inits, which are predicated on the use of scripts that run per the
current run-levels' configuration or on request, Android's init defines its own configu-
ration semantics and relies mostly on changes to global properties to trigger the exe-
cution of specific instructions.
The main configuration file for init is usually stored as /init.rc, but there's also usually
a device-specific configuration file stored as /init.device_name.rc and device-specific
script stored as /etc/init.device_name.sh, where device_name is the name of the device.
You can get a high degree of control over the system's startup and its behavior by
modifying those files. For instance, you can disable the Zygote from starting up auto-
Native User-Space | 47

matically and then starting it manually yourself after having used adb to shell into the
device.
Global properties
A very interesting aspect of Android's init is how it manages a global set of properties
that can be accessed and set from many parts of the system, with the appropriate rights.
Some of these properties are set at build time, while others are set in init's configuration
files and still others are set at runtime. Some properties are also persisted to storage for
permanent use. Since init manages the properties, it can detect any changes and there-
fore trigger the execution of a set of commands based on its configuration.
The OOM adjustments mentioned earlier, for instance, are set on startup by the
init.rc file. So are network properties. Properties set at build time are stored in the /
system/build.prop file and include the build date and build system details. At runtime,
the system will have over a hundred different properties, ranging from IP and GSM
configuration parameters to the battery's level. Use the getprop command to get the
current list of properties and their values.
udev events
As I explained earlier, access to devices in Linux is done through nodes within the /
dev directory. In the older days, Linux distributions would ship with thousands of
entries in that directory to accomodate all possible device configurations. Eventually,
though, a few schemes were proposed to make the creation of such nodes dynamic.
For some time now, the system in use has been udev, which relies on runtime events
generated by the kernel every time hardware is added or removed from the system.
In most Linux distributions, the handling of udev hotplug events is done by the
udevd daemon. In Android, these events are handled by the ueventd daemon built as
part of Android's init and accessed through a symbolic link from /sbin/ueventd to /
init. To know which entries to create in /dev, ueventd relies on the /ueventd.rc and /
ueventd.device_name.rc files.
Toolbox
Much like the root filesystem's directory hierarchy, there are essential binaries on most
Linux system, listed by the FHS for the /bin and /sbin directories. In most Linux dis-
tributions, the binaries in those directories are built from separate packages coming
from different sites on the net. In an embedded system, it doesn't make sense to have
to deal with so many packages, nor necessarily have that many separate binaries.
The approach taken by the classic BusyBox package is to build a single binary that
essentially has what amounts to a huge switch-case, which checks for the first param-
eter on the command line and executes the corresponding functionality. All commands
are then made to be symbolic links the busybox command. So when you type ls, for
48 | Chapter 2: Internals Primer

example, you're actually invoking BusyBox. But since BusyBox's behavior is predicated
on the first parameter on the command line and that parameter is ls, it will behave as
if you had run that command from a standard Linux shell.
Android doesn't use BusyBox, but includes its own tool, Toolbox, that basically func-
tions in the very same way using symbolic links to the toolbox command. Unfortu-
nately, Toolbox is nowhere as feature-full as BusyBox. In fact, if you've ever used Busy-
Box, you're likely going to be very disappointed when using Toolbox. The rationale for
creating a tool from scratch in this case seems to make most sense when viewed from
the licensing angle, BusyBox being GPL licensed. In addition, some Android developers
have stated that their goal was to create a minimal tool for shell-based debugging and
not to provide a full replacement for shell tools as BusyBox does. At any rate, Toolbox
is BSD licensed and manufacturers can therefore modify it and distribute it without
having to track the modifications made by their developers or making any sources
available to their customers.
You might still want to include BusyBox alongside Toolbox to benefit from its capa-
bilities. If you don't want to ship it as part of your final product because of its licensing,
you could include it temporarily during development and strip it in the final production
release. We'll cover this in more detail later.
Daemons
As part of the system startup, Android's init starts a few key daemons that continue to
run throughout the lifetime of the system. Some daemon, such as adbd, are started on
demand, depending on changes to global properties.
Table 2-4. Native Android daemons
Daemon Description
servicemanager The Binder Context Manager. Acts as an index of all Binder services running in the system.
vold The volume manager. Handles the mounting and formatting of mounted volumes and images.
netd The network manager. Handles tethering, NAT, PPP, PAN, and USB RNDIS.
debuggerd The debugger daemon. Invoked by Bionic's linker when a process crashes to do a postmortem analysis. Allows
gdb to connect from the host.
Zygote The Zygote process. It's responsible for warming up the system's cache and starting the System Server. We'll
discuss it in more detail later in this chapter.
mediaserver The Media server. Hosts most media-related services. We'lll discuss it in more detail later in this chapter.
dbus-daemon The D-Bus message daemon. Acts as an intermediary between D-Bus users. Have a look at its man page for
more information.
bluetoothd The Bluetooth daemon. Manages Bluetooth devices. Provides services through D-Bus.
installd The .apk installation daemon. Takes care of installing and uninstalling .apk files and managing the related
filesystem entries.
keystore The KeyStore daemon. Manages an encrypted key-pair value store for cryptographic keys, SSL certs for instance.
Native User-Space | 49

Daemon Description
system_server Android's System Server. This daemon hosts the vast majority of system services that run in Android.
adbd The ADB daemon. Manages all aspects of the connection between the target and the host's adb command.
Command-Line Utilities
More than 150 command-line utilities are scattered over Android's root filesystem. /
system/bin contains the majority of them, but some "extras" are in /system/xbin and a
handful are in /sbin. Around 50 of those in /system/bin are actually symbolic links to /
system/bin/toolbox. The majority of the rest come from the Android base framework,
from external projects merged into the AOSP, or from various other parts of the AOSP.
We'll get the chance to cover the various binaries found in the AOSP in more detail in
Chapter 5.
Dalvik and Android's Java
In a nutshell, Dalvik is Android's Java virtual machine. It allows Android to run the
byte-code generated from Java-based apps and Android's own system components, and
provides both with the required hooks and environment to interface with the rest of
the system, including native libraries and the rest of the native user-space. There's more
to be said about Dalvik and Android's brand of Java, though. But before we can delve
into that explanation, we must first cover some Java basics.
Without boring you with yet another history lesson on the Java language and its origins,
suffice it to say that Java was created by James Gosling at Sun in the early '90s, that it
rapidly became very popular, and that it was, in sum, more than well established before
Android came around. From a developer perspective, the are two aspects that are im-
portant to keep in mind with regard to Java: its differences with a traditional language
such as C and C++, and the components that make up what we commonly refer to as
"Java."
By design, Java is an interpreted language. Unlike C and C++, where the code you write
gets compiled by a compiler into binary assembly instructions to be executed by a CPU
matching the architecture targeted by the compiler, the code that you write in Java gets
compiled by a Java compiler into architecture-independent byte-code that is executed
at a run-time by a byte-code interpreter, also commonly referred to as a "virtual ma-
chine."‡ This modus operandi, along with Java's semantics, enable the language to
include quite a few features not traditionally found in previous languages, such as re-
flection§ and anonymous classes.‖ Also, unlike C and C++, Java doesn't require you to
‡This term was less ambiguous when Java came out, because "virtual machine" software such as VMWare
and VirtualBox weren't as common or as popular as they are today. Such virtual machines do far more than
interpret byte-code, as Java virtual machines do.
§The ability to ask an object whether it implements a certain method.
50 | Chapter 2: Internals Primer

keep track of objects you allocate. In fact, it requires you to lose track of all unused
objects, since it's got an integrated garbage-collector that will ensure all such objects
are destroyed when no active code holds a reference to them any longer.
At a practical level, Java is actually made up of a few distinct things: the Java compiler,
the Java byte-code interpreter—more commonly known as the Java Virtual Machine
(JVM)—and the Java libraries commonly used by Java developers. Together, these are
usually obtained by developers through the Java Development Kit (JDK) provided free
of charge by Oracle. Android actually relies on the JDK for the Java compiler, but it
doesn't use the JVM or the libraries found in the JDK. Instead of the JVM, it relies on
Dalvik, and instead of the JDK libraries, it relies on the Apache Harmony project, a
clean-room implementation of the Java libraries hosted under the umbrella of the
Apache project.
According to its developer, Dan Bornstein, Dalvik distinguishes itself from the JVM by
being specifically designed for embedded systems. Namely, it targets systems that have
slow CPUs and relatively litte RAM, run OSes that don't use swap space, and are battery
powered.
While the JVM munches on .class files, Dalvik prefers the .dex delicatessen. .dex files
are actually generated by postprocessing the .class files generated by the Java compiler
through Android's dx utility. Among other things, an uncompressed .dex file is 50%
smaller than its originating .jar# file. Another interesting factoid is that Dalvik is reg-
ister-based whereas the JVM is stack-based, though that is likely to have little to no
meaning to you unless you're an avid student of VM theory, architecture, and internals.
If you'd like to get more information about the features and internals of
Dalvik, I strongly encourage you to take a look at Dan Bornstein's Goo-
gle I/O 2008 presentation entitled "Dalvik Virtual Machine Internals."
It's about one hour long and available on YouTube. You can also just
go to YouTube and search for "Dan Bornstein Dalvik."
If you'd like to get the inside track on the benefits and tradeoffs between
stack-based VMs versus register-based VMs, have a look at the paper
entitled "Virtual Machine Showdown: Stack Versus Registers" by Shi et
al. in proceedings of VEE'05, June 11-12, 2005, Chicago, IL, p. 153-163.
A feature of Davlik very much worth highlighting, though, is that since 2010 it has
included a Just-In-Time (JIT) compiler for ARM. This means that Dalvik converts apps'
byte-codes to binary assembly instructions that run natively on the target's CPU instead
of being interpreted one instruction at a time by the VM. The result of this conversion
‖Snippets of code that are passed as a parameter to a method being invoked. An anonymous class might be
used, for instance, as a callback registration method, thereby enabling the developer to visualize the code
handling an event at the same location they invoke the callback registration method.
#.jar files are actually Java ARchives (JAR) containing many .class files, each of which contain only a single class.
Dalvik and Android's Java | 51

is then stored for future use. Hence, apps take longer to load the first time, but once
they've been JIT'ed, they load and run much faster. The only caveat here is that JIT isn't
available for any other architecture than ARM. So, in sum, the fastest architecture to
run Android on is, for now, ARM.
As an embedded developer, you're unlikely to need to do anything specific to get Dalvik
to work on your system. Dalvik was written to be architecture-independent. It has been
reported that some of the early ports of Dalvik suffered from some endian issues. How-
ever, these issues seem to have subsided since.
Java Native Interface (JNI)
Despite its power and benefits, Java can't always operate in a vacuum, and code written
in Java sometimes needs to interface to code coming from other languages. This is
especially true in an embedded environment such as Android, where low-level func-
tionality is never too far away. To that end, the Java Native Interface (JNI) mechanism
is provided. It's essentially a call gate to other languages such as C and C++. It's an
equivalent to pinvoke in the .NET/C# world.
App developers sometimes use JNI to call the native code they compile with the NDK
from their regular Java code built using the SDK. Interally, though, the AOSP massively
relies on JNI to enable Java-coded services and components to interface with Android's
low-level functionality, which is mostly written in C and C++. Java-written system
services, for instance, very often use JNI to communicate with matching native code
that interfaces with a given service's corresponding hardware.
A large part of the heavy lifting to allow Java to communicate with other languages
through JNI is actually done by Dalvik. If you go back to Table 2-3 in the previous
section, for instance, you'll notice the libnativehelper.so library, which is provided as
part of Dalvik for facilitating JNI calls.
In later parts of the book, we'll actually get the chance to use JNI to interface Java and
C code. For the moment being, keep in mind that JNI is central to platform work in
Android and that it can be a relatively complex mechanism to use, especially to make
sure you use the appropriate call semantics and function parameters.
Unfortunately, JNI seems to be a dark art reserved to the initiated. In
other words, it's rather difficult to find good documentation on the
topic. There is one authorative book on the topic, The Java™ Native
Interface Programmer’s Guide and Specification by Sheng Liang (Addi-
son-Wesley). You can purchase a copy from your favorite online book-
store, but it's also freely available for download as a PDF. Given how
precious this document is, I suggest you grab a copy in earnest for pos-
terity, just in case it spontaneously evaporates from the net for one rea-
son or another.
52 | Chapter 2: Internals Primer

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

