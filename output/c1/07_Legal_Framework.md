> 翻译：[Ross.Zeng](https://github.com/zengrx)
> 校对：


### 法律体系

与其他软件一样，安卓的使用和发行也受到如许可、知识产权、市场现实的限制。

#### 代码许可

正如我们之前讨论过的，“安卓”由兼容安卓的Linux内核与AOSP（释放的）两部分组成。虽然仅仅为了运行AOSP而修改，但Linux内核一直处于相同的GNU GPLv2许可下。因此，请记住，你不允许在GPL外的任何其他许可下提交对内核的修改。如果从[android.git.kernel.org](android.git.kernel.org)获取内核代码、修改并在你自己的系统上运行。只要遵守GPL，就能使用源码，甚至包含你所修改的部分去编译映像，并把内核映像发布到产品中去。

内核中也包含了一份来自Linus Torvalds的声明，在源码中很清楚的指出了，只有内核才遵循GPL协议，而运行在其上的应用则**不再**受约束。所以，你可以自由地在Linux内核上创建程序，并在选定的许可下发布它们。

这些规则及其适用性受到了开源领域，或是许多支持、使用Linux内核作为产品基础公司的理解与接纳。除内核之外，基于Linux的发行版中大量关键组件也通常得到一或多个GPL许可。例如GNU的C库（glibc）和GNU编译器（GCC）就分别在LGPL与GPL下发布。而uClibc和Busybox这类嵌入式Linux系统中常用的重要软件包也被许可在LGPL与GPL下。

当然并不是所有人都喜欢GPL。事实上，在衍生类产品上强加许可约束对于大型组织来说是一个严峻的挑战。尤其是考虑到地理分布、开发单位间的文化差异以及对外部代理商的依赖。例如，在北美销售的制造商可能需要与几十上百家供应商打交道才能将产品推向市场，其中的任何一家供应商都有可能交付遵循或不遵循GPL协议的代码。无论代码来自哪个供应商，在销售给客户的项目中，制造商必须要给GPL提供源码。此外，也需要推出审核机制，从而保证基于GPL项目中的工程师遵守许可。

当谷歌着手与制造商们开始打造“开放式”手机操作系统时，很快便明白必须尽可能地避免GPL污染。事实上，除了Linux之外也考虑过其他内核，但因为Linux已经具备了ARM制造商在内的强大工业支持，所以最终还是选择了它。并且其与系统其他部分隔离得很好，所以GPL造成的影响很小。

尽管做了许多努力确保大量的用户空间组件许可不会带来GPL污染类似的问题，谷歌为AOSP打造的大多数组件都以Apache 2.0许可发布。而一些核心组件，例如Bionic库（安卓下的C/C++库）和工具箱都是在BSD许可下发布。也有一些经典的开源项目被纳入到AOSP的*external/*目录，假设OEM制造商不对这部分内容进行客制化（不做任何衍生修改），那么编译出的二进制格式文件不会带来任何问题，并且可以在android.git.kernel.org提供这些二进制文件给使用者下载，这也符合GPL协议对衍生修改继承GPL的定义。

不同于GPL，ASL并不会要求衍生的作品在一个指定的许可下发布。事实上，你可以选择任何一个合适的协议去发布你的修改。以下是ASL的相关部分（完整的协议在http://www.apache.org/licenses/获取）：
+ “根据许可证的条款和条件，每个贡献者在此授予您永久性、全球的、非排他性的、免费的、免版税的、不可撤销的专利实施许可，以源码或的目标的方式复制、筹备、公开展示、公开履行、授权和分发和这些作品及衍生作品。”
+ “……您可以给您的修改添加您自己的版权声明，可以提供使用、复制或分发您修改的不同的许可协议条款，或者对于任何这样的派生作品整体上，只要您的使用、复制及分发作品符合本许可规定的条件。”

此外，ASL明确地提供了专利许可授权，这意味着你可以不需要从谷歌获取任何专利许可，就可以使用ASL授权的安卓源码。不过也规定了一些“管理”上的要求，例如需要清晰地标记被修改的文件等。尽管如此，本质上你已经可以按照意愿自由地授权所做的修改。包括Bionic与Toolbox在内，BSD许可还能够允许二进制形式的发布。

因此，只要继续遵守ASL，制造商可以使用AOSP并客制化成他们所需要的样子，甚至在有需要时保留修改专利。别的不谈，。。。翻不通啊

Hence, manufacturers can take the AOSP and customize to their needs while keeping those modifications proprietary if they wish, so long as they continue abiding by the rest of the provisiongs of the ASL. if noting else, this idmishes the burden of having to implement a process to track all modifications in order to provide those modifications back to recipients who would be entitled to request them had the  GPL been used instead.

#### 品牌使用

相对于源码方面的慷慨，谷歌对安卓相关的品牌元素把控相对严格。让我们来看看这些元素和它们相关的使用术语。官方列表和官方术语可以在[这里](http://www.android.com/branding.html)查阅

*安卓机器人*
这就是那个随处可见的绿色小机器人。它的角色相当于Linux企鹅，其使用权限也类似。事实上，谷歌声称“它可以免费在市场传播中被使用、复制和修改”。唯一的要求是根据创作共用署名许可条款做出适当的规定。

*安卓标识*
这是一个字母集合，使用客制化字型拼出A-N-D-R-O-I-D并且在设备及模拟器开机阶段展示，或使用在android.com网站。在任何情况下你都不被授权使用这个标识。

*安卓客制化字型*
这是用来渲染Android标识的自定义字型，它的使用与标识一样受到限制。

*官方名称中的“安卓”*
如谷歌的声明，“Android” 一词只能在有适当的商标归属时用于描述安卓。例如你不能在未得到谷歌允许的情况下将你的产品命名为“xxx Android”。在后文中将要列出有关安卓兼容性的问答中写到：“如果制造商希望在他们的产品中使用Android名称，那么他们必须先证明这些设备是兼容的”。因此，将设备称为“安卓”是谷歌想要保护的特权。而本质上，必须先保证你的设备能够兼容安卓，与谷歌接洽并达成某种协议后，才能够通告这是“安卓”设备。

*官方名称中的"Droid"*
你不能单独使用“Droid”作为名称，例如“xxx Droid”。但是好像作者也没有搞明白啊所以我也不想翻这段了(oﾟvﾟ)ノ

*信息中的“安卓”*
只要遵循适当的条款（例如Android^TM^使用 <- 这里我不确定写成 安卓^TM^ 后是否是同一个意思）就能在文本中使用，当然也要标记出合适的商标归属。

#### 谷歌的安卓应用程序

通常AOSP中含有能够以ASL获取的核心应用，而安卓手机中通常还会包含一系列附加的谷歌应用，例如安卓应用市场、YouTube、谷歌地图、Gmail等。用户们显然希望谷歌的应用成为安卓的一部分，所以你会想要把这些都安装在设备中。在这种情况下就需要通过兼容性测试并与谷歌达成协议，这点与在产品中使用“Android”颇为相似。这里将会简要地提及一下安卓兼容性程序。

#### 第三方应用市场

虽然主要的应用程序市场由谷歌提供，用户通过预先安装在手机上的安卓应用市场应用去下载安装其他应用，不过也有其他玩家正在扩展安卓开放的接口及许可完成自己修改的应用市场。例如亚马逊和巴诺这样的在线电商，或是威瑞森及斯普林特这类移动网络提供商。甚至还有一个开源项目F-Droid([仓库在这里](http://f-droid.org/repository))，提供了应用程序以及发布在GPL许可下的后端服务。

#### 甲骨文与谷歌之争

作为Sun微系统的一部分，甲骨文也获得了Sun公司对Java语言的知识产权。根据Java创始人之一James Gosling的说法，？？？

As part of acquiring Sun Microsystem, Oracle also acquired Sun's intellectual property (IP) rights to the Java language and, according to Java creator James Gosling, it was clear during the acquisition process that Oracle intended from the onset to go after Google with Sun's Java IP portfolio. And in August 2010 it did just that, filing suit against Google, claiming that it infringed on serveral patents and commited copyright violations.

撇开案子不谈，安卓确实严重依赖Java，而Sun创造了Java并且拥有这门语言大量相关的知识产权。？？？尽管如此，安卓的开发团队还是想方设法让操作系统尽可能少使用Sun的Java。Java的使用主要包括三个方面：语言本身及其语义，运行由Java编译器生成Java字节码的虚拟机，包含Java程序运行时需使用包的类库。

Without going into the merits of the case, it's obvious that Android does indeed heavily rely on Java. And clearly Sun created Java and owned a lot of intellectual property around the language it created. In what appears to have been an effort to anticipate any claims Sun may put forward against Android, nonethless, the Android development team went out of its way to make the OS use as little of Sun's Java as possible. Java is in fact comprised mainly of three things: the language and its semantics, the virtual machine that runs the Java bytecode generated by the Java compiler, and the class library that contains the packages used by Java applications at run time.

官方版本的Java组件由甲骨文的Java开发工具包（JDK）及Java运行时环境（JRE）提供。而安卓只依赖JDK中的Java编译器。安卓使用了定制的Dalvik虚拟机，而不是甲骨文的Java虚拟机；使用Apache Harmony而不是官方类库。这样看，谷歌似乎在尽一切合理的努力避免卷入版权或发行问题。

然而法律诉讼的结果仍有待观望，这可能需要几年时间才能够被解决（*译注：2018年3月28日，美国联邦巡回上诉法院当地时间周二裁定，谷歌Android系统使用Java接口侵犯了甲骨文公司的版权，谷歌面临88亿美元的赔偿*）。在此期间，主持案件的法官似乎希望认真解决这一问题。在2011年5月，他要求甲骨文公司将索赔由132减为3（亿），而谷歌需要将现有的技术应用由数百将至8个。根据Groklaw（译注：一个报道免费及开源社区相关法律新闻的网站）的说法，法官似乎在向各方询问“他们是否预感审判最终会失败”。

另一个间接而又非常相关的是，IBM在2010年10月加入甲骨文的OpenJDK。Apache Harmony一直以来主要由IBM推动，用于安卓的类库，现在IBM的离开几乎宣判了这个项目被抛弃。这件事的发展对安卓的影响在本书编写时还是个未知数。