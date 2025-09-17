# RockPaperScissors-Python

A two-player Rock Paper Scissors game implemented in Python using OpenCV and MediaPipe for hand gesture recognition.

## 👥 Team Members
- [@yaswanth-gajula](https://github.com/SuggulaDharanipriya)  
- [@SuggulaDharanipriya](https://github.com/yaswanth-gajula)

## Features and Functionality

*   **Real-time Hand Gesture Recognition:** Uses MediaPipe to detect hand landmarks and recognize gestures (Rock, Paper, Scissors).
*   **Two-Player Mode:**  Detects gestures from two players using the webcam.
*   **Scoring:** Keeps track of the scores for both players.
*   **Countdown Timer:** Implements a countdown timer before each round to allow players to prepare their gestures.
*   **Winner Determination:**  Determines the winner of each round based on the classic Rock Paper Scissors rules.
*   **Visual Feedback:** Provides visual feedback through OpenCV, including hand landmarks, player boxes, countdown timer, results, and scores.
*   **FPS Display:** Shows the frames per second (FPS) for performance monitoring.
*   **Clear Instructions:** Prompts players to show their hands clearly inside designated boxes.

## Technology Stack

*   **Python 3.20.0**
*   **OpenCV (cv2):**  For video capture and display.  Install with: `pip install opencv-python`
*   **MediaPipe:** For hand tracking and gesture recognition. Install with: `pip install mediapipe`
*   **Time:** For managing the countdown and result display duration.

## Prerequisites

Before running the game, ensure you have the following installed:

*   **Python:**  Version 3.6 or higher.
*   **Webcam:** A working webcam connected to your computer.

## Installation Instructions

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/yaswanth-gajula/RockPaperScissors-Python.git
    cd RockPaperScissors-Python
    ```

2.  **Install the required Python packages:**

    ```bash
    pip install opencv-python mediapipe
    ```

## Usage Guide

1.  **Run the `two_player_rps.py` script:**

    ```bash
    python two_player_rps.py
    ```

2.  **Game Play:**

    *   The game will open a window displaying the webcam feed.
    *   Two boxes are displayed, one for each player.
    *   Press the `s` key to start a round. A countdown timer will appear.
    *   During the countdown, each player should make a Rock, Paper, or Scissors gesture with their hand inside their respective box.
    *   After the countdown, the game will determine the winner and display the result and updated scores.
    *   If the gesture is not detected, "Unknown" is shown, and if it's invalid during the countdown, a message is displayed.
    *   Press the `q` key to quit the game.

## License Information

No license specified. All rights reserved.

## Contact/Support Information

For questions or support, please contact 2300030194cseh@gmail.com
