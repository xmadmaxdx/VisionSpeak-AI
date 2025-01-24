import cv2
import easyocr
import requests
from gtts import gTTS
import os
import pygame
import numpy as np

# Set up API key and endpoint
API_KEY = "Free-For-YT-Subscribers-@DevsDoCode-WatchFullVideo"
BASE_URL = "https://api.ddc.xiolabs.xyz/v1"

# Initialize EasyOCR reader
try:
    reader = easyocr.Reader(['en'])
except Exception as e:
    print(f"EasyOCR failed to initialize: {e}")
    reader = None

def send_to_api(text):
    """Send text to the AI API and get the response."""
    if not API_KEY or not BASE_URL:
        print("API key or endpoint not configured!")
        return "API not configured."
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "model": "provider-3/gpt-4o-mini",
        "messages": [{"role": "user", "content": text}]
    }
    try:
        response = requests.post(f"{BASE_URL}/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response from API.")
    except Exception as e:
        return f"API request failed: {e}"

def text_to_speech(response_text):
    """Convert AI response to speech and play it automatically."""
    try:
        tts = gTTS(response_text, lang="en")
        tts.save("response.mp3")
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load the MP3 file
        pygame.mixer.music.load("response.mp3")
        
        # Play the MP3 file
        pygame.mixer.music.play()

        # Keep the program running while the audio plays
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Check if music is still playing

    except Exception as e:
        print(f"Text-to-Speech failed: {e}")

def draw_buttons(frame):
    """Draw floating buttons on the camera feed."""
    height, width, _ = frame.shape
    # Button 1: "Find"
    cv2.rectangle(frame, (20, height - 100), (180, height - 50), (0, 255, 0), -1)
    cv2.putText(frame, "Find", (40, height - 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

def check_button_click(x, y, frame_height):
    """Check if the "Find" button was clicked."""
    if 20 <= x <= 180 and frame_height - 100 <= y <= frame_height - 50:
        return "Find"
    return None

def mask_buttons(frame):
    """Mask the button regions so OCR doesn't read them."""
    height, width, _ = frame.shape
    # Mask the "Find" button
    cv2.rectangle(frame, (20, height - 100), (180, height - 50), (0, 0, 0), -1)

def preprocess_image(image):
    """Preprocess the image to make the background black and text white for better readability."""
    image = np.array(image)  # Convert PIL Image to NumPy array
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # Convert to grayscale

    # Invert the grayscale image to make background black and text white
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Sharpen the image to enhance text clarity
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])  # Sharpening kernel
    sharpened_image = cv2.filter2D(binary_image, -1, kernel)

    return sharpened_image

def main():
    # Initialize camera
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # For Windows
    # Or for Linux:
    # cap = cv2.VideoCapture(1, cv2.CAP_V4L2)

    if not cap.isOpened():
        print("Error: Unable to access camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break
        
        # Mask out buttons to prevent OCR from reading them
        mask_buttons(frame)

        # Draw buttons for visual representation
        draw_buttons(frame)
        
        cv2.imshow("Camera Feed", frame)

        # Capture mouse click events
        def mouse_click(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                frame_height, _, _ = frame.shape
                button = check_button_click(x, y, frame_height)
                
                if button == "Find":
                    # Take a screenshot
                    screenshot = frame.copy()
                    cv2.imwrite("screenshot.jpg", screenshot)

                    if reader:
                        # Preprocess the image before OCR
                        preprocessed_image = preprocess_image(screenshot)

                        # Extract text using EasyOCR
                        result = reader.readtext(preprocessed_image)
                        extracted_text = " ".join([detection[1] for detection in result])

                        # Clean or validate the extracted text
                        extracted_text = extracted_text.replace("Find", "").strip()
                        print("Extracted Text:", extracted_text)

                        if extracted_text:
                            # Send cleaned text to AI
                            response = send_to_api(f"Analyze this text and answer questions if applicable: {extracted_text}")
                            print("AI Response:", response)

                            # Text-to-Speech
                            text_to_speech(response)
                        else:
                            print("No meaningful text detected.")
                    else:
                        print("EasyOCR is not available.")

        # Bind the mouse callback
        cv2.setMouseCallback("Camera Feed", mouse_click)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    try:
        cv2.destroyAllWindows()
    except cv2.error as e:
        print(f"Error closing OpenCV windows: {e}")

main()
