## Volume control via fingertips
Initial steps & libraries used :

    install pycaw(pip3 install pycaw)
    install mediapipe (pip3 install mediapipe)
    install numpy (pip3 install numpy)
    intsall opencv_python (pip3 install opencv_python)
    
<hr>

This project is for volume control of PC via fingertips. Firstly made a hand detecting & landmarks detecting module(<a href="https://github.com/jainharshit3107/Advance-ComputerVision/blob/master/VolumeControl/HandModulee.py" >HandModulee.py</a>) that returns the landmark positions of hands as a list.<br>
Then moving ahead made a <a href="https://github.com/jainharshit3107/Advance-ComputerVision/blob/master/VolumeControl/VolumeControl.py" >volumecontrol.py</a>, choosed thumb_tip, Index-finger_tip for controling the volume, the lower the gap b/w thumb and index finger lesser will be the volume and vice-versa.<br>
<b>pycaw</b>(https://github.com/AndreMiras/pycaw) library for - Audio controlling in Windows (py3)<br> Numpy Library - <b>np.interp</b>(https://numpy.org/doc/stable/reference/generated/numpy.interp.html) used to return a standard number between our Handrange and Max&Min vol range.<br>
<br>
<b>Reference & Special thanks - </b> <br>
Google Mediapipe Hand tracking - https://google.github.io/mediapipe/solutions/hands <br>
Murtaza's Workshop youtube - https://www.youtube.com/channel/UCYUjYU5FveRAscQ8V21w81A

