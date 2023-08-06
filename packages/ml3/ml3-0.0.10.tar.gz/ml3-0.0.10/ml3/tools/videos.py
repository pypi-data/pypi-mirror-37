import cv2
import glob
from tqdm import tqdm
import os
from itertools import chain
import re


def img_2_video(img_path, video_name, fps = 1):
	"""
	将一系列图片合成成一个视频
	:param img_path:图片的目录
	:param video_name:视频名称
	:param fps:帧率，可以根据实际情况调整
	:return:成功则返回True，否则返回False
	"""
	# 支持的图片格式
	img_type = ['jpg', 'png', 'gif', 'jpeg', 'bmp', 'tif', 'tga']
	
	# 转换成相对路径
	img_type = list(map(lambda x:os.path.join(img_path, '*.'+x), img_type))
	
	# 获取文件夹下的所有图片名
	img_list = list(map(lambda x:glob.glob(x), img_type))
	imgs = list(chain.from_iterable(img_list))	# 转换成一维列表
        # 按照最后面匹配到的数字排序
        p = re.compile("(\d+)")
        imgs = sorted(imgs, key = lambda s:int(re.findall(p, s)[-1]))

	if not imgs:
		print (u"没有找到需要合成视频的图片！")
		return False
		
	try:
		img_one = cv2.imread(imgs[0])	# 获取第一张图片的大小
	except:
		return False
	# 这里注意大小的表达和VideoWriter参数中的大小相反
	img_size = img_one.shape[1], img_one.shape[0]	
	
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	videoWriter = cv2.VideoWriter(video_name, fourcc, fps, img_size)

	print ("开始写入视频")
	try:
		for imgname in tqdm(imgs):
			frame = cv2.imread(imgname)
			videoWriter.write(frame)
			
		videoWriter.release()
		print ("success saved: " + video_name)
		return True
	except:
		return False


	
def main():
	img_2_video('img/word_cloud', 'a.avi')
	

if __name__ == "__main__":
	main()
