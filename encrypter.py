import cv2
import numpy as np
from tkinter import Tk, Label, Button, Canvas, filedialog
from PIL import Image, ImageTk


class ImageEncrypterDecrypter:

    def __init__(self, root):
        # Initializing the GUI components
        self.root = root
        self.root.title("Image Encryption/Decryption")

        self.label = Label(root, text="Select an Image:")
        self.label.pack(pady=10)

        self.canvas = Canvas(root, width=600, height=300)
        self.canvas.pack(pady = 10)

        self.upload_button = Button(root, text="Upload Image", command=self.load_image)
        self.upload_button.pack(pady=10)

        self.encrypt_button = Button(root, text="Encrypt", command=self.encrypt_image)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = Button(root, text="Decrypt", command=self.decrypt_image)
        self.decrypt_button.pack(pady=10)

        self.save_button = Button(root, text="Save", command=self.save_image)
        self.save_button.pack(pady=10)

        self.image_path = None
        self.original_image = None
        self.encrypted_image = None
        self.encryption_key = None


    def load_image(self):
        """This function can load an image from the hardware to the application"""
        try:
            # Open a file dialog to select an image
            file_path = filedialog.askopenfilename()
            if file_path:
                self.image_path = file_path

                # Load and convert the image to grayscale
                original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                original_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2RGB)

                # Display the original image and save a reference
                self.original_image = original_image
                self.display_image(original_image)

        except Exception as e:
            self.display_error("Error loading image: " + str(e))


    def encrypt_image(self):
        """This function encrypts a image using a random key generator"""
        try:
            if self.image_path and self.original_image is not None:

                key = self.generate_key(self.original_image.shape)
                encrypted_image = self.encrypt(self.original_image, key)

                self.display_image(encrypted_image)
                self.encrypted_image = encrypted_image
                self.encryption_key = key

        except Exception as e:
            self.display_error("Error encrypting image: " + str(e))


    def decrypt_image(self):
        """This function decrypts the previously encrypted image using a stored key value"""

        try:
            if self.encrypted_image is not None and self.encryption_key is not None:
                # Decrypting the image using the stored key
                decrypted_image = self.decrypt(self.encrypted_image, self.encryption_key)

                # Display the decrypted image
                self.display_image(decrypted_image)

        except Exception as e:
            self.display_error("Error decrypting image: " + str(e))


    def save_image(self):
        """This function allows user to save the image post encryption/decryption"""

        try:
            if self.encrypted_image is not None:
                # Open a file dialog to save the encrypted image
                save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                           filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
                if save_path:
                    # Save the encrypted image
                    cv2.imwrite(save_path, self.encrypted_image)

        except Exception as e:
            self.display_error("Error saving image: " + str(e))


    def encrypt(self, image, key):
        """The loaded image is encrypted using this function"""

        # Perform pixel-wise encryption using a key
        encrypted_image = np.copy(image)

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                encrypted_image[i, j] = (image[i, j] + key[i % len(key)]) % 256

        return encrypted_image


    def decrypt(self, encrypted_image, key):
        """The selected image is decrypted using this function"""

        # Perform pixel-wise decryption using the same key
        decrypted_image = np.copy(encrypted_image)

        for i in range(encrypted_image.shape[0]):
            for j in range(encrypted_image.shape[1]):
                decrypted_image[i, j] = (encrypted_image[i, j] - key[i % len(key)]) % 256

        return decrypted_image


    def generate_key(self, shape):
        """This function generates a pseudo-random number to encrypt the image"""

        # Generate a key based on the shape of the image
        key = np.random.randint(0, 256, shape[0])
        return key


    def display_error(self, message):
        # Display error messages
        print("Error: " + message)


    def display_image(self, image):
        # Displaying the processed image
        img = Image.fromarray(image)
        img.thumbnail((300, 300))
        img = ImageTk.PhotoImage(img)

        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        x_center = (canvas_width - img.width()) // 2
        y_center = (canvas_height - img.height()) // 2

        # Displaying the image at the center
        self.canvas.create_image(x_center, y_center, anchor="nw", image=img)
        self.canvas.image = img

