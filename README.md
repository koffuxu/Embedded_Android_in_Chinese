Embedded_Android_in_Chinese
===========================
Descrption:

Translate Embedded Android book with co-work

How to co-work:
a,进入项目地址，先fork这个项目到你的项目中。
b,把你fork的项目clone到你本地
c,git branch dev 新建一个分支
d,git checkout dev 切换到dev分支
e, git remote add upstream https://github.com/koffuxu/Embedded_Android_in_Chinese把项目添加你的远程仓库
f,git remote update 把koffuxu的分支拿下来
g,git fetch upstream master 把koffuxu的maser分支更新到本地
h, git rebase upstream/master更新合并
i, git push -u origin dev 提交更新


之后更新使用如下命令

git remote update upstream  把koffuxu的修改更新到本地
git rebase upstream/master更新合并



