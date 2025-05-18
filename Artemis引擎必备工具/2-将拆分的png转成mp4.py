import cv2
import os

# Print data
def cout(message):
    print(' [Data] ' + message)

# Check if 'out' directory exists
if not os.path.exists('./out'):
    cout('没有找到 out 目录')
    input('按回车键退出程序')
    quit()

cout('找到 out 目录')

# Read PNG files
img_p = []
for file in sorted(os.listdir('./out'), key=lambda x: int(x.split('.')[0])):
    if file.endswith('.png'):
        img_p.append('./out/' + file)

if not img_p:
    cout('没有找到 PNG 文件')
    input('按回车键退出程序')
    quit()

cout('找到 PNG 文件')

# Ensure 'result' directory exists
if not os.path.exists('./result'):
    cout('没有找到 result 目录')
    cout('创建一个新的 result 目录')
    os.mkdir('result')
    cout('创建 result 目录成功')

cout('找到 result 目录')

# Create MP4 from PNG files
cout('开始合成MP4')
frame = cv2.imread(img_p[0])
height, width, layers = frame.shape

video_out_path = './result/result.mp4'
video_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'mp4v'), 45, (width, height))

for image in img_p:
    video_out.write(cv2.imread(image))

video_out.release()
cout('合成MP4成功')
cout(f'MP4在 {video_out_path} 中')

# Exit
cout('程序成功运行完毕')
input('按回车键退出程序\n')
quit()
