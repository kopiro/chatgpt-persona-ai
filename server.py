import time
import flask

from flask import g

from playwright.sync_api import sync_playwright

APP = flask.Flask(__name__)
PLAY = sync_playwright().start()
BROWSER = PLAY.chromium.launch_persistent_context(
    user_data_dir="/tmp/playwright",
    headless=False,
)

PAGE = BROWSER.new_page()
AI_NAME = open('./ai_name.txt', 'r').read()
AI_HEADER = open('./ai_header.txt', 'r').read()
AI_DEFAULT_LANGUAGE = 'en'

LOCALE_MAP = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "ja": "Japanese",
    "zh": "Chinese",
    "ar": "Arabic",
    "ru": "Russian",
    "is": "Icelandic"
}

def map_locale_to_english(locale: str) -> str:
    if locale not in LOCALE_MAP:
        return "English"
    return LOCALE_MAP[locale]

def get_input_box():
    return PAGE.query_selector("textarea")

def is_logged_in():
    return get_input_box() is not None

def can_send():
    return PAGE.query_selector('textarea ~ button > svg') != None

def get_last_shown_message():
    page_elements = PAGE.query_selector_all(".text-base")
    last_node = page_elements[-1]
    has_action_buttons = last_node.query_selector("button > svg")
    if has_action_buttons != None:
        return last_node.inner_text()
    return None


def send_message(message):
    while not can_send():
        print("cant_send - waiting...")
        time.sleep(1)

    box = get_input_box()
    box.click()
    box.fill(message)
    box.press("Enter")

def get_last_message():
    last_message = get_last_shown_message()
    if last_message == None:
        print("last_message_null - waiting...")
        time.sleep(1)
        return get_last_message()

    return last_message

@APP.route("/chat", methods=["POST"])
def chat():
    try:
        body = flask.request.get_json()
        message_desc = f"'{body['message']}' from {body['sender']}"
        print(f"{message_desc} is been served now")
        
        send_message(f"This is a conversation between {AI_NAME} and {body['sender']}\n{body['sender']} is writing in {map_locale_to_english(body['translate_from'])}, {AI_NAME} will reply in {map_locale_to_english(body['translate_to'])}\n\n{body['sender']}: {body['message']}\n{AI_NAME}: ")
        
        response = get_last_message()
        print("Response: ", response)
        
        return flask.jsonify({
            "response": response
        })
    except BaseException as err:
        print(err)
        return flask.jsonify({
            "error": {
                "message": str(err)
            }
        })

def main():
    PAGE.goto("https://chat.openai.com/")

    if not is_logged_in():
        print("Please log-in and press ENTER when you're done:")
        input()
        main()
        return

    print("Priming AI...")
    send_message(AI_HEADER)

    APP.run(port=8080, threaded=False)


if __name__ == "__main__":
    main()
