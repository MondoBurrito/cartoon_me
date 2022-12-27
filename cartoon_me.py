# Built-in libraries
import os  # Interact with the operating system.
import sys

# 3rd party libraries
import cv2  # Image processing.
import easygui  # Open a filebox.
import imageio  # Read image stored at a perticular path.
import matplotlib.pyplot as plt  # Form the plot of the image.
import numpy  # Store image.
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import filedialog
from tkinter import *


def upload():
    """Open a filebox to choose a file and store the file path as a string."""
    image_path = easygui.fileopenbox()
    # Pass that file path string into cartoon_me function.
    cartoon_me(image_path)


def cartoon_me(image_path):
    # Read the image file path chosen in upload().
    # imread stores images as numbers.
    original_image = cv2.imread(image_path)
    # Image is read as a numpy array. Cell values depict RGB vals of a pixel.
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    # print(original_image)  # Confirm mumpy array.

    # Weed out non-image files.
    if original_image is None:
        print("Can not find an image. Please choose an image file.")
        sys.exit()

    # Image is resized after each transformation in order to keep all images
    # at a similar scale.
    resized_1 = cv2.resize(original_image, (960, 540))

    # Convert image to greyscale.
    grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    resized_2 = cv2.resize(grayscale_image, (960, 540))
    # Plot grayscale image.
    plt.imshow(resized_2, cmap="gray")

    # Apply a median blur to smooth out the image.
    smooth_grayscale_image = cv2.medianBlur(grayscale_image, 5)
    resized_3 = cv2.resize(smooth_grayscale_image, (960, 540))
    # Plot smoothed image.
    plt.imshow(resized_3, cmap="gray")

    # Retrieve the edges of the image by using threshold.
    get_edge = cv2.adaptiveThreshold(
        smooth_grayscale_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )
    resized_4 = cv2.resize(color_image, (960, 540))
    plt.imshow(resized_4, cmap="gray")

    # Apply filter to remove noise and keep edge sharp.
    color_image = cv2.bilateralFilter(original_image, 9, 300, 300)
    resized_5 = cv2.resize(color_image, (960, 540))
    plt.imshow(resized_5, cmap="gray")

    # Mask edges.
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=get_edge)
    resized_6 = cv2.resize(cartoon_image, (960, 540))
    plt.imshow(resized_6, cmap="gray")

    # Plot the transition.
    images = [resized_1, resized_2, resized_3, resized_4, resized_5]
    fig, axes = plt.subplots(
        3,
        2,
        figsize=(8, 8),
        subplot_kw={"xticks": [], "yticks": []},
        gridspec_kw=dict(hspace=0.1, wspace=0.1),
    )
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap="gray")

    # Make the save button in the main window.
    save_1 = Button(
        top,
        text="Save image",
        command=lambda: save(image_path, resized_6),
        padx=30,
        pady=5,
    )
    save_1.configure(
        background="#364156", foreground="white", font=("calibri", 10, "bold")
    )
    save_1.pack(side=TOP, pady=50)


def save(resized_6, image_path):
    # Save image using imwrite().
    new_name = "cartoon_me_image"
    path_1 = os.path.dirname(image_path)
    extension = os.path.splitext(image_path)[1]
    path = os.path.join(path_1, new_name + extension)
    cv2.imwrite(path, cv2.cvtColor(resized_6, cv2.COLOR_RGB2BGR))
    I = f"Image saves by name {new_name} at {path}"
    tk.messagebox.showinfo(title=None, message=I)


# Make the main window.
top = tk.Tk()
top.geometry("400x400")
top.title("Cartoon Me")
top.configure(background="white")
label = Label(top, background="#CDCDCD", font=("calibri", 20, "bold"))


# Make the "Cartoon Me" button in the main window.
upload = Button(top, text="Cartoon me", command=upload, padx=10, pady=5)
upload.configure(background="#364156", foreground="white", font=("calibri", 10, "bold"))
upload.pack(side=TOP, pady=50)


top.mainloop()
