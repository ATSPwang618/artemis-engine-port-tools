![Artemis Engine Logo](https://github.com/ATSPwang618/artemis-engine-port-tools/blob/main/PlayStation_Vita_illustration.svg.png)
# artemis-engine-port-tools
这个是一个关于artemis engine引擎跨平台移植的工具合集包

说明：

（1）artemis Android

        1.将artemis项目打包成安卓apk的工程文件

        2.用法：

        （1）pc上安装好java和Android studio，按照默认位置进行配置android sdk的环境变量（配置环境遇到问题建议问问deepseek，每个人的电脑都不一样）
        
        （2）ArtemisEngineAndroid目录下新建一个文件local.properties，内容是：
        
          ---------------------------------
          
          # 使用双反斜杠转义
          
          sdk.dir=C\:\\Users\\26241\\AppData\\Local\\Android\\Sdk
          
          # 或使用正斜杠（推荐）
          
          sdk.dir=C:/Users/26241/AppData/Local/Android/Sdk
          
          ----------------------------------
          
        （3）将Artemis项目文件的所有游戏资源移动到ArtemisEngineAndroid\app\src\main\assets目录下方
        
          注意启动ini文件要加入安卓端启动配置信息
          
        （4）cmd打开ArtemisEngineAndroid目录，运行命令
        
          gradlew.bat clean build --stacktrace
          
        （5）在build目录下找到输出的apk文件，安装测试即可，建议使用谷歌默认的安装器，一些国产安卓app安装器会拦截安装包的安装，因为没有验证

（2）asb解密查看：

        用法：
        
        cmd打开软件，输入命令asbutil.exe的路径  asb文件路径
        
        例如：C:\Users\26241\Desktop\asbutil.exe C:\Users\26241\Desktop\script.asb
        
        即可得到这个asb文件里面的明文代码：
        
        C:\Users\26241>C:\Users\26241\Desktop\asbutil.exe C:\Users\26241\Desktop\script.asb

（3）ios模板包.ipa

        这个是ios的官方逆向模版壳，需要mac电脑进行打包文件，我没有这个，只能拜托大家自行尝试啦！

（4）artemis Android（支持emote工程）

        这个是支持emote的模版官方逆向壳，与artemis Android一样的用法，目前我没尝试

（5）PFS文件解包工具

        这个是对Artemis engine的独有数据包xxx.pfs的解包工具集合

        使用方法详细参见目录集合
        
（6）批量处理Artemis engine 工程分辨率

        推荐使用工具VisualNovelUpscaler
        
        地址：https://github.com/hokejyo/VisualNovelUpscaler













-----------------------------------------------
 在此特别感谢群友@沧海的分享，感谢@Anno tokyo大佬的无私分享！！

 
 特别感谢项目：https://github.com/morkt/GARbro
 
        





        
        
