# Architecture 101: How Project Insight Works 🧠

Use this guide if you are confused about how your code connects to the rest of the project.

## The "Hub and Spoke" Model

Imagine our project is a bicycle wheel.

-   **The Hub (Center):** This is our SQLite Database (`data/database.sqlite`).
-   **The Spokes:** These are the Squads (Vision, NLP, Web).

## How Data Moves

### The Vision Squad (Producer)

-   **Input:** Camera Feed.
-   **Process:** AI detects faces and calculates "Engagement Score".
-   **Output:** Every 1 second, it runs an SQL command:
    ```sql
    INSERT INTO metrics (focused_count) VALUES (20)
    ```

### The NLP Squad (Producer)

-   **Input:** Microphone.
-   **Process:** AI converts speech to text.
-   **Output:** Every sentence, it runs an SQL command:
    ```sql
    INSERT INTO transcripts (text) VALUES ("Hello World")
    ```

### The Web Squad (Consumer)

-   **Input:** The SQLite Database.
-   **Process:** The dashboard asks the DB: "Give me the last 10 rows."
-   **Output:** It draws a graph on the screen.

## Why do we do this?

Because Vision and Audio run at different speeds.

-   Vision runs fast (15 times per second).
-   Audio runs slow (1 sentence every 5 seconds).

If we connected them directly, the slow Audio would make the Camera lag. By using the Database in the middle, they can run at their own speeds without waiting for each other!

## Folder Explanation

-   `src/vision`: Only touch this if you are in Squad A.
-   `src/nlp`: Only touch this if you are in Squad B.
-   `src/robotics`: This code talks to the Arduino.
-   `main.py`: The boss script. It starts the Vision process and the NLP process separately (using multiprocessing).
