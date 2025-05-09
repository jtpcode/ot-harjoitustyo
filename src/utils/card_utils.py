def card_names_to_png_filenames(card_name):
    filename = f"{card_name.lower().replace(" // ", "_slash_").replace(' ', '_')}.png"

    return filename
