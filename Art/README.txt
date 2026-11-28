Function Button Split Assets
=============================

Files:
- Button_Base.png : icon-free circular button base, reconstructed from the uploaded Book button.
- Icon_Book.png   : isolated book icon with transparent background.
- Icon_Moon.png   : isolated moon-and-star icon with transparent background.
- Preview.png     : visual inspection sheet; do not import as a game sprite.

Pixel dimensions:
- Button_Base: 120 x 153
- Icon_Book:   66 x 51
- Icon_Moon:   59 x 60

Unity suggestion:
Create a Button GameObject with an Image using Button_Base.png.
Add a child Image for the selected icon (Icon_Book.png or Icon_Moon.png).
Keep the icon centered and control its tint/scale independently.

Note:
The icon-free center of Button_Base.png is reconstructed by pixel inpainting because the supplied images were flattened composites, not original layered source files. The original silver frame and gray interior are retained; no new ornament has been added.
