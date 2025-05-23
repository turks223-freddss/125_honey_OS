import tkinter as tk

class CalculatorWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.input_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Entry field
        entry = tk.Entry(self, textvariable=self.input_var, font=('Arial', 18), justify='right', bd=5, relief=tk.RIDGE)
        entry.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

        # Button labels
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '+'],
            ['C', '0', '=', '-']
        ]

        # Create buttons
        for row_idx, row in enumerate(buttons):
            for col_idx, label in enumerate(row):
                button = tk.Button(self, text=label, font=('Arial', 16), width=4, height=2,
                                   command=lambda l=label: self.on_button_click(l))
                button.grid(row=row_idx + 1, column=col_idx, sticky='nsew', padx=2, pady=2)

        # Make grid cells expand
        for i in range(4):
            self.columnconfigure(i, weight=1)
        for i in range(5):
            self.rowconfigure(i, weight=1)

    def on_button_click(self, label):
        if label == 'C':
            self.input_var.set('')
        elif label == '=':
            try:
                result = str(eval(self.input_var.get()))
                self.input_var.set(result)
            except Exception:
                self.input_var.set('Error')
        else:
            self.input_var.set(self.input_var.get() + label)
    
   
    def set_input_from_string(self, input_string):
        word_to_symbol = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
            'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13',
            'fourteen': '14', 'fifteen': '15', 'sixteen': '16', 'seventeen': '17',
            'eighteen': '18', 'nineteen': '19', 'twenty': '20', 'thirty': '30',
            'forty': '40', 'fifty': '50', 'sixty': '60', 'seventy': '70',
            'eighty': '80', 'ninety': '90',
            'plus': '+', 'add': '+', 'minus': '-', 'subtract': '-',
            'times': '*', 'multiplied': '*', 'multiply': '*',
            'divided': '/', 'divide': '/', 'over': '/'
        }

        allowed_chars = '0123456789+-*/(). '

        # ✅ First: check if input_string already looks like numbers/operators
        if all(char in allowed_chars for char in input_string):
            self.input_var.set(input_string)
            return

        # ✅ Second: handle word-based input
        words = input_string.lower().split()
        result_parts = []

        i = 0
        while i < len(words):
            word = words[i]
            # Handle compound numbers like "thirty seven"
            if word in ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']:
                if i + 1 < len(words) and words[i + 1] in word_to_symbol and int(word_to_symbol[words[i + 1]]) < 10:
                    combined = int(word_to_symbol[word]) + int(word_to_symbol[words[i + 1]])
                    result_parts.append(str(combined))
                    i += 2
                    continue
                else:
                    result_parts.append(word_to_symbol[word])
            elif word in word_to_symbol:
                result_parts.append(word_to_symbol[word])
            else:
                # 🚨 If unknown word, error out
                self.input_var.set('Error')
                return
            i += 1

        final_expr = ' '.join(result_parts)

        # ✅ Final check: make sure no invalid characters slipped in
        if all(char in allowed_chars for char in final_expr):
            self.input_var.set(final_expr)
        else:
            self.input_var.set('Error')