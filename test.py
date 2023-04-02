import os

files = os.listdir("C:/Users/oskar/OneDrive - TUNI.fi/Ohjelmointi/Ohjelmointi 1/Tehtävät/13_Graafiset_kayttoliittymat/chess/pieces")
print(files)

for i in files:
    os.rename("C:/Users/oskar/OneDrive - TUNI.fi/Ohjelmointi/Ohjelmointi 1/Tehtävät/13_Graafiset_kayttoliittymat/chess/pieces/" + i, i.replace("_png_256px",""))