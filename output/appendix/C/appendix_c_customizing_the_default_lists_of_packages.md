# 附录 C：自定义默认包列表

正如我们在第 4 章看到的，构建系统可以修改为添加到其默认构建的包。我们在那一章中没有介绍的是构建系统如何创建它用于创建镜像的默认包列表，以及我们如何进行自定义。显然，修改获取功能正常的 AOSP 所需的基本默认包集合这样的事情是有风险的，因为你可能最终生成过时的镜像。尽管如此，值得一看它是如何工作的以及里面有什么。至少，你会更好地了解如果需要动手时应该在哪里查找。

## 总体依赖

在 2.3/Gingerbread 中，有两个主要变量决定什么被包含在 AOSP 中：`GRANDFATHERED_USER_MODULES` 和 `PRODUCT_PACKAGES`。第一个是从 `build/core/user_tags.mk` 中的静态列表生成的，包含 AOSP 所需的大量"核心"包，如 adbd、系统服务和 Bionic。这个文件不应该被编辑，并以一个警告开头：

```
# This is the list of modules grandfathered to use a user tag
# DO NOT ADD ANY NEW MODULE TO THIS FILE
#
# user modules are hard to control and audit and we don't want
# to add any new module in the system
```

实际上，`GRANDFATHERED_USER_MODULES` 中的包列表或多或少是固定的——我们想要关注的是添加到 `PRODUCT_PACKAGES` 中的包。事实上，有一整套文件在帮助向 `PRODUCT_PACKAGES` 添加更多包时循序渐进，因为完整的 `.mk` 文件列表根据 `device/<vendor>/<product>/` 中的相关文件中的产品描述逐一被包含。

在 4.2/Jelly Bean 中，`GRANDFATHERED_USER_MODULES` 和 `build/core/user_tags.mk` 都不存在了。相反，有一个精简得多的 `GRANDFATHERED_ALL_PREBUILT` 和一个带有与之前类似警告的 `build/core/legacy_prebuilts.mk`。2.3/Gingerbread 的 `GRANDFATHERED_USER_MODULES` 的大部分现在要么在 `build/target/product/base.mk` 中，要么在 `build/target/product/core.mk` 中，并被添加到 `PRODUCT_PACKAGES` 中，其使用方式与 2.3/Gingerbread 相同。

## 组装最终的 PRODUCT_PACKAGES

一般来说，产品将使用 `inherit-product` makefile 函数，正如我们在第 4 章添加 CoyotePad 时所做的那样，以导入包含它们可以构建的 `PRODUCT_PACKAGES` 变量先前声明的其他 `.mk` 文件。

用于大多数 `PRODUCT_PACKAGES` 集合的核心文件是 `build/target/product/core.mk`。在 2.3/Gingerbread 中，这个文件不继承自任何其他 `.mk` 文件。然而在 4.2/Jelly Bean 中，它继承自 `build/target/product/base.mk`。在两个版本中，`build/target/product/core.mk` 都包含 SSL 库和浏览器应用等包。大多数产品描述——除了用于构建 SDK 的那个——实际上并不仅仅依赖这个文件中定义的包集。相反，它们至少依赖 2.3/Gingerbread 中的 `build/target/product/generic.mk` 和 4.2/Jelly Bean 中的 `build/target/product/generic_no_telephony.mk`，两者都依赖 `core.mk`，另外还包括日历、Launcher2 和设置等主要应用的包。例如，2.3/Gingerbread 中的默认模拟器构建依赖 `generic.mk`。我在本书某些部分使用的 TI 为 BeagleBone 提供的默认树也是如此。

然而，大多数产品会走得更远。在 2.3/Gingerbread 中，它们将使用 `build/target/product/full.mk`，它依赖 `generic.mk` 以获取一些额外的输入法（如拼音IME，简体中文键盘）和一些语言区域设置。例如，`full.mk` 被用作 device/samsung/crespo/（Nexus S）的基准。这是我在第 4 章为 CoyotePad 使用的内容。

在 4.2/Jelly Bean 中，大多数产品将使用 `build/target/product/full_base.mk` 而不是 `build/target/product/full.mk`。前者依赖 `generic_no_telephony.mk` 而不是依赖 `generic.mk`。你可以在 device/asus/grouper/ 和 device/samsung/tuna/ 中看到使用 `full_base.mk` 的例子。

## 精简包

我经常从开发者那里收到的一个请求是解释如何精简 AOSP 的大小。为此，你需要浏览 `GRANDFATHERED_USER_MODULES`（如果你使用 2.3/Gingerbread）或 `GRANDFATHERED_ALL_PREBUILT`（如果你使用 4.2/Jelly Bean）中的包列表，以及两种情况下的 `PRODUCT_PACKAGES`，并删除你认为对你的系统不必要的任何内容。正如我之前提到的，这是一个棘手的问题，因为你可能会生成一个无法正常工作的 AOSP。实际上，AOSP 的构建系统不在包之间提供任何类型的依赖检查。

不过，你可以遵循一些基本规则。一般来说，我建议不要尝试修改遗留包列表或在 4.2/Jelly Bean 中修改 `base.mk` 中的包，除非你非常有信心你理解 AOSP 的内部结构以及你正在做的更改的影响。从 `core.mk` 开始，删除包会稍微安全一些。而且你离 `core.mk` 的依赖链越远，删除模块就越安全，不会导致 AOSP 损坏。例如，你可以从 2.3/Gingerbread 的 `generic.mk` 或 4.2/Jelly Bean 的 `generic_no_telephony.mk` 中删除 Launcher2，你将生成一个功能正常的 AOSP。它不会有你习惯的主屏幕，但仍然可以工作。同样的情况适用于那些相同文件中的许多应用。
