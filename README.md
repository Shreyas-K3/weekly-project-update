# Weekly Project Update App

A minimal, secure-enough project update dashboard built with Streamlit, SQLite, and GitHub.

## 🚀 Quick Start

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the App:**
    ```bash
    streamlit run streamlit_app.py
    ```

3.  **Default Admin Flow:**
    * Open the app.
    * Open Sidebar (top left arrow) -> Select "Admin Panel".
    * Create a new project (e.g., Code: `TEST001`, Name: `Alpha Tower`).
    * Click "Update Project".

4.  **Client Flow:**
    * Switch Sidebar to "Client View".
    * Enter Name and Project Code (`TEST001`).
    * View Dashboard & Submit Comments.

## 📂 Folder Structure
* `app/`: Core logic (Client, Admin, DB, Styling).
* `data/`: Stores `app.db` (SQLite). **Note:** On Streamlit Cloud, this file is ephemeral unless you use third-party storage, but persists between soft reboots.
* `streamlit_app.py`: Main entry point.

## 🎨 Styling
* **Font:** Expects `AvantGarde.woff2` in `app/assets/fonts/`.
* **Theme:** Enforced Dark Mode with Red/Black/White brand colors.

## ☁️ Deployment (Streamlit Cloud)
1.  Push this repo to GitHub.
2.  Go to [Streamlit Cloud](https://streamlit.io/cloud).
3.  New App -> Select Repository.
4.  Main file: `streamlit_app.py`.
5.  Deploy!

## ⚠️ Notes
* **Project Code:** Stored in plain text. Do not use for highly sensitive passwords.
* **Real-time:** Admin page polls every 10s if toggle is active.
* **WebSocket Upgrade:** Search code for `TODO` to see where to implement websockets for true real-time.
