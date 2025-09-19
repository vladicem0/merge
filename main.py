import os


"""
Перемещение файлов из path1 в path2 с игнорированием совпадающих по имени и размеру
и переносом с переименованием совпадающих только по имени
"""


path1 = 'G:\\vid\\Download\\'
path2 = 'G:\\vid\\_pic\\'


def check_similar_names(saved_pictures: list[str], picture: str) -> bool:
    for pic in saved_pictures:
        i, cnt = 0, 0
        if len(pic) == len(picture):
            continue
        elif len(pic) < len(picture):
            lng = len(pic) - 4
        else:
            lng = len(picture) - 4
        while i < lng:
            if picture[i] == pic[i]:
                cnt += 1
            i += 1
        if cnt > 10 and cnt > lng / 10 * 6 and (pic[:-4] in picture[:-4] or picture[:-4] in pic[:-4]):
            print(pic, ' | ', picture)
            return True
    return False


def replace(similar_name: bool = False) -> None:
    new_pictures = os.listdir(path1)
    cnt = len(new_pictures)
    rem_cnt = 0  # Счетчик совпадающих файлов

    try:
        os.mkdir(path1 + '__tmp')
    except FileExistsError:
        pass

    for picture in new_pictures:
        removed = False
        saved_pictures = os.listdir(path2)
        if os.path.isdir(path1 + picture):
            continue
        if '.trashed' in picture:
            os.remove(path1 + picture)
            continue
        if '.mp4' in picture:
            print('mp4')
            continue

        os.replace(path1 + picture, path1 + '__tmp\\' + picture)  # Перемещение целевого файла во временную папку

        for i in range(1000):  # Проверка на наличие признаков автоматического переименования "file (i).fl" и их удал-е
            if f' ({i}).' in picture:
                new_name = picture.split(f' ({i}).')[0] + '.' + picture.split(f' ({i}).')[1]
                os.rename(path1 + '__tmp\\' + picture, path1 + '__tmp\\' + new_name)
                picture = new_name
                break

        if picture in saved_pictures and os.path.getsize(path1 + '__tmp\\' + picture) == os.path.getsize(path2 + picture):
            # Удаление файла, если он уже есть в целевой папке
            if os.path.getsize(path1 + '__tmp\\' + picture) == os.path.getsize(path2 + picture):
                os.remove(path1 + '__tmp\\' + picture)
                rem_cnt += 1
                continue

        for i in range(1000):  # Удаление файла, если он уже есть в целевой папке с измененным именем "file (i).fl"
            if (''.join(picture.split('.')[:-1]) + f' ({i}).' + picture.split('.')[-1] in saved_pictures and
                    os.path.getsize(path1 + '__tmp\\' + picture) == os.path.getsize(
                        path2 + ''.join(picture.split('.')[:-1]) + f' ({i}).' + picture.split('.')[-1])):
                os.remove(path1 + '__tmp\\' + picture)
                removed = True
                rem_cnt += 1
                break

        if similar_name:
            if check_similar_names(saved_pictures, picture):
                removed = True
                os.replace(path1 + '__tmp\\' + picture, path1 + picture)
        if removed is True:
            continue

        i = 1
        if picture in saved_pictures:  # Переименование файла, если в целевой папке имеется файл с аналогичным именем
            while ''.join(picture.split('.')[:-1]) + f' ({i}).' + picture.split('.')[-1] in saved_pictures:
                i += 1
            new_name = ''.join(picture.split('.')[:-1]) + f' ({i}).' + picture.split('.')[-1]
            os.rename(path1 + '__tmp\\' + picture, path1 + '__tmp\\' + new_name)
            picture = new_name
        os.replace(path1 + '__tmp\\' + picture, path2 + picture)

    os.rmdir(path1 + '__tmp')
    print('total', cnt)
    print('removed', rem_cnt)


if __name__ == '__main__':
    replace()
    input()
