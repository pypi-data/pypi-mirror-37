import ybc_speech
import ybc_browser


def todo():
    """
    功能：录制一段语音，打开语音指定的网址，默认打开百度首页。

    参数：无

    返回：若正常打开网页则无返回，否则返回-1
    """
    for i in range(3):
        filename = ybc_speech.record("tmp.wav", 4)
        try:
            urlName = ybc_speech.voice2text(filename)
        except:
            urlName = "百度"

        if ybc_browser.open_browser(urlName) != -1:
            return
    return -1


def main():
    todo()


if __name__ == '__main__':
    main()
