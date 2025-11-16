import os

VID1 = os.path.join('vid1.mp4')
VID2 = os.path.join('vid2.mp4')

print('vid1 exists:', os.path.exists(VID1))
print('vid2 exists:', os.path.exists(VID2))

try:
    from backend.utils.blink_rate_detector import detect_blink_rate
except Exception as e:
    print('Failed to import blink detector:', e)
    raise

if os.path.exists(VID1):
    print('\nRunning blink detection on vid1.mp4...')
    res1 = detect_blink_rate(VID1)
    print('Result vid1:', res1)
else:
    print('vid1.mp4 not found, skipping')

if os.path.exists(VID2):
    print('\nRunning blink detection on vid2.mp4...')
    res2 = detect_blink_rate(VID2)
    print('Result vid2:', res2)
else:
    print('vid2.mp4 not found, skipping')
