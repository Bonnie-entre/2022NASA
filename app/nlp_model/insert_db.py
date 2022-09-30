from .. import models
from ..database import SessionLocal, connect_cursor


def get_next_fileID():
    cursor = connect_cursor()
    cursor.execute(f"""SELECT * FROM files ORDER BY ID DESC LIMIT 1;""" )
    posts = cursor.fetchall()
    if(len(posts)==0):
        return 0
    return dict(posts[0])['id']+1


def create_files(db, _filename, _file_title, _output_outline, _output_keyword, _output_keyword_float, _output_pic):
    new_file = models.Files(
        filename = _filename,
        file_title = _file_title,
        output_outline = _output_outline,
        output_keyword = _output_keyword,
        output_keyword_float = _output_keyword_float,
        output_pic = _output_pic,
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    print("successfully add")
    return new_file

