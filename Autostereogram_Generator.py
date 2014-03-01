'''
Created on Oct 1, 2013

@author: Piyush Verma
'''
from PIL import Image
import argparse
from random import randint

DEBUG = 0

def randomStrip(width, height, background = 0):
	strip = Image.new("RGB", (width, height))
	pix = strip.load()
	
	#if background image is provided
	if(background):
		#backgroundRGB = background.convert('RGB')
		backgroundPixels = background.load()
		backgroundWidth, backgroundHeight = background.size
		
		for x in range(width):
			for y in range(height):
				backgroundX = x % backgroundWidth
				backgroundY = y % backgroundHeight
				pix[x, y] = backgroundPixels[backgroundX, backgroundY]
	else:
	
		for x in range(width):
			for y in range(height):
				r = randint(0, 256)
				g = randint(0, 256)
				b = randint(0, 256)
				pix[x, y] = (r, g, b)
		
	return strip
		
	

def autostereogram(depthMap, background = 0):
	depth = Image.open(depthMap).convert('I')
	depthWidth, depthHeight = depth.size;
	
	if background:
		backgroundImage = Image.open(background)		
	
	stripWidth = int(depthWidth/4)
	
	#depth offset
	offset = 0.25
	
	#check if autostereogram generation is possible, i.e. strip width is wide enough for the depth offset.
	if(round(255 * offset) >= stripWidth):
		print("Strip width has to be greater than the depth offset.")
			
	if(background):
		strip = randomStrip(stripWidth, depthHeight, backgroundImage)
	else:
		strip = randomStrip(stripWidth, depthHeight)
		
	if DEBUG:
		strip.show()
		
	output = Image.new('RGB', (depthWidth + stripWidth, depthHeight))
	
	depthPixels = depth.load()
	stripPixels = strip.load()
	outputPixels = output.load()
	
	output.paste(strip, (0, 0))
	
	for y in range(depthHeight):
		for x in range(depthWidth):
			outPixelx = round(x + offset * depthPixels[x, y])
			outputPixels[x + stripWidth, y] = outputPixels[outPixelx, y]
	
	output.save("autostereogram_" + depthMap.split('.')[0] + ".jpg")
	output.show()
			
	

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("depthMap", help="Path of the depth map image file.")
	parser.add_argument("--outFile", help="Output file path with an appropriate Image file format.")
	parser.add_argument("--background", help="Background image file path.")
	args = parser.parse_args()
	
	if(args.background):
		autostereogram(args.depthMap, args.background)
	else:
		autostereogram(args.depthMap)
	
	
	
if __name__ == "__main__":
	main()
	