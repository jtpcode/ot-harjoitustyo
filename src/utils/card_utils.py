def card_name_to_png_filename(card_name, set_code):
    filename = f"{card_name.lower().replace(' // ', '_slash_').replace(' ', '_')}_{set_code}.png"

    return filename
