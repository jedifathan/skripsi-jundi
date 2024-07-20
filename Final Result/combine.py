from PIL import Image

def combine_images(image1_path, image2_path, output_path):
    # Open the images
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    # Get the heights of the images
    height1 = img1.height
    height2 = img2.height

    # Use the maximum height for the combined image
    max_height = max(height1, height2)

    # Create a new image with the combined width and max height
    combined_width = img1.width + img2.width
    combined_image = Image.new('RGB', (combined_width, max_height))

    # Paste the first image
    combined_image.paste(img1, (0, 0))

    # Paste the second image
    combined_image.paste(img2, (img1.width, 0))

    # Save the combined image
    combined_image.save(output_path)

# Example usage
combine_images('Pow50%_pow_M20.png', 'Pow50%_aff_M20.png', 'combined_pow50%_pow_aff.jpg')
