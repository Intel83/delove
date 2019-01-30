import wx
import sys
import g_interface as gi


def main():
    app = wx.App(redirect=False)
    frame = gi.MainWindow("Delove.pl - automat magazynowy")
    frame.Show()
    app.MainLoop()

    sys.exit()


if __name__ == '__main__':
    main()
