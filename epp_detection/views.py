import cv2
from django.shortcuts import render

from epp_detection.services import check_EPP_in_image


# Create your views here.




def test(request):
    if request.method == "POST":

        check_EPP_in_image()
        return