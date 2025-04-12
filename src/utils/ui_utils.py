def center_window(root, height, width):
    """Centers the view (window) in the middle of the screen 

    Args:
        root:
            TKinter -element, which initializes the user interface.
        height (int):
            Window height in pixels
        width (int):
            Window width in pixels
    """

    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
