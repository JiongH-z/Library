import json
import os

class ReaderLoanInformation:
    def __init__(self,name,lend_book):
        self.name = name
        self.lend_book = []
        for book in lend_book:
            self.lend_book.append(book)

    def add_loan_book(self,wanted_add_book):
        if wanted_add_book not in self.lend_book:
            self.lend_book.append(wanted_add_book)
            print('借阅信息添加成功')
        else:
            print('添加失败')

    def reduce_lend_book(self,wanted_reduce_book):
        if wanted_reduce_book in self.lend_book:
            self.lend_book.remove(wanted_reduce_book)
        else:
            print('未借此书')

    def __str__(self):
        return f'姓名：{self.name}，已借阅图书：{self.lend_book}'



class Library:
    def __init__(self):
        self.all_reader_info = []    #!存的全是对象
        self.filepath = 'Library_info.json'
        self.load_data()

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
                print(f'✅ 数据已保存到 {self.filepath}')
        except Exception as e:
            print(f'❌ 保存失败：{e}')

    def load_data(self):
        try:
            if not os.path.exists(self.filepath):
                with open(self.filepath, 'w') as file:
                    json.dump([],file)
            with open(self.filepath,'r',encoding='utf-8') as file:
                data = json.load(file)

                for item in data:
                    reader_info = ReaderLoanInformation(item['name'],item['book_name'])
                    self.all_reader_info.append(reader_info)
                    print(f'✅ 成功从{self.filepath}中加载数据')
        except Exception as e:
            print(f'❌ 加载失败：{e}')

    def lend_book(self):
        print('进入借书流程')
        name = input('请输入借阅者姓名')

        book_name = input('请输入借阅的图书名字')

        for reader_info in self.all_reader_info:
            if name == reader_info.name:
                reader_info.add_loan_book(book_name)
                print('已更新借书信息')
                print(reader_info)
                self.save_data()
                return

        reader_info = ReaderLoanInformation(name,book_name)
        self.all_reader_info.append(reader_info)
        print('已新建读者信息，借书成功')
        for reader_info in self.all_reader_info:
            print(reader_info)
        self.save_data()


    def return_book(self):
        print('进入还书流程')
        name = input('请输入借阅者姓名')
        for reader_info in self.all_reader_info:
            if name == reader_info.name:
                book_name = input('请输入归还的图书名字')
                reader_info.reduce_lend_book(book_name)
                self.save_data()
            else:
                print('未查找到借阅者姓名')
                break
        for reader_info in self.all_reader_info:
            print(reader_info)