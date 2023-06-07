from app import app

def allowed_file(filename):
    if not "." in filename:
        return False
    return filename.rsplit(".", 1)[1].upper() in app.config["ALLOWED_FILE_EXTENSIONS"]

def allowed_file_size(filesize):
    return int(filesize) <= app.config["MAX_FILE_FILESIZE"]

def isInvalid(name):
    invalid_symbols = ['<', '>', '"', '&', "*", "=", "SELECT", "WHERE"]
    for symbol in invalid_symbols:
        if name.find(symbol) != -1:
            return True
    return False
