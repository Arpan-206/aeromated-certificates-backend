from PIL import Image, ImageDraw, ImageFont

def cert_gen(name, cert_id):
    cert = Image.open("template_files/cert.png")
    draw = ImageDraw.Draw(cert)
    name_font = ImageFont.truetype(
        'template_files/fonts/CollegiateInsideFLF.ttf', 150)
    name_line_width = name_font.getmask(name).getbbox()[2]
    draw.text((645, 675),
              name, font=name_font, fill=(17, 17, 16))
    cert.save(f"certificates/{cert_id}.png")

    return 0