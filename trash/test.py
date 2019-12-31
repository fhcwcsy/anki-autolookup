class foo:
    def test(self):
        print('foo')

class bar(foo):
    def test(self):
        super().test()
        print('bar')

if __name__ == "__main__":
    a = bar()
    a.test()
