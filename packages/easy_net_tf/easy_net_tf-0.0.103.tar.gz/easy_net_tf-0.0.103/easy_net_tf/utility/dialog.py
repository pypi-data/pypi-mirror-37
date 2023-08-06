import tkinter
import tkinter.filedialog
import tkinter.messagebox


class UtilityDialog:
    @staticmethod
    def file_dialog(func, hint='', initial_dir='', mode=None):
        r = tkinter.Tk()
        r.withdraw()

        if mode is None:
            result = func(title=hint,
                          initialdir=initial_dir)
        else:
            result = func(mode=mode,
                          title=hint,
                          initial_dir=initial_dir)

        return result

    @staticmethod
    def message(func, title, message):
        r = tkinter.Tk()
        r.withdraw()

        func(title=title,
             message=message)


if __name__ == '__main__':
    # path = UtilityDialog.file_dialog_tk_avoid(func=tkinter.filedialog.askdirectory,
    #                                           hint='hello')
    # print(path)

    UtilityDialog.message(
        func=tkinter.messagebox.showinfo,
        title='hello',
        message='message'
    )
