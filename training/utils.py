from django.contrib.staticfiles import finders
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings

def generate_certificate(employee_name, trainer_name, course_name):
    # Get paths to image and fonts
    template_path = finders.find('images/certificate.png')
    font_times_path = finders.find('fonts/times_new_roman.ttf')
    font_amsterdam_path = finders.find('fonts/UKIJDi.ttf')

    if not template_path:
        raise FileNotFoundError("Certificate template not found.")
    if not font_times_path or not font_amsterdam_path:
        raise FileNotFoundError("Font file not found.")

    # Path to save the generated certificate
    output_path = os.path.join(settings.MEDIA_ROOT, f'certificates/{employee_name}_{course_name}.png')

    # Open the certificate template
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # Load fonts
    font_large = ImageFont.truetype(font_times_path, 48)  # Font for course name
    font_larger = ImageFont.truetype(font_times_path, 98)  # Font for employee name

    # Add text to the certificate
    draw.text((650, 380), f"{course_name} course", font=font_large, fill="black")  # Employee name
    draw.text((750, 650), employee_name, font=font_larger, fill="black")   # Course name
    #draw.text((400, 420), f"Instructor: {trainer_name}", font=font_large, fill="black")  # Trainer name

    # Save the certificate
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)

    return output_path