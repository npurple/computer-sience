#coding=utf8

'''
Factory Method（工厂方法）

意图：

    定义一个用于创建对象的接口，让子类决定实例化哪一个类。Factory Method 使一个类的实例化延迟到其子类。

适用性：

    当一个类不知道它所必须创建的对象的类的时候。

    当一个类希望由它的子类来指定它所创建的对象的时候。

    当类将创建对象的职责委托给多个帮助子类中的某一个，并且你希望将哪一个帮助子类是代理者这一信息局部化的时候。
'''
class CL():
    def __init__(self):
        self.books = dict(fiction='小说', sience='科学', economics='经济', arts='艺术')

    def get_name(self, code):
        try:
            return self.books[code]
        except KeyError:
            return str(code)

class EL():
    def get_name(self, code):
        return str(code)


def get_localizer(lang='English'):
    languages = dict(English=EL, Chinese=CL)
    return languages[lang]()

ch, en = get_localizer('English'), get_localizer('Chinese')

for book in 'fiction sience arts econom'.split():
    print(ch.get_name(book), en.get_name(book))
        

