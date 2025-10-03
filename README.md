This project recreates the Harry Potter invisibility cloak effect using Python + OpenCV. It detects a red cloak in real-time and replaces it with:

The captured background (classic invisibility effect)

A custom image background

A background video

You can switch between these modes while the program is running.

✨ Features

Real-time webcam feed processing

Automatic background capture using the median of multiple frames

Smooth cloak masking with morphological operations

Dynamic mode switching during runtime

Keyboard controls for recapturing background or changing modes

⚙️ Requirements

Python

OpenCV

NumPy

Install dependencies:

pip install opencv-python numpy


Run the script:

python Cloak.py


Wear a red cloth in front of your webcam. Choose mode at startup:

i → Invisibility (captured background)

c → Custom image background

v → Video background

Runtime controls:

[b] → Recapture background

[i] → Switch to invisibility mode

[c] → Switch to custom image mode

[v] → Switch to video mode

[ESC] → Exit

💡 Future Improvements

GUI for mode selection

Dynamic cloak color detection

Export invisibility video recordings

This project demonstrates computer vision techniques, including background subtraction, masking, and real-time video processing, while creating a fun and interactive experience.
