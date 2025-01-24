# Vision.py User Guide

This guide will walk you through the usage of the `vision.py` script, which integrates multiple features such as optical character recognition (OCR), AI-powered text analysis, and text-to-speech functionalities.

---

## Running the Script

1. **Start the Camera Feed**:
   - The script uses OpenCV to capture video from your webcam.
   - To start the script, simply run the Python file in your terminal:
     ```bash
     python vision.py
     ```

2. **Interact with Floating Buttons**:
   - You'll see two floating buttons at the bottom of the camera feed:
     - **Find**: Click on this button to extract text from the image, send it to the AI for analysis, and hear the AI's response.
     - **Image-Quiz**: Click on this button to take a screenshot and send it to the AI for image-based analysis.
   
3. **Text Extraction**:
   - When you click the **Find** button, the script takes a screenshot of the current frame.
   - The OCR function extracts any text from the screenshot and sends it to the AI for analysis.

4. **AI Response**:
   - Once the AI processes the text, the response is converted to speech and played back using **pygame** and **gTTS**.
   - You'll hear the AI's answer or analysis.

---

## Troubleshooting

1. **Camera Issues**:
   - If the camera feed doesn't open, ensure you have the right camera connected and accessible.
   - On Windows, the script uses `cv2.VideoCapture(1, cv2.CAP_DSHOW)`. If you're on Linux, you might need to use `cv2.VideoCapture(1, cv2.CAP_V4L2)`.

2. **OCR Not Working**:
   - If **EasyOCR** fails to initialize, make sure the library is installed correctly.
   - Check that your webcam is properly capturing clear images with sufficient lighting for better OCR accuracy.

3. **API Errors**:
   - If you see errors related to the API, ensure your API key and endpoint are correctly set.
   - Verify the API is accessible and working by testing it with a simple request.

---

## Additional Notes

- **Preprocessing**: The script preprocesses the captured image to make the text more readable before running OCR.
- **Masking**: The buttons are masked out during OCR to prevent the script from reading them as text.
- **Image-Quiz Functionality**: The "Image-Quiz" button is a placeholder in the current version. You can integrate an actual image-based API in this function for future enhancement.

---

## Conclusion

The `vision.py` script is a powerful tool for integrating OCR, AI-based text analysis, and text-to-speech functionalities into your application. By following this guide, you can easily set up and use the script to interact with AI in real-time via your webcam.

Happy coding!
