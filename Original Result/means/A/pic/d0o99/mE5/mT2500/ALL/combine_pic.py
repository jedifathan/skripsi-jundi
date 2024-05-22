from PIL import Image

def combine_images_side_by_side(image1_path, image2_path, output_path):
    # Open the images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # Get the dimensions of the images
    width1, height1 = image1.size
    width2, height2 = image2.size

    # Ensure both images have the same height
    max_height = max(height1, height2)
    image1 = image1.resize((int(width1 * (max_height / height1)), max_height))
    image2 = image2.resize((int(width2 * (max_height / height2)), max_height))

    # Create a new blank image with the combined width and the maximum height
    combined_width = image1.width + image2.width
    combined_image = Image.new('RGB', (combined_width, max_height))

    # Paste the first image onto the new image at position (0, 0)
    combined_image.paste(image1, (0, 0))

    # Paste the second image onto the new image at position (width1, 0)
    combined_image.paste(image2, (image1.width, 0))

    # Save the combined image
    combined_image.save(output_path)

# Example usage
image1_path = "/mnt/c/Users/mjund/Documents/Kuliah/Trial/means/A/pic/d0o99/mE5/mT2500/ALL/A_0o99_5_2500_4o0_ActiveImplementsVsTime_ALL_M0.png"
image2_path = "/mnt/c/Users/mjund/Documents/Kuliah/Trial/means/A/pic/d0o99/mE5/mT2500/ALL/A_0o99_5_2500_4o0_ActiveImplementsVsTime_ALL_M20.png"
output_path = "combined_image_act_imp.jpg"
combine_images_side_by_side(image1_path, image2_path, output_path)
