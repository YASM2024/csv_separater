import os, csv

HEADERS = {
    'type1': [],
    'type2': [],
    'type3': [],
    'type4': [],
}

def main(csvfile, outpath):
    log = {}

    # 例：4列目の値でファイル分割する（インデックスは0から始まるので3）
    target_col = 3
    types = get_file_types(csvfile, column=target_col)

    mk_folders(outpath)
    seen_filenames = {}

    for t in types:
        separated_file = filter(csvfile, target_col, t)

        separated_file = set_header(separated_file, HEADERS[t])
        sanitized_filename = sanitize_filename(t)

        if sanitized_filename in seen_filenames:
            seen_filenames[sanitized_filename] += 1
            unique_filename = f"{sanitized_filename}_{seen_filenames[sanitized_filename]}"
        else:
            seen_filenames[sanitized_filename] = 1
            unique_filename = sanitized_filename

        save_data(separated_file, os.path.join(outpath, f'{unique_filename}.csv'))

        log[target_col] = t

    return log

def get_file_types(file, column):
    types = set()
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ヘッダーをスキップ
        for row in reader:
            types.add(row[column])
    return list(types)

def mk_folders(dir):
    try:
        if not os.path.isdir(dir):
            os.mkdir(dir)
            return True  # フォルダが作成された場合
        else:
            return True  # フォルダが既に存在する場合
    except Exception as e:
        warnings.warn(f"Error creating directory {dir}: {e}")
        return False  # エラーが発生した場合

def filter(file, column, value, match='exact'):
    filtered_rows = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # ヘッダーを取得
        for row in reader:
            if match == 'exact' and row[column] == value:
                filtered_rows.append(row)
            elif match == 'partial' and value in row[column]:
                filtered_rows.append(row)
    return [headers] + filtered_rows

def set_header(file, header):
    original_header = file[0]
    if len(header) != len(original_header):
        raise ValueError(f"Header length {len(header)} does not match number of columns {len(original_header)}")
    file[0] = header
    return file

def save_data(data, path):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def sanitize_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    sanitized = ''.join('_' if c in invalid_chars else c for c in filename)
    return sanitized
