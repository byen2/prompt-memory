import wikipedia
import json
import os
import openai

account_dict = json.load(open("account.info", encoding = "utf-8"))
openai.api_key = account_dict["key"]

# Function accesses openai API and resturns response
def getResponse(prompt, model = "gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = 0, #degree of randomness of the model
    )
    return response.choices[0].message["content"]

# ChatGPT prompt to generate N random Wikipedia article names
# input: int N
# writes article names inside gen.txt file
def generateArticleNames(N):
    num_articles = N
    prompt = f"""

    Do the following instructions:
    1. Generate N random Wikipedia article names.
    2. N is defined by the number enclosed in <>.

    Respond with the following format:
    1. Put each article name on its own line
    2. Do not number the articles.
    3. Place a newline after each line.
    4. Print only this content.

    <{num_articles}>
    """ 
    response = getResponse(prompt)
    print(response)
    with open("gen.txt", "w") as outfile:
        outfile.write(response)

# grabs wikipedia page title and wikipedia text summary given 
# input: string topic
# generate json file containing "title" and "text" of wikipedia entry
def getWikiSection(topic):
    content = {
        "title": wikipedia.page(topic, auto_suggest = False).title,
        "text": wikipedia.summary(topic, auto_suggest = False)
    }

    file_name = "../json_en/" + topic + ".json"
    file_exists = os.path.isfile(file_name)

    if not file_exists:
        #print(topic)
        with open(file_name, "w") as outfile:
            json.dump(content, outfile)

def main():
    generateArticleNames(10)
    file = open("gen.txt", "r")
    #file = open("topic.txt", "r")
    for line in file:
        getWikiSection(line.strip())
    file.close()

if __name__ == "__main__":
    main()
