import controller
from word_stock_view import WordStockView


def main():
    view = WordStockView(controller.Controller())
    view.mainloop()


if __name__ == '__main__':
    main()
