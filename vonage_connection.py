import vonage
class VonageConnection:
    def __init__(self, key=config.VONAGE_KEY, secret=config.VONAGE_SECRET):
        self.client = vonage.Client(key=key, secret=secret)
        self.sender = "15635260736"
        self.sms = vonage.Sms(self.client)

    def send_message(self, to, text):
        responseData = self.sms.send_message(
            {
                "from": self.sender,
                "to": to,
                "text": text,
            }
        )
        print(responseData)
        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")