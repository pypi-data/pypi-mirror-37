from time import sleep

from win10toast import ToastNotifier
import zroya


def notify_win10toast():
    toaster = ToastNotifier()
    toaster.show_toast("Hello World!!!",
                       "Python is 10 seconds awsm!",
                       icon_path="custom.ico",
                       duration=10)


def notify_zroya():
    def onClick(nid, action_id):
        print("clicked")  # never called

    # Initialize zroya module. Make sure to call this function.
    # All parameters are required
    zroya.init("YourAppName", "CompanyName", "ProductName", "SubProduct", "Version")

    # Create notification template. TYPE_TEXT1 means one bold line withou image.
    template = zroya.Template(zroya.TemplateType.Text1)
    # Set first line
    template.setFirstLine("My First line")
    template.setSecondLine("It is nice to meet you.")
    template.setThirdLine("How are you?")

    # Save notification id for later use
    notificationID = zroya.show(template, on_click=onClick)

    sleep(10)

    # Hide notification
    zroya.hide(notificationID)


if __name__ == "__main__":
    notify_win10toast()
    # notify_zroya()
