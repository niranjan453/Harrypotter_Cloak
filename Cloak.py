import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

for _ in range(15):
    _ = cap.read()

bg_frames = []

for _ in range(30):
    ok, fr = cap.read()
    if not ok:
        continue
    fr = cv2.flip(fr, 1)
    bg_frames.append(fr)

if not bg_frames:
    raise RuntimeError("Could not capture background frames.")

background = np.median(np.stack(bg_frames, axis=0), axis=0).astype(np.uint8)

print("[i] Invisibility (use captured bg)")
print("[c] Custom image bg")
print("[v] Video bg")

mode = input("Choose mode (i/c/v): ").strip().lower()

bg_img = None
bg_video = None

if mode == 'c':
    path = input("Path to bg image: ").strip()
    bg_img = cv2.imread(path)
    if bg_img is None:
        raise ValueError("Could not read image at: " + path)

elif mode == 'v':
    path = input("Path to bg video (eg .mp4): ").strip()
    bg_video = cv2.VideoCapture(path)
    if not bg_video.isOpened():
        raise ValueError("Could not open the video at: " + path)

kernel = np.ones((3, 3), np.uint8)

lower_red1 = np.array([0, 120, 70], dtype=np.uint8)
upper_red1 = np.array([10, 255, 255], dtype=np.uint8)
lower_red2 = np.array([170, 120, 70], dtype=np.uint8)
upper_red2 = np.array([180, 255, 255], dtype=np.uint8)

print("Controls: [b]=recapture background [i]=invisibility [c]=image [v]=video [ESC]=quit")

while True:
    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

    donor = background.copy()

    if mode == 'c':
        donor = cv2.resize(bg_img, (w, h))
    elif mode == 'v':
        ok_bg, bgf = bg_video.read()
        if not ok_bg:
            bg_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok_bg, bgf = bg_video.read()
        donor = cv2.resize(bgf, (w, h))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=1)

    inv_mask = cv2.bitwise_not(mask)

    cloak_region = cv2.bitwise_and(donor, donor, mask=mask)
    live_region = cv2.bitwise_and(frame, frame, mask=inv_mask)
    out = cv2.addWeighted(cloak_region, 1.0, live_region, 1.0, 0.0)

    cv2.putText(out, f"Mode {'Invisibility' if mode=='i' else 'Image' if mode=='c' else 'Video'}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("CLOAK+", out)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

    if key == ord('b'):
        tmp = []
        for _ in range(20):
            ok2, fr2 = cap.read()
            if ok2:
                tmp.append(cv2.flip(fr2, 1))
        if tmp:
            background = np.median(np.stack(tmp, axis=0), axis=0).astype(np.uint8)
            print("Background Recaptured")

    if key == ord('i'):
        mode = 'i'
        print("Mode set to: Invisibility")

    if key == ord('c'):
        mode = 'c'
        print("Mode set to: Custom Image")

    if key == ord('v'):
        mode = 'v'
        print("Mode set to: Video")

cap.release()
if bg_video is not None:
    bg_video.release()
cv2.destroyAllWindows()