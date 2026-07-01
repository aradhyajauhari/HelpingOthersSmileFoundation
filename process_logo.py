from PIL import Image

def process_logo():
    img = Image.open('logo.png').convert("RGBA")
    data = img.getdata()
    
    new_data = []
    # threshold for white
    for item in data:
        # if r, g, b are all > 240, it's likely the background
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save('proper_logo.png', "PNG")
    
    # Let's crop for favicon. The image is 676x624. 
    # The figures are likely in the top portion. Let's crop a square.
    # We can calculate the bounding box of non-transparent pixels, or just crop a fixed area.
    # Let's use getbbox() which gets the bounding box of non-zero alpha.
    bbox = img.getbbox()
    if bbox:
        # The text is at the bottom, so bounding box will include text.
        # We need to crop just the top part.
        # Looking at typical logos with text below, the mark is usually the top 60% or 70%.
        pass

    # To be safe and remove the text (which is black/dark blue), let's find the gap between the logo mark and text.
    # A simple crop for favicon: maybe top 676x450, and then square it.
    width, height = img.size
    
    # We will just guess the crop for the favicon. Let's say we crop y from 0 to 450, and x from 0 to width.
    # Let's actually scan rows to find an empty horizontal gap (all transparent).
    empty_rows = []
    for y in range(height):
        is_empty = True
        for x in range(width):
            if img.getpixel((x, y))[3] > 0:
                is_empty = False
                break
        if is_empty:
            empty_rows.append(y)
            
    # Find the largest gap of empty rows that might separate the logo and text.
    # The text is likely at the bottom.
    split_y = height
    # Look for a significant gap in the lower half
    in_gap = False
    gap_start = 0
    max_gap = 0
    best_split = height
    
    for y in range(int(height * 0.4), int(height * 0.9)):
        is_empty = True
        # Check a few pixels in the row to speed up, or all
        for x in range(0, width, 5):
            if img.getpixel((x, y))[3] > 10:
                is_empty = False
                break
        
        if is_empty:
            if not in_gap:
                in_gap = True
                gap_start = y
        else:
            if in_gap:
                gap_length = y - gap_start
                if gap_length > max_gap:
                    max_gap = gap_length
                    best_split = gap_start + gap_length // 2
                in_gap = False

    if best_split < height and max_gap > 5:
        # We found a gap between logo and text!
        logo_mark = img.crop((0, 0, width, best_split))
    else:
        # Fallback
        logo_mark = img.crop((0, 0, width, int(height*0.75)))
        
    # Now get bounding box of the logo mark to make it tightly cropped
    mark_bbox = logo_mark.getbbox()
    if mark_bbox:
        logo_mark = logo_mark.crop(mark_bbox)
        
    # Make it a square for favicon
    mw, mh = logo_mark.size
    size = max(mw, mh)
    favicon = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    offset = ((size - mw) // 2, (size - mh) // 2)
    favicon.paste(logo_mark, offset)
    favicon.save('favicon.png', "PNG")
    
    # Also save an SVG version of the favicon if possible? No, PNG is fine for modern favicons.

if __name__ == "__main__":
    process_logo()
