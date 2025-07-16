import cloudinary.uploader

def image_upload_cloudinary_and_get_url(image_file):
    result = cloudinary.uploader.upload(image_file)
    image_url = result.get('secure_url')
    return image_url