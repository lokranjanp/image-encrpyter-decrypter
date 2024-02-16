from encrypter import *

root = Tk()
app = ImageEncrypterDecrypter(root)

print(app.image_path)

root.geometry("400x600")
root.mainloop()
