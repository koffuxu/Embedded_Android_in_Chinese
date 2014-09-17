> 翻译：[koffuxu](https://github.com/koffuxu)

> 校对：

# AOSP内部

现在，我们已经下载下来了AOSP，就让我们来看看这个里面有些什么，最重要的是，与我们前面章节提到的内容建议联系。如果你很渴望知道你自己客户Android的运行，建议你路过这节，当时完成后面的章节后回过来看。如果你仍然阅读，让我们来看看下面这张介绍AOSP顶层目录的表格3-1。

*表格3-1 AOSP 内容总揽*

<table>
<thead>
<tr>
<th>目录</th>
<th>内容</th>
<th>大小（MB）</th>
</tr>
</thead>
<tbody>
<tr>
<td><em>bionic</em></td>
<td>Android的客户C库</td>
<td>14</td>
</tr>
<tr>
<td><em>bootable</em></td>
<td>涉及bootloader和recovery机制</td>
<td>4</td>
</tr>
<tr>
<td><em>build</em></td>
<td>编译系统</td>
<td>4</td>
</tr>
<tr>
<td><em>cts</em></td>
<td>兼容性测试</td>
<td>78</td>
</tr>
<tr>
<td><em>dalvik</em></td>
<td>Dalvik虚拟机</td>
<td>35</td>
</tr>
<tr>
<td><em>development</em></td>
<td>开发工具</td>
<td>65</td>
</tr>
<tr>
<td><em>device</em></td>
<td>设备相关的文件和模块</td>
<td>17</td>
</tr>
<tr>
<td><em>external</em></td>
<td>AOSP使用的外部项目</td>
<td>854</td>
</tr>
<tr>
<td><em>frameworks</em></td>
<td>诸如system services之类的核心组件</td>
<td>361</td>
</tr>
<tr>
<td><em>hardware</em></td>
<td>HAL和硬件支持库</td>
<td>27</td>
</tr>
<tr>
<td><em>libcore</em></td>
<td>Apache Harmony库</td>
<td>54</td>
</tr>
<tr>
<td><em>ndk</em></td>
<td>本地开发工具箱</td>
<td>13</td>
</tr>
<tr>
<td><em>packages</em></td>
<td>Android的应用程序，providers和输入法</td>
<td>117</td>
</tr>
<tr>
<td><em>prebuilt</em></td>
<td>预编译工具，包括工具链</td>
<td>1,389</td>
</tr>
<tr>
<td><em>sdk</em></td>
<td>软件开发工具</td>
<td>14</td>
</tr>
<tr>
<td><em>system</em></td>
<td>Android的“嵌入式Linux”平台</td>
<td>31</td>
</tr>
</tbody>
</table>

正如你所见，*prebuild*和*external*是目录树中最大的两个文件夹，接近整个代码的75%。有趣的是，这两个文件夹是由开放源码项目组成的，它们包括各种GNU版本的工具链，Kernel镜像文件，通用库和像OpenSSl和WebKit等等之类的框架层。*libcore*也是另外一个开放源码项目，Apache Harmony。本质上，这个进一步证明，Android是一个高度依赖于其它开源生涯项目而存在的系统。但，Android仍然包含了许多“原生”（或接近“原生”）的代码；大约有800MB。

![figure_3_1](../images/3-1_androids_architecture.png)

*图 3-1. Android构架*

为了更好的理解Android的源码，回头参考前面章节[图 2-1]()是非常有用的，它说明了Android的构架。[图 3-1]()是从另外一个角度说明在AOSP源码中各个组件的结构。明显地，许多关键的组件是来自*framework/base*这个文件夹，它相当于Android的“大脑”枢纽。事实上，这个目录是值得仔细阅读的，在[表 3-2]()和[表 3-3]()分别包含了大量移动块，这些作为一个嵌入式的开发者也许会感兴趣。

*表 3-2 frameworks/base/内容总揽*

<table>
<thead>
<tr>
<th>目录</th>
<th>内容</th>
</tr>
</thead>
<tbody>
<tr>
<td><em>cmds</em></td>
<td>本地命令和精灵进程</td>
</tr>
<tr>
<td><em>core</em></td>
<td>以Andoird.*开头的包</td>
</tr>
<tr>
<td><em>data</em></td>
<td>字体和声音</td>
</tr>
<tr>
<td><em>graphics</em></td>
<td>2D图形和渲染脚本</td>
</tr>
<tr>
<td><em>include</em></td>
<td>C语言头文件</td>
</tr>
<tr>
<td><em>keystore</em></td>
<td>安全密钥存储</td>
</tr>
<tr>
<td><em>libs</em></td>
<td>C库</td>
</tr>
<tr>
<td><em>location</em></td>
<td>本地provider</td>
</tr>
<tr>
<td><em>media</em></td>
<td>媒体服务，StageFright，编解码等待</td>
</tr>
<tr>
<td><em>native</em></td>
<td>一些框架层组件的本地代码</td>
</tr>
<tr>
<td><em>obex</em></td>
<td>蓝牙Obex</td>
</tr>
<tr>
<td><em>opengl</em></td>
<td>OpenGL库和Java代码</td>
</tr>
<tr>
<td><em>packages</em></td>
<td>一些像状态栏那校报核心包</td>
</tr>
<tr>
<td><em>services</em></td>
<td>系统服务</td>
</tr>
<tr>
<td><em>telephony</em></td>
<td>电话API</td>
</tr>
<tr>
<td><em>tools</em></td>
<td>一些像<em>aapt</em>和<em>aidl</em>的核心工具</td>
</tr>
<tr>
<td><em>voip</em></td>
<td>RTP和SIP的API</td>
</tr>
<tr>
<td><em>vpn</em></td>
<td>VPN管理</td>
</tr>
<tr>
<td><em>wifi</em></td>
<td>Wifi管理和API</td>
</tr>
</tbody>
</table>

***

*表 3-3 system/core/内容总揽*

<table>
<thead>
<tr>
<th>目录</th>
<th>内容</th>
</tr>
</thead>
<tbody>
<tr>
<td><em>adb</em></td>
<td>ADB的守护进程和客户端</td>
</tr>
<tr>
<td><em>cpio</em></td>
<td>用于生成RAM镜像的<em>mkbootfs</em>工具[^b]</td>
</tr>
<tr>
<td><em>debuggerd</em></td>
<td><a href="">第2章</a>涉及到的<em>debuggerd</em>命令</td>
</tr>
<tr>
<td><em>fastboot</em></td>
<td>fastboot是使用“fastboot”协议与Android bootloaders通信的工具</td>
</tr>
<tr>
<td><em>include</em></td>
<td>整个系统的C语言头文件</td>
</tr>
<tr>
<td><em>init</em></td>
<td>Android的<em>init</em></td>
</tr>
<tr>
<td><em>libacc</em></td>
<td>“几乎”是C的编译库用于编译类C代码；用于渲染[^c]</td>
</tr>
<tr>
<td><em>libcutils</em></td>
<td>不属于标准C库的各种C工具函数；用于整个目录</td>
</tr>
<tr>
<td><em>libdiskconfig</em></td>
<td>用于读取和配置磁盘，用于<em>vold</em></td>
</tr>
<tr>
<td><em>liblinenoise</em></td>
<td>BSD_licesed readline()的替代 <a href=""><em>http://github.com/antirez/linenoise</em></a>；用于Android的Shell</td>
</tr>
<tr>
<td><em>liblog</em></td>
<td>如<a href="">图2-2</a>所示是与Android内核Logger模块的接口和库；用  于整个目录</td>
</tr>
<tr>
<td><em>libmincrypt</em></td>
<td>基础的RSA和SHA功能；用于recovery机制和<em>mkbootimg</em>工具</td>
</tr>
<tr>
<td><em>libnetutils</em></td>
<td>网络配置库；用于<em>netd</em></td>
</tr>
<tr>
<td><em>libpixdlfinger</em></td>
<td>底层的图形渲染功能</td>
</tr>
<tr>
<td><em>libsysutils</em></td>
<td>系统各个组件通信的工具，用于<em>netd</em>和<em>vold</em></td>
</tr>
<tr>
<td><em>libzipfile</em></td>
<td>打包zlib用于处理zip文件</td>
</tr>
<tr>
<td><em>logcat</em></td>
<td><em>logcat</em>工具</td>
</tr>
<tr>
<td><em>logwrapper</em></td>
<td>Android的Logger系统中，用于标准输出和标准错误输出重定向传递命令参数的工具</td>
</tr>
<tr>
<td><em>mkbootimg</em></td>
<td>使用RAM Disk和Kernel制作一个启动镜像</td>
</tr>
<tr>
<td><em>netcfg</em></td>
<td>网络配置工具</td>
</tr>
<tr>
<td><em>rootdir</em></td>
<td>默认的Android根目录结构和内容</td>
</tr>
<tr>
<td><em>run-as</em></td>
<td>按照指定的用户ID运行指定程序的工具</td>
</tr>
<tr>
<td><em>sh</em></td>
<td>Android Shell</td>
</tr>
<tr>
<td><em>toolbox</em></td>
<td>Android的工具箱（BusyBox替代）</td>
</tr>
</tbody>
</table>


还有，*base/* ,*frameworkds/*包含了其它的目录，但是他们没有*base/*基础，同样的，除了*core/*,*system/*也包含了一些像*netd/*和*vold/*的目录，这些分别包含了*netd*和*vold*的守护进程。

另外，在顶层目录中，根目录包含了一个Makefle文件。这个文件几乎是空，这个主要是包含用于Android编译系统的入口：

```
### DO NOT EDIT THIS FILE ###
include build/core/main.mk
### DO NOT EDIT THIS FILE ###

```

正如你已经知道，这与我提供与你的AOSP理解相距甚远。毕竟，在2.3.x/Gingerbread有超过14,000目录和100,000文件。按标准来说，这已经是一个很大的工程了。相比之下，基于释放版的3.0.x版本Linux内核有2,000个目录和35,000文件。随着我们的推进，我们将有机会探索AOSP的源码。我强烈建议，尽管，你早前已经开始探索和经历整个源码，你可以轻松的以自己的方式来查看源码。

