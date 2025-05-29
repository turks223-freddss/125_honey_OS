from PIL import Image, ImageTk

def resize_icon(path, size=(32, 32)):
  img = Image.open(path)
  img = img.resize(size, Image.Resampling.LANCZOS)
  return ImageTk.PhotoImage(img)