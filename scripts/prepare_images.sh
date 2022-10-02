#!/bin/bash
mkdir images/256
mkdir images/512
mogrify -format jpg -path images/512 outputs/*.png
mogrify -format jpg -path images/256 -thumbnail 256x256 outputs/*.png