# virtual-Mouse-OpenCV
A setup to control mouse using hand gestures

Hey, there
To use this project simply calculate HSV value of tracking colours (initially seted to track yellow, blue and red). To get HSV value use HSV_Calc.py file and repeatedly adjust HSV value to get black and white background (Black->Non tracking area and White->Tracking area) using following keys:-
a->decreases MIN Hue vale (H)
q->increases MIN Hue value (H)
w->increase MIN Saturation (S)
s->decreases MIN Saturation (S)
e->increases MIN Value (V)
d->decreases MIN Value (V)
r->increases MAX Hue (H)
f->decreases MAX Hue  (S)
t->increases MAX Saturation (S)
g->decreases MAX Saturation (S)
y->increases MAX Value (V)
h->decreases MAX Value (V)
After getting Upper and Lower HSV values using adjustments plug the Upper and Lower values of numpy arrays in source code of main.py of numpy arrays variable.
Now run main.py and do the following to see mouse in action:
move trackers together in camera frame:->Moves mouse in xy plane
touch two trackers together->One causes left or right click and vice-versa for the other one
Messages shall be raised accordingly to the action.

PLZ install numpy and open-cv python libraries using pip before running both the python files
HAPPY CODING
