#!/bin/bash

function merge_pdf(){
    gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress -sOutputFile=passport.pdf passport1.pdf passport2.pdf
}

