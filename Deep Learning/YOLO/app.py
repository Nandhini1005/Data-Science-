import streamlit as st
import cv2
import tempfile
from PIL import Image
from streamlit_option_menu import option_menu

from detector import detect_image, detect_video
from auth import register_user, login_user


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Surveillance",
    page_icon="🎥",
    layout="wide"
)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MENU ----------------
selected = option_menu(
    menu_title="Smart Surveillance",
    options=["Home", "Login", "Register", "About"],
    icons=["house", "box-arrow-in-right",
           "person-plus", "info-circle"],
    menu_icon="camera-video",
    default_index=0,
    orientation="horizontal"
)

# =====================================================
# REGISTER PAGE
# =====================================================
if selected == "Register":

    st.title("📝 Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):

        if username and password:
            register_user(username, password)
            st.success("Registration Successful ✅")
        else:
            st.warning("Fill all fields")

# =====================================================
# LOGIN PAGE
# =====================================================
elif selected == "Login":

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = login_user(username, password)

        if user:
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
        else:
            st.error("Invalid Username or Password")

# =====================================================
# ABOUT PAGE
# =====================================================
elif selected == "About":

    st.title("ℹ About")

    st.write("""
    Smart Surveillance System using YOLOv8.

    Features:
    - Person Detection
    - Vehicle Detection
    - Security Monitoring
    - Image Detection
    - Video Detection
    - Webcam Detection
    """)

# =====================================================
# HOME PAGE
# =====================================================
elif selected == "Home":

    st.title("🎥 Smart Surveillance Dashboard")

    if not st.session_state.logged_in:
        st.warning("Please login first.")
        st.stop()

    mode = st.selectbox(
        "Choose Detection Mode",
        [
            "Image Detection",
            "Video Detection",
            "Webcam Detection"
        ]
    )

    # ---------------- IMAGE ----------------
    if mode == "Image Detection":

        uploaded_file = st.file_uploader(
            "Upload Image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:

            image = Image.open(uploaded_file)

            st.image(image, caption="Uploaded Image")

            result_image, df = detect_image(image)

            st.image(
                result_image,
                caption="Detection Result",
                use_container_width=True
            )

            st.subheader("Detection Analytics")
            st.dataframe(df)

            if not df.empty:
                st.bar_chart(df["Object"].value_counts())

    # ---------------- VIDEO ----------------
    elif mode == "Video Detection":

        uploaded_video = st.file_uploader(
            "Upload Video",
            type=["mp4", "avi", "mov"]
        )

        if uploaded_video is not None:

            temp_file = tempfile.NamedTemporaryFile(
                delete=False
            )

            temp_file.write(uploaded_video.read())

            cap = cv2.VideoCapture(temp_file.name)

            frame_placeholder = st.empty()

            while cap.isOpened():

                ret, frame = cap.read()

                if not ret:
                    break

                frame = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                result_frame, _ = detect_video(frame)

                frame_placeholder.image(
                    result_frame,
                    channels="RGB",
                    use_container_width=True
                )

            cap.release()

    # ---------------- WEBCAM ----------------
    elif mode == "Webcam Detection":

        run = st.checkbox("Start Webcam")

        frame_window = st.image([])

        camera = cv2.VideoCapture(0)

        while run:

            success, frame = camera.read()

            if not success:
                st.error("Webcam not detected")
                break

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            result_frame, _ = detect_video(frame)

            frame_window.image(
                result_frame,
                channels="RGB"
            )

        camera.release()