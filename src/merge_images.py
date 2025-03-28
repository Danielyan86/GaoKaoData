from PIL import Image
import os


def merge_images_horizontal(image1_path, image2_path, output_path):
    # Open the images
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    # Calculate dimensions for the merged image
    width = img1.width + img2.width
    height = max(img1.height, img2.height)

    # Create a new blank image
    merged_image = Image.new("RGB", (width, height), "white")

    # Paste the images
    merged_image.paste(img1, (0, 0))
    merged_image.paste(img2, (img1.width, 0))

    # Save the merged image
    merged_image.save(output_path)


if __name__ == "__main__":
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    vis_dir = os.path.join(os.path.dirname(current_dir), "output", "visualizations")

    # Paths to your images
    zhongkao_path = os.path.join(vis_dir, "中考分数分布图.png")
    gaokao_path = os.path.join(vis_dir, "高考分数分布图.png")
    output_path = os.path.join(vis_dir, "merged_distribution.png")

    merge_images_horizontal(zhongkao_path, gaokao_path, output_path)
    print(f"Images merged successfully! Output saved as: {output_path}")
