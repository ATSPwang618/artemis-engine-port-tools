import cv2
import os
import shutil

# Print data
def cout(message):
    print(' [Data] ' + message)

# Clear directory content
def dell(p):
    if os.path.exists(p):
        shutil.rmtree(p)
        os.mkdir(p)

# Get input
inp = input("请输入视频文件路径: ")
if inp == '':
    cout('打开 mp4 文件失败')
    input('按回车键退出程序')
    quit()
if not os.path.isfile(inp):
    cout('输入的路径不是有效的文件')
    input('按回车键退出程序')
    quit()
cout('输入成功')

# Create and clear 'out' directory
if not os.path.exists('./out'):
    cout('没有找到 out 目录')
    cout('创建一个新的 out 目录')
    os.mkdir('out')
    cout('创建 out 目录成功')

cout('找到 out 目录')
cout('开始清理 out 目录')

dell('./out')

cout('正在清理.....')

cout('清理 out 目录成功')
cout('切换工作目录')
os.chdir('./out')
cout('切换工作目录成功')

# Read video
cout('开始读取视频')
cout('  开始打开视频')
video = cv2.VideoCapture(inp)
if video.isOpened():
    open, f = video.read()
    cout('  打开视频成功')
else:
    open = False
    cout('  打开 mp4 文件失败')
    input('按回车键退出程序\n')
    quit()
jj = 1
cout('  开始读取视频帧')
while open:
    ret, f = video.read()
    if f is None:
        break
    if ret == True:
        cv2.imwrite(str(jj) + '.png', f)
        cout('    保存 ' + str(jj) + '.png 成功')
        jj += 1
cout('读取视频成功')

# Release resources
video.release()
cout('释放资源')
cout('程序成功运行完毕')
input('按回车键退出程序\n')
quit()
