from PIL import Image
import os


def embed_text(image_path, text, output_path):
    """
    Embed text into an image using a robust steganography method.
    """
    try:
        # Open the image
        img = Image.open(image_path).convert("RGB")
        pixels = list(img.getdata())
        
        # Convert text to binary with a special delimiter
        binary_text = ''.join(format(ord(char), '08b') for char in text) + '00000000'  # Null byte as end marker
        
        # Verify capacity
        if len(binary_text) > len(pixels) * 3:
            raise ValueError("Text is too long to fit in the selected image.")
        
        # Embed binary data into the LSB of image pixels
        new_pixels = []
        idx = 0
        for pixel in pixels:
            r, g, b = pixel
            if idx < len(binary_text):
                r = (r & ~1) | int(binary_text[idx])
                idx += 1
            if idx < len(binary_text):
                g = (g & ~1) | int(binary_text[idx])
                idx += 1
            if idx < len(binary_text):
                b = (b & ~1) | int(binary_text[idx])
                idx += 1
            new_pixels.append((r, g, b))
        
        # Handle remaining pixels (if text is shorter than capacity)
        new_pixels.extend(pixels[len(new_pixels):])
        
        # Save the image with embedded text
        img.putdata(new_pixels)
        img.save(output_path, "PNG")  # PNG preserves pixel values better than JPEG
        print(f"Text successfully embedded into '{output_path}'.")
    except Exception as e:
        print(f"Error during embedding: {e}")


def extract_text(image_path):
    """
    Extract text embedded in an image using a robust steganography method.
    """
    try:
        # Open the image
        img = Image.open(image_path).convert("RGB")
        pixels = list(img.getdata())
        
        # Extract binary data from the LSB of pixel values
        binary_text = ""
        for pixel in pixels:
            r, g, b = pixel
            binary_text += str(r & 1)
            binary_text += str(g & 1)
            binary_text += str(b & 1)
        
        # Group binary data into bytes and decode
        chars = [binary_text[i:i + 8] for i in range(0, len(binary_text), 8)]
        message = ""
        for char in chars:
            if char == '00000000':  # Stop at the null byte (delimiter)
                break
            message += chr(int(char, 2))
        
        print("Extracted hidden text:", message)
        return message
    except Exception as e:
        print(f"Error during extraction: {e}")


def main():
    """
    Main function to interact with the user.
    """
    print("Simple Steganography Tool")
    print("1. Embed text in an image")
    print("2. Extract text from an image")
    choice = input("Choose an option (1/2): ").strip()
    
    if choice == "1":
        # Embed text
        image_path = input("Enter the path to the source image: ").strip()
        if not os.path.exists(image_path):
            print("Image file not found.")
            return
        text = input("Enter the text to hide: ").strip()
        output_path = input("Enter the output file path (e.g., output_image.png): ").strip()
        embed_text(image_path, text, output_path)
    elif choice == "2":
        # Extract text
        image_path = input("Enter the path to the image: ").strip()
        if not os.path.exists(image_path):
            print("Image file not found.")
            return
        extract_text(image_path)
    else:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
