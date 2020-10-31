# 基于BERT神经网络的智能网络谣言监测系统_简单的说明文件

### 本项目推出了【安装版】和【源代码版】两种版本
## 1. 安装版安装说明
点击gitee 或github 界面上方或右侧 Release ,即可下载最新的Release 安装版。

**安装版不再需要单独配置 python 环境，【可以独立运行】。**

安装时，随安装向导的指引一步步安装即可

已经在以下操作系统中测试并安装成功：

* Microsoft Windows 10 (x64)
* Microsoft Windows 7 (x64)
### 注意
* 克隆源代码常常会包含最新的bug修复和更新，而安装版的修复更新会略有延迟。

* **安装版仅支持64位的计算机和操作系统，32位计算机和操作系统用户请下载源代码版。**

* **由于部分硬件的原因，导致无法兼容，这时请尝试源代码运行。**



## 2. 源代码版安装说明
源代码版应当在正确的python环境下运行，所以需要安装环境。

已经在以下操作系统中测试并部署成功：

* Microsoft Windows 10 (x64)
* Microsoft Windows 7 (x64)

### 2.1 配置环境
环境具体所需的依赖包的名字在`runtime_command.txt`内。执行其内的语句即可安装所有依赖包。

_runtime_command.txt 的内容_（**示例，请关注实时更新的具体文件**）

`pip install numpy==1.19.2 matplotlib tensorflow==1.15 pyqt5==5.15.0 pyqt5-sip==12.8.1 pyqt5-stubs==5.14.2 pyqt5-tools lac wordcloude`

_**本系统使用python3， linux系统需要使用pip3**_


**【提示】 tensorflow的包体积较大，为节省时间推荐通过本地包的方式进行下载！支持的tensorflow版本为 1.15。**

### 2.2 运行
本系统的启动文件为**main_window_run.py**，在安装环境完毕后，你需要执行
`python main_window_run.py`
即可启动。

_**本系统使用python3， linux系统需要替换为python3**_

### 2.3 在anaconda下配置
首先，你需要使用现有的环境或者新建一个环境，例如：

`conda create -n INRMS_runtime python=3.7`

然后切换到该环境内:

`conda activate INRMS_runtime`

即可按照前两条内的pip语句进行配置。

**_本条目中使用的是anaconda3。_**
## 帮助与反馈
如果有任何bug、反馈或者疑问，**欢迎在页面内提交issue!**

## 版权信息
_Copyright (C) HZU nobug 项目组 Feng SX. L.JG. 2020._

_标注信息： Liu Y, Liu K, Liu W.S, Guo S.Y_