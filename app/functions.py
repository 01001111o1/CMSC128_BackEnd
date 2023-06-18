"""
File contains the the functions that validates file uploads and form input fields
"""

from app import app

"""
allowed_file: function

parameter: filename

returns: true if the file extension is a PDF
"""
def allowed_file(filename):
    if not "." in filename:
        return False
    return filename.rsplit(".", 1)[1].upper() in app.config["ALLOWED_FILE_EXTENSIONS"]

"""
allowed_file_size: function

parameter: filesize

returns: true if the file size is at most 32mb
"""
def allowed_file_size(filesize):
    return int(filesize) <= app.config["MAX_FILE_FILESIZE"]

"""
isInvalid: function

parameter: name

returns: true if an input field contains one of the symbols or strings that is invalid
"""
def isInvalid(name):
    invalid_symbols = ['<', '>', '"', '&', "*", "=", "SELECT", "WHERE"]
    for symbol in invalid_symbols:
        if name.find(symbol) != -1:
            return True
    return False