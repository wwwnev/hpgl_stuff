import cv2
import numpy as np
import sys
DIM_MAX_X = 10365
DIM_MAX_Y = 7692

#nb d'unite (du plotter) entre les lignes)
interL_plot = 20

#on met l'image en gris et on la flip pour que sont 0,0 soit le 0,0 du plotter
#pcq les arrays numpy partent d'en haut (comme une bonne vieille matrice) mais le plotter
# cest comme un espace 2D avec des axes X et Y
im_gray = np.array(cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE))
(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
im_bw = cv2.flip(im_bw,0)

dim = np.shape(im_bw)
dimx = dim[1]
dimy = dim[0]

#true si l'image est plus longue que dimensions max, false sinon
switch = dimx / dimy > DIM_MAX_X / DIM_MAX_Y

#calcul du ratio de pixel a coordonnee plotter
r = 5
if switch:
    r = int(DIM_MAX_X / dimx)
else:
    r = int(DIM_MAX_Y / dimy)

#distance entre chaque ligne sampled (du bitmap evidemment)
interL_yimg = int(dimy / DIM_MAX_Y * interL_plot)

cv2.imshow('img',im_bw)
cv2.waitKey(0)
cv2.destroyAllWindows()

#ecrivons du hpgl !!
f = open(sys.argv[1].split('.')[0] + '.hpgl', 'w')
f.write('IN;SP1;PU0,0;')

draw = False

for i in range(0,dimy,interL_yimg):
    for j in range(dimx):
        #blanc a noir
        if not(draw) and im_bw[i][j] == 0: 
            f.write('PU'+str(j*r)+','+str(i*r)+';PD'+str(j*r)+','+str(i*r)+';\n')
            draw = True
        #noir a noir
        
        #noir a blanc
        if draw and im_bw[i][j] != 0:
            f.write('PD'+str(j*r)+','+str(i*r)+';PU'+str(j*r)+','+str(i*r)+';\n')
            draw = False
        #blanc a blanc
    if draw:
        f.write('PD'+str(dimx*r-1)+','+str(i*r)+';PU'+str(dimx*r-1)+','+str(i*r)+';\n')
        draw = False
f.write('SP0;PU0,0;IN;')
f.close()


