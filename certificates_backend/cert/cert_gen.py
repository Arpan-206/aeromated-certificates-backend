from PIL import Image, ImageDraw, ImageFont
from datetime import date

def cert_gen(name, course, yoc_director, organization, organization_rep, organization_rep_designation, cert_id):
    cert = Image.open("template_files/cert.png")
    logo = Image.open(f"assets/logos/{organization}.png").resize((250, 250))
    draw = ImageDraw.Draw(cert)
    width, height = list(cert.size)
    name_font = ImageFont.truetype(
        'template_files/fonts/collegiate/CollegiateInsideFLF.ttf', 100)
    sign_font = ImageFont.truetype('./template_files/fonts/Autography.otf', 50)
    course_font = ImageFont.truetype(
        './template_files/fonts/collegiate/CollegiateFLF.ttf', 40)
    designation_font = ImageFont.truetype(
        './template_files/fonts/collegiate/CollegiateInsideFLF.ttf', 25)
    name_line_width = name_font.getmask(name).getbbox()[2]
    course_line_width = course_font.getmask(course).getbbox()[2]
    sign_font_width = sign_font.getmask(yoc_director).getbbox()[2]
    designation_font_width = designation_font.getmask(
        organization_rep_designation).getbbox()[2]
    sub_font = ImageFont.truetype('./template_files/fonts/collegiate/CollegiateFLF.ttf', 10)
    sub_font_width = sub_font.getmask(f"This certificate was generated on {date.today()}").getbbox()[2] 
    draw.text(((width - name_line_width) // 2, 750),
              name, font=name_font, fill=(17, 17, 16))
    draw.text(((width - course_line_width)// 2, 975), course, font=course_font, fill=(17, 17, 16))
    draw.text((460 - sign_font_width / 30, 1100), yoc_director, font=sign_font, fill=(17, 17, 16))
    draw.text((440, 1180), "Director\nYouth Organizations Council",
              align="center", font=designation_font, fill=(17, 17, 16))
    draw.text((1180 - sign_font_width / 30, 1100), organization_rep, font=sign_font, fill=(17, 17, 16))
    draw.text((1400 - 7 * designation_font_width / 10, 1180),
              f"{organization_rep_designation}\n{organization}", align="center", font=designation_font, fill=(17, 17, 16))
    draw.text(((width - sub_font_width) // 2, height - 80), f"This certificate was generated on {date.today()}.", font=sub_font, fill=(17, 17, 16))
    cert.paste(logo, ((width // 2) - 130, (height // 2) - 650), logo)
    cert.save(f"certificates/{cert_id}.png")

    return 0

def delete_cert(cert_id):
    import os
    os.remove(f"certificates/{cert_id}.png")

    return 0