def center_window(root, width, height):
    """Centers the current view (window) in the middle of the screen.

    Args:
        root:
            TKinter -element, which initializes the user interface.
        width (int):
            Window width.
        height (int):
            Window height.
    """

    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
