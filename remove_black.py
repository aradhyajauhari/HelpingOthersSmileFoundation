from PIL import Image

def process_img(filename):
    try:
        img = Image.open(filename).convert("RGBA")
        data = img.getdata()
        
        new_data = []
        for item in data:
            if item[0] < 40 and item[1] < 40 and item[2] < 40:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
                
        img.putdata(new_data)
        
        # crop to bounding box of non-transparent pixels
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
            
        img.save(filename, "PNG")
        print(f"Processed {filename}")
    except Exception as e:
        print(f"Error on {filename}: {e}")

process_img('favicon.png')
process_img('logo.png')
process_img('proper_logo.png')
