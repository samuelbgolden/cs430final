from tkinter import Frame, Tk, Label, Text, Button, StringVar, END, Listbox
from tkinter.ttk import Notebook
from datetime import datetime
from algs import *


class App(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.winfo_toplevel().title("CS430 Final Project: Samuel Golden")
        self.parent = parent

        # init fonts
        FONT = 'Din'
        TEXT_FONT = 'Courier'
        self.titleFont = (FONT, 16)
        self.headerFont = (FONT, 14, 'bold')
        self.textFont = (TEXT_FONT, 12)
        self.statusFont = (FONT, 12, 'italic')

        # init widgets
        self.outputLabel = Label(self, text='Algorithmic output:', font=self.titleFont)
        self.outputNb = Notebook(self)
        self.mstTab = Frame(self.outputNb)
        self.inputLabel = Label(self, text='Matrix input (-1 = no link, separate weight with single space, no trailing newline):', font=self.titleFont)
        self.matrixLabel = Label(self, text='Given Matrix', font=self.titleFont)
        self.matrixText = Text(self, font=self.textFont, height=8, width=30)
        self.matrixFrame = Frame(self)
        self.runButton = Button(self, text='Run', font=self.headerFont, relief='raised', borderwidth=5, command=self.run)
        self.statusStr = StringVar()
        self.statusStr.set('IDLE: not running.')
        self.statusBar = Label(self, textvariable=self.statusStr, font=self.statusFont)

        self.grid_all()
        self.config_text()
        self.config_nb()

    def run(self):
        self.write_status("RUNNING: parsing input matrix...")
        matrixInput = self.matrixText.get("1.0", END)  # 1.0 means line 1, char 0
        matrix = matrixInput.split('\n')
        matrix = [row.split(' ') for row in matrix]
        if len(matrix[-1]) == 1:
            del matrix[-1]

        for r in range(len(matrix)):
            for v in range(len(matrix[r])):
                try:
                    matrix[r][v] = int(matrix[r][v])
                except ValueError:
                    self.write_status(f"STOPPED: invalid entry in matrix '{matrix[r][v]}'.")
                    return

        self.write_status("RUNNING: validating input matrix...")
        matrixSize = len(matrix)
        for row in matrix:
            if len(row) != matrixSize:
                self.write_status("STOPPED: matrix size invalid (must be square).")
                return

        for i in range(0, matrixSize):
            if matrix[i][i] != 0:
                self.write_status("STOPPED: matrix diagonal should all be zeros (node cannot have link to itself)")
                return

        self.write_status("RUNNING: drawing table for parsed matrix...")

        matrixTable = MatrixTable(self.matrixFrame, matrix)
        matrixTable.grid(row=0, column=0, sticky='nsew')
        self.matrixFrame.update()

        self.write_status("RUNNING: running MST algorithm...")

        unsortedEdges, sortedEdges, mstEdges = mst(matrix)

        self.write_status("RUNNING: drawing MST visualization...")

        mstView = MSTView(self.mstTab)
        mstView.populate(unsortedEdges, sortedEdges, mstEdges)
        mstView.grid(row=0, column=0, sticky='nsew')

        self.write_status("IDLE: Done. Last successful run: " + datetime.now().strftime("%H:%M:%S"))

    def write_status(self, string):
        self.statusStr.set(string)
        self.parent.update()

    def config_text(self):
        start_matrix = "0 200 500 10 -1\n200 0 80 70 90\n50 80 0 -1 40\n10 70 -1 0 20\n-1 90 40 20 0"
        self.matrixText.insert(END, start_matrix)

    def config_nb(self):
        self.outputNb.add(self.mstTab, text='Minimum Spanning Tree')
        self.outputNb.select(self.mstTab)
        self.outputNb.enable_traversal()

    def grid_all(self):
        to_grid = [
        #    r  c  rs cs stick  widget
            (1, 0, 1, 2, 'nsw', self.outputLabel),
            (2, 0, 1, 2, 'nsew', self.outputNb),
            (3, 0, 1, 2, 'nsw', self.inputLabel),
            (4, 0, 1, 1, 'nsew', self.matrixText),
            (4, 1, 1, 1, 'nsew', self.matrixFrame),
            (5, 0, 1, 2, 'ns', self.runButton),
            (6, 0, 1, 2, 'nsew', self.statusBar)
        ]
        for w in to_grid:
            w[5].grid(row=w[0], column=w[1], sticky=w[4], columnspan=w[3], rowspan=w[2], padx=10, pady=10)

        self.columnconfigure(0, weight=1)


class MatrixTable(Frame):
    def __init__(self, parent, matrix, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.size = len(matrix)
        self.matrix = matrix

        self.headFont = ('Din', 12, 'bold')
        self.entryFont = ('Din', 12)

        self.matrixLabels = []
        for x in range(self.size+1):
            self.matrixLabels.append([None] * (self.size + 1))

        self.populate()

        for r in range(self.size+1):
            for c in range(self.size+1):
                self.matrixLabels[r][c].grid(row=r, column=c, sticky='nsew')

    def populate(self):
        for r in range(self.size+1):
            for c in range(self.size+1):
                if c == 0 and r == 0:
                    self.matrixLabels[0][0] = Label(self, text='   ', font=self.entryFont, relief='ridge')
                elif c == 0:
                    self.matrixLabels[r][0] = Label(self, text=f"R{r-1}", font=self.headFont, relief='ridge')
                elif r == 0:
                    self.matrixLabels[0][c] = Label(self, text=f"R{c-1}", font=self.headFont, relief='ridge')
                else:
                    val = self.matrix[r-1][c-1]
                    if val == 0:
                        fgcolor = 'green'
                    elif val == -1:
                        fgcolor = 'red'
                    else:
                        fgcolor = 'black'
                    self.matrixLabels[r][c] = Label(self, text=str(val), fg=fgcolor, font=self.entryFont, relief='ridge')


class MSTView(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.labelFont = ('Din', 14, 'bold')
        self.lbFont = ('Din', 14)
        self.arrowFont = ('Din', 28, 'bold')

        self.unsortedLabel = Label(self, text='Given Edges', font=self.labelFont)
        self.unsortedLb = Listbox(self, width=8, font=self.lbFont)
        self.arrow1 = Label(self, text=' >>> ', font=self.arrowFont)
        self.sortedLabel = Label(self, text='Sorted Edges', font=self.labelFont)
        self.sortedLb = Listbox(self, width=8, font=self.lbFont)
        self.arrow2 = Label(self, text=' >>> ', font=self.arrowFont)
        self.mstLabel = Label(self, text='Edges in MST', font=self.labelFont)
        self.mstLb = Listbox(self, width=8, font=self.lbFont)

        self.unsortedLabel.grid(row=0, column=0, sticky='nsew')
        self.unsortedLb.grid(row=1, column=0, sticky='nsew')
        self.arrow1.grid(row=1, column=1, sticky='nsew')
        self.sortedLabel.grid(row=0, column=2, sticky='nsew')
        self.sortedLb.grid(row=1, column=2, sticky='nsew')
        self.arrow2.grid(row=1, column=3, sticky='nsew')
        self.mstLabel.grid(row=0, column=4, sticky='nsew')
        self.mstLb.grid(row=1, column=4, sticky='nsew')

    def populate(self, u, s, m):
        for edge in u:
            self.unsortedLb.insert(END, f"R{edge[0]} <-> R{edge[1]}")

        for edge in s:
            self.sortedLb.insert(END, f"R{edge[0]} <-> R{edge[1]}")

        for edge in m:
            self.mstLb.insert(END, f"R{edge[0]} <-> R{edge[1]}")

        summed = sum([x[2] for x in m])
        sumLabel = Label(self, text=f"Sum of MST weights:\n{summed}", font=self.lbFont)
        sumLabel.grid(row=1, column=5, sticky='nsew')


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    app.grid(row=0, column=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()


