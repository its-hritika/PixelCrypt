from PIL import Image
import piexif

def hide_text(image_path, text, output_path):
    """
    Hide text in an image while preserving metadata (if present).
    """
    try:
        # Open the image
        img = Image.open(image_path)
        img = img.convert("RGB")  # Ensure the image is in RGB mode
        
        # Load EXIF data, if available
        exif_data = img.info.get("exif", None)
        if exif_data:
            exif_data = piexif.load(exif_data)
        else:
            exif_data = {}  # Handle cases with no EXIF metadata

        # Convert text to binary and add a delimiter to mark the end of the text
        binary_text = ''.join(format(ord(char), '08b') for char in text) + '11111111'  # End marker

        # Hide the binary text in the LSB of the image's pixel values
        pixels = list(img.getdata())
        new_pixels = []
        idx = 0
        for pixel in pixels:
            r, g, b = pixel
            if idx < len(binary_text):
                r = (r & ~1) | int(binary_text[idx])  # Modify LSB of red channel
                idx += 1
            if idx < len(binary_text):
                g = (g & ~1) | int(binary_text[idx])  # Modify LSB of green channel
                idx += 1
            if idx < len(binary_text):
                b = (b & ~1) | int(binary_text[idx])  # Modify LSB of blue channel
                idx += 1
            new_pixels.append((r, g, b))

        # Add remaining pixels if text is shorter than image capacity
        new_pixels.extend(pixels[len(new_pixels):])

        # Save the new image with the modified pixels and original metadata
        img.putdata(new_pixels)
        if exif_data:
            exif_bytes = piexif.dump(exif_data)
            img.save(output_path, "jpeg", exif=exif_bytes)
        else:
            img.save(output_path, "jpeg")
        
        print(f"Text successfully hidden in '{output_path}' with metadata preserved.")
    except Exception as e:
        print(f"Error hiding text: {e}")

def extract_text(image_path):
    """
    Extract hidden text from an image.
    """
    try:
        # Open the image
        img = Image.open(image_path)
        pixels = list(img.getdata())

        # Extract binary data from the LSB of the pixel values
        binary_text = ""
        for pixel in pixels:
            r, g, b = pixel
            binary_text += str(r & 1)
            binary_text += str(g & 1)
            binary_text += str(b & 1)

        # Split binary data into 8-bit chunks and convert to characters
        chars = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]
        message = ""
        for char in chars:
            if char == '11111111':  # Stop at the delimiter
                break
            message += chr(int(char, 2))

        print("Hidden message:", message)
    except Exception as e:
        print(f"Error extracting text: {e}")

def main():
    """
    Main function to provide a menu for user interaction.
    """
    print("Simple Steganography Tool")
    print("1. Hide text in an image")
    print("2. Extract hidden text from an image")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        # Hide text
        image_path = input("Enter the path to the image: ")
        text = input("Enter the text to hide: ")
        output_path = input("Enter the output image path (e.g., output_image.jpg): ")
        hide_text(image_path, text, output_path)
    elif choice == "2":
        # Extract text
        image_path = input("Enter the path to the image: ")
        extract_text(image_path)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
