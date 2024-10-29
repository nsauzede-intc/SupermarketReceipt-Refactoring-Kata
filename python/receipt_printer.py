from model_objects import ProductUnit

class TextFormatter:
    def format_line_with_whitespace(self, whitespace_size, value):
        line = ""
        for i in range(whitespace_size):
            line += self.format_whitespace()
        line += value
        line += self.format_newline()
        return line
    def format_multi_item_pricing(self, price, quantity):
        whitespace = self.format_whitespace()
        return f"{whitespace * 2}{price}{whitespace}*{whitespace}{quantity}{self.format_newline()}"
    def format_total_header(self):
        return f"Total:{self.format_whitespace()}"
    def format_discount(self, description, name):
        return f"{description}{self.format_whitespace()}({name})"
    def format_newline(self):
        return "\n"
    def format_whitespace(self):
        return " "
    def header(self):
        return ""
    def footer(self):
        return ""
    def row_header(self):
        return ""
    def row_footer(self):
        return ""

class HTMLFormatter:
    def format_line_with_whitespace(self, whitespace_size, value):
        line = '</td><td align="right">'
        line += value
        line += self.format_newline()
        return line
    def format_multi_item_pricing(self, price, quantity):
        whitespace = self.format_whitespace()
        return f"{whitespace * 2}{price}{whitespace}*{whitespace}{quantity}{self.format_newline()}"
    def format_total_header(self):
        return f"Total:{self.format_whitespace()}"
    def format_discount(self, description, name):
        return f"{description}{self.format_whitespace()}({name})"
    def format_newline(self):
        return ""
    def format_whitespace(self):
        return " "
    def header(self):
        #return '<table border="1"><th>h1</th><th>h2</th>\n'
        return '<table>\n'
    def footer(self):
        return "</table>\n"
    def row_header(self):
        return "<tr><td>"
    def row_footer(self):
        return "</td></tr>\n"

class ReceiptPrinter:

    def __init__(self, columns=40, formatter=TextFormatter()):
        self.columns = columns
        self.formatter = formatter
        import os
        if "HTML" in os.environ:
            self.formatter = HTMLFormatter()
  
    def print_receipt(self, receipt):
        result = ""
        result += self.formatter.header()
        for item in receipt.items:
            receipt_item = self.print_receipt_item(item)
            result += receipt_item

        for discount in receipt.discounts:
            discount_presentation = self.print_discount(discount)
            result += discount_presentation

        result += self.formatter.format_newline()
        result += self.present_total(receipt)
        result += self.formatter.footer()
        return str(result)

    def print_receipt_item(self, item):
        total_price_printed = self.print_price(item.total_price)
        name = item.product.name
        line = self.format_line_with_whitespace(name, total_price_printed)
        if item.quantity != 1:
            line += self.formatter.format_multi_item_pricing(self.print_price(item.price), self.print_quantity(item))
        return line

    def format_line_with_whitespace(self, name, value):
        line = self.formatter.row_header() + name
        whitespace_size = self.columns - len(name) - len(value)
        line += self.formatter.format_line_with_whitespace(whitespace_size, value)
        return line + self.formatter.row_footer()

    def print_price(self, price):
        return "%.2f" % price

    def print_quantity(self, item):
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        else:
            return '%.3f' % item.quantity

    def print_discount(self, discount):
        name = self.formatter.format_discount(discount.description, discount.product.name)
        value = self.print_price(discount.discount_amount)
        return self.format_line_with_whitespace(name, value)

    def present_total(self, receipt):
        name = self.formatter.format_total_header()
        value = self.print_price(receipt.total_price())
        return self.format_line_with_whitespace(name, value)
