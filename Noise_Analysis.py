import numpy as np # Koristimo numpy biblioteku za namistanje opacity slike 
import cv2 # Koristimo opencv biblioteku za prikaz i rad sa slikama

mod_slike = 1  # Ocemo li sliku koristiti u grayscaleu ili sa bojama, 0 = grayscale, 1 = boje
image = cv2.imread("slika.jpg",mod_slike) # Ucitavamo nasu sliku sa zadanim modom

to_equalize_histogram = 0 # Ako zelimo izjednacit histogram, 0 = ne, 1 = da (Slika mora biti grayscale da bi se izjednacio histogram)

if to_equalize_histogram == 1 and mod_slike == 1:
    print("\n\n\nSlika mora biti grayscale da bi se izjednacio histogram, promijnei mod_slike u 0\n\n\n")

if to_equalize_histogram == 1:
    image = cv2.equalizeHist(image)

noise_amplitude = 3 # Odreduje kolicinu median blurra, zbog ogranicenosti medianBlur funkcije ovo moze biti samo neparni integer
image_median = cv2.medianBlur(image, noise_amplitude) # Stvaramo sliku sa nasim median filterom (ovaj filter skida noise sa slike)
image_sound = image - image_median # Posto je nama cilj dobiti samo noise od slike uzimamo nasu sliku te joj oduzimamo sliku sa median filterom

# Racunamo parametre skaliranja slike
scale_percent = 30 # Postotak od originalne slike 
width = int(image_sound.shape[1] * scale_percent / 100)
height = int(image_sound.shape[0] * scale_percent / 100)
dim = (width, height) # Nove dimenzije slike 

# Skaliramo fotografiju na odredenu vrijednost
image_resized  = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
sound_resized = cv2.resize(image_sound, dim, interpolation = cv2.INTER_AREA)

# Konvertiramo u 32-bitne da je lakse racunati opacity jer vrijednosti idu od 0 - 1
image = np.array(image_resized, dtype=np.float)
image /= 255.0
image_sound = np.array(sound_resized, dtype=np.float)
image_sound /= 255.0
 
opacity = 1 # Sa ovim odredujemo koliko ce biti opacity, od 0 - 1
output = ((image * (1-opacity)) + (image_sound * opacity))

# Ispis originalne i modificirane slike na ekran
cv2.imshow("Original", image_resized)
cv2.imshow("Noise analysis slika", output)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("modificirana_slika.jpg", output)

