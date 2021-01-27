
import cv2

def diff_rect(img1, img2, pos=None):
    """find counters include pos in differences between img1 & img2 (cv2 images)"""
    diff = cv2.absdiff(img1, img2)
    diff = cv2.GaussianBlur(diff, (3, 3), 0)
    edges = cv2.Canny(diff, 100, 200)
    _, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return None
    contours.sort(key=lambda c: len(c))
    # no pos provide, just return the largest different area rect
    if pos is None:
        cnt = contours[-1]
        x0, y0, w, h = cv2.boundingRect(cnt)
        x1, y1 = x0+w, y0+h
        return (x0, y0, x1, y1)
    # else the rect should contain the pos
    x, y = pos
    for i in range(len(contours)):
        cnt = contours[-1-i]
        x0, y0, w, h = cv2.boundingRect(cnt)
        x1, y1 = x0+w, y0+h
        if x0 <= x <= x1 and y0 <= y <= y1:
            return (x0, y0, x1, y1) 