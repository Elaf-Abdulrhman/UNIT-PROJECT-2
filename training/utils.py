from django.contrib.staticfiles import finders
from PIL import Image, ImageDraw, ImageFont
import os

def generate_certificate(employee_name, trainer_name, course_name):
    # Get paths to image and fonts
    template_path = finders.find('images/certificate.png')
    font_times_path = finders.find('fonts/times_new_roman.ttf')
    font_amsterdam_path = finders.find('fonts/UKIJDi.ttf')

    if not template_path:
        raise FileNotFoundError("Certificate template not found.")
    if not font_times_path or not font_amsterdam_path:
        raise FileNotFoundError("Font file not found.")

    # Load image
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # Load fonts
    font_name = ImageFont.truetype(font_amsterdam_path, size=48)
    font_course = ImageFont.truetype(font_times_path, size=36)
    font_trainer = ImageFont.truetype(font_times_path, size=28)

    # Draw text on certificate (adjust coordinates as needed)
    draw.text((400, 300), employee_name, font=font_name, fill='black')
    draw.text((400, 360), course_name, font=font_course, fill='black')
    draw.text((400, 420), f"Instructor: {trainer_name}", font=font_trainer, fill='black')

    # Save certificate
    output_path = os.path.join("certificates", f"{employee_name}_certificate.png")
    os.makedirs("certificates", exist_ok=True)
    image.save(output_path)

    return output_path