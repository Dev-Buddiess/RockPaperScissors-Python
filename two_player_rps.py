import cv2
import mediapipe as mp
import time

# ---------- Setup ----------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

GESTURES = {0: "Rock", 1: "Paper", 2: "Scissors", -1: "Unknown"}

# ---------- Colors (BGR) ----------
P1_COLOR = (34, 139, 34)       # Forest Green
P2_COLOR = (34, 34, 178)       # Crimson Red
COUNTDOWN_OUTLINE = (0, 215, 255)  # Gold Accent
COUNTDOWN_TEXT = (250, 250, 255)   # Snow White
RESULT_COLOR = (0, 215, 255)       # Gold Accent

# ---------- Gesture Detection ----------
def detect_gesture(hand_landmarks):
    tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
    lm = hand_landmarks.landmark

    fingers = []
    for i in range(1, 5):
        tip = lm[tip_ids[i]]
        pip = lm[tip_ids[i] - 2]
        fingers.append(1 if tip.y < pip.y else 0)

    count = sum(fingers)
    thumb_open = abs(lm[4].x - lm[5].x) > 0.04

    if count == 0:
        return 0  # Rock
    if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0:
        return 2  # Scissors
    if count >= 3 or (count >= 2 and thumb_open):
        return 1  # Paper
    return -1

# ---------- Winner Decision ----------
def decide_winner(p1, p2):
    if p1 == p2:
        return "Draw"
    if (p1 == 0 and p2 == 2) or (p1 == 1 and p2 == 0) or (p1 == 2 and p2 == 1):
        return "Player 1"
    return "Player 2"

# ---------- Main Game ----------
cap = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    p1_score = 0
    p2_score = 0
    state = "idle"
    countdown_start = 0
    countdown_secs = 3
    result_text = ""
    show_result_until = 0
    prev_time = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)

        # ---------- Boxes ----------
        p1_box = (0, 0, w // 2, h)
        p2_box = (w // 2, 0, w, h)
        cv2.rectangle(frame, (p1_box[0], p1_box[1]), (p1_box[2], p1_box[3]), P1_COLOR, 2)
        cv2.rectangle(frame, (p2_box[0], p2_box[1]), (p2_box[2], p2_box[3]), P2_COLOR, 2)
        cv2.putText(frame, "Player 1", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, P1_COLOR, 3)
        cv2.putText(frame, "Player 2", (w - 200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, P2_COLOR, 3)

        # ---------- Process Hands ----------
        p1_move, p2_move = -1, -1
        if res.multi_hand_landmarks:
            for handLms in res.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                wrist = handLms.landmark[0]
                wrist_x = int(wrist.x * w)
                gesture = detect_gesture(handLms)

                if wrist_x < w // 2:
                    p1_move = gesture
                else:
                    p2_move = gesture

        # ---------- Show Moves ----------
        p1_text = GESTURES[p1_move] if p1_move in GESTURES else "Unknown"
        p2_text = GESTURES[p2_move] if p2_move in GESTURES else "Unknown"
        cv2.putText(frame, p1_text, (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, P1_COLOR, 2)
        cv2.putText(frame, p2_text, (w - 200, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, P2_COLOR, 2)

        # ---------- Controls ----------
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('s') and state == "idle":
            countdown_start = time.time()
            state = "countdown"

        # ---------- Countdown ----------
        if state == "countdown":
            elapsed = time.time() - countdown_start
            secs_left = max(0, int(countdown_secs - elapsed) + 1)

            box_w, box_h = 50, 50
            center_x, center_y = w // 2, h // 2
            top_left = (center_x - box_w // 2, center_y - box_h // 2)
            bottom_right = (center_x + box_w // 2, center_y + box_h // 2)

            cv2.rectangle(frame, top_left, bottom_right, (0, 0, 0), -1)  # black fill
            cv2.rectangle(frame, top_left, bottom_right, COUNTDOWN_OUTLINE, 2)  # gold outline

            cv2.putText(frame, str(secs_left), (center_x - 15, center_y + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, COUNTDOWN_TEXT, 3)

            if elapsed >= countdown_secs:
                if p1_move == -1 or p2_move == -1:
                    result_text = "Invalid gesture! Show hands clearly inside the boxes."
                else:
                    winner = decide_winner(p1_move, p2_move)
                    if winner == "Player 1":
                        p1_score += 1
                        result_text = f"P1 {GESTURES[p1_move]} beats P2 {GESTURES[p2_move]}"
                    elif winner == "Player 2":
                        p2_score += 1
                        result_text = f"P2 {GESTURES[p2_move]} beats P1 {GESTURES[p1_move]}"
                    else:
                        result_text = f"Draw ({GESTURES[p1_move]})"
                show_result_until = time.time() + 2.0
                state = "show_result"

        # ---------- Show Result ----------
        if state == "show_result":
            cv2.putText(frame, result_text, (w // 2 - 300, h - 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, RESULT_COLOR, 2)
            if time.time() > show_result_until:
                state = "idle"

        # ---------- Scores ----------
        cv2.putText(frame, f"P1 Score: {p1_score}", (50, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, P1_COLOR, 2)
        cv2.putText(frame, f"P2 Score: {p2_score}", (w - 220, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, P2_COLOR, 2)

        # ---------- FPS ----------
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time > 0 else 0
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # ---------- Display ----------
        cv2.namedWindow("Two Player RPS", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Two Player RPS", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Two Player RPS", frame)

    cap.release()
    cv2.destroyAllWindows()
