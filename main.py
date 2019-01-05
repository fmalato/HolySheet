import binarizer as bin
import cv2 as cv
import stringUtils


bible = 'Muenchen'
binar = bin.Binarizer(bible)

#binar.binarize()
#binar.rotate('image.png')
#img = cv.imread('result.png')
#cropped = cv.imread('cropped.png')
#binar.calimero(img, cropped)

groundTruth = open("genesis1-20.txt", "r")
lines = groundTruth.readlines()

dictionary = stringUtils.getWordsCounterDict(lines)

for x in range(14, 62, 1):
    image = cv.imread('GenesisPages/old/Muenchen_binarized/Gut-0{x}.png'.format(x=x))
    binar.findRotationAngle(image)

# Problemi patologici
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-014.jpg', 14, "_P0_C0", "_P0_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-015.jpg', 15, "_P1_C0", "_P1_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-016.jpg', 16, "_P2_C0", "_P2_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-017.jpg', 17, "_P3_C0", "_P3_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-018.jpg', 18, "_P4_C0", "_P4_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-019.jpg', 19, "_P5_C0", "_P5_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-020.jpg', 20, "_P6_C0", "_P6_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-021.jpg', 21, "_P7_C0", "_P7_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-022.jpg', 22, "_P8_C0", "_P8_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-023.jpg', 23, "_P9_C0", "_P9_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-024.jpg', 24, "_P10_C0", "_P10_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-025.jpg', 25, "_P11_C0", "_P11_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-026.jpg', 26, "_P12_C0", "_P12_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-027.jpg', 27, "_P13_C0", "_P13_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-028.jpg', 28, "_P14_C0", "_P14_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-029.jpg', 29, "_P15_C0", "_P15_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-030.jpg', 30, "_P16_C0", "_P16_C1", dictionary)

# Segmenta male le parole...
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-031.jpg', 31, "_P17_C0", "_P17_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-032.jpg', 32, "_P18_C0", "_P18_C1", dictionary)

# Bene
#binar.linesCropping('GenesisPages/old/Muenchen/Gut-033.jpg', 33, "_P19_C0", "_P19_C1", dictionary)

