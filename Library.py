class ReaderLoanInformation:
    def __init__(self,name,*lend_book):
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
        self.all_reader_info = []

    def lend_book(self):
        print('进入借书流程')
        name = input('请输入借阅者姓名')

        book_name = input('请输入借阅的图书名字')

        for reader_info in self.all_reader_info:
            if name == reader_info.name:
                reader_info.add_loan_book(book_name)
                print('已更新借书信息')
                print(reader_info)
                return

        reader_info = ReaderLoanInformation(name,book_name)
        self.all_reader_info.append(reader_info)
        print('已新建读者信息，借书成功')
        for reader_info in self.all_reader_info:
            print(reader_info)


    def return_book(self):
        print('进入还书流程')
        name = input('请输入借阅者姓名')
        for reader_info in self.all_reader_info:
            if name == reader_info.name:
                book_name = input('请输入归还的图书名字')
                reader_info.reduce_lend_book(book_name)
            else:
                print('未查找到借阅者姓名')
            for reader_info in self.all_reader_info:
                print(reader_info)







# class Book:
#     def __init__(self,name,num):
#         self.name = name
#         self.num = num
#
#     def return_book(self):
#         self.num += 1
#     def lend_book(self):
#         self.num -= 1





if __name__ == '__main__':
    library = Library()
    library.lend_book()
    library.lend_book()
    library.return_book()


