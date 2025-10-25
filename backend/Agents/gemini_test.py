from GeminiAI import GeminiAI

if __name__ == "__main__":
    message = "What are some good strategies for file organization?"

    response = GeminiAI().process_message(message=message)

    print("Gemini Response")

    print(response)

    print("\n\nPrinting message only\n\n")

    print(response['Message'])

    message = "Access my google drive files"

    response = GeminiAI().process_message(message=message)

    print("Gemini Response")

    print(response)

    print("\n\nPrinting Tools Only\n\n")

    print(response["Tools"])