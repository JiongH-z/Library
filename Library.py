import json
import os

class ReaderLoanInformation:
    def __init__(self,name,*lend_book):
        self.name = name
        self.lend_book = []
        for book in lend_book:
            self.lend_book.append(book)

    def add_lend_book(self,wanted_add_book):
        if wanted_add_book not in self.lend_book:
            self.lend_book.append(wanted_add_book)
            print('✅借阅信息添加成功')
        else:
            print('❌添加失败')

    def reduce_lend_book(self,wanted_reduce_book):
        if wanted_reduce_book in self.lend_book:
            self.lend_book.remove(wanted_reduce_book)
        else:
            print('❌未借此书')

    def __str__(self):
        return f'姓名：{self.name}，已借阅图书：{self.lend_book}'



class Library:
    def __init__(self):

        ###存的是借阅数据
        self.all_reader_info = []    #!存的全是对象
        self.filepath = 'Library_info.json'

        ###存的是图书对象 book = Book(book_name,remain_num)
        self.all_remain_book = []
        self.book_filepath = 'book_remain.json'

        ###加载文件数据
        self.load_data()
        self.load_book_data()

    ##初始化书本以及数量
    def set_book(self):
        print('进入图书管理模式')
        book_name = input('请输入新建图书名字')
        book_num = int(input('请输入图书存量'))
        book = Book(book_name,book_num)
        self.all_remain_book.append(book)
        print('成功在图书馆中存入新书')
        self.save_book_data()

    def save_book_data(self):
        data = []
        for remain_book in self.all_remain_book:
            data.append({
                'book_name': remain_book.book_name,
                'num': remain_book.remain_num
            })
        try:
            with open(self.book_filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                print(f'✅ 图书数据已保存到 {self.book_filepath}')
        except Exception as e:
            print(f'❌ 图书数据保存失败：{e}')

    def load_book_data(self):
        try:
            if not os.path.exists(self.book_filepath):
                with open(self.book_filepath, 'w') as file:
                    json.dump([],file)
            with open(self.book_filepath,'r',encoding='utf-8') as file:
                data = json.load(file)
                if data:
                    for item in data:
                        book_data = Book(item['book_name'],item['num'])
                        self.all_remain_book.append(book_data)
                        print(f'✅ 成功从{self.book_filepath}中加载图书数据')
        except Exception as e:
            print(f'❌ 图书数据加载失败：{e}')


    def save_data(self):
        data = []
        for reader_info in self.all_reader_info:
            data.append({
                'name': reader_info.name,
                'book_name': reader_info.lend_book
            })
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                print(f'✅ 借阅数据已保存到 {self.filepath}')
        except Exception as e:
            print(f'❌ 借阅数据保存失败：{e}')

    def load_data(self):
        try:
            if not os.path.exists(self.filepath):
                with open(self.filepath, 'w') as file:
                    json.dump([],file)
            with open(self.filepath,'r',encoding='utf-8') as file:
                data = json.load(file)
                if data:  ##!确保data不为空
                    for item in data:
                        #! data是一个个对象，item['book_name']即reader_info.lend_book，是一个列表
                        ###!这里必须使用*item，把传入的列表解包后重新存入列表,不然会导致每读取一次就多一层嵌套
                        reader_info = ReaderLoanInformation(item['name'],*item['book_name'])
                        self.all_reader_info.append(reader_info)
                        print(f'✅ 成功从{self.filepath}中加载借阅数据')
        except Exception as e:
            print(f'❌ 借阅数据加载失败：{e}')

    def lend_book(self):
        print('进入借书流程')
        name = input('请输入借阅者姓名')

        book_name = input('请输入借阅的图书名字')

        #!这里的item虽然只是循环变量，但是item.reduce_num()是调用对象的方法，直接改变列表里对象的值，所以可以直接写item.reduce_num()
        for item in self.all_remain_book:
            if book_name == item.book_name and item.remain_num > 0:
                item.reduce_num()
                self.save_data()
                for reader_info in self.all_reader_info:
                    if name == reader_info.name:
                        reader_info.add_lend_book(book_name)
                        print('✅借书成功')
                        print(reader_info)
                        self.save_data()
                        return

                reader_info = ReaderLoanInformation(name,book_name)
                self.all_reader_info.append(reader_info)
                print('✅已新建读者信息，借书成功')
                self.save_data()
                return
        print('图书库中没有此书或已被借走')



    def return_book(self):
        print('进入还书流程')
        name = input('请输入借阅者姓名')
        for reader_info in self.all_reader_info:
            if name == reader_info.name:
                book_name = input('请输入归还的图书名字')
                for item in self.all_remain_book:
                    if book_name == item.book_name:
                        item.add_num()
                        self.save_data()
                        reader_info.reduce_lend_book(book_name)
                        print('✅还书成功')
                        self.save_data()
                        return
        print('❌未查找到借阅者姓名')


    def show_all_info(self):
        for reader_info in self.all_reader_info:
            print(reader_info)

    def show_book(self):
        for book_info in self.all_remain_book:
            print(book_info)

    def run(self):
        while True:
            print('1.借书 2.还书 3.展示所有借阅信息 4.进入图书管理模式 5.查看所有图书 6.退出')
            selection = input('请选择使用的功能')
            match selection:
                case '1':
                    self.lend_book()
                case '2':
                    self.return_book()
                case '3':
                    self.show_all_info()
                case '4':
                    self.set_book()
                case '5':
                    self.show_book()
                case '6':
                    print('✅成功退出系统')
                    break
                case _:
                    print('❌无效命令')




class Book:
    def __init__(self,book_name,remain_num):
        self.book_name = book_name
        self.remain_num = remain_num


    def remain_book(self):
        pass

    def add_num(self):
        self.remain_num += 1

    def reduce_num(self):
        self.remain_num -= 1

    def __str__(self):
        return f"图书名字：{self.book_name }，剩余数量：{self.remain_num}"



if __name__ == '__main__':
    reader = Library()
    reader.run()
